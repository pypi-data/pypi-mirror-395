import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from typing import Tuple

import h5py
import numpy

__all__ = ["save_bliss_scan"]


def save_bliss_scan(
    tmpdir: Path,
    image: numpy.ndarray,
    npoints_per_file: int,
    npoints: int,
    scannr: int,
    subscannr: int = 1,
    sequence: str = "add",
    lima_names: Tuple[str, ...] = ("p3",),
    counter_names: Tuple[str, ...] = ("diode1", "diode2"),
    positioner_names: Tuple[str, ...] = ("diffty", "diffrz"),
    title: Optional[str] = None,
) -> Path:
    dataset_filename = tmpdir / "sample_dataset.h5"
    lima_dirname = tmpdir / f"scan{scannr:04d}"
    lima_dirname.mkdir()
    with h5py.File(str(dataset_filename), mode="w") as root:
        root.attrs["NX_class"] = "NXroot"
        root.attrs["creator"] = "bliss"
        scan = root.create_group(f"{scannr}.{subscannr}")
        scan.attrs["NX_class"] = "NXentry"
        if title is not None:
            scan["title"] = title

        instrument = scan.create_group("instrument")
        instrument.attrs["NX_class"] = "NXinstrument"
        measurement = scan.create_group("measurement")
        measurement.attrs["NX_class"] = "NXcollection"

        if positioner_names:
            positioners = instrument.create_group("positioners")
            positioners.attrs["NX_class"] = "NXcollection"

        for name in counter_names:
            _save_counter(scan, name, npoints)
        for name in lima_names:
            _save_lima(
                scan,
                name,
                image,
                npoints,
                npoints_per_file,
                lima_dirname,
                scannr,
                sequence,
            )
        for name in positioner_names:
            _save_positioner(scan, name, npoints)

        scan["end_time"] = datetime.now().astimezone().isoformat()
    return dataset_filename


def _save_counter(scan: h5py.Group, name: str, npoints: int) -> None:
    diode = _add_detector(scan, name)
    diode["data"] = numpy.arange(npoints)


def _save_lima(
    scan: h5py.Group,
    name: str,
    image: numpy.ndarray,
    npoints: int,
    npoints_per_file: int,
    lima_dirname: Path,
    scannr: int,
    sequence: str,
) -> None:
    tot_shape = (npoints,) + image.shape
    lima_shape = (npoints_per_file,) + image.shape
    nlima = npoints // npoints_per_file + bool(npoints % npoints_per_file)
    lima_dtype = float
    layout = h5py.VirtualLayout(tot_shape, dtype=lima_dtype)
    for i in range(nlima):
        with h5py.File(str(lima_dirname / f"{name}_{i}.h5"), mode="w") as limaroot:
            limaroot.attrs["NX_class"] = "NXroot"
            entry = limaroot.create_group("entry_0000")
            entry.attrs["NX_class"] = "NXentry"
            lmeasurement = entry.create_group("measurement")
            lmeasurement.attrs["NX_class"] = "NXcollection"
            lmeasurement["data"] = numpy.full(lima_shape, numpy.nan)

            i0 = i * npoints_per_file
            i1 = min(i0 + npoints_per_file, npoints)
            for itot in range(i0, i1):
                if sequence == "add":
                    lmeasurement["data"][itot - i0, ...] = image + itot
                else:
                    m = itot / (npoints - 1) + 1
                    if itot == 0:
                        monitor = _add_detector(scan, "monitor")
                        monitor["data"] = numpy.zeros(npoints)
                    monitor["data"][itot] = m
                    lmeasurement["data"][itot - i0, ...] = image * m

            spath = os.path.join(f"scan{scannr:04d}", f"{name}_{i}.h5")
            sdset = "/entry_0000/measurement/data"

            sshape = (i1 - i0,) + lima_shape[1:]
            vsource = h5py.VirtualSource(spath, sdset, shape=sshape, dtype=lima_dtype)

            layout[i0:i1] = vsource[:]
    detector = _add_detector(scan, name)
    detector.create_virtual_dataset("data", layout, fillvalue=numpy.nan)


def _add_detector(scan: h5py.Group, name: str) -> h5py.Group:
    grp = scan["instrument"].create_group(name)
    grp.attrs["NX_class"] = "NXdetector"
    scan["measurement"][name] = h5py.SoftLink(f"{grp.name}/data")
    return grp


def _save_positioner(scan: h5py.Group, name: str, npoints: int) -> None:
    positioner = _add_positioner(scan, name)
    positioner["value"] = numpy.arange(npoints)


def _add_positioner(scan: h5py.Group, name: str) -> h5py.Group:
    instrument = scan["instrument"]
    grp = instrument.create_group(name)
    grp.attrs["NX_class"] = "Nxpositioner"
    scan["measurement"][name] = h5py.SoftLink(f"{grp.name}/value")
    instrument["positioners"][name] = h5py.SoftLink(f"{grp.name}/value")
    return grp
