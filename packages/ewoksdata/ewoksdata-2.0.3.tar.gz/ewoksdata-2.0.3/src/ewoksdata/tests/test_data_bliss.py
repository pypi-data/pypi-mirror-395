import h5py
import numpy
import pytest
from fabio.edfimage import edfimage

from ..data import bliss


def test_get_data_edf(tmpdir):
    filename = str(tmpdir / "data.edf")
    img1 = numpy.random.uniform(((10, 12)))
    edf = edfimage(data=img1)
    edf.write(filename)
    img2 = bliss.get_data(filename)
    numpy.testing.assert_array_equal(img1, img2)


def test_get_data_hdf5(tmpdir):
    filename = str(tmpdir / "data.h5")
    img1 = numpy.random.uniform(((10, 12)))
    with h5py.File(filename, "w") as f:
        f["img"] = img1

    img2 = bliss.get_data(f"{filename}::/img")
    numpy.testing.assert_array_equal(img1, img2)

    img3 = bliss.get_data(f"{filename}?path=/img")
    numpy.testing.assert_array_equal(img1, img3)

    filename_non_existing = str(tmpdir / "data_non_existing.h5")
    with pytest.raises(TimeoutError):
        _ = bliss.get_data(f"{filename_non_existing}?path=/img", retry_timeout=0)

    filename_non_existing = str(tmpdir / "data_non_existing.edf")
    with pytest.raises(TimeoutError):
        _ = bliss.get_data(filename_non_existing, retry_timeout=0)


@pytest.mark.parametrize("lima_names", [(), ("p3",), ("p3", "p4")])
@pytest.mark.parametrize("counter_names", [(), ("diode1",), ("diode1", "diode2")])
def test_iter_bliss_data(lima_names, counter_names, bliss_scan):
    nexpected = len(lima_names) + len(counter_names)
    index = None
    filename, npoints, scan_nb = bliss_scan
    with bliss.iter_bliss_data(
        filename, scan_nb, lima_names=lima_names, counter_names=counter_names
    ) as bliss_data_iterator:
        for index, data in bliss_data_iterator:
            assert len(data) == nexpected
            if "diode1" in counter_names:
                assert data["diode1"] == index
            if "diode2" in counter_names:
                assert data["diode2"] == index
            if "p3" in lima_names:
                assert (data["p3"] == index).all()
            if "p4" in lima_names:
                assert (data["p4"] == index).all()

    if nexpected:
        assert index == npoints - 1
    else:
        assert index is None


def test_closure_of_iter_bliss_data(bliss_scan):
    filename, npoints, scan_nb = bliss_scan

    # This opens filename with `locking=False`
    with bliss.iter_bliss_data(
        filename, scan_nb, counter_names=[], lima_names=("p3",)
    ) as lima_iterator:
        for i in range(npoints):
            next(lima_iterator)

    # Make sure that the file is closed and can be reopened with a different locking flag
    with h5py.File(filename, "r", locking=True):
        pass
