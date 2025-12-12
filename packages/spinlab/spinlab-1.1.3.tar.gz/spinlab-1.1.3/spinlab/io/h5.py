from ..core.data import SpinData
import warnings
import numpy as _np
import h5py as _h5py

None_alias = "__PYTHON_NONE__"  # h5 does not have Null type


python_types = [None]
replace_types = [None_alias]


# args and kwargs is for compability
def load_h5(path, *args, **kwargs):
    """Returns Dictionary of slDataObjects

    Args:
        path (str): Path to h5 file

    Returns:
        sldata_collection: workspace object with data
    """

    f = _h5py.File(path, "r")
    keys_list = f.keys()

    if list(keys_list) == [
        "__SpinDATA__"
    ]:  # If Only SpinData object in h5 file, return SpinData object, not dictionary
        data = read_sldata(f["__SpinDATA__"])
        return data

    sl_dict = {}

    for key in keys_list:
        if f[key].attrs["spinlab_data_type"] == "sldata":
            data = read_sldata(f[key])
        elif f[key].attrs["spinlab_data_type"] == "dict":
            data = read_dict(f[key])
        else:
            warnings.warn("could not import key: %s" % str(key))

        sl_dict[key] = data
    return sl_dict


def read_sldata(sldata_group):
    coords = []
    dims = []
    attrs = {}
    spinlab_attrs = {}
    proc_attrs = {}
    values = sldata_group["values"][:]
    version = sldata_group.attrs["spinlab_version"]

    for index in range(len(_np.shape(values))):
        dim_key = sldata_group["values"].dims[index].keys()[0]  # assumes 1 key only
        coords.append(sldata_group["values"].dims[index][dim_key][:])
        dims.append(dim_key)

    for k in sldata_group["attrs"].attrs.keys():
        v = sldata_group["attrs"].attrs[k]
        if v in replace_types:
            ix = replace_types.index(v)
            v = python_types[ix]
        attrs[k] = v
    for k in sldata_group["attrs"]:
        v = sldata_group["attrs"][k][:]
        attrs[k] = v

    if "spinlab_attrs" in sldata_group.keys():
        for k in sldata_group["spinlab_attrs"].attrs.keys():
            v = sldata_group["spinlab_attrs"].attrs[k]
            if v in replace_types:
                ix = replace_types.index(v)
                v = python_types[ix]
            spinlab_attrs[k] = v
        for k in sldata_group["spinlab_attrs"]:
            v = sldata_group["spinlab_attrs"][k][:]
            spinlab_attrs[k] = v

    data = SpinData(values, dims, coords, attrs, spinlab_attrs)

    if "proc_attrs" in sldata_group.keys():
        proc_attrs = []
        for k in sldata_group["proc_attrs"].keys():
            proc_attrs_name = k.split(":", 1)[1]
            proc_attrs_dict = dict(sldata_group["proc_attrs"][k].attrs)
            data.add_proc_attrs(proc_attrs_name, proc_attrs_dict)

    return data


def read_dict(sldata_group):
    data = dict(sldata_group["attrs"].attrs)
    return data


def save_h5(dataDict, path, overwrite=False):
    """Save workspace in .h5 format

    Args:
        dataDict (dict): sldata_collection object to save.
        path (str): Path to save data
        overwrite (bool): If True, h5 file can be overwritten. Otherwise, h5 file cannot be overwritten
    """

    if overwrite:
        mode = "w"
    else:
        mode = "w-"

    keysList = dataDict.keys()

    f = _h5py.File(path, mode)

    try:
        for key in keysList:
            slDataObject = dataDict[key]
            slDataGroup = f.create_group(key, track_order=True)
            if isinstance(slDataObject, SpinData):
                write_sldata(slDataGroup, slDataObject)
            elif isinstance(slDataObject, dict):
                write_dict(slDataGroup, slDataObject)
            else:
                warnings.warn("Could not write key: %s" % str(key))

        f.close()

    except:
        f.close()
        raise Warning("h5 close due to error")


def write_sldata(slDataGroup, slDataObject):
    """Takes file/group and writes slData object to it

    Args:
        slDataGroup: h5 group to save data to
        slDataObject: sldata object to save in h5 format
    """
    slDataGroup.attrs["spinlab_version"] = slDataObject.version
    slDataGroup.attrs["spinlab_data_type"] = "sldata"
    dims_group = slDataGroup.create_group("dims")  # dimension names e.g. x,y,z
    attrs_group = slDataGroup.create_group("attrs")  # dictionary information
    sl_dataset = slDataGroup.create_dataset("values", data=slDataObject.values)

    # Save axes information
    for ix in range(len(slDataObject.coords)):
        label = slDataObject.dims[ix]
        this_axes = slDataObject.coords[ix]
        dims_group.create_dataset(label, data=this_axes)
        dims_group[label].make_scale(label)

        sl_dataset.dims[ix].attach_scale(dims_group[label])

    # Save Experiment Attributes
    for key in slDataObject.attrs:
        value = slDataObject.attrs[key]

        if isinstance(value, _np.ndarray):
            attrs_group.create_dataset(key, data=value)
        else:
            if value in python_types:
                ix = python_types.index(value)
                value = replace_types[ix]
            attrs_group.attrs[key] = value

    # Save SpinLab Attributes
    if hasattr(slDataObject, "spinlab_attrs"):
        spinlab_attrs_group = slDataGroup.create_group(
            "spinlab_attrs", track_order=True
        )

        for key in slDataObject.spinlab_attrs:
            value = slDataObject.spinlab_attrs[key]

            if isinstance(value, _np.ndarray):
                spinlab_attrs_group.create_dataset(key, data=value)
            else:
                if value in python_types:
                    ix = python_types.index(value)
                    value = replace_types[ix]
                spinlab_attrs_group.attrs[key] = value

    # Save proc_steps
    if hasattr(slDataObject, "proc_attrs"):
        proc_attrs = slDataObject.proc_attrs
        proc_attrs_group = slDataGroup.create_group("proc_attrs", track_order=True)
        for ix in range(len(proc_attrs)):
            proc_step_name = proc_attrs[ix][0]
            proc_dict = proc_attrs[ix][1]
            proc_attrs_group_subgroup = proc_attrs_group.create_group(
                "%i:%s" % (ix, proc_step_name)
            )
            for key in proc_dict:
                value = proc_dict[key]
                if value is not None:
                    proc_attrs_group_subgroup.attrs[key] = value


def write_dict(slDataGroup, slDataObject):
    """Writes dictionary to h5 file

    Args:
        slDataGroup (h5py.Group): h5 group to write attrs dictionary
        slDataObject (SpinData): SpinData object to write
    """
    #    slDataGroup.attrs['spinlab_version'] = slDataObject.version
    slDataGroup.attrs["spinlab_data_type"] = "dict"
    #    slDataGroup.attrs['spinlab_version'] = slDataObject.version
    attrs_group = slDataGroup.create_group("attrs")

    for key in slDataObject.keys():
        attrs_group.attrs[key] = slDataObject[key]
