import numpy as _np


def average(data, axis="Average"):
    """Average a dimension using numpy.mean

    Args:
        data (object) : SpinData object
        dim (str) : Dimension to average

    Returns:
        SpinData: Averaged data

    Examples:

        >>> data_averaged = sl.average(data)
    """

    out = data.copy()
    proc_attr_name = "average"
    proc_parameters = {"axis": axis}
    proc_attrs_list = out.proc_attrs

    out = _np.mean(out, axis=axis)  # it will automatically assign proc_attrs
    out.proc_attrs = proc_attrs_list
    out.add_proc_attrs(proc_attr_name, proc_parameters)

    return out
