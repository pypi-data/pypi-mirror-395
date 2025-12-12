from datetime import datetime

import astropy.units as u
import numpy as np
import pytest
from astropy.table import Table
from astropy.time import Time
from dkist_data_simulator.spec214.visp import TimeDependentVISPDataset

from dkist_inventory.header_parsing import HeaderParser
from dkist_inventory.transforms import TransformBuilder


@pytest.fixture(scope="session")
def simple_header_table():
    """
    This is a minimal header table to test the header parser.

    It's pretty hacky but we want to get rid of everything we don't need to make it easier to inspect
    """
    ds = TimeDependentVISPDataset(
        n_steps=4, n_maps=5, n_stokes=4, time_delta=1, linewave=500 * u.nm, detector_shape=(3, 2)
    )

    headers = ds.generate_headers()
    table = Table(headers)
    test_keys = [
        "DNAXIS",
        "DNAXISd",
        "DTYPEd",
        "DUNITd",
        "DPNAMEd",
        "DWNAMEd",
        "DAAXES",
        "DEAXES",
        "DINDEXk",
        "CRVALn",
        "PCi_j",
        "NAXIS",
        "NAXISn",
        "BUNIT",
        "CTYPEn",
        "CUNITn",
        "DATE-AVG",
    ]
    header = table[0]
    DNAXIS, DAAXES, DEAXES, NAXIS = (
        int(header["DNAXIS"]),
        int(header["DAAXES"]),
        int(header["DEAXES"]),
        int(header["NAXIS"]),
    )
    all_keys = []
    for key in test_keys:
        keys = [key]
        if key.endswith("d"):
            keys = [key[:-1] + str(d) for d in range(1, DNAXIS + 1)]
        if key.endswith("k"):
            keys = [key[:-1] + str(k) for k in range(DAAXES + 1, DAAXES + DEAXES + 1)]
        if key.endswith("n"):
            keys = [key[:-1] + str(n) for n in range(1, NAXIS + 1)]
        if key.startswith("PC"):
            keys = []
            for i in range(1, NAXIS + 1):
                for j in range(1, NAXIS + 1):
                    keys.append(f"PC{i}_{j}")
        all_keys += keys
    return table[all_keys]


@pytest.fixture
def parser(simple_header_table):
    return HeaderParser(simple_header_table)


def test_slice_for_file_axes(parser):
    assert parser.header["NAXIS1"] == 2
    assert parser.header["NAXIS2"] == 3
    assert parser.dataset_shape == (2, 3, 4, 5, 4)
    assert parser.files_shape == (4, 5, 4)

    assert parser.slice_for_file_axes(0) == (slice(None), 0, 0)
    assert parser.slice_for_file_axes(0, 2) == (slice(None), 0, slice(None))

    assert parser.varying_spatial_daxes == {"crval": [3, 4], "pc": [3, 4]}

    assert parser.slice_for_dataset_array_axes(3, indexing="fits") == (slice(None), 0, 0)
    assert parser.slice_for_dataset_array_axes(4, indexing="fits") == (0, slice(None), 0)
    assert parser.slice_for_dataset_array_axes(5, indexing="fits") == (0, 0, slice(None))

    static_axes = parser.header_array[parser.slice_for_dataset_array_axes(5, indexing="fits")]
    assert static_axes.shape == (4,)
    assert np.allclose(static_axes["CRVAL3"], static_axes["CRVAL3"][0])

    varying_axes = parser.header_array[parser.slice_for_dataset_array_axes(4, indexing="fits")]
    assert varying_axes.shape == (5,)
    assert not np.allclose(varying_axes["CRVAL3"], varying_axes["CRVAL3"][0])

    varying_axes = parser.header_array[parser.slice_for_dataset_array_axes(3, indexing="fits")]
    assert varying_axes.shape == (4,)
    assert not np.allclose(varying_axes["CRVAL3"], varying_axes["CRVAL3"][0])


def test_midpoint_header(parser):
    midpoint_header = parser.midpoint_header
    midpoint_time = Time(midpoint_header["DATE-AVG"])

    times = Time(parser.headers["DATE-AVG"])
    time_min, time_max = np.min(times), np.max(times)
    expected_midpoint_time = time_min + (time_max - time_min) / 2

    # The fixture at the top of the file uses 1s as it's time delta, we should
    # be more than half a frame out
    assert np.abs(midpoint_time - expected_midpoint_time) < 0.5 * u.s

    # Assert that we have some frames with the same times
    # This validates the test input is testing the right thing
    assert len(times) != len(np.unique(times))


@pytest.mark.parametrize(
    "dataset_name", ["dlnirsp", "visp", "dlnirsp-mosaic", "vbi", "vbi-mosaic-red"]
)
def test_pixel_axis_type_map(dataset_name, simulated_dataset):
    header_parser = HeaderParser.from_filenames(simulated_dataset(dataset_name).glob("*.fits"))
    header_parser = header_parser.group_mosaic_tiles()[0]
    pixel_axis_type_map = header_parser.pixel_axis_type_map

    # We ignore stokes on the end
    expected_map_ordering = {
        "dlnirsp": ["SPATIAL", "SPECTRAL", "TEMPORAL"],
        "dlnirsp-mosaic": ["SPECTRAL", "SPATIAL", "TEMPORAL"],
        "visp": ["SPECTRAL", "SPATIAL", "TEMPORAL"],
        "vbi": ["SPATIAL", "TEMPORAL"],
    }
    expected_map_ordering["vbi-mosaic-red"] = expected_map_ordering["vbi"]

    expected = expected_map_ordering[dataset_name]
    assert list(pixel_axis_type_map.keys())[: len(expected)] == expected


def test_cryo_sit_and_stare(simulated_dataset):
    ds_dir = simulated_dataset("cryonirsp-sp-time-varying-multi-meas-sit-no-stokes")
    header_parser = HeaderParser.from_filenames(ds_dir.glob("*"))
    assert header_parser.pixel_axis_type_map["TEMPORAL"] == [2, 3]
