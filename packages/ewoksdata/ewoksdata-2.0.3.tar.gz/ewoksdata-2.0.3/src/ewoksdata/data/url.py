import sys
from typing import Tuple
from typing import Union

from silx.io.url import DataUrl


def as_dataurl(url: Union[str, DataUrl]) -> DataUrl:
    if isinstance(url, str) and sys.platform == "win32":
        url = url.replace("\\", "/")
    if not isinstance(url, DataUrl):
        url = DataUrl(url)
    return url


def as_h5url(url: Union[str, DataUrl]) -> DataUrl:
    url = as_dataurl(url)
    if not url.data_path():
        return DataUrl(f"{url.file_path()}::/")
    return url


def h5dataset_url_parse(url: Union[str, DataUrl]) -> Tuple[str, str, Tuple]:
    url = as_h5url(url)
    filename = str(url.file_path())
    h5path = url.data_path()
    idx = url.data_slice()
    if idx is None:
        idx = tuple()
    return filename, h5path, idx
