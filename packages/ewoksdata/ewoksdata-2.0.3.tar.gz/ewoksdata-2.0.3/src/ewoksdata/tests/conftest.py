import numpy
import pytest

from . import data


@pytest.fixture(scope="session")
def bliss_scan(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("sample_dataset")
    npoints_per_file = 3
    npoints = 31
    scannr = 2
    image = numpy.zeros((10, 12))
    return (
        str(
            data.save_bliss_scan(
                tmpdir,
                image,
                npoints_per_file,
                npoints,
                scannr,
                subscannr=1,
                lima_names=("p3", "p4"),
                counter_names=("diode1", "diode2"),
                sequence="add",
            )
        ),
        npoints,
        scannr,
    )
