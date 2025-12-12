from importlib.metadata import version

from packaging.version import Version


def _not_supported_by_blissdata_version(*_, **kw):
    raise RuntimeError(f"Not supported by blissdata {_BLISSDATA_VERSION}")


from blissdata.h5api import dynamic_hdf5  # noqa F401

_BLISSDATA_VERSION = Version(version("blissdata"))

if _BLISSDATA_VERSION >= Version("2.0.0rc1"):
    from .blissdatav2 import iter_bliss_scan_data_from_memory  # noqa F401
    from .blissdatav2 import iter_bliss_scan_data_from_memory_slice  # noqa F401
    from .blissdatav2 import last_lima_image  # noqa F401

    BUFFER_IN_MEMORY_DEFAULT = False
elif _BLISSDATA_VERSION >= Version("1"):
    from .blissdatav1 import iter_bliss_scan_data_from_memory  # noqa F401
    from .blissdatav1 import iter_bliss_scan_data_from_memory_slice  # noqa F401
    from .blissdatav1 import last_lima_image  # noqa F401

    BUFFER_IN_MEMORY_DEFAULT = True
else:
    from .blissdatav0 import iter_bliss_scan_data_from_memory  # noqa F401
    from .blissdatav0 import last_lima_image  # noqa F401

    iter_bliss_scan_data_from_memory_slice = _not_supported_by_blissdata_version
    BUFFER_IN_MEMORY_DEFAULT = True
