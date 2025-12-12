"""
Helper functions for parsing files and processing headers.
"""

import datetime
import logging
import re
from collections import Counter
from functools import partial
from itertools import product
from pathlib import Path
from string import ascii_uppercase
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import TypedDict
from typing import TypeVar
from typing import cast

import astropy.units as u
import numpy as np
import scipy.stats
from astropy.table import Column
from astropy.table import MaskedColumn
from astropy.table import Table
from astropy.time import Time
from sqids import Sqids

from dkist_inventory.header_parsing import HeaderParser
from dkist_inventory.transforms import TransformBuilder

__all__ = ["generate_inventory_from_frame_inventory", "generate_asdf_filename"]

T = TypeVar("T")


def process_json_headers(bucket, json_headers):
    """
    Extract the filenames and FITS headers from the inventory headers.

    Parameters
    ----------
    bucket: `str`
        The bucket in which the dataset resides.
    json_headers : `list` of `dict
        A list of dicts containing the JSON version of the headers as stored in inventory.

    Returns
    --------
    filenames
        The filenames (object keys) of the FITS files.
    fits_headers
        The FITS headers.
    extra_inventory
        The inventory keys directly extracted from the frame inventory

    """
    known_non_fits_keys = {
        "_id",
        "bucket",
        "frameStatus",
        "objectKey",
        "createDate",
        "updateDate",
        "lostDate",
        "headerHDU",
        "COMMENT",
        "",
    }
    fits_keys = set(json_headers[0].keys()).difference(known_non_fits_keys)

    def key_filter(keys, headers):
        return {x: headers[x] for x in keys if x in headers}

    non_fits_headers = list(map(partial(key_filter, known_non_fits_keys), json_headers))
    fits_headers = list(map(partial(key_filter, fits_keys), json_headers))

    filenames = [Path(h["objectKey"]).name for h in non_fits_headers]

    extra_inventory = {
        "original_frame_count": len(json_headers),
        "bucket": bucket,
        "create_date": datetime.datetime.utcnow().isoformat("T"),
    }

    return filenames, fits_headers, extra_inventory


def _get_world_coordinates(wcs) -> dict[str, u.Quantity]:
    """
    Return the world coordinates of all the edge pixels for all the dimensions
    correlated to a spatial dimension.
    """
    # Compute the pixel indices of all edges of the higher-dimensional cube
    #  spanned by the axes correlated to a spatial dimension.
    edge_pixels = _compute_edge_pixels(wcs)

    # Compute the world coord values of all the edge pixels
    world_coords = wcs.array_index_to_world_values(*edge_pixels)

    return {
        name: world_coords[idx] << u.Unit(wcs.world_axis_units[idx])
        for idx, name in enumerate(wcs.world_axis_physical_types)
    }


def _compute_edge_pixels(wcs) -> list[np.ndarray]:
    """
    Return a list of index arrays that define all edges of the n-dimensional cube spanned by the axes in a WCS object.
    """
    wcs_shape = np.array(wcs.array_shape)
    num_axes = len(wcs.array_shape)

    # `slice_combos` contains all permutations of [0, -1, None] over all axes.
    # For example, 2 axes will produce [(0, 0), (0, -1), (0, None), (-1, 0),
    # (-1, -1), (-1, None), (None, 0), (None, -1), (None, None)] We'll use
    # `None` to denote `slice(None)` (i.e., the whole axis) for now
    #
    # We need to use (a - 1) as the "end" edge pixel because
    # wcs.array_index_to_world_values doesn't interpret negative indices as
    # starting in from the end of the array, but rather as being on the opposite
    # side of 0. Freaky.
    slice_combos = product(*[[0, a - 1, None] for a in wcs_shape])
    # Edges are defined as only varying along a single axis at a time. So we use
    # filter to grab slices that only have a single `None` value.
    slice_combos = list(filter(lambda x: x.count(None) == 1, slice_combos))

    logging.info(f"For {num_axes} axis there are {len(slice_combos)} edge slices")

    # Now build up a list of the indices for each WCS dimension
    edge_pixels = []
    for a in range(num_axes):
        idx_array = np.array([], dtype=int)
        for slice_tuple in slice_combos:
            # `slice_tuple` will be something like, e.g., (0, 0, None)

            # Get the slice for the current axis
            s = slice_tuple[a]

            # Regardless of the current axis (`a`) we need a number index values equal to the length of the *axis
            # that is varying*. I.e., the axis that has a `None` in the tuple
            edge_axis_length = wcs_shape[slice_tuple.index(None)]

            # Make the index values for this particular slice tuple
            if s is None:
                # If the current axis is the varying one then the index values are just arange (i.e., every pixel along
                # the axis).
                idx_array = np.append(idx_array, np.arange(edge_axis_length))
            else:
                # Otherwise, it's either 0 or (axis_length - 1) repeated the length of the varying axis
                idx_array = np.append(idx_array, np.ones(edge_axis_length, dtype=int) * s)

        edge_pixels.append(idx_array)

    logging.info(f"Axes dims are {wcs_shape}")
    logging.info(f"There are {edge_pixels[0].shape} total edge pixels")

    return edge_pixels


def _inventory_from_wcs(wcs):
    """
    This function extracts the extents of various world axes to put into
    inventory.

    It does this by calculating all the coordinates of all axes anywhere in the
    array and then finding the maxima.

    It aims to be as general as possible, despite this possibly being overkill,
    just to minimise the chances that this needs changing in the future. To do
    this is uses a bunch of wcs trickery which will be explained inline.
    """
    # These are the world axis physical types (mangled by axis_world_coords_values)
    # which we want to parse if they are present.
    known_fields = {
        "custom:pos.helioprojective.lat",
        "custom:pos.helioprojective.lon",
        "em.wl",
        "time",
        "phys.polarization.stokes",
    }

    required_fields = {"custom:pos.helioprojective.lat", "custom:pos.helioprojective.lon"}

    # Validate the required fields are present
    present_world_types = known_fields.intersection(wcs.world_axis_physical_types)
    if not present_world_types.issuperset(required_fields):
        raise ValueError(
            "The WCS being converted to inventory needs HPC lat and lon "
            "as well as temporal axes."
            f"This one only has {present_world_types}."
        )

    # TODO: When NDCube is fixed to not make the full array every time we should only do the edge method (_get_world_coordinates)
    # spatially correlated axes and use NDCube for the rest.
    world_coords = _get_world_coordinates(wcs)

    # Calculate the min and max values along each world axis
    min_dict = {field: np.min(world_coords[field]) for field in world_coords.keys()}
    max_dict = {field: np.max(world_coords[field]) for field in world_coords.keys()}

    # Construct all required inventory fields
    bounding_box = np.array(
        list(
            map(
                _closest_angle_to_zero,
                (
                    min_dict["custom:pos.helioprojective.lon"],
                    min_dict["custom:pos.helioprojective.lat"],
                    max_dict["custom:pos.helioprojective.lon"],
                    max_dict["custom:pos.helioprojective.lat"],
                ),
            )
        )
    ).reshape((2, 2))

    inventory = {"boundingBox": tuple(map(tuple, bounding_box.tolist()))}

    if "time" in world_coords.keys():
        # Do some WCS trickery to extract the callable which converts the time
        # delta returned by axis_world_coords into a Time object that we can
        # convert to a string.
        time_index = wcs.world_axis_physical_types.index("time")
        time_key = wcs.world_axis_object_components[time_index][0]
        time_converter = wcs.world_axis_object_classes[time_key][3]
        inventory["startTime"] = time_converter(
            min_dict["time"], unit=min_dict["time"].unit
        ).datetime.isoformat("T")
        inventory["endTime"] = time_converter(
            max_dict["time"], unit=max_dict["time"].unit
        ).datetime.isoformat("T")

    # Add wavelength fields if the wavelength axis is present
    if "em.wl" in present_world_types:
        inventory["wavelengthMin"] = min_dict["em.wl"].to_value(u.nm)
        inventory["wavelengthMax"] = max_dict["em.wl"].to_value(u.nm)

    # Add the stokes fields if the stokes axis is present
    if "phys.polarization.stokes" in present_world_types:
        # Extract the stokes converter which converts the index to string representation.
        stokes_index = wcs.world_axis_physical_types.index("phys.polarization.stokes")
        stokes_key = wcs.world_axis_object_components[stokes_index][0]
        stokes_converter = wcs.world_axis_object_classes[stokes_key][0]
        stokes_components = stokes_converter(
            np.unique(world_coords["phys.polarization.stokes"])
        ).symbol.tolist()

        inventory["hasAllStokes"] = len(stokes_components) > 1
        inventory["stokesParameters"] = list(map(str, stokes_components))
    else:
        inventory["stokesParameters"] = ["I"]
        inventory["hasAllStokes"] = False

    return inventory


def _closest_angle_to_zero(angle: u.Quantity[u.arcsec]) -> float:
    """
    Given an angle, make sure that it is the closest version of that angle to zero degrees.

    For example, use -2 degrees, not +358 degrees.
    """
    angle = angle.to_value(u.arcsec)
    one_rotation = 1296000  # arcsecs
    negative_rotation_angle = angle - one_rotation
    positive_rotation_angle = angle + one_rotation
    angles = [angle, negative_rotation_angle, positive_rotation_angle]
    return round(min(angles, key=abs), 2)


def identity(x: T) -> T:
    """
    Return the argument unchanged. Useful as a default for functions that expect a mapping operation
    """
    return x


def _get_unique(
    column: Column | MaskedColumn,
    singular: bool = False,
    expected_type: Callable[[Any], T] = identity,
) -> List[T] | T:
    """
    Get unique values (omitting masked values) from the column, mapping by the expected_type

    If singular = True, raise an error if there is more than one value
    """
    if isinstance(column, MaskedColumn):
        column = column[~column.mask]  # Omit masked values e.g. sparse values
    uniq = list(set(column))
    uniq.sort()

    uniq_types: List[T] = list(map(expected_type, uniq))

    if singular:
        return _singular(uniq_types)

    return uniq_types


def _singular(values: List[T]) -> T:
    """
    Expect a list of a single item. If the list is empty or has more items raise an error
    """
    if len(values) == 1:
        return values[0]
    else:
        raise ValueError(f"Values '{values}' do not result in a singular unique value.")


def _get_counts(column: List[str]) -> Dict[str, int]:
    return dict(Counter(column))


def _get_count_true(column: List[bool]) -> int:
    return sum(int(val) for val in column)


class Distribution(TypedDict):
    min: float
    p25: float
    med: float
    p75: float
    max: float


def _get_distribution(values: List[float]) -> Optional[Distribution]:
    # np.percentile does not accept a masked type, even if all values are unmasked
    if len(values) == 0:
        return None
    if isinstance(values, MaskedColumn):
        values = np.asarray(values[~values.mask])
    return {
        "min": float(np.min(values)),
        "p25": float(np.percentile(values, 25)),
        "med": float(np.median(values)),
        "p75": float(np.percentile(values, 75)),
        "max": float(np.max(values)),
    }


def _get_number_apply(column, func):
    return float(func(column))


def _get_keys_matching(
    headers, pattern, expected_type: Callable[[str], T] = identity, singular: bool = True
) -> List[T]:
    """
    Get all the values from all the keys matching the given re pattern.

    All values are de-duplicated and returned in a sorted list.

    Parameters
    ----------
    headers : `astropy.table.Table`
        All the headers

    pattern : `str`
        A regex pattern

    expected_type : `callable`
        A mapping function that returns a type

    singular : `bool`
        If True, raise an error if there is more than one value in a key

    """
    results = []

    prog = re.compile(pattern)
    for key in headers.colnames:
        if prog.match(key):
            values = _get_unique(headers[key], singular=singular, expected_type=expected_type)
            if isinstance(values, list):
                results.extend(values)
            else:
                results.append(values)
    return sorted(list(set(results)))


def _get_optional_key(headers, key, *, default=None, function, **kwargs):
    if key in headers.colnames:
        return function(headers[key], **kwargs)
    return default


def _inventory_from_headers(headers: Table):
    # TODO: Make this function take a header parser and move all the help
    # functions onto the header parser.
    inventory = {}

    mode = partial(scipy.stats.mode, keepdims=False, nan_policy="raise")

    # These keys might get updated by parsing the gwcs object.
    if _get_unique(headers["INSTRUME"]) == "VBI":
        inventory["wavelengthMin"] = _get_unique(headers["WAVEMIN"])
        inventory["wavelengthMax"] = _get_unique(headers["WAVEMAX"])
    else:
        inventory["wavelengthMin"] = inventory["wavelengthMax"] = _get_unique(
            headers["LINEWAV"], expected_type=int
        )[0]

    inventory["startTime"] = Time(headers["DATE-BEG"], format="isot").sort()[0].isot
    inventory["endTime"] = Time(headers["DATE-END"], format="isot").sort()[-1].isot

    # non-optional keys
    inventory["datasetId"] = _get_unique(headers["DSETID"], singular=True, expected_type=str)
    inventory["exposureTime"] = _get_number_apply(headers["XPOSURE"], lambda x: mode(x).mode)
    inventory["instrumentName"] = _get_unique(headers["INSTRUME"], singular=True, expected_type=str)
    inventory["recipeId"] = _get_unique(headers["RECIPEID"], singular=True, expected_type=int)
    inventory["recipeInstanceId"] = _get_unique(
        headers["RINSTID"], singular=True, expected_type=int
    )
    inventory["recipeRunId"] = _get_unique(headers["RRUNID"], singular=True, expected_type=int)
    inventory["targetTypes"] = _get_unique(headers["OBJECT"], expected_type=str)
    inventory["primaryProposalId"] = _get_unique(
        headers["PROP_ID"], singular=True, expected_type=str
    )
    inventory["primaryExperimentId"] = _get_unique(
        headers["EXPER_ID"], singular=True, expected_type=str
    )
    inventory["dataset_size"] = (
        _get_number_apply(headers["FRAMEVOL"], np.sum) * u.Mibyte
    ).to_value(u.Gibyte)
    inventory["contributingExperimentIds"] = _get_keys_matching(
        headers, r"EXPRID\d\d$", expected_type=str
    )
    inventory["contributingProposalIds"] = _get_keys_matching(
        headers, r"PROPID\d\d$", expected_type=str
    )
    inventory["headerDataUnitCreationDate"] = headers[0]["DATE"]
    inventory["headerVersion"] = _get_unique(headers["HEADVERS"], singular=True, expected_type=str)
    inventory["headerDocumentationUrl"] = _get_unique(
        headers["HEAD_URL"], singular=True, expected_type=str
    )
    inventory["infoUrl"] = _get_unique(headers["INFO_URL"], singular=True, expected_type=str)
    inventory["calibrationDocumentationUrl"] = _get_unique(
        headers["CAL_URL"], singular=True, expected_type=str
    )
    inventory["health"] = _get_counts(cast(List[str], headers["DSHEALTH"]))
    inventory["inputDatasetObserveFramesPartId"] = _get_unique(
        headers["IDSOBSID"], singular=True, expected_type=int
    )

    # Optional Keys with defaults
    inventory["qualityAverageFriedParameter"] = _get_optional_key(
        headers, "ATMOS_R0", default=np.nan, function=_get_number_apply, func=np.mean
    )
    inventory["qualityAveragePolarimetricAccuracy"] = _get_optional_key(
        headers, "POL_SENS", default=np.nan, function=_get_number_apply, func=np.mean
    )
    inventory["highLevelSoftwareVersion"] = _get_optional_key(
        headers,
        "HLSVERS",
        default="unknown",
        function=_get_unique,
        singular=True,
        expected_type=str,
    )
    inventory["workflowName"] = _get_optional_key(
        headers,
        "WKFLNAME",
        default="unknown",
        function=_get_unique,
        singular=True,
        expected_type=str,
    )
    inventory["workflowVersion"] = _get_optional_key(
        headers,
        "WKFLVERS",
        default="unknown",
        function=_get_unique,
        singular=True,
        expected_type=str,
    )

    inventory["polarimetricAccuracy"] = _get_optional_key(
        headers, "POL_SENS", default=None, function=_get_distribution
    )
    inventory["friedParameter"] = _get_optional_key(
        headers, "ATMOS_R0", default=None, function=_get_distribution
    )
    inventory["lightLevel"] = _get_optional_key(
        headers, "LIGHTLVL", default=None, function=_get_distribution
    )
    inventory["gosStatus"] = _get_optional_key(
        headers, "GOS_STAT", default=None, function=_get_counts
    )
    inventory["aoLocked"] = _get_optional_key(
        headers, "AO_LOCK", default=None, function=_get_count_true
    )
    inventory["spectralLines"] = (
        _get_keys_matching(headers, r"SPECLN\d\d$", expected_type=str, singular=False) or None
    )
    # MANPROCD is a recently added header so it will not be included in older headers until reprocessing occurs
    # Without MANPROCD, man_proc_value will be None and it is assumed that the dataset can be auto processed
    # Any datasets that were manually processed will be identified and corrected separately
    # If there is a single True instance of MANPROCD, then the dataset was manually processed
    man_proc_value = _get_optional_key(
        headers,
        "MANPROCD",
        default=None,
        function=_get_unique,
        singular=True,
        expected_type=bool,
    )
    inventory["isManuallyProcessed"] = man_proc_value is True

    # Keys which might not be in output
    unique_optional_key_map = {
        "IDSPARID": ("inputDatasetParametersPartId", int),
        "IDSCALID": ("inputDatasetCalibrationFramesPartId", int),
        "OBSPR_ID": ("observingProgramExecutionId", str),
        "IP_ID": ("instrumentProgramExecutionId", str),
        # If the PRODUCT header exists, use it for productId
        "PRODUCT": ("productId", str),
    }
    for fits_key, (inventory_key, expected_type) in unique_optional_key_map.items():
        if fits_key in headers.colnames:
            inventory[inventory_key] = _get_unique(
                headers[fits_key], singular=True, expected_type=expected_type
            )

    # If PRODUCT header did not exist, productId will not be populated
    if "productId" not in inventory:
        # compute productId from IDSOBSID and PROCTYPE
        proc_type = _get_unique(headers["PROCTYPE"], singular=True, expected_type=str)
        inventory["productId"] = compute_product_id(
            inventory["inputDatasetObserveFramesPartId"], proc_type
        )

    return inventory


# a duplicate function exists in dkist-processing-common, which is where it will ultimately live
def compute_product_id(ids_obs_id: int, proc_type: str) -> str:
    """
    Compute the productId from IDSOBSID and PROCTYPE.

    Parameters
    ----------
    ids_obs_id
       The IDSOBSID which uniquely identifies the product.

    proc_type
       The PROCTYPE, e.g. `L1`.

    Returns
    -------
    productId: `str`
        The computed product id.

    """
    sqid_factory = Sqids(alphabet=ascii_uppercase, min_length=5)
    sqid = sqid_factory.encode([ids_obs_id])
    return f"{proc_type}-{sqid}"


def extract_inventory(
    header_parser: HeaderParser,
    transform_builder: TransformBuilder = None,
    **extra_inventory: Mapping[str, Any],
) -> Mapping[str, Any]:
    """
    Generate the inventory record for an asdf file from an asdf tree.

    Parameters
    ----------
    headers
       The raw sorted header with `'filenames'` and `'headers'` columns as
       returned by `.make_sorted_table`.

    extra_inventory
        Additional inventory keys that can not be computed from the headers or the WCS.

    Returns
    -------
    tree: `dict`
        The updated tree with the inventory.

    """
    header_parsers = header_parser.group_mosaic_tiles()

    if transform_builder is None:
        transforms = [TransformBuilder(hp) for hp in header_parsers]
    else:
        transforms = [transform_builder]

    wcs_inventory = _inventory_from_wcs(transforms[0].gwcs)

    if len(transforms) != 1:
        # If we have a tiled dataset then we need to use the boundingBox keys
        # for each tile to calculate the global bounding box. We assume all the
        # other keys are invariant over the tiles, if they turn out not to be,
        # this is the place to calculate them.
        bounding_boxes = []
        for transform in transforms:
            inv = _inventory_from_wcs(transform.gwcs)
            bounding_boxes.append(inv["boundingBox"])

        boxes = np.array(bounding_boxes, dtype=float)

        global_bbox = (
            (boxes[:, 0, 0].min(), boxes[:, 0, 1].min()),
            (boxes[:, 1, 0].max(), boxes[:, 1, 1].max()),
        )
        wcs_inventory["boundingBox"] = global_bbox

    # The headers will populate passband info for VBI and then wcs will
    # override it if there is a wavelength axis in the dataset, any supplied
    # kwargs override things extracted from dataset.
    inventory = {
        **_inventory_from_headers(header_parser.headers),
        **wcs_inventory,
        **extra_inventory,
    }

    # After this point we are assuming all these keys do not vary between mosaic tiles.
    transform_builder = transforms[0]
    inventory["hasSpectralAxis"] = transform_builder.spectral_sampling is not None
    inventory["hasTemporalAxis"] = transform_builder.temporal_sampling is not None
    inventory["averageDatasetSpectralSampling"] = transform_builder.spectral_sampling
    inventory["averageDatasetSpatialSampling"] = transform_builder.spatial_sampling
    inventory["averageDatasetTemporalSampling"] = transform_builder.temporal_sampling

    # Calculate the asdfObjectKey and qualityReportObjectKey
    instrument = inventory["instrumentName"].upper()
    start_time = datetime.datetime.fromisoformat(inventory["startTime"])
    asdf_filename = generate_asdf_filename(
        instrument=instrument, start_time=start_time, dataset_id=inventory["datasetId"]
    )
    inventory["asdfObjectKey"] = (
        f"{inventory['primaryProposalId']}/{inventory['datasetId']}/{asdf_filename}"
    )
    quality_report_filename = generate_quality_report_filename(dataset_id=inventory["datasetId"])
    inventory["qualityReportObjectKey"] = (
        f"{inventory['primaryProposalId']}/{inventory['datasetId']}/{quality_report_filename}"
    )

    return inventory


def generate_asdf_filename(instrument: str, start_time: datetime, dataset_id: str):
    """
    Generate the filename to use for ASDF files.

    Example: VISP_L1_20240411T142700_ABCDE_metadata.asdf
    """
    return f"{instrument}_L1_{start_time:%Y%m%dT%H%M%S}_{dataset_id}_metadata.asdf"


def generate_quality_report_filename(dataset_id: str):
    """
    Generate the filename to use for Quality Report files.

    Example: ABCDE_quality_report.pdf
    """
    return f"{dataset_id}_quality_report.pdf"


# This is the function called by dataset-inventory-maker
def generate_inventory_from_frame_inventory(bucket: str, json_headers: List[Dict[str, Any]]):
    """
    Generate the complete inventory record from frame inventory.

    Parameters
    ----------
    bucket
        The bucket in which the dataset resides.
    json_headers
        A list of dicts containing the JSON version of the headers as stored in inventory.

    Returns
    -------
    dataset_inventory
        The complete dataset inventory
    """
    filenames, fits_headers, extra_inventory = process_json_headers(bucket, json_headers)
    header_parser = HeaderParser.from_headers(fits_headers)
    return extract_inventory(header_parser, **extra_inventory)
