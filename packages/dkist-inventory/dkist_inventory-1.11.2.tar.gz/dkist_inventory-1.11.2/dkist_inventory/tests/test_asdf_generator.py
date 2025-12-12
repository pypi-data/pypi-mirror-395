import pathlib
from importlib import metadata

import asdf
import astropy.units as u
import dkist
import numpy as np
import pytest
from dkist.dataset import Dataset
from dkist.dataset import TiledDataset
from dkist.io import DKISTFileManager
from dkist_data_simulator.spec214.vbi import SimpleVBIDataset

from dkist_inventory.asdf_generator import asdf_tree_from_filenames
from dkist_inventory.asdf_generator import dataset_from_fits
from dkist_inventory.asdf_generator import references_from_filenames
from dkist_inventory.header_parsing import HeaderParser


def test_array_container_shape(header_filenames):
    header_parser = HeaderParser.from_filenames(header_filenames, hdu=0)
    header_parser = header_parser.group_mosaic_tiles()[0]

    # References from filenames
    array_container = references_from_filenames(header_parser, hdu_index=0, relative_to=".")
    assert array_container.output_shape == array_container.dask_array.shape


def test_asdf_tree(header_filenames):
    tree = asdf_tree_from_filenames(header_filenames)
    assert isinstance(tree, dict)


def test_asdf_tree_with_headers_and_inventory_args():
    # given
    file_count = 5
    headers = []
    file_names = []
    for i, ds in enumerate(
        SimpleVBIDataset(
            n_time=file_count,
            time_delta=1,
            linewave=550 * u.nm,
            detector_shape=(10, 10),
        )
    ):
        h = ds.header()
        h["BITPIX"] = 8
        headers.append(h)
        file_names.append(f"wibble_{i}.fits")
    tree = asdf_tree_from_filenames(file_names, headers)
    assert isinstance(tree, dict)


def test_validator(header_parser):
    header_parser._headers[3]["NAXIS"] = 5
    # vbi-mosaic-single raises a KeyError because it's only one frame
    with pytest.raises((ValueError, KeyError), match="NAXIS"):
        header_parser._validate_headers()


def test_references_from_filenames(header_parser):
    # references_from_filenames only works on a single tile
    header_parser = header_parser.group_mosaic_tiles()[0]
    base = header_parser.filenames[0].parent
    refs: DKISTFileManager = references_from_filenames(
        header_parser,
        relative_to=base,
    )

    for ref in refs.filenames:
        assert base.as_posix() not in ref


def test_dataset_from_fits(header_directory):
    asdf_filename = "test_asdf.asdf"
    asdf_file = pathlib.Path(header_directory) / asdf_filename
    try:
        dataset_from_fits(header_directory, asdf_filename)

        assert asdf_file.exists()

        # Make sure the dang thing is loadable by `dkist`
        assert isinstance(repr(dkist.load_dataset(asdf_file)), str)

        with asdf.open(asdf_file) as adf:
            ds = adf["dataset"]
            assert isinstance(ds, (Dataset, TiledDataset))
            if isinstance(ds, Dataset):
                assert ds.unit is u.count
                # A simple test to see if the headers are 214 ordered
                assert ds.headers.colnames[0] == "SIMPLE"
                assert ds.headers.colnames[1] == "BITPIX"
            elif isinstance(ds, TiledDataset):
                assert ds[0, 0].unit is u.count

            history_entries = adf.get_history_entries()
            assert len(history_entries) == 1
            assert "dkist-inventory" in history_entries[0]["description"]
            software = history_entries[0]["software"]
            assert isinstance(software, dict)
            assert software["name"] == "dkist-inventory"
            assert software["version"] == metadata.distribution("dkist-inventory").version
    finally:
        asdf_file.unlink()


@pytest.fixture
def vtf_data_directory_with_suffix(simulated_dataset, suffix):
    dataset_name = "vtf"  # Chosen because it's light
    return simulated_dataset(dataset_name, suffix=suffix)


@pytest.mark.parametrize("suffix", ["fits", "dat"])
def test_dataset_from_fits_with_different_glob(vtf_data_directory_with_suffix, suffix):
    asdf_filename = "test_asdf.asdf"
    asdf_file = pathlib.Path(vtf_data_directory_with_suffix) / asdf_filename

    test_history = [
        (
            "Written in a dkist-inventory test.",
            {
                "name": "spam",
                "author": "King Arthur",
                "homepage": "https://ni.knight",
                "version": "7",
            },
        )
    ]

    dataset_from_fits(
        vtf_data_directory_with_suffix,
        asdf_filename,
        glob=f"*{suffix}",
        extra_history=test_history,
    )

    try:
        assert asdf_file.exists()

        with asdf.open(asdf_file) as adf:
            ds = adf["dataset"]
            assert isinstance(ds, (Dataset, TiledDataset))
            if isinstance(ds, Dataset):
                assert ds.unit is u.count
                # A simple test to see if the headers are 214 ordered
                assert ds.headers.colnames[0] == "SIMPLE"
                assert ds.headers.colnames[1] == "BITPIX"
            elif isinstance(ds, TiledDataset):
                assert ds[0, 0].unit is u.count

            history_entries = adf.get_history_entries()
            assert len(history_entries) == 2
            assert "dkist-inventory" in history_entries[0]["description"]
            assert history_entries[1]["description"] == test_history[0][0]
            assert history_entries[1]["software"] == test_history[0][1]

    finally:
        asdf_file.unlink()


def test_mosaic_order(simulated_dataset, dl_mosaic_tile_shape):
    ds = simulated_dataset("dlnirsp-mosaic")
    files = list(ds.glob("*.fits"))
    files.sort()
    tree = asdf_tree_from_filenames(files)
    dataset = tree["dataset"]
    dataset_small = dataset.slice_tiles[0, 0]
    assert dataset_small.shape == dl_mosaic_tile_shape
    for nindex1, nindex2 in np.ndindex(dataset_small._data.shape):
        assert nindex1 == dataset_small[nindex1, nindex2].headers["MINDEX1"] - 1
        assert nindex2 == dataset_small[nindex1, nindex2].headers["MINDEX2"] - 1
