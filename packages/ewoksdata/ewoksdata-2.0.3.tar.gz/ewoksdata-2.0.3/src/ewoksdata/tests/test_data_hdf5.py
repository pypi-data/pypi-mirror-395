from ..data import hdf5


def test_bliss_data(bliss_scan):
    filename, nb_points, scan_nb = bliss_scan
    with hdf5.h5context(filename) as f:
        values = f[f"/{scan_nb}.1/measurement/diode1"][()]
        assert values.tolist() == list(range(nb_points))
        values = f[f"/{scan_nb}.1/measurement/diode2"][()]
        assert values.tolist() == list(range(nb_points))
        values = f[f"/{scan_nb}.1/measurement/p3"][:, 0, 0]
        assert values.tolist() == list(range(nb_points))
        values = f[f"/{scan_nb}.1/measurement/p3"][:, -1, -1]
        assert values.tolist() == list(range(nb_points))
