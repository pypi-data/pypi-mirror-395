import astropy.units as u
import pytest
from dkist.conftest import *
from dkist_data_simulator.spec214.cryo import SimpleCryonirspCIDataset
from dkist_data_simulator.spec214.cryo import SimpleCryonirspSPDataset
from dkist_data_simulator.spec214.cryo import TimeDependentCryonirspCIDataset
from dkist_data_simulator.spec214.cryo import TimeDependentCryonirspSPDataset
from dkist_data_simulator.spec214.dlnirsp import MosaicedDLNIRSPDataset
from dkist_data_simulator.spec214.dlnirsp import SimpleDLNIRSPDataset
from dkist_data_simulator.spec214.vbi import MosaicedVBIBlueDataset
from dkist_data_simulator.spec214.vbi import MosaicedVBIRedAllDataset
from dkist_data_simulator.spec214.vbi import MosaicedVBIRedDataset
from dkist_data_simulator.spec214.vbi import SimpleVBIDataset
from dkist_data_simulator.spec214.vbi import TimeDependentVBIDataset
from dkist_data_simulator.spec214.visp import SimpleVISPDataset
from dkist_data_simulator.spec214.visp import TimeDependentVISPDataset
from dkist_data_simulator.spec214.vtf import SimpleVTFDataset
from filelock import FileLock

from dkist_inventory.header_parsing import HeaderParser
from dkist_inventory.transforms import TransformBuilder


@pytest.fixture(scope="session")
def dl_mosaic_tile_shape() -> tuple[int, int]:
    return (2, 3)


@pytest.fixture(scope="session")
def dataset(dl_mosaic_tile_shape):
    def _dataset(dataset_name):
        datasets = {
            "visp": SimpleVISPDataset(2, 2, 4, 5, linewave=500 * u.nm, detector_shape=(32, 32)),
            "vtf": SimpleVTFDataset(2, 2, 4, 5, linewave=500 * u.nm, detector_shape=(32, 32)),
            "vbi": SimpleVBIDataset(
                n_time=5, time_delta=5, linewave=500 * u.nm, detector_shape=(32, 32)
            ),
            "cryonirsp-sp-single-meas-no-stokes": SimpleCryonirspSPDataset(
                n_meas=1, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-sp-multi-meas-no-stokes": SimpleCryonirspSPDataset(
                n_meas=2, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-single-meas-no-stokes": SimpleCryonirspCIDataset(
                n_meas=1, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-raster-single-meas-no-stokes": SimpleCryonirspCIDataset(
                n_meas=1,
                n_steps=2,
                n_maps=2,
                n_stokes=1,
                time_delta=10,
                linewave=1083 * u.nm,
                raster_step=0.5 * u.arcsec,
            ),
            "cryonirsp-ci-multi-meas-no-stokes": SimpleCryonirspCIDataset(
                n_meas=2, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-sp-single-meas-stokes": SimpleCryonirspSPDataset(
                n_meas=1, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-sp-multi-meas-stokes": SimpleCryonirspSPDataset(
                n_meas=2, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-single-meas-stokes": SimpleCryonirspCIDataset(
                n_meas=1, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-multi-meas-stokes": SimpleCryonirspCIDataset(
                n_meas=2, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-sp-time-varying-single-meas-no-stokes": TimeDependentCryonirspSPDataset(
                n_meas=1, n_steps=3, n_maps=4, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-sp-time-varying-multi-meas-no-stokes": TimeDependentCryonirspSPDataset(
                n_meas=2, n_steps=3, n_maps=4, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-time-varying-single-meas-no-stokes": TimeDependentCryonirspCIDataset(
                n_meas=1, n_steps=3, n_maps=4, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-time-varying-multi-meas-no-stokes": TimeDependentCryonirspCIDataset(
                n_meas=2, n_steps=3, n_maps=4, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-sp-time-varying-single-meas-stokes": TimeDependentCryonirspSPDataset(
                n_meas=1, n_steps=3, n_maps=4, n_stokes=4, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-sp-time-varying-multi-meas-stokes": TimeDependentCryonirspSPDataset(
                n_meas=3, n_steps=4, n_maps=5, n_stokes=4, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-time-varying-single-meas-stokes": TimeDependentCryonirspCIDataset(
                n_meas=1, n_steps=3, n_maps=4, n_stokes=4, time_delta=10, linewave=1083 * u.nm
            ),
            "cryonirsp-ci-time-varying-multi-meas-stokes": TimeDependentCryonirspCIDataset(
                n_meas=5,
                n_steps=3,
                n_maps=4,
                n_stokes=4,
                time_delta=10,
                linewave=1083 * u.nm,
                raster_step=3.2 * u.arcsec,
            ),
            "cryonirsp-sp-time-varying-multi-meas-sit-no-stokes": TimeDependentCryonirspSPDataset(
                n_meas=10, n_steps=1, n_maps=1, n_stokes=1, time_delta=10, linewave=1083 * u.nm
            ),
            "vbi-mosaic-red": MosaicedVBIRedDataset(
                n_time=2, time_delta=10, linewave=400 * u.nm, detector_shape=(32, 32)
            ),
            "vbi-mosaic-blue": MosaicedVBIBlueDataset(
                n_time=2, time_delta=10, linewave=400 * u.nm, detector_shape=(32, 32)
            ),
            "vbi-mosaic-red-all": MosaicedVBIRedAllDataset(
                n_time=2, time_delta=10, linewave=400 * u.nm, detector_shape=(32, 32)
            ),
            "vbi-mosaic-single": MosaicedVBIBlueDataset(
                n_time=1, time_delta=10, linewave=400 * u.nm, detector_shape=(32, 32)
            ),
            "vbi-time-varying": TimeDependentVBIDataset(
                n_time=4, time_delta=10, linewave=400 * u.nm, detector_shape=(32, 32)
            ),
            "visp-time-varying-single": TimeDependentVISPDataset(
                n_maps=1,
                n_steps=4,
                n_stokes=1,
                time_delta=10,
                linewave=500 * u.nm,
                detector_shape=(16, 128),
            ),
            "visp-time-varying-multi": TimeDependentVISPDataset(
                n_maps=2,
                n_steps=3,
                n_stokes=4,
                time_delta=10,
                linewave=500 * u.nm,
                detector_shape=(16, 128),
            ),
            "dlnirsp": SimpleDLNIRSPDataset(
                n_mosaic_repeats=4,
                n_stokes=1,
                time_delta=10,
                linewave=500 * u.nm,
                array_shape=(10, 10, 10),
            ),
            "dlnirsp-mosaic": MosaicedDLNIRSPDataset(
                n_mosaic_repeats=3,
                n_X_tiles=dl_mosaic_tile_shape[0],
                n_Y_tiles=dl_mosaic_tile_shape[1],
                n_stokes=4,
                time_delta=1,
                linewave=1083 * u.nm,
                array_shape=(10, 10, 10),
            ),
        }
        return datasets[dataset_name]

    return _dataset


@pytest.fixture(scope="session")
def simulated_dataset(cached_tmpdir, dataset, worker_id):
    def _simulated_dataset(dataset_name, suffix="fits"):
        atmpdir = cached_tmpdir / f"{dataset_name}_{suffix}"
        # Ensure that if running with pytest-xdist we only generate the dataset
        # once and all processes share it.
        # The cached_tmpdir fixture will return a temp path which is shared
        # between all workers
        with FileLock(cached_tmpdir / f"{dataset_name}.lock"):
            # Do not do the exists check unless we have the lock
            if not atmpdir.exists():
                ds = dataset(dataset_name)
                ds.generate_files(atmpdir, f"{dataset_name.upper()}_{{ds.index}}.{suffix}")
                return atmpdir

        return atmpdir

    return _simulated_dataset


@pytest.fixture(
    scope="session",
    params=[
        "vtf",
        "vbi",
        "visp",
        "cryonirsp-sp-single-meas-no-stokes",
        "cryonirsp-sp-multi-meas-no-stokes",
        "cryonirsp-ci-single-meas-no-stokes",
        "cryonirsp-ci-multi-meas-no-stokes",
        "cryonirsp-sp-single-meas-stokes",
        "cryonirsp-sp-multi-meas-stokes",
        "cryonirsp-ci-single-meas-stokes",
        "cryonirsp-ci-multi-meas-stokes",
        "cryonirsp-sp-time-varying-single-meas-no-stokes",
        "cryonirsp-sp-time-varying-multi-meas-no-stokes",
        "cryonirsp-ci-time-varying-single-meas-no-stokes",
        "cryonirsp-ci-time-varying-multi-meas-no-stokes",
        "cryonirsp-sp-time-varying-single-meas-stokes",
        "cryonirsp-sp-time-varying-multi-meas-stokes",
        "cryonirsp-ci-time-varying-single-meas-stokes",
        "cryonirsp-ci-time-varying-multi-meas-stokes",
        "cryonirsp-sp-time-varying-multi-meas-sit-no-stokes",
        "vbi-mosaic-red",
        "vbi-mosaic-blue",
        "vbi-mosaic-red-all",
        "vbi-mosaic-single",
        "vbi-time-varying",
        "visp-time-varying-single",
        "visp-time-varying-multi",
        "dlnirsp",
        "dlnirsp-mosaic",
    ],
)
def dataset_name(request):
    return request.param


@pytest.fixture
def header_directory(dataset_name, simulated_dataset):
    return simulated_dataset(dataset_name)


@pytest.fixture
def vbi_time_varying_transform_builder(simulated_dataset):
    header_directory = simulated_dataset("vbi-time-varying")
    header_parser = HeaderParser.from_filenames(header_directory.glob("*"))
    return TransformBuilder(header_parser)


@pytest.fixture
def header_filenames(header_directory):
    files = list(header_directory.glob("*.fits"))
    files.sort()
    return files


@pytest.fixture
def header_parser(header_filenames):
    return HeaderParser.from_filenames(header_filenames)


@pytest.fixture
def transform_builder(header_filenames):
    # We can't build a single transform builder for a mosaic
    if "mosaic" in header_filenames[0].as_posix():
        pytest.skip()
    header_parser = HeaderParser.from_filenames(header_filenames)
    return TransformBuilder(header_parser)


@pytest.fixture
def non_varying_transform_builder(header_filenames):
    if "varying" in header_filenames[0].as_posix() or "mosaic" in header_filenames[0].as_posix():
        pytest.skip()
    header_parser = HeaderParser.from_filenames(header_filenames)
    return TransformBuilder(header_parser)
