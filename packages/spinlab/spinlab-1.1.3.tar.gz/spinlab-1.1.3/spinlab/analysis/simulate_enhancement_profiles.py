"""Modules to calculate Spin enhancement profiles"""

import numpy as _np
from scipy import optimize
import spinlab as _sl
import warnings
from ..constants import constants


def sim_sl_profile(
    data,
    B0,
    nucleus="1H",
    sl_process="SE",
    add_details=False,
    remove_background=True,
    normalize=True,
    integrate=True,
):
    """Simulate Spin enhancment profile

    Simulate Spin enhancement profile based on the EPR spectrum. For more details:

    Banerjee, D., D. Shimon, A. Feintuch, S. Vega, and D. Goldfarb. “The Interplay between the Solid Effect and the Cross Effect Mechanisms in Solid State (1)(3)C Spin at 95 GHz Using Trityl Radicals.” Journal of Magnetic Resonance 230 (May 2013): 212–19.
    https://doi.org/10.1016/j.jmr.2013.02.010.

    Args:
        data (Spindata): EPR spectrum
        B0 (float): Field position for the Spin experiment in (T)
        nucleus (int): Nucleus for Spin experiment
        sl_process (int): Select Spin mechanism, SE - Solid Effect, CE/TM - Cross-Effect/Thermal Mixing
        add_details (boolean): Add individual spectra to proc_attrs. Default is False
        remove_background (boolean): Remove 0th order background from EPR spectrum. Default is True
        normalize (boolean): Normalize EPR spectrum to maximum amplitude of 1. Default is True
        integrate (boolean): Integrate EPR spectrum. Default is True

    Returns:
        data (Spindata): Simulated Spin enhancement profile

    .. math::

    """
    out = data.copy()

    # Some error checks:
    if out.attrs.get("experiment_type") == None:
        print("Error: Key experiment_type not present")
        return

    if out.attrs["experiment_type"] != "epr_spectrum":
        print("Error: EPR spectrum required as input.")
        return

    if len(out.dims) > 1:
        print("Error: This function requires a 1D EPR spectrum as input.")
        return

    if remove_background == True:
        out = _sl.remove_background(out, dim="B0", deg=0)  # Remove background

    if normalize == True:
        out = _sl.normalize(out)

    if integrate == True:
        out = _sl.cumulative_integrate(out, dim="B0")  # Calculate cumsum

    ## Calculate number of points to shift
    slLarmorFrequency = _sl.mr_properties(nucleus, B0)  # Nuclear Larmor Frequency
    slLarmorFrequency_G = slLarmorFrequency / (
        1000 * _sl.mr_properties("0e") / 2 / pi
    )  # Nuclear Larmor Frequency in [G]
    deltaB0_G = (out.coords["B0"][1] - out.coords["B0"][0]) * 10
    points_to_shift = round(slLarmorFrequency_G / deltaB0_G)

    ## Shift EPR spectra using mumpy's roll function
    EPRdataPos = out.copy()
    EPRdataPos.values = _np.roll(EPRdataPos.values, points_to_shift)

    EPRdataNeg = out.copy()
    EPRdataNeg.values = _np.roll(out.values, (-1) * points_to_shift)
    EPRdataNeg.values = (-1) * EPRdataNeg.values

    if sl_process == "SE":
        out = EPRdataPos + EPRdataNeg
    elif sl_process == "CE/TM":
        out = out.values * (EPRdataPos + EPRdataNeg)

    proc_attr_name = "sim_sl_profile"
    proc_parameters = {
        "nucleus": nucleus,
        "sl_process": sl_process,
        "remove_background": remove_background,
        "normalize": normalize,
        "integrate": integrate,
    }

    out.add_proc_attrs(proc_attr_name, proc_parameters)

    if add_details == True:
        sim_data = _np.array([out.values, EPRdataNeg.values, EPRdataPos.values])

        proc_attr_name = "sim_sl_profile"
        proc_parameters = {
            "sim_data": sim_data,
        }

        out.add_proc_attrs(proc_attr_name, proc_parameters)

    return out
