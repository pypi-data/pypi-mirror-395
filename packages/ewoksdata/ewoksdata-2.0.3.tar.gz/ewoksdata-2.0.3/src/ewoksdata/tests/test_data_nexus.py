import time

import pytest
from silx.io import h5py_utils
from silx.io.url import DataUrl

from ..data import nexus
from ..data import url


def test_create_nexus_group(tmp_path):
    with nexus.create_nexus_group(str(tmp_path / "file.h5")) as (
        h5item,
        already_existed,
    ):
        assert not already_existed
        assert h5item.name == "/results"
    with nexus.create_nexus_group(str(tmp_path / "file.h5")) as (
        h5item,
        already_existed,
    ):
        assert already_existed
        assert h5item.name == "/results"

    with nexus.create_nexus_group(
        str(tmp_path / "file.h5::/c"), default_levels=("a", "b")
    ) as (h5item, already_existed):
        assert not already_existed
        assert h5item.name == "/c/b"
    with nexus.create_nexus_group(
        str(tmp_path / "file.h5::/c"), default_levels=("a", "b")
    ) as (h5item, already_existed):
        assert already_existed
        assert h5item.name == "/c/b"
    with nexus.create_nexus_group(str(tmp_path / "file.h5::/c/b")) as (
        h5item,
        already_existed,
    ):
        assert already_existed
        assert h5item.name == "/c/b"


@pytest.mark.parametrize("as_string", [True, False])
@pytest.mark.parametrize("data_path", ["", "::/1.1/measurement/integrated"])
def test_create_url(tmp_path, data_path, as_string):
    tmp_url = DataUrl(f"{tmp_path / 'file.h5'}{data_path}")

    if data_path:
        expected_url = url.as_dataurl(tmp_url.path())
    else:
        expected_url = url.as_dataurl(f"{tmp_url.path()}::/results")

    if as_string:
        input_url = tmp_url.path()
    else:
        input_url = tmp_url

    created_url = nexus.create_url(input_url)
    assert created_url == expected_url

    with h5py_utils.open_item(
        created_url.file_path(), created_url.data_path(), mode="a"
    ) as item:
        # Add unique id to identify the item
        item_id = f"CREATED AT {time.time()}"
        item.attrs["id"] = item_id

    created_url = nexus.create_url(input_url, overwrite=False)
    with h5py_utils.open_item(
        created_url.file_path(), created_url.data_path()
    ) as new_item:
        # It is the same item
        assert new_item.attrs["id"] == item_id

    created_url = nexus.create_url(input_url, overwrite=True)
    with h5py_utils.open_item(
        created_url.file_path(), created_url.data_path()
    ) as new_item:
        # It is a different item
        assert "id" not in new_item.attrs
