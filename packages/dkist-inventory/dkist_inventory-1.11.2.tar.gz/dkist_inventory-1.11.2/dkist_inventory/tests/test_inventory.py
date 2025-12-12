import copy
import datetime
import json
import re
from argparse import Namespace
from itertools import combinations

import astropy.units as u
import gwcs.coordinate_frames as cf
import numpy as np
import pytest
from astropy import table
from dkist.dataset.loader import ASDF_FILENAME_PATTERN
from dkist_data_simulator.spec214.visp import SimpleVISPDataset

from dkist_inventory.header_parsing import HeaderParser
from dkist_inventory.inventory import Distribution
from dkist_inventory.inventory import _closest_angle_to_zero
from dkist_inventory.inventory import _compute_edge_pixels
from dkist_inventory.inventory import _get_distribution
from dkist_inventory.inventory import _get_unique
from dkist_inventory.inventory import _inventory_from_headers
from dkist_inventory.inventory import _inventory_from_wcs
from dkist_inventory.inventory import compute_product_id
from dkist_inventory.inventory import extract_inventory
from dkist_inventory.inventory import generate_asdf_filename
from dkist_inventory.inventory import generate_inventory_from_frame_inventory
from dkist_inventory.inventory import generate_quality_report_filename
from dkist_inventory.inventory import process_json_headers
from dkist_inventory.transforms import TransformBuilder


@pytest.fixture
def headers_inventory_214_required():
    """A minimal collection of headers to test inventory creation."""  # noqa
    return table.Table(
        {
            "LINEWAV": [550, 550, 550],
            "XPOSURE": [10, 20, 30],
            "INSTRUME": ["VBI", "VBI", "VBI"],
            "RECIPEID": [10, 10, 10],
            "RINSTID": [20, 20, 20],
            "RRUNID": [30, 30, 30],
            "OBJECT": ["A", "B", "C"],
            "FRAMEVOL": [100, 120, 130],
            "NEXPERS": [3, 3, 3],
            "EXPER_ID": ["00", "00", "00"],
            "EXPRID01": ["00", "00", "00"],
            "EXPRID02": ["10", "10", "10"],
            "EXPRID03": ["20", "20", "20"],
            "NPROPOS": [3, 3, 3],
            "PROP_ID": ["001", "001", "001"],
            "PROPID01": ["001", "001", "001"],
            "PROPID02": ["30", "30", "30"],
            "DSETID": ["1234", "1234", "1234"],
            "DATE": ["2024/01/02T00:01:02", "2024/01/02T00:01:02", "2024/01/02T00:01:02"],
            "DNAXIS": [3, 3, 3],
            "DINDEX3": [1, 2, 3],
            "DAAXES": [2, 2, 2],
            "DEAXES": [1, 1, 1],
            "NAXIS": [2, 2, 2],
            "NAXIS1": [2, 2, 2],
            "NAXIS2": [2, 2, 2],
            "BUNIT": ["ct", "ct", "ct"],
            "HEADVERS": ["1.2.3"] * 3,
            "HEAD_URL": ["https://head_url.test"] * 3,
            "INFO_URL": ["https://info_url.test"] * 3,
            "CAL_URL": ["https://cal_url.test"] * 3,
            "DSHEALTH": ["GOOD", "GOOD", "ILL"],
            "DATE-BEG": ["2021-01-01T00:00:00", "2021-01-01T00:10:00", "2021-01-01T00:20:00"],
            "DATE-END": ["2021-01-01T00:05:00", "2021-01-01T00:15:00", "2021-01-01T00:25:00"],
            "IDSOBSID": [200] * 3,
            "PROCTYPE": ["L1"] * 3,
        }
    )


@pytest.fixture
def headers_inventory_214_optional(headers_inventory_214_required):
    """A minimal collection of headers to test inventory creation."""  # noqa
    # The distribution of `MaskedConstants` is intentional so that *every* row has at least one masked value,
    # which may offer important guard rails for future development.
    new_keys = {
        "ATMOS_R0": [1, np.ma.core.MaskedConstant(), 2],
        "POL_SENS": [500, 500, 500],
        "IP_ID": ["asdf"] * 3,
        "OBSPR_ID": ["qwer"] * 3,
        "WKFLVERS": ["zxcv"] * 3,
        "WKFLNAME": ["hjkl"] * 3,
        "HLSVERS": ["yuio"] * 3,
        "IDSCALID": [100] * 3,
        "IDSPARID": [300] * 3,
        "WAVEBAND": ["Some Line"] * 3,
        "LIGHTLVL": [1, 10, 100],
        "GOS_STAT": ["open", "open", "closed"],
        "AO_LOCK": [True, True, False],
        "NSPECLNS": [2, 2, 2],
        # SPECLNXX values can vary in position because they are evaluated on a frame by frame basis
        "SPECLN01": ["Fe XIII", "Fe XIII", "Na I"],
        "SPECLN02": ["Na I", "Na I", "Fe XIII"],
        # Important to have at least one masked value in the first row for testing `HeaderParser` instantiation
        "SPECLN03": [np.ma.core.MaskedConstant(), "Scott alpha", np.ma.core.MaskedConstant()],
        "MANPROCD": [True, True, True],
    }
    return table.hstack([headers_inventory_214_required, table.Table(new_keys)])


@pytest.fixture
def fake_transform_builder(request, mocker):
    markers = [marker for marker in request.node.own_markers if marker.name == "use_gwcs_fixture"]
    if len(markers) != 1:
        raise ValueError()

    transform_builder = mocker.Mock()
    transform_builder.gwcs = request.getfixturevalue(markers[0].args[0])
    transform_builder.spatial_sampling = 1
    transform_builder.spectral_sampling = None
    transform_builder.temporal_sampling = 0.4

    return transform_builder


@pytest.fixture
def dummy_wcs_with_axis_shape() -> Namespace:
    return Namespace(array_shape=(3, 4, 5, 6, 7))


def add_mongo_fields_to_header(fits_headers: list, pop_keys: tuple = None):
    pop_keys = pop_keys or tuple()
    for i, header in enumerate(fits_headers):
        header["createDate"] = datetime.datetime.utcnow().isoformat()
        header["updateDate"] = datetime.datetime.utcnow().isoformat()
        header["lostDate"] = datetime.datetime.utcnow().isoformat()
        header["objectKey"] = f"proposalid/datasetid/wibble_{i}.fits"
        header["bucket"] = "data"
        header["frameStatus"] = "it_is_a_frame"
        header["_id"] = 100 + i
        for key in pop_keys:
            header.pop(key)

    return fits_headers


def non_required_keys_combinations():
    keys = ["lostDate", "updateDate"]
    combo = []
    for i in range(len(keys) + 1):
        combo += list(combinations(keys, i))
    return combo


@pytest.fixture(
    scope="function", params=["headers_inventory_214_required", "headers_inventory_214_optional"]
)
def headers_214(request):
    """
    Parameterise over two fixtures
    """
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="function", params=non_required_keys_combinations())
def json_headers(headers_214, request):
    fits_headers = copy.deepcopy(_inventory_from_headers(headers_214))
    return add_mongo_fields_to_header([fits_headers], request.param)


def test_process_json_headers(json_headers, headers_214):
    filenames, fits_headers, extra_inventory = process_json_headers(
        json_headers[0]["bucket"], json_headers
    )
    assert filenames == ["wibble_0.fits"]
    assert fits_headers == [_inventory_from_headers(headers_214)]
    assert extra_inventory["original_frame_count"] == 1
    assert extra_inventory["bucket"] == "data"
    assert extra_inventory["create_date"]


def test_valid_inventory_required(headers_inventory_214_required):
    inv = _inventory_from_headers(headers_inventory_214_required)
    assert isinstance(inv, dict)

    assert inv["wavelengthMin"] == inv["wavelengthMax"] == 550
    assert inv["instrumentName"] == "VBI"
    assert inv["recipeId"] == 10
    assert inv["recipeInstanceId"] == 20
    assert inv["recipeRunId"] == 30
    assert set(inv["targetTypes"]) == {"A", "B", "C"}
    assert inv["primaryProposalId"] == "001"
    assert inv["primaryExperimentId"] == "00"
    for eid in inv["contributingExperimentIds"]:
        assert inv["contributingExperimentIds"].count(eid) == 1
        assert eid in ["10", "20", "00"]
    for pid in inv["contributingProposalIds"]:
        assert inv["contributingProposalIds"].count(pid) == 1
        assert pid in ["30", "001"]
    assert inv["headerDataUnitCreationDate"] == "2024/01/02T00:01:02"
    assert inv["headerVersion"] == "1.2.3"
    assert inv["headerDocumentationUrl"] == "https://head_url.test"
    assert inv["infoUrl"] == "https://info_url.test"
    assert inv["calibrationDocumentationUrl"] == "https://cal_url.test"

    assert inv["health"]["GOOD"] == 2
    assert inv["health"]["ILL"] == 1

    # Test default values
    assert inv["qualityAverageFriedParameter"] is np.nan
    assert inv["qualityAveragePolarimetricAccuracy"] is np.nan
    assert inv["workflowName"] == "unknown"
    assert inv["workflowVersion"] == "unknown"
    assert inv["workflowVersion"] == "unknown"

    assert inv["friedParameter"] is None
    assert inv["polarimetricAccuracy"] is None
    assert inv["lightLevel"] is None
    assert inv["spectralLines"] is None


def test_valid_inventory_optional(headers_inventory_214_optional):
    inv = _inventory_from_headers(headers_inventory_214_optional)
    assert isinstance(inv, dict)

    assert inv["wavelengthMin"] == inv["wavelengthMax"] == 550
    assert inv["instrumentName"] == "VBI"
    assert inv["qualityAverageFriedParameter"] == np.mean([1, 2])
    assert inv["qualityAveragePolarimetricAccuracy"] == 500
    assert inv["recipeId"] == 10
    assert inv["recipeInstanceId"] == 20
    assert inv["recipeRunId"] == 30
    assert set(inv["targetTypes"]) == {"A", "B", "C"}
    assert inv["primaryProposalId"] == "001"
    assert inv["primaryExperimentId"] == "00"
    for eid in inv["contributingExperimentIds"]:
        assert eid in ["10", "20", "00"]
    for pid in inv["contributingProposalIds"]:
        assert pid in ["30", "001"]
    assert inv["headerDataUnitCreationDate"] == "2024/01/02T00:01:02"
    assert inv["headerVersion"] == "1.2.3"
    assert inv["headerDocumentationUrl"] == "https://head_url.test"
    assert inv["infoUrl"] == "https://info_url.test"
    assert inv["calibrationDocumentationUrl"] == "https://cal_url.test"

    assert inv["workflowName"] == "hjkl"
    assert inv["workflowVersion"] == "zxcv"
    assert inv["inputDatasetParametersPartId"] == 300
    assert inv["inputDatasetObserveFramesPartId"] == 200
    assert inv["inputDatasetCalibrationFramesPartId"] == 100
    assert inv["observingProgramExecutionId"] == "qwer"
    assert inv["instrumentProgramExecutionId"] == "asdf"
    assert inv["polarimetricAccuracy"]["p25"] == 500
    assert inv["friedParameter"]["p25"] == 1.25
    assert inv["friedParameter"]["med"] == 1.5

    assert inv["lightLevel"]["min"] == 1
    assert inv["lightLevel"]["p25"] > 1
    assert inv["lightLevel"]["p25"] < 10
    assert inv["lightLevel"]["med"] == 10
    assert inv["lightLevel"]["p75"] > 10
    assert inv["lightLevel"]["p75"] < 100
    assert inv["lightLevel"]["max"] == 100

    assert inv["gosStatus"]["open"] == 2
    assert inv["gosStatus"]["closed"] == 1

    assert inv["aoLocked"] == 2
    assert inv["spectralLines"] == ["Fe XIII", "Na I", "Scott alpha"]


def test_inventory_compute_edge_pixels(dummy_wcs_with_axis_shape):
    """
    Given: A WCS object with the array_shape property
    When: Computing the indices for all the edge pixels
    Then: None of the interior pixels are included and the edge pixels are the correct length
    """
    non_edge_grid = np.meshgrid(
        *[np.arange(1, a - 1) for a in dummy_wcs_with_axis_shape.array_shape]
    )
    # This is a list of tuples containing the (x, y, z, ...) coordinates of every single interior (i.e., not on an edge)
    # pixel in the WCS array.
    non_edge_coords = list(zip(*[np.ravel(g) for g in non_edge_grid]))

    edge_idx = _compute_edge_pixels(dummy_wcs_with_axis_shape)
    # Convert edge_idx to the same (x, y, z, ...) format mentioned above
    edge_coords = list(zip(*edge_idx))

    # Make sure none of the edge pixels are inside the interior of the ND cube
    for idx_tuple in edge_coords:
        assert idx_tuple not in non_edge_coords

    # Make sure there are the correct number of edge pixels
    num_axes = len(dummy_wcs_with_axis_shape.array_shape)
    expected_num_edge_px = sum(
        [a * 2 ** (num_axes - 1) for a in dummy_wcs_with_axis_shape.array_shape]
    )
    assert all([len(i) == expected_num_edge_px for i in edge_idx])


def test_inventory_from_wcs(identity_gwcs_4d):
    inv = _inventory_from_wcs(identity_gwcs_4d)
    time_frame = list(
        filter(lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_4d.output_frame.frames)
    )[0]
    shape = identity_gwcs_4d.pixel_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["wavelengthMin"] == 0
    assert inv["wavelengthMax"] == shape[2] - 1
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat("T")
    assert inv["endTime"] == (time_frame.reference_frame + (shape[3] - 1) * u.s).datetime.isoformat(
        "T"
    )
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False


def test_inventory_from_wcs_stokes(identity_gwcs_5d_stokes):
    inv = _inventory_from_wcs(identity_gwcs_5d_stokes)
    time_frame = list(
        filter(
            lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_5d_stokes.output_frame.frames
        )
    )[0]
    shape = identity_gwcs_5d_stokes.pixel_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["wavelengthMin"] == 0
    assert inv["wavelengthMax"] == shape[2] - 1
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat("T")
    assert inv["endTime"] == (time_frame.reference_frame + (shape[3] - 1) * u.s).datetime.isoformat(
        "T"
    )
    assert inv["stokesParameters"] == ["I", "Q", "U", "V"]
    assert inv["hasAllStokes"] is True


def test_inventory_from_wcs_2d(identity_gwcs_3d_temporal):
    inv = _inventory_from_wcs(identity_gwcs_3d_temporal)
    time_frame = list(
        filter(
            lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_3d_temporal.output_frame.frames
        )
    )[0]
    shape = identity_gwcs_3d_temporal.pixel_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert "wavelengthMin" not in inv
    assert "wavelengthMax" not in inv
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat("T")
    assert inv["endTime"] == (time_frame.reference_frame + (shape[2] - 1) * u.s).datetime.isoformat(
        "T"
    )
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False


def test_unique_error():
    with pytest.raises(ValueError):
        _get_unique([1, 2, 3], singular=True)

    assert _get_unique([1, 2, 3], singular=False)


@pytest.mark.use_gwcs_fixture("identity_gwcs_4d")
def test_extract_inventory(headers_214, fake_transform_builder, identity_gwcs_4d):
    inv = extract_inventory(
        HeaderParser.from_headers(headers_214, validate=False),
        transform_builder=fake_transform_builder,
    )

    time_frame = list(
        filter(lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_4d.output_frame.frames)
    )[0]
    shape = identity_gwcs_4d.pixel_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["wavelengthMin"] == 0
    assert inv["wavelengthMax"] == shape[2] - 1
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat("T")
    assert inv["endTime"] == (time_frame.reference_frame + (shape[3] - 1) * u.s).datetime.isoformat(
        "T"
    )
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False
    assert inv["instrumentName"] == "VBI"
    assert inv["qualityAverageFriedParameter"] in (np.nan, np.mean([1, 2]))
    assert inv["qualityAveragePolarimetricAccuracy"] in (np.nan, 500)
    assert inv["recipeId"] == 10
    assert inv["recipeInstanceId"] == 20
    assert inv["recipeRunId"] == 30
    assert set(inv["targetTypes"]) == {"A", "B", "C"}
    assert inv["primaryProposalId"] == "001"
    assert inv["primaryExperimentId"] == "00"
    for eid in inv["contributingExperimentIds"]:
        assert eid in ["10", "20", "00"]
    for pid in inv["contributingProposalIds"]:
        assert pid in ["30", "001"]
    assert inv["hasSpectralAxis"] == False
    assert inv["hasTemporalAxis"] == True
    assert inv["averageDatasetSpectralSampling"] is None
    assert inv["averageDatasetSpatialSampling"] == 1
    assert inv["averageDatasetTemporalSampling"] == 0.4
    assert inv["qualityReportObjectKey"]

    # Check that we can dump to json
    assert json.dumps(inv)


@pytest.mark.use_gwcs_fixture("identity_gwcs_3d_temporal")
def test_extract_inventory_no_wave(
    headers_inventory_214_optional, fake_transform_builder, identity_gwcs_3d_temporal
):
    header_parser = HeaderParser.from_headers(headers_inventory_214_optional, validate=False)
    inv = extract_inventory(header_parser, transform_builder=fake_transform_builder)

    time_frame = list(
        filter(
            lambda x: isinstance(x, cf.TemporalFrame), identity_gwcs_3d_temporal.output_frame.frames
        )
    )[0]
    shape = identity_gwcs_3d_temporal.pixel_shape

    # This test transform is just 0 - n_pixel in all dimensions
    assert inv["boundingBox"] == ((0, 0), (shape[0] - 1, shape[1] - 1))
    assert inv["wavelengthMin"] == inv["wavelengthMax"] == 550
    assert inv["startTime"] == time_frame.reference_frame.datetime.isoformat("T")
    assert inv["endTime"] == (time_frame.reference_frame + (shape[2] - 1) * u.s).datetime.isoformat(
        "T"
    )
    assert inv["stokesParameters"] == ["I"]
    assert inv["hasAllStokes"] is False
    assert inv["instrumentName"] == "VBI"
    assert inv["qualityAverageFriedParameter"] == np.mean([1, 2])
    assert inv["qualityAveragePolarimetricAccuracy"] == 500
    assert inv["recipeId"] == 10
    assert inv["recipeInstanceId"] == 20
    assert inv["recipeRunId"] == 30
    assert set(inv["targetTypes"]) == {"A", "B", "C"}
    assert inv["primaryProposalId"] == "001"
    assert inv["primaryExperimentId"] == "00"
    for eid in inv["contributingExperimentIds"]:
        assert eid in ["10", "20", "00"]
    for pid in inv["contributingProposalIds"]:
        assert pid in ["30", "001"]
    assert inv["hasSpectralAxis"] == False
    assert inv["hasTemporalAxis"] == True
    assert inv["averageDatasetSpectralSampling"] is None
    assert inv["averageDatasetSpatialSampling"] == 1
    assert inv["averageDatasetTemporalSampling"] == 0.4
    assert inv["qualityReportObjectKey"]

    # Check that we can dump to json
    assert json.dumps(inv)


def test_extract_inventory_all_datasets(header_parser):
    inv = extract_inventory(header_parser)
    assert isinstance(inv, dict)


@pytest.fixture(scope="session")
def vbi_mosaic_headers(dataset):
    ds_gen = dataset("vbi-mosaic-blue")
    return ds_gen.generate_headers()


def test_vbi_mosaic(vbi_mosaic_headers):
    json_headers = add_mongo_fields_to_header(vbi_mosaic_headers)
    inventory = generate_inventory_from_frame_inventory("data", json_headers)
    # TODO: This test asserts the bounding box code gives the same answer it
    # did when it was first written With a known dataset we should check this
    # matches reality by plotting these coordinates
    np.testing.assert_allclose(
        inventory["boundingBox"], [[-84.29, -83.11], [-9.33, -7.97]], rtol=1e-5
    )

    # Check that we can dump to json
    assert json.dumps(inventory)


@pytest.mark.parametrize(
    "angle, expected",
    [
        pytest.param(-350.3216588987, -350.32, id="normal angle"),
        pytest.param(1295745.619448686, -254.38, id="positive rotation"),
        pytest.param(-1295821.510599849, 178.49, id="negative rotation"),
    ],
)
def test_closest_angle_to_zero(angle, expected):
    assert _closest_angle_to_zero(angle * u.arcsec) == expected


def test_stokes_shape(simulated_dataset):
    dataset_path = simulated_dataset("vtf")
    header_parser = HeaderParser.from_filenames(dataset_path.glob("*"))
    wcs = TransformBuilder(header_parser).gwcs

    acm = np.array(
        [
            [True, True, False, False, False],  # noqa
            [True, True, False, False, False],  # noqa
            [False, False, True, False, False],  # noqa
            [False, False, True, True, False],  # noqa
            [False, False, False, False, True],
        ]
    )  # noqa

    assert acm.shape == wcs.axis_correlation_matrix.shape
    assert np.allclose(wcs.axis_correlation_matrix, acm)
    inventory = _inventory_from_wcs(wcs)
    assert inventory["stokesParameters"] == ["I", "Q", "U", "V"]


def test_time_varying_visp_wcs(simulated_dataset):
    # this is upsettingly wrong
    dataset_path = simulated_dataset("visp-time-varying-single")
    header_parser = HeaderParser.from_filenames(dataset_path.glob("*"))
    wcs = TransformBuilder(header_parser).gwcs
    inventory = _inventory_from_wcs(wcs)


def test_spectral_limit_determination(simulated_dataset, cached_tmpdir):
    """
    Given: a VISP dataset
    When: finding the maximum and minimum wavelengths in inventory
    Then: they match the values calculated from the coordinate system
    """
    dataset_name = "visp_spectral_limit_determination"
    dataset_path = cached_tmpdir / dataset_name
    linewave = 500
    length_of_axis = 50
    ds = SimpleVISPDataset(
        n_maps=1,
        n_steps=2,
        n_stokes=4,
        time_delta=5,
        linewave=linewave * u.nm,
        detector_shape=(length_of_axis, length_of_axis),
    )
    ds.generate_files(
        base_path=dataset_path, filename_template=f"{dataset_name.upper()}_{{ds.index}}.fits"
    )
    header_parser = HeaderParser.from_filenames(dataset_path.glob("*"))
    wcs = TransformBuilder(header_parser).gwcs
    inventory = _inventory_from_wcs(wcs)
    expected_wavelength_min = ds.linewave - (ds.spectral_scale * 0.5 * length_of_axis * u.pix)
    expected_wavelength_max = ds.linewave + (ds.spectral_scale * 0.5 * (length_of_axis - 1) * u.pix)
    assert u.allclose(inventory["wavelengthMin"] * u.nm, expected_wavelength_min)
    assert u.allclose(inventory["wavelengthMax"] * u.nm, expected_wavelength_max)


def test_distribution():
    """
    Given: various numeric inputs
    When: finding the distribution
    Then: calculate Distribution values as permissively as possible
    """

    assert _get_distribution([]) is None

    d1 = _get_distribution([1.0])
    assert d1 is not None
    assert d1["min"] == 1
    assert d1["p75"] == 1

    d2 = _get_distribution([0.0, 10])
    assert d2 is not None
    assert d2["med"] == 5
    assert d2["p25"] == 2.5
    assert d2["p75"] == 7.5

    d3 = _get_distribution([0.0, 10, 100])
    assert d3 is not None
    assert d3["med"] == 10
    assert d3["p25"] == 5.0
    assert d3["p75"] == 55.0


def test_generate_asdf_filename():
    instrument = "VBI"
    start_time = datetime.datetime(2024, 1, 5, 4, 9, 6)
    dataset_id = "AJFNR"
    asdf_filename = generate_asdf_filename(
        instrument=instrument, start_time=start_time, dataset_id=dataset_id
    )
    assert asdf_filename == "VBI_L1_20240105T040906_AJFNR_metadata.asdf"
    assert bool(re.match(ASDF_FILENAME_PATTERN, asdf_filename))


def test_generate_quality_report_filename():
    dataset_id = "DALEX"
    quality_report_filename = generate_quality_report_filename(dataset_id=dataset_id)
    assert quality_report_filename == "DALEX_quality_report.pdf"


@pytest.mark.parametrize(
    "product_value, expected_product_id",
    [
        pytest.param("from_product_header", "from_product_header", id="product_header_exists"),
        # IDSOBSID of 200
        pytest.param(None, "L1-YDWFH", id="no_product_header"),
    ],
)
def test_product_id(
    product_value: str | None,
    expected_product_id: str,
    headers_inventory_214_required: table.Table,
):
    """
    Given: fits headers
    When: calculating productId
    Then: productId is computed properly
    """
    if product_value is not None:
        extra_col = {
            "PRODUCT": [product_value] * 3,
        }
        fits_headers = table.hstack([headers_inventory_214_required, table.Table(extra_col)])
    else:
        fits_headers = headers_inventory_214_required
    inventory = _inventory_from_headers(fits_headers)
    assert inventory.get("productId") is not None
    assert inventory["productId"] == expected_product_id


@pytest.mark.parametrize(
    "mandprocd_values, expected_is_manually_processed",
    [
        pytest.param(None, False, id="none"),
        pytest.param([False, False, False], False, id="all_false"),
        pytest.param([True, True, True], True, id="all_true"),
    ],
)
def test_is_manually_processed(
    mandprocd_values: list[bool] | None,
    expected_is_manually_processed: bool,
    headers_inventory_214_required: table.Table,
):
    """
    Given: fits headers
    When: calculating isManuallyProcessed
    Then: isManuallyProcessed is computed properly
    """
    if mandprocd_values is not None:
        extra_col = {
            "MANPROCD": mandprocd_values,
        }
        fits_headers = table.hstack([headers_inventory_214_required, table.Table(extra_col)])
    else:
        fits_headers = headers_inventory_214_required
    inventory = _inventory_from_headers(fits_headers)
    assert inventory.get("isManuallyProcessed") is not None
    assert isinstance(inventory.get("isManuallyProcessed"), bool)
    assert inventory["isManuallyProcessed"] == expected_is_manually_processed


@pytest.mark.parametrize(
    "ids_obs_id, proc_type",
    [
        pytest.param(42, "alpha", id="42"),
        pytest.param(1_000, "beta", id="thousand"),
        pytest.param(1_000_000, "gamma", id="million"),
    ],
)
def test_product_id_calculation(ids_obs_id: int, proc_type: str):
    """
    Given: integer IDSOBSID and string PROCTYPE
    When: calculating the productId
    Then: the productId is computed properly
    """
    product_id = compute_product_id(ids_obs_id, proc_type)
    assert isinstance(product_id, str)
    assert product_id.startswith(f"{proc_type}-")
    assert len(product_id) >= len(proc_type) + 6
    # same result the second time around
    assert product_id == compute_product_id(ids_obs_id, proc_type)
