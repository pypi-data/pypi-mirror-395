import warnings

import astropy.units as u
import gwcs
import gwcs.coordinate_frames as cf
import numpy as np
import pytest
from astropy.coordinates import SkyCoord
from astropy.coordinates.matrix_utilities import angle_axis
from astropy.coordinates.matrix_utilities import rotation_matrix
from astropy.io import fits
from astropy.modeling import Model
from astropy.modeling import models
from astropy.time import Time
from astropy.wcs import WCS
from dkist.wcs.models import BaseVaryingCelestialTransform
from dkist_data_simulator.spec214.cryo import SimpleCryonirspCIDataset
from dkist_data_simulator.spec214.cryo import SimpleCryonirspSPDataset
from dkist_data_simulator.spec214.vbi import SimpleVBIDataset
from dkist_data_simulator.spec214.vbi import TimeDependentVBIDataset
from dkist_data_simulator.spec214.visp import SimpleVISPDataset
from dkist_data_simulator.spec214.visp import TimeDependentVISPDataset

from dkist_inventory.header_parsing import HeaderParser
from dkist_inventory.transforms import TransformBuilder
from dkist_inventory.transforms import linear_spectral_model
from dkist_inventory.transforms import linear_time_model
from dkist_inventory.transforms import spatial_model_from_header
from dkist_inventory.transforms import spectral_model_from_framewave
from dkist_inventory.transforms import time_model_from_date_obs


@pytest.fixture
def wcs(header_parser):
    # If it's a mosaic dataset use the wcs of the first tile
    transform_builder = TransformBuilder(header_parser.group_mosaic_tiles()[0])
    return transform_builder.gwcs


@pytest.fixture
def non_varying_wcs(non_varying_transform_builder):
    return non_varying_transform_builder.gwcs


def test_transform(transform_builder):
    assert isinstance(transform_builder.transform, Model)


def test_frames(transform_builder):
    frames = transform_builder.frames
    assert all([isinstance(frame, cf.CoordinateFrame) for frame in frames])


def test_roundtrip(wcs, dataset_name):
    """
    Test that a pixel>world>pixel transformation gives the same outputs as inputs.

    This asserts that the forward and backwards transforms run without error.
    """
    pixel_inputs = [0] * wcs.pixel_n_dim
    world_outputs = wcs.pixel_to_world_values(*pixel_inputs)
    pixel_outputs = wcs.world_to_pixel_values(*world_outputs)
    assert np.allclose(pixel_inputs, pixel_outputs, atol=1e-6)


def test_input_name_ordering(transform_builder):
    # Check the ordering of the input and output frames
    wcs = transform_builder.gwcs
    allowed_pixel_names = {
        "VISP": (
            ("slit position", "wavelength", "raster position", "scan number"),
            ("slit position", "wavelength", "raster position", "scan number", "stokes"),
            ("slit position", "wavelength", "raster position"),
            ("slit position", "wavelength", "raster position", "stokes"),
            ("wavelength", "slit position", "raster position", "scan number"),
            ("wavelength", "slit position", "raster position", "scan number", "stokes"),
            ("wavelength", "slit position", "raster position"),
            ("wavelength", "slit position", "raster position", "stokes"),
        ),
        "VTF": (
            ("spatial x", "spatial y", "scan position", "scan repeat number", "stokes"),
            ("spatial x", "spatial y", "scan position", "scan repeat number"),
            ("spatial x", "spatial y", "scan position"),
        ),
        "VBI": (("spatial x", "spatial y", "frame number"),),
        "CRYO-NIRSP": (
            # SP
            (
                "dispersion axis",
                "spatial along slit",
                "map scan step number",
                "scan number",
                "stokes",
            ),
            ("dispersion axis", "spatial along slit", "map scan step number", "scan number"),
            (
                "dispersion axis",
                "spatial along slit",
                "measurement number",
                "map scan step number",
                "scan number",
                "stokes",
            ),
            (
                "dispersion axis",
                "spatial along slit",
                "measurement number",
                "map scan step number",
                "scan number",
            ),
            ("dispersion axis", "spatial along slit", "measurement number", "map scan step number"),
            # CI
            (
                "helioprojective latitude",
                "helioprojective longitude",
                "map scan step number",
                "scan number",
                "stokes",
            ),
            (
                "helioprojective latitude",
                "helioprojective longitude",
                "map scan step number",
                "scan number",
            ),
            (
                "helioprojective latitude",
                "helioprojective longitude",
                "measurement number",
                "map scan step number",
                "scan number",
                "stokes",
            ),
            (
                "helioprojective latitude",
                "helioprojective longitude",
                "measurement number",
                "map scan step number",
                "scan number",
            ),
        ),
        "DL-NIRSP": (("spatial x", "spatial y", "wavelength", "mosaic repeat"),),
    }
    assert wcs.input_frame.axes_names in allowed_pixel_names[transform_builder.header["INSTRUME"]]


def test_output_name_ordering(transform_builder):
    wcs = transform_builder.gwcs

    allowed_world_names = {
        "VISP": (
            # These are split to correspond to the order of the `_values`
            # numbers not the high level objects.
            ("helioprojective longitude", "wavelength", "helioprojective latitude", "time"),
            (
                "helioprojective longitude",
                "wavelength",
                "helioprojective latitude",
                "time",
                "stokes",
            ),
        ),
        "VTF": (
            (
                "helioprojective longitude",
                "helioprojective latitude",
                "wavelength",
                "time",
                "stokes",
            ),
            ("helioprojective longitude", "helioprojective latitude", "wavelength", "time"),
        ),
        "VBI": (("helioprojective longitude", "helioprojective latitude", "time"),),
        "CRYO-NIRSP": (
            # SP
            ("wavelength", "helioprojective longitude", "helioprojective latitude", "time"),
            (
                "wavelength",
                "helioprojective longitude",
                "helioprojective latitude",
                "time",
                "stokes",
            ),
            # If multi-meas are present (time), they come before latitude
            ("wavelength", "helioprojective longitude", "time", "helioprojective latitude"),
            (
                "wavelength",
                "helioprojective longitude",
                "time",
                "helioprojective latitude",
                "stokes",
            ),
            # CI
            ("helioprojective longitude", "helioprojective latitude", "time"),
            ("helioprojective longitude", "helioprojective latitude", "time", "stokes"),
            # ??
            ("wavelength", "helioprojective longitude", "time", "helioprojective latitude"),
            # TODO: This is wrong, but I am not going to fix it until we are actually testing with cryo data
            # We should be able to delete all of these and the tests still pass
            ("wavelength", "helioprojective latitude", "time", "helioprojective longitude"),
            (
                "wavelength",
                "helioprojective latitude",
                "time",
                "helioprojective longitude",
                "stokes",
            ),
            ("wavelength", "helioprojective latitude", "helioprojective longitude", "time"),
            (
                "wavelength",
                "helioprojective latitude",
                "helioprojective longitude",
                "time",
                "stokes",
            ),
            ("helioprojective latitude", "helioprojective longitude", "time"),
            ("helioprojective latitude", "helioprojective longitude", "time", "stokes"),
        ),
        "DL-NIRSP": (
            ("helioprojective longitude", "helioprojective latitude", "wavelength", "time"),
        ),
    }

    assert wcs.output_frame.axes_names in allowed_world_names[transform_builder.header["INSTRUME"]]


def test_output_frames(transform_builder):
    wcs = transform_builder.gwcs
    allowed_frame_orders = {
        "VISP": (
            (cf.CelestialFrame, cf.SpectralFrame, cf.TemporalFrame, cf.StokesFrame),
            (cf.CelestialFrame, cf.SpectralFrame, cf.TemporalFrame),
            (cf.SpectralFrame, cf.CelestialFrame, cf.TemporalFrame, cf.StokesFrame),
            (cf.SpectralFrame, cf.CelestialFrame, cf.TemporalFrame),
        ),
        "VTF": (
            (cf.CelestialFrame, cf.SpectralFrame, cf.TemporalFrame, cf.StokesFrame),
            (cf.CelestialFrame, cf.SpectralFrame, cf.TemporalFrame),
        ),
        "VBI": ((cf.CelestialFrame, cf.TemporalFrame),),
        "CRYO-NIRSP": (
            # SP
            (cf.SpectralFrame, cf.CelestialFrame, cf.TemporalFrame, cf.StokesFrame),
            (cf.SpectralFrame, cf.CelestialFrame, cf.TemporalFrame),
            # CI
            (cf.CelestialFrame, cf.TemporalFrame, cf.StokesFrame),
            (cf.CelestialFrame, cf.TemporalFrame),
        ),
        "DL-NIRSP": ((cf.CelestialFrame, cf.SpectralFrame, cf.TemporalFrame),),
    }
    types = tuple((type(frame) for frame in wcs.output_frame.frames))
    assert types in allowed_frame_orders[transform_builder.header["INSTRUME"]]


def test_transform_models(non_varying_wcs):
    # Test that there is one lookup table and two linear models for both the
    # wcses
    sms = non_varying_wcs.forward_transform._leaflist
    smtypes = [type(m) for m in sms]
    if len(smtypes) == 4:  # VTF and VISP
        assert sum(mt is models.Linear1D for mt in smtypes) == 2
        assert sum(mt is models.Tabular1D for mt in smtypes) == 1
    if len(smtypes) == 2:  # VBI
        assert sum(mt is models.Linear1D for mt in smtypes) == 1


def first_header(header_filenames):
    return fits.getheader(header_filenames[0])


def test_spatial_model(header_filenames):
    sampling, spatial = spatial_model_from_header(first_header(header_filenames))
    assert isinstance(spatial, Model)


def test_linear_spectral():
    lin = linear_spectral_model(10 * u.nm, 0 * u.nm)
    assert isinstance(lin, models.Linear1D)
    assert u.allclose(lin.slope, 10 * u.nm / u.pix)
    assert u.allclose(lin.intercept, 0 * u.nm)


def test_linear_time():
    lin = linear_time_model(10 * u.s)
    assert isinstance(lin, models.Linear1D)
    assert u.allclose(lin.slope, 10 * u.s / u.pix)
    assert u.allclose(lin.intercept, 0 * u.s)


@pytest.mark.parametrize("dataset_name", ["vbi"])
def test_time_from_dateobs(dataset_name, simulated_dataset):
    directory = simulated_dataset(dataset_name)
    header_filenames = directory.glob("*")
    date_obs = [fits.getheader(f)["DATE-BEG"] for f in header_filenames]
    date_obs.sort()
    delta = Time(date_obs[1]) - Time(date_obs[0])
    sampling, time = time_model_from_date_obs(np.array(date_obs))
    assert isinstance(time, models.Linear1D)
    np.testing.assert_allclose(time.slope, delta.to(u.s) / (1 * u.pix))


def test_time_from_dateobs_lookup(header_filenames):
    date_obs = [fits.getheader(f)["DATE-BEG"] for f in header_filenames]
    date_obs[3] = (Time(date_obs[3]) + 10 * u.s).isot
    deltas = Time(date_obs) - Time(date_obs[0])
    sampling, time = time_model_from_date_obs(np.array(date_obs))
    assert isinstance(time, models.Tabular1D)
    assert (time.lookup_table == deltas.to(u.s)).all()
    np.testing.assert_allclose(time.lookup_table, deltas.to(u.s))


def test_spectral_framewave(header_filenames):
    head = first_header(header_filenames)

    # Skip the VISP headers
    if "FRAMEWAV" not in head:
        return

    nwave = head["DNAXIS3"]
    framewave = [fits.getheader(h)["FRAMEWAV"] for h in header_filenames]

    sampling, m = spectral_model_from_framewave(framewave[:nwave])
    assert isinstance(m, models.Linear1D)

    sampling, m2 = spectral_model_from_framewave(framewave)
    assert isinstance(m2, models.Tabular1D)


def test_time_varying_vbi_wcs(vbi_time_varying_transform_builder):
    if not hasattr(Model, "_calculate_separability_matrix"):
        pytest.skip()
    wcs = vbi_time_varying_transform_builder.gwcs
    assert np.allclose(
        wcs.axis_correlation_matrix,
        np.array([[True, True, True], [True, True, True], [False, False, True]]),  # noqa  # noqa
    )


def test_non_time_varying_vtf(dataset):
    ds = dataset("vtf")
    wcs = TransformBuilder(HeaderParser.from_headers(ds.generate_headers())).gwcs
    assert wcs.forward_transform.n_inputs == 5


def test_split_visp_matrix(dataset):
    """
    Given:
        A VISP dataset where the spatial pixel axes are not next to each
        other and there is no need to duplicate pixel inputs to the transform
    Then:
        Generate a WCS
    Assert:
        The axis correlation matrix matches the expected matrix
    """
    ds = dataset("visp-time-varying-single")
    header_parser = HeaderParser.from_headers(ds.generate_headers())
    builder = TransformBuilder(header_parser)
    wcs = builder.gwcs

    # This test case is Stokes I only, one map scan, 4 raster steps.
    # We have 3 pixel axes: slit_y, disperson, raster
    # and 4 world axes: lat, lon, wave, time
    # Time varies along the raster dimension
    # lat and lon vary along slit_y and also raster
    # wave varies along dispersion

    # breakpoint()
    # Remember that the correlation matrix is (world, pixel)
    # i.e. rows are world axes, cols are pixel axes
    np.testing.assert_allclose(
        wcs.axis_correlation_matrix,
        [[True, False, True], [False, True, False], [True, False, True], [False, False, True]],
    )


def test_split_visp_matrix_dupe(dataset):
    """
    Given:
        A VISP dataset where the spatial pixel axes are not next to each
        other and there is a need to duplicate pixel inputs to the transform
    Then:
        Generate a WCS
    Assert:
        The axis correlation matrix matches the expected matrix
    """
    ds = dataset("visp")
    header_parser = HeaderParser.from_headers(ds.generate_headers())
    builder = TransformBuilder(header_parser)
    wcs = builder.gwcs

    # This test case is full stokes, two map scans, 2 raster steps.
    # We have 5 pixel axes: slit_y, disperson, raster, scan number, stokes
    # and 5 world axes: lat, lon, wave, time, stokes
    # Time varies along the raster dimension and the scan number dimension
    # lat and lon vary along slit_y and raster (not scan number as this has a fixed pointing)
    # wave varies along dispersion

    # Remember that the correlation matrix is (world, pixel)
    # i.e. rows are world axes, cols are pixel axes
    assert np.allclose(
        wcs.axis_correlation_matrix,
        [
            [True, False, True, False, False],
            [False, True, False, False, False],
            [True, False, True, False, False],
            [False, False, True, True, False],
            [False, False, False, False, True],
        ],
    )


"""
The following set of helpers and tests are to validate and help develop how we build the VISP WCSes.
Specifically, they are to validate how we invert the two spatial axes ordering in the gWCS.

In the FITS headers latitude is the first axis and longitude is the third axis.
In the gWCS the two spatial axes have to be ordered lon, lat.
These tests are to help ensure that we are doing that inversion correctly.
"""


class RotatedVISPDataset(SimpleVISPDataset):
    def __init__(self, *args, rotation_angle=0 * u.deg, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotation_angle = rotation_angle

    @property
    def fits_wcs(self):
        w = super().fits_wcs
        spatial_pc_new = rotation_matrix(self.rotation_angle)[:2, :2]
        # Now insert the spectral axes into the pc matrix
        # First insert two zeros as the second row to pad the non-spectral axes
        pc_new = np.insert(spatial_pc_new, 1, [0, 0], axis=0)
        # then insert the spectral column into the new (3, 2) matrix
        pc_new = np.insert(pc_new, 1, [0, 1, 0], axis=1)
        w.wcs.pc = pc_new
        return w


class RotatedVBIDataset(SimpleVBIDataset):
    def __init__(self, *args, rotation_angle=0 * u.deg, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotation_angle = rotation_angle

    @property
    def fits_wcs(self):
        w = super().fits_wcs
        w.wcs.pc = rotation_matrix(self.rotation_angle)[:2, :2]
        return w


@u.quantity_input
def matrix2d_to_angle(matrix) -> u.Quantity[u.deg]:
    matrix_3d = np.identity(3)
    matrix_3d[:2, :2] = matrix
    if (matrix_3d == np.identity(3)).all():
        return 0 * u.deg

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        angle, axis = angle_axis(matrix_3d)

    return angle * axis[-1]


# @pytest.fixture(params=np.linspace(-60, 60, 7, endpoint=True).tolist())
@pytest.fixture
def rotation_angle(request):
    return 0 * u.deg


@pytest.fixture
@u.quantity_input
def visp_header_parser(rotation_angle: u.Quantity[u.deg]):
    dataset = RotatedVISPDataset(
        1,
        10,
        1,
        1,
        linewave=500 * u.nm,
        detector_shape=(1000, 2560),
        slit_width=0.06 * u.arcsec,
        rotation_angle=rotation_angle,
        raster_step=0.12 * u.arcsec,
    )

    headers = dataset.generate_headers()
    hp = HeaderParser.from_headers(headers)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wcs = WCS(hp.header)
    # Set the WCS shape to equal the whole raster scan
    wcs._naxis[2] = hp.header["DNAXIS3"]
    tb = TransformBuilder(hp)

    return hp, wcs, tb.gwcs


@pytest.fixture
@u.quantity_input
def vbi_header_parser(rotation_angle: u.Quantity[u.deg]):
    dataset = RotatedVBIDataset(
        n_time=5,
        time_delta=1,
        linewave=500 * u.nm,
        rotation_angle=rotation_angle,
    )

    headers = dataset.generate_headers()
    hp = HeaderParser.from_headers(headers)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wcs = WCS(hp.header)

    tb = TransformBuilder(hp)

    return hp, wcs, tb.gwcs


def extract_pcs(wcs, gwcs):
    spatial_pc = wcs.wcs.pc
    if spatial_pc.shape == (3, 3):
        spatial_pc = np.delete(np.delete(spatial_pc, 1, 1), 1, 0)
    # This will only work for the non-varying transform
    # Extract the matrix by finding the Affinetransform in the model
    aft = next(
        filter(
            lambda sm: isinstance(sm, models.AffineTransformation2D),
            gwcs.forward_transform.traverse_postorder(),
        )
    )
    wcs_pc = aft.matrix.value

    return spatial_pc, wcs_pc


def extract_skycoord(coord):
    if isinstance(coord, SkyCoord):
        return coord
    return next(filter(lambda x: isinstance(x, SkyCoord), coord))


@pytest.fixture
def fixture_finder(request):
    return request.getfixturevalue(request.param)


def get_border_coords(wcs, initial_ind=0, spatial_pixel_axes=None):
    if spatial_pixel_axes is None:
        world_axis_lat = np.argwhere(["lat" in s for s in wcs.world_axis_physical_types])[0, 0]
        pixel_axes = np.argwhere(wcs.axis_correlation_matrix[world_axis_lat]).T[0]
    else:
        pixel_axes = spatial_pixel_axes

    nx, ny = np.array(wcs.pixel_shape)[pixel_axes]
    n_per_edge = 101
    xs = np.linspace(-0.5, nx - 0.5, n_per_edge)
    ys = np.linspace(-0.5, ny - 0.5, n_per_edge)
    xs = np.concatenate((xs, np.full(n_per_edge, xs[-1]), xs, np.full(n_per_edge, xs[0])))
    ys = np.concatenate((np.full(n_per_edge, ys[0]), ys, np.full(n_per_edge, ys[-1]), ys))

    xx = [initial_ind] * wcs.pixel_n_dim
    xx[pixel_axes[1]] = xs
    xx[pixel_axes[0]] = ys
    x = np.broadcast_arrays(*xx)
    return extract_skycoord(wcs.pixel_to_world(*x))


@pytest.mark.parametrize(
    "fixture_finder",
    [
        "vbi_header_parser",
        "visp_header_parser",
    ],
    indirect=True,
)
def test_compare_fits_to_gwcs_coords(fixture_finder, rotation_angle):
    parser, wcs, g_wcs = fixture_finder
    spatial_pc, gwcs_pc = extract_pcs(wcs, g_wcs)

    wcs_angle = matrix2d_to_angle(spatial_pc)
    gwcs_angle = matrix2d_to_angle(gwcs_pc)

    assert u.allclose(rotation_angle, wcs_angle)
    if parser.header["INSTRUME"] == "VISP":
        # The rotation for gwcs has opposite sign
        # because the lat/lon axes are flipped
        assert u.allclose(wcs_angle, gwcs_angle * -1)
    else:
        assert u.allclose(wcs_angle, gwcs_angle)

    coords_gwcs = get_border_coords(g_wcs)
    coords_wcs = get_border_coords(wcs)

    assert u.allclose(coords_wcs.Ty, coords_gwcs.Ty)
    assert u.allclose(coords_wcs.Tx, coords_gwcs.Tx)


@pytest.fixture
@u.quantity_input
def rotation_shift_rate() -> u.Quantity[u.deg / u.s]:
    return 0 * u.deg / u.s


@pytest.fixture
@u.quantity_input
def visp_varying_header_parser(
    rotation_angle: u.Quantity[u.deg],
    rotation_shift_rate: u.Quantity[u.deg / u.s],
):
    dataset = TimeDependentVISPDataset(
        1,
        10,
        1,
        1,
        linewave=500 * u.nm,
        detector_shape=(1000, 2560),
        slit_width=0.06 * u.arcsec,
        rotation_angle=rotation_angle,
        raster_step=0.1 * u.arcsec,
        rotation_shift_rate=rotation_shift_rate,
    )

    headers = dataset.generate_headers()
    hp = HeaderParser.from_headers(headers)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wcses = []
        for header in hp.headers:
            wcses.append(WCS(dict(header)))
    tb = TransformBuilder(hp)

    return hp, wcses, tb.gwcs


@pytest.fixture
@u.quantity_input
def cryo_sp_header_parser(rotation_angle: u.Quantity[u.deg]):
    dataset = SimpleCryonirspSPDataset(
        n_meas=1, n_steps=7, n_maps=1, n_stokes=1, time_delta=10, linewave=1083 * u.nm
    )

    headers = dataset.generate_headers()
    hp = HeaderParser.from_headers(headers)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wcses = []
        for header in hp.headers:
            wcses.append(WCS(dict(header)))

    tb = TransformBuilder(hp)

    return hp, wcses, tb.gwcs


def extract_pcs_varying(wcs, g_wcs):
    spatial_pc = wcs.wcs.pc
    if spatial_pc.shape == (3, 3):
        spatial_pc = np.delete(np.delete(spatial_pc, 1, 1), 1, 0)
    # This will only work for the non-varying transform
    # Extract the matrix by finding the VaryingTransform in the model
    aft = next(
        filter(
            lambda sm: isinstance(sm, BaseVaryingCelestialTransform),
            g_wcs.forward_transform.traverse_postorder(),
        )
    )
    wcs_pc = aft.pc_table.value
    return spatial_pc, wcs_pc


@pytest.mark.parametrize(
    "fixture_finder", ["visp_varying_header_parser", "cryo_sp_header_parser"], indirect=True
)
def test_compare_fits_to_gwcs_varying(fixture_finder, rotation_angle, rotation_shift_rate):
    parser, wcses, g_wcs = fixture_finder
    instrument = parser.header["INSTRUME"]
    for iraster, wcs in enumerate(wcses):
        spatial_pc, gwcs_pc = extract_pcs_varying(wcs, g_wcs)

        # Check the first angle
        wcs_angle = matrix2d_to_angle(spatial_pc)
        gwcs_angle = matrix2d_to_angle(gwcs_pc[iraster])

        assert u.allclose(rotation_angle + rotation_shift_rate * (iraster * u.s), wcs_angle)
        if instrument == "VISP":
            # The rotation for gwcs has opposite sign
            # because the lat/lon axes are flipped
            assert u.allclose(wcs_angle, gwcs_angle * -1)
        else:
            assert u.allclose(wcs_angle, gwcs_angle)

        slit_pixel_coords = np.arange(parser.dataset_shape[-1])

        # Extract just the slit coords
        wcs_ind = 0 if instrument == "VISP" else 1
        coords_wcs = wcs.array_index_to_world(0, 0, slit_pixel_coords)[wcs_ind]
        # The inverse transform fix also fixes the order of the frames and therefore class order
        if instrument == "VISP" and not hasattr(g_wcs, "_call_forward"):
            wcs_ind = 1

        coords_gwcs = g_wcs.array_index_to_world(
            *np.broadcast_arrays(iraster, 0, slit_pixel_coords)
        )[wcs_ind]

        assert u.allclose(coords_wcs.Ty, coords_gwcs.Ty, atol=1e-14 * u.arcsec)
        assert u.allclose(coords_wcs.Tx, coords_gwcs.Tx, atol=1e-14 * u.arcsec)


@pytest.fixture
@u.quantity_input
def vbi_varying_header_parser(
    rotation_angle: u.Quantity[u.deg],
    rotation_shift_rate: u.Quantity[u.deg / u.s],
):
    dataset = TimeDependentVBIDataset(
        10,
        1,
        linewave=500 * u.nm,
        rotation_angle=rotation_angle,
        rotation_shift_rate=rotation_shift_rate,
    )

    headers = dataset.generate_headers()
    hp = HeaderParser.from_headers(headers)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wcses = []
        for header in hp.headers:
            wcses.append(WCS(dict(header)))
    tb = TransformBuilder(hp)

    return hp, wcses, tb.gwcs


@pytest.fixture
@u.quantity_input
def cryo_ci_header_parser(rotation_angle: u.Quantity[u.deg]):
    dataset = SimpleCryonirspCIDataset(
        n_meas=1,
        n_steps=7,
        n_maps=1,
        n_stokes=1,
        time_delta=10,
        linewave=1083 * u.nm,
        raster_step=0.5 * u.arcsec,
    )

    headers = dataset.generate_headers()
    hp = HeaderParser.from_headers(headers)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wcses = []
        for header in hp.headers:
            wcses.append(WCS(dict(header)))

    tb = TransformBuilder(hp)

    return hp, wcses, tb.gwcs


@pytest.mark.parametrize(
    "fixture_finder", ["vbi_varying_header_parser", "cryo_ci_header_parser"], indirect=True
)
def test_time_varying_image_coords(fixture_finder, rotation_angle, rotation_shift_rate):
    parser, wcses, gwcs = fixture_finder
    for iframe, wcs in enumerate(wcses):
        spatial_pc, gwcs_pc = extract_pcs_varying(wcs, gwcs)

        # Check the first angle
        wcs_angle = matrix2d_to_angle(spatial_pc)
        gwcs_angle = matrix2d_to_angle(gwcs_pc[iframe])

        assert u.allclose(rotation_angle + rotation_shift_rate * (iframe * u.s), wcs_angle)
        assert u.allclose(wcs_angle, gwcs_angle)

        # Extract the border coords
        coords_gwcs = get_border_coords(gwcs, initial_ind=iframe, spatial_pixel_axes=[0, 1])
        coords_wcs = get_border_coords(wcs)

        assert u.allclose(coords_wcs.Ty, coords_gwcs.Ty)
        assert u.allclose(coords_wcs.Tx, coords_gwcs.Tx)
