"""
Functionality relating to creating gWCS frames and Astropy models from SPEC 214 headers.
"""

import logging
import re
from functools import partial
from itertools import product

import astropy.modeling.models as m
import astropy.units as u
import gwcs
import gwcs.coordinate_frames as cf
import numpy as np
from astropy.coordinates import ITRS
from astropy.coordinates import CartesianRepresentation
from astropy.modeling import CompoundModel
from astropy.time import Time
from dkist.wcs.models import AsymmetricMapping
from dkist.wcs.models import CoupledCompoundModel
from dkist.wcs.models import Ravel
from dkist.wcs.models import generate_celestial_transform
from dkist.wcs.models import varying_celestial_transform_from_tables
from sunpy.coordinates import Helioprojective

from dkist_inventory.header_parsing import HeaderParser

__all__ = [
    "TransformBuilder",
    "spectral_model_from_framewave",
    "time_model_from_date_obs",
    "generate_lookup_table",
    "linear_time_model",
    "linear_spectral_model",
    "spatial_model_from_header",
]


PRIMARY_WCS_CTYPE = re.compile(r"(CTYPE\d+$)")


def identify_spatial_axes(header):
    """
    Given a FITS WCS header identify which axis number is lat and which is lon.
    """
    latind = None
    lonind = None
    for k, v in header.items():
        key_is_not_primary_wcs_ctype = not bool(re.search(PRIMARY_WCS_CTYPE, k))
        if key_is_not_primary_wcs_ctype:
            continue
        if isinstance(v, str) and v.startswith("HPLN-"):
            lonind = int(k[5:])
        if isinstance(v, str) and v.startswith("HPLT-"):
            latind = int(k[5:])

    if latind is None or lonind is None:
        raise ValueError("Could not extract HPLN and HPLT from the header.")

    latalg = header[f"CTYPE{latind}"][5:]
    lonalg = header[f"CTYPE{lonind}"][5:]

    if latalg != lonalg:
        raise ValueError(
            "The projection of the two spatial axes did not match."
        )  # pragma: no cover

    return lonind, latind


def spatial_model_from_header(header):
    """
    Given a FITS compliant header with CTYPEx,y as HPLN, HPLT return a
    `~astropy.modeling.CompositeModel` for the transform.

    This function finds the HPLN and HPLT keys in the header and returns a
    model in Lon, Lat order.
    """
    lonind, latind = identify_spatial_axes(header)

    cunit1, cunit2 = u.Unit(header[f"CUNIT{lonind}"]), u.Unit(header[f"CUNIT{latind}"])
    crpix = ((header[f"CRPIX{lonind}"], header[f"CRPIX{latind}"]) * u.pix) - 1 * u.pix
    cdelt = u.Quantity(
        [
            header[f"CDELT{lonind}"] * (cunit1 / u.pix),
            header[f"CDELT{latind}"] * (cunit2 / u.pix),
        ]
    )
    crval = u.Quantity([header[f"CRVAL{lonind}"] * cunit1, header[f"CRVAL{latind}"] * cunit2])
    pc = (
        np.array(
            [
                [header[f"PC{lonind}_{lonind}"], header[f"PC{lonind}_{latind}"]],
                [header[f"PC{latind}_{lonind}"], header[f"PC{latind}_{latind}"]],
            ]
        )
        * u.pix
    )

    latproj = header[f"CTYPE{latind}"][5:]
    lonpole = header.get("LONPOLE")
    if not lonpole and latproj == "TAN":
        lonpole = 180

    if not lonpole:
        raise ValueError(f"LONPOLE not specified and not known for projection {latproj}")

    projections = {"TAN": m.Pix2Sky_TAN()}

    scale, transform = (
        np.mean(cdelt).to_value(u.arcsec / u.pix),
        generate_celestial_transform(
            crpix, cdelt, pc, crval, lon_pole=lonpole, projection=projections[latproj]
        ),
    )

    # Ensure we reverse the ordering of the inputs if we are flipping the axes
    # TODO: Should this be folded into the first mapping?
    if latind < lonind:
        transform = m.Mapping([1, 0]) | transform

    return scale, transform


def varying_spatial_model_from_headers(axes: list[int], parser: HeaderParser):
    """
    Generate a varying celestial model from a set of headers.
    """
    header = dict(parser.header)
    varying_axes = parser.varying_spatial_daxes
    vaxes = parser.compute_varying_axes_numbers(varying_axes)

    lonind, latind = identify_spatial_axes(header)
    cunit1, cunit2 = u.Unit(header[f"CUNIT{lonind}"]), u.Unit(header[f"CUNIT{latind}"])
    cdelt = u.Quantity(
        [
            header[f"CDELT{lonind}"] * (cunit1 / u.pix),
            header[f"CDELT{latind}"] * (cunit2 / u.pix),
        ]
    )

    # Extract tables
    varying_header_array = parser.header_array[
        parser.slice_for_dataset_array_axes(*vaxes, indexing="fits")
    ]
    varying_shape = [header[f"DNAXIS{d}"] for d in vaxes]

    if "crval" in varying_axes:
        crval_table = varying_header_array[[f"CRVAL{i}" for i in (lonind, latind)]]
        # Coerce the astropy table to a regular float numpy array
        crval_table = np.array(crval_table.tolist())
        crval_table = crval_table.reshape(varying_shape + [2])
        crval_table = crval_table << cunit1
    else:
        crval_table = u.Quantity(
            [header[f"CRVAL{lonind}"] * cunit1, header[f"CRVAL{latind}"] * cunit2]
        )

    # For the pc matrix we don't want to extract it flipped
    if "pc" in varying_axes:
        pc_table = varying_header_array[[f"PC{i}_{j}" for i, j in product(*[(lonind, latind)] * 2)]]
        # Coerce the astropy table to a regular float numpy array
        pc_table = np.array(pc_table.tolist())
        pc_table = pc_table.reshape(varying_shape + [2, 2])
        pc_table = pc_table << u.pix
    else:
        pc_table = (
            np.array(
                [
                    [header[f"PC{lonind}_{lonind}"], header[f"PC{lonind}_{latind}"]],
                    [header[f"PC{latind}_{lonind}"], header[f"PC{latind}_{latind}"]],
                ]
            )
            * u.pix
        )

    if "crpix" in varying_axes:
        crpix_table = varying_header_array[[f"CRPIX{i}" for i in (lonind, latind)]]
        # Coerce the astropy table to a regular float numpy array
        crpix_table = np.array(crpix_table.tolist())

        # This block adapts the crpix table to account for the fact
        # that when the crpix3 value is changing for a cryo raster
        # (VISP doesn't change crpix3) the fits headers are correct
        # for N images with a length one rastering axis.  We need to
        # offset them so the 0th pixel is the first one.
        # This is done by modifying the first (numpy's last) file axis
        # (the one that's the last in the FITS array).

        # Depending on any future uses of varying crpix this might be cryo specific
        if lonind in varying_axes["crpix"]:
            crpix_offset = np.zeros_like(crpix_table)
            crpix_offset[..., :, 0] = np.arange(crpix_table.shape[-2])
            crpix_table += crpix_offset
        # This probably could be made to work, but I think it's best
        # to leave it undefined for now as it shouldn't have any use.
        if latind in varying_axes["crpix"]:
            raise ValueError(
                "I didn't expect you to have a latitude index in your crpix tables, I don't know what to do."
            )
        crpix_table = crpix_table.reshape(varying_shape + [2])
        crpix_table = crpix_table << u.pix
    else:
        crpix_table = u.Quantity(
            [header[f"CRPIX{lonind}"], header[f"CRPIX{latind}"]],
            unit=u.pix,
        )

    crpix_table -= 1 * u.pix

    # Which daxes have DTYPE == "SPATIAL" (+1 to shift to FITS)
    primary_spatial_axes = (np.array(parser.axes_types) == "SPATIAL").nonzero()[0] + 1
    # If any axes the pointing is varying across have a primary type of SPATIAL
    # then we are a slit spectrograph where the pointing is changing with the
    # raster dimension (hopefully).
    slit = None
    if (np.array(vaxes)[:, None] == primary_spatial_axes).any():
        # The slit axis should be the second axis unless lat and lon are
        # backwards, then we are going to reverse the ordering of the pixel
        # dimensions below, so we have to reverse the axis which is the slit
        # axis.
        slit = int(latind > lonind)
    vct = varying_celestial_transform_from_tables(
        cdelt=cdelt, crpix_table=crpix_table, crval_table=crval_table, pc_table=pc_table, slit=slit
    )

    # Ensure we reverse the ordering of the inputs if we are flipping the axes
    if latind < lonind:
        mapping = list(range(vct.n_inputs))
        mapping[0] = 1
        mapping[1] = 0
        # Set up a mapping which is the identity mapping in the backward direction
        vct = (
            AsymmetricMapping(
                forward_mapping=mapping, backward_mapping=tuple(range(vct.inverse.n_outputs))
            )
            | vct
        )

    return np.mean(cdelt).to_value(u.arcsec / u.pix), vct


@u.quantity_input
def linear_spectral_model(spectral_width: u.nm, reference_val: u.nm):
    """
    Linear model in a spectral dimension. The reference pixel is always 0.
    """
    return m.Linear1D(slope=spectral_width / (1 * u.pix), intercept=reference_val, name="Spectral")


@u.quantity_input
def linear_time_model(cadence: u.s, reference_val: u.s = 0 * u.s):
    """
    Linear model in a temporal dimension. The reference pixel is always 0.
    """
    if reference_val is None:
        reference_val = 0 * cadence.unit
    return m.Linear1D(slope=cadence / (1 * u.pix), intercept=reference_val, name="Temporal")


def generate_lookup_table(lookup_table, interpolation="linear", points_unit=u.pix, **kwargs):
    if not isinstance(lookup_table, u.Quantity):
        raise TypeError("lookup_table must be a Quantity.")

    kwargs = {"bounds_error": False, "fill_value": np.nan, "method": interpolation, **kwargs}

    points = np.arange(lookup_table.size) * points_unit
    # TODO: Add a check here that points increases monotonically
    if lookup_table.ndim == 1:
        # The integer location is at the centre of the pixel.
        return m.Tabular1D(points, lookup_table, **kwargs)
    else:
        return Ravel(lookup_table.shape, order="F") | m.Tabular1D(
            # points is a tuple of 1D Quantity arrays but needs flattening
            points,
            lookup_table.flatten(order="F"),
            **kwargs,
        )


def time_model_from_date_obs(date_obs, date_beg=None):
    """
    Return a time model that best fits a list of dateobs's.
    """
    if not date_beg:
        date_beg = date_obs.flat[0]

    # I assume we need the .T here to change from fortran to C order which time expects
    deltas = Time(date_obs.T.flat, format="isot") - Time(date_beg.T.flat, format="isot")

    # Work out if we have a uniform delta (i.e. a linear model)
    ddelta = deltas.to(u.s)[1:] - deltas.to(u.s)[:-1]

    deltas = deltas.reshape(date_obs.shape, order="F")

    # If the length of the axis is one, then return a very simple model
    if ddelta.size == 0:
        raise ValueError(
            "Why do you have a temporal axis in the DTYPEn keys if you only have a len 1 time axis?"
        )
    elif u.allclose(ddelta[0], ddelta, atol=10 * u.us) and deltas.ndim == 1:
        slope = ddelta[0]
        intercept = 0 * u.s
        return slope.to_value(u.s), linear_time_model(cadence=slope, reference_val=intercept)
    else:
        logging.info(f"Creating tabular temporal axis. ddeltas: {ddelta}")
        return np.mean(deltas).to_value(u.s), generate_lookup_table(deltas.to(u.s), name="Temporal")


def spectral_model_from_framewave(framewav):
    """
    Construct a linear or lookup table model for wavelength based on the
    framewav keys.
    """
    framewav = u.Quantity(framewav, unit=u.nm)
    wave_beg = framewav[0]

    deltas = wave_beg - framewav
    ddeltas = deltas[:-1] - deltas[1:]
    # If the length of the axis is one, then return a very simple model
    if ddeltas.size == 0:
        raise ValueError(
            "Why do you have a spectral axis in the DTYPEn keys if you only have a len 1 spectral axis?"
        )
    if u.allclose(ddeltas[0], ddeltas):
        slope = ddeltas[0]
        return slope.to_value(u.nm), linear_spectral_model(slope, wave_beg)
    else:
        logging.info(f"creating tabular wavelength axis. ddeltas: {ddeltas}")
        return np.mean(ddeltas).to_value(u.nm), generate_lookup_table(framewav, name="Spectral")


class TransformBuilder:
    """
    This class builds compound models and frames in order when given axes types.
    """

    def __init__(self, header_parser: HeaderParser):
        if not isinstance(header_parser, HeaderParser):
            raise TypeError("Must specify the headers as a HeaderParser instance")

        self.parser = header_parser

        self.spectral_sampling = None
        self.spatial_sampling = None
        self.temporal_sampling = None

        # This must be last
        # Build the components of the transform
        self._build()

    @property
    def header(self):
        return self.parser.header

    @property
    def headers(self):
        return self.parser.headers

    @property
    def pixel_frame(self):
        """
        A `gwcs.coordinate_frames.CoordinateFrame` object describing the pixel frame.
        """
        DNAXIS = self.header["DNAXIS"]
        return cf.CoordinateFrame(
            naxes=DNAXIS,
            axes_type=["PIXEL"] * DNAXIS,
            axes_order=range(DNAXIS),
            unit=[u.pixel] * DNAXIS,
            axes_names=[self.header[f"DPNAME{n}"] for n in range(1, DNAXIS + 1)],
            name="pixel",
        )

    @property
    def gwcs(self):
        """
        `gwcs.WCS` object representing these headers.
        """
        world_frame = cf.CompositeFrame(self.frames)

        out_wcs = gwcs.WCS(
            forward_transform=self.transform, input_frame=self.pixel_frame, output_frame=world_frame
        )
        out_wcs.pixel_shape = self.parser.dataset_shape
        out_wcs.array_shape = self.parser.dataset_shape[::-1]

        return out_wcs

    @property
    def frames(self):
        """
        The coordinate frames, in Python order.
        """
        return self._frames

    @property
    def transform(self):
        """
        Return the compound model.
        """
        # self._transforms is a tuple of (pixel_axes, model, callable(right)).
        # The callable returns a CompoundModel instance when the right hand
        # side of the operator is passed.
        # We iterate backwards through the models generating the model for the
        # right hand side of the next step up the tree (i.e. from the inner
        # most operator to the outermost). So we start with the last model
        # instance (ignoring the callable), then pass that model to the next
        # callable as the right hand side, and continue to work our way back up
        # the tree.
        axes, right, _ = self._transforms[-1]
        pixel_inputs = [*axes]
        for axes, _, func in self._transforms[:-1][::-1]:
            pixel_inputs = [*axes, *pixel_inputs]
            right = func(right=right)

        # If any of the pixel axes are in the wrong order (i.e. spatial axes are split)
        # then we need to reorder the inputs to match.
        pixel_dtypes = set(self.parser.axes_types)
        pixel_indicies = {
            dtype: ind
            for dtype, ind in self.parser.pixel_axis_type_map.items()
            if dtype in pixel_dtypes
        }
        # If there is a jump in the pixel_indicies then we have a split axis and
        # need to compensate for it
        split_inputs = not all(
            [((np.array(a)[1:] - np.array(a)[:-1]) == 1).all() for a in pixel_indicies.values()]
        )
        # If the number of inputs to the generated transform doesn't match the
        # number of pixel dimensions in the dataset or the dimensions are not
        # uniformly ordered then we construct a mapping to share some pixel
        # inputs between multiple models
        expected_inputs = len(self.parser.dataset_shape)
        if (right.n_inputs != expected_inputs) or split_inputs:
            mapping = m.Mapping(pixel_inputs)
            right = mapping | right
        # If the number of inputs *still* doesn't match something has gone very wrong.
        if right.n_inputs != expected_inputs:
            raise ValueError(
                f"The transform that has been constructed has {right.n_inputs} inputs "
                f"which does not match the expected number ({expected_inputs}) of pixel inputs."
            )  # pragma: no cover

        # If any of the world axes are in the wrong order (i.e. spatial axes are split or transforms are reordered)
        # then we need to reorder the outputs to match.
        all_known_world_indices = np.concatenate(
            list(self.world_type_index_map.values()), axis=None
        )
        if (all_known_world_indices != np.arange(len(all_known_world_indices))).any():
            sorted_world_type_index_map = self.world_type_index_map
            spatial_indices = np.array(self.world_type_index_map["SPATIAL"])
            # If we don't have split spatial world axes
            if ((spatial_indices[1:] - spatial_indices[:-1]) == 1).all():
                # sort the type map to order the keys in order of world axes rather than transform.
                sorted_world_type_index_map = dict(
                    sorted(self.world_type_index_map.items(), key=lambda x: min(x[1]))
                )
                # Now change the values to be sequential in the transform order
                # (i.e. the order they are returned from the transform before
                # the mapping), but sorted into the order of the desired world
                # axes from the original type_index_map
                ind = 0
                for key, value in self.world_type_index_map.items():
                    sorted_world_type_index_map[key] = list(range(ind, ind + len(value)))
                    ind += len(value)

            all_known_world_indices = np.concatenate(
                list(sorted_world_type_index_map.values()), axis=None
            )
            right = right | m.Mapping(all_known_world_indices.tolist())

        return right

    """
    Internal Stuff
    """

    @staticmethod
    def _compound_model_partial(left, op="&"):
        return partial(CompoundModel, left=left, op=op)

    def _build(self):
        """
        Build the state of the thing.
        """
        make_map = {
            "STOKES": self.make_stokes,
            "TEMPORAL": self.make_temporal,
            "SPECTRAL": self.make_spectral,
            "SPATIAL": self.make_spatial,
        }

        # This is the number of world coordinates allowed for each physical type
        type_world_lengths = {
            "STOKES": 1,
            "TEMPORAL": 1,
            "SPECTRAL": 1,
            "SPATIAL": 2,
        }

        self._frames = []
        self._transforms = []

        # type_map is the mapping of world type to pixel axes.
        # i.e. the pixel axes along which a given world coordinate varies.
        type_map = self.parser.pixel_axis_type_map

        # Figure out what world indices map to what type
        world_type_index_map = {}
        for pixel_type, pixel_indices in type_map.items():
            pixel_indices = np.array(pixel_indices)
            all_known_world_indices = np.array([])
            if world_type_index_map:
                all_known_world_indices = np.concatenate(
                    list(world_type_index_map.values()), axis=None
                )

            # Make sure that we truncate any many pixel to fewer world transforms
            # For example this applies to 3 pixel spatial and 2 pixel temporal
            if len(pixel_indices) > type_world_lengths[pixel_type]:
                pixel_indices = pixel_indices[0 : type_world_lengths[pixel_type]]

            # Compute any overlap with the known list of world dimensions and
            # shift the output so there is no overlap
            world_offset = 0
            duplicate_indices = np.intersect1d(all_known_world_indices, pixel_indices)
            if duplicate_indices.any():
                world_offset = duplicate_indices.size

            # Check for a gap that might result from collapsing an index
            if (
                len(all_known_world_indices) > 0
                and min(pixel_indices) > max(all_known_world_indices) + 1
            ):
                # subtract 1 to make diff the offset that must be subtracted to correct for a gap
                diff = min(pixel_indices) - max(all_known_world_indices) - 1
                world_offset -= diff

            world_type_index_map[pixel_type] = (np.array(pixel_indices) + world_offset).tolist()

        self.world_type_index_map = world_type_index_map

        for dtype, axes in type_map.items():
            axes, frame, right, func = make_map[dtype](axes)
            self._frames.append(frame)
            self._transforms.append((axes, right, func))

    def get_units(self, *iargs):
        """
        Get zee units
        """
        return [self.header.get(f"DUNIT{i + 1}", None) for i in iargs]

    def make_stokes(self, axes):
        """
        Add a stokes axes to the builder.
        """
        if not len(axes) == 1:
            raise ValueError("There can only be one STOKES axis.")
        i = axes[0]

        name = self.header[f"DWNAME{i + 1}"]
        frame = cf.StokesFrame(axes_order=self.world_type_index_map["STOKES"], name=name)
        transform = generate_lookup_table(
            [1, 2, 3, 4] * u.one, interpolation="nearest", name="Stokes"
        )

        return axes, frame, transform, self._compound_model_partial(left=transform)

    def make_spectral(self, axes):
        """
        Decide how to make a spectral axes.
        """
        if not len(axes) == 1:
            raise ValueError("There can only be one SPECTRAL axis.")
        i = axes[0]
        n = i + 1
        name = self.header[f"DWNAME{n}"]
        frame = cf.SpectralFrame(
            axes_order=self.world_type_index_map["SPECTRAL"],
            axes_names=(name,),
            unit=self.get_units(i),
            name=name,
        )

        if "WAV" in self.header.get(f"CTYPE{n}", ""):  # Matches AWAV and WAVE
            self.spectral_sampling, transform = self.make_spectral_from_wcs(n)
        elif "FRAMEWAV" in self.header.keys():
            self.spectral_sampling, transform = self.make_spectral_from_dataset(n)
        else:
            raise ValueError(
                "Could not parse spectral WCS information from this header."
            )  # pragma: no cover

        return axes, frame, transform, self._compound_model_partial(left=transform)

    def make_temporal(self, axes):
        """
        Add a temporal axes to the builder.
        """
        frame = cf.TemporalFrame(
            axes_order=self.world_type_index_map["TEMPORAL"],
            name="temporal",
            axes_names=("time",),
            unit=(u.s,),
            reference_frame=Time(self.header["DATE-AVG"]),
        )
        dslice = self.parser.slice_for_dataset_array_axes(*axes, indexing="python")
        dates = self.parser.header_array[dslice]["DATE-AVG"]
        self.temporal_sampling, transform = time_model_from_date_obs(dates)
        return axes, frame, transform, self._compound_model_partial(left=transform)

    def make_spatial(self, axes):
        """
        Add a helioprojective spatial pair to the builder.
        """
        daxes = (np.array(axes) + 1).tolist()
        name = self.header[f"DWNAME{daxes[0]}"]
        name = name.split(" ")[0]

        # TODO: Ideally we would store these as arrays so they vary
        # I don't think that's really possible though, so we use the midpoint
        obstime = Time(self.parser.midpoint_header["DATE-AVG"])
        obsgeo = [self.parser.midpoint_header[k] for k in ("OBSGEO-X", "OBSGEO-Y", "OBSGEO-Z")]
        observer = ITRS(CartesianRepresentation(*obsgeo * u.m), obstime=obstime)

        # Make the frame.
        # We always order the transform and the frame lon, lat so lon is always
        # before lat in the world coordinates, because the inner transform has
        # to be this way round.

        # The dataset axes with a type of SPATIAL
        spatial_dind = [
            d for d in range(1, self.header["DNAXIS"] + 1) if self.header[f"DTYPE{d}"] == "SPATIAL"
        ]

        # Identify the indices of lat, lon based on CTYPE
        spatial_ind = identify_spatial_axes(self.header)
        # Extract the axes names from the header (so we don't hard code them)
        # but flip the order based on spatial_ind if needed.
        axes_names = [
            self.header[f"DWNAME{da}"] for _, da in sorted(zip(spatial_ind, spatial_dind))
        ]
        frame = cf.CelestialFrame(
            axes_order=self.world_type_index_map["SPATIAL"],
            name=name,
            reference_frame=Helioprojective(obstime=obstime, observer=observer),
            axes_names=axes_names,
            unit=self.get_units(*np.array(spatial_dind) - 1),
            axis_physical_types=(
                "custom:pos.helioprojective.lon",
                "custom:pos.helioprojective.lat",
            ),
        )

        # Make the transform
        varying_spatial_axes = self.parser.varying_spatial_daxes
        if varying_spatial_axes:
            self.spatial_sampling, transform = varying_spatial_model_from_headers(axes, self.parser)
            # At this point we have already verified that if there are both pc and
            # crval keys in this dict they are the same length, so just use the
            # first one.
            shared_inputs = len(list(varying_spatial_axes.values())[0])
            compound_partial = partial(
                CoupledCompoundModel, op="&", left=transform, shared_inputs=shared_inputs
            )
            # Crop off the axes which are shared by the previous model as they
            # have already been added
            axes = axes[:-shared_inputs]
        else:
            self.spatial_sampling, transform = spatial_model_from_header(self.header)
            compound_partial = self._compound_model_partial(left=transform)

        return axes, frame, transform, compound_partial

    def make_spectral_from_dataset(self, n):
        """
        Make a spectral axes from (VTF) dataset info.
        """
        s = self.parser.slice_for_dataset_array_axes(n - 1, indexing="python")
        framewave = np.array(self.parser.header_array[s]["FRAMEWAV"])
        return spectral_model_from_framewave(framewave)

    def make_spectral_from_wcs(self, n):
        """
        Add a spectral axes from the FITS-WCS keywords.
        """
        unit = u.Unit(self.header[f"CUNIT{n}"])
        spectral_cdelt = self.header[f"CDELT{n}"] * unit
        wavelength_at_pixel_zero = self.find_wavelength_at_zero_pixel(n)
        return spectral_cdelt.to_value(u.nm), linear_spectral_model(
            spectral_width=spectral_cdelt, reference_val=wavelength_at_pixel_zero * unit
        )

    def find_wavelength_at_zero_pixel(self, n):
        """
        Find the value of the wavelength at the zeroth pixel in the spectral dimension
        """
        return self.header[f"CRVAL{n}"] - (self.header[f"CRPIX{n}"] * self.header[f"CDELT{n}"])
