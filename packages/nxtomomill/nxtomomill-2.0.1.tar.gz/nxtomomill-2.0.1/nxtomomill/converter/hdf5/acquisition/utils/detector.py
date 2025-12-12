from __future__ import annotations

import h5py


def has_valid_detector(node, detectors_names):
    """
    :return True if the node looks like a valid nx detector
    """
    for key in node.keys():
        if (
            "NX_class" in node[key].attrs
            and node[key].attrs["NX_class"] == "NXdetector"
        ):
            if detectors_names is None or key in detectors_names:
                return True
    return False


def get_nx_detectors(node: h5py.Group) -> tuple:
    """

    :param node: node to inspect
    :return: tuple of NXdetector (h5py.Group) contained in `node`
             (expected to be the `instrument` group)
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "NX_class" in subnode.attrs:
            if subnode.attrs["NX_class"] == "NXdetector":
                if "data" in subnode and hasattr(subnode["data"], "ndim"):
                    if subnode["data"].ndim == 3:
                        nx_detectors.append(subnode)
    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)


def guess_nx_detector(node: h5py.Group) -> tuple:
    """
    Try to guess what can be an nx_detector without using the "NXdetector"
    NX_class attribute. Expect to find a 3D dataset named 'data' under
    a subnode
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "data" in subnode:
            if isinstance(subnode["data"], h5py.Dataset) and subnode["data"].ndim == 3:
                nx_detectors.append(subnode)

    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)
