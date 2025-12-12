import numpy as _np
from ..core.data import SpinData
from ..core.util import concat

from scipy.integrate import trapezoid as _trapezoid
from scipy.integrate import cumulative_trapezoid as _cumulative_trapezoid


def cumulative_integrate(data, dim="f2", regions=None):
    """Cumulative integration

    Args:
        data (SpinData): Data object
        dim (str): Dimension to perform cumulative integration
        regions (None, list): List of tuples to specify range of integration [(min, max), ...]

    Returns:
        data: cumulative sum of data

    Examples:
        Example showing cumulative integration of lorentzian function

        >>> import numpy as np
        >>> from matplotlib.pylab import *
        >>> import spinlab as sl
        >>> x = np.r_[-10:10:1000j]
        >>> y = sl.math.lineshape.lorentzian(x,0,1)
        >>> data = sl.SpinData(y, ['f2'], [x])
        >>> data_int = sl.cumulative_integrate(data)
        >>> figure()
        >>> sl.plot(data)
        >>> sl.plot(data_int)
        >>> show()


    """

    out = data.copy()

    if regions == None:
        index = out.index(dim)
        out.values = _cumulative_trapezoid(
            out.values, out.coords[dim], axis=index, initial=0
        )

        proc_attr_name = "cumlative_integrate"
        proc_parameters = {
            "dim": dim,
            "regions": regions,
        }
        out.add_proc_attrs(proc_attr_name, proc_parameters)
        return out

    else:
        data_list = []
        for region in regions:
            proc_attr_name = "cumlative_integrate"
            proc_parameters = {
                "dim": dim,
                "regions": regions,
            }
            out.add_proc_attrs(proc_attr_name, proc_parameters)
            data_list.append(cumulative_integrate(out[dim, region], dim))

        return data_list


def integrate(data, dim="f2", regions=None):
    """Integrate data along given dimension. If no region is given, the integral is calculated over the entire range.

    Args:
        data (SpinData): Data object
        dim (str): Dimension to perform integration. Default is "f2"
        regions (None, list): List of tuples defining the region to integrate

    Returns:
        data (SpinData): Integrals of data. If multiple regions are given the first value corresponds to the first region, the second value corresponds to the second region, etc.

    Examples:
        Integrated entire data region:

            >>> data = sl.integrate(data)

        Integrate single peak/region:

            >>> data = sl.integrate(data, regions=[(4, 5)])

        Integrate two regions:

            >>> data = sl.integrate(data, regions=[(1.1, 2.1), (4.5, 4.9)])

    """
    out = data.copy()
    out.attrs["experiment_type"] = "integrals"

    index = out.index(dim)
    if regions == None:
        out.values = _trapezoid(out.values, out.coords[dim], axis=index)
        out.coords.pop(dim)

        # if error_regions == None:
        #     out.error = np.zeros(out.shape)
        #     print("add errors")

        # else:
        #     signal = max(out.values)
        #     noise = np.trapz(out.)

    else:
        if len(regions) == 2 and (
            not hasattr(regions[0], "__iter__")
        ):  # allow special case of regions=(1,2)
            regions = ((regions[0], regions[1]),)
        data_list = []
        for region in regions:
            data_list.append(integrate(out[dim, region], dim))

        x = _np.array(list(range(len(data_list))))
        dim_name = "integrals"
        out = concat(data_list, dim_name, coord=x)

    proc_attr_name = "integrate"
    proc_parameters = {
        "dim": dim,
        "regions": regions,
    }

    out.add_proc_attrs(proc_attr_name, proc_parameters)

    return out
