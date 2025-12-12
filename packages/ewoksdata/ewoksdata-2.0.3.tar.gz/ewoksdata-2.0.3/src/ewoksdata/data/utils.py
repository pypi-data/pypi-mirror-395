from numbers import Number
from typing import Mapping

import numpy


def is_data(data):
    if isinstance(data, (numpy.ndarray, Number)):
        return True
    if isinstance(data, (str, list)) and data:
        return True
    return False


def data_from_storage(data, remove_numpy=True):
    if isinstance(data, numpy.ndarray):
        if not remove_numpy:
            return data
        elif data.ndim == 0:
            return data.item()
        else:
            return data.tolist()
    elif isinstance(data, Mapping):
        return {
            k: data_from_storage(v, remove_numpy=remove_numpy)
            for k, v in data.items()
            if not k.startswith("@")
        }
    else:
        return data
