"""
========================
操作 Xarray 数据对象的一些工具
------------------------
Author: Lilidream
Date: 2025-03-09
========================
"""
from xarray import DataArray, Dataset
import xarray as xr
from typing import Literal
import warnings
import numpy as np
from typing import List, Literal

def switch_longitude(data: DataArray | Dataset, lon_name: str='longitude',
                     center: Literal['auto', '180', '0', 180, 0]='auto'
                     ) -> DataArray | Dataset:
    """
    将经度坐标在 -180 到 180 和 0 到 360 两种模式之间切换。

    Switch the longitude coordinate between -180 to 180 and 0 to 360 modes.

    Parameters
    ----------
    data : DataArray | Dataset
        xarray 数据。 xarray data.

    lon_name : str, optional
        经度维度的名称。The name of longitude dimension, by default 'lon'

    center : Literal["auto", "180", "0", 180, 0], optional
        新坐标的中心，"180"/180 表示 0 到 360，"0"/0 表示 -180 到 180，默认为 “auto"，
        会根据源数据的经度切换为另一种模式。

        The center of the new coordinate, "180"/180 means 0 to 360,
        "0"/0 means -180 to 180, default is "auto",
        which will switch to another mode according to the source data.

    Returns
    -------
    DataArray | Dataset
        新的数据对象。The new data object.

    """
    if center not in ('auto', '180', '0', 180, 0):
        raise ValueError('center must be "auto", "180", "0", 180 or 0')

    if isinstance(center, int):
        center = str(center)

    # 自动判断
    if center == 'auto':
        lon_min = data[lon_name].min().item()
        lon_max = data[lon_name].max().item()

        if lon_min >= 0 and lon_max <= 180:
            # 经度在 0 - 180 之间，无法判断模式，也无需处理
            warnings.warn('The longitude is in the range of 0-180, no need to switch.')
            return data
        elif lon_min < 0 and lon_max <= 180:
            center = '180'
        elif lon_min >= 0 and lon_max <= 360:
            center = '0'
        else:
            raise ValueError('The longitude is not in the range of 0-180 or 0-360.')

    if center == '180':
        # from -180..179 to 0..359
        data = data.assign_coords(
            **{lon_name: (lambda x: ((x[lon_name] + 360) % 360))}
            )
    else:
        # from 0..359 to -180..179
        data = data.assign_coords(
            **{lon_name: (lambda x: ((x[lon_name] + 180) % 360) - 180)}
        )

    return data.sortby(lon_name)


def safe_sel(data: DataArray | Dataset, indexers: dict=None,
             method: Literal[None, "nearest", "pad", "ffill",
                             "backfill", "bfill"]=None,
             tolerance=None, drop: bool=False, **kwargs) -> DataArray | Dataset:
    """
    选择数据时自动根据维度数值的增减来调整选取，避免选出空数据。
    例如纬度的坐标为 90 到 -90， 使用 slice(0, 50) 时会根据维度调整为 slice(50, 0)。
    维度的值只能是单调递增或递减的。

    Automatically adjust the selection according to the increase or decrease
    of the dimension values to avoid selecting empty data.
    For example, the coordinate of latitude is from 90 to -90,
    when using slice(0, 50), it will be adjusted to slice(50, 0) according to
    the dimension.
    The value of the dimension must be monotonically increasing or decreasing.

    Parameters
    ----------
    data : DataArray | Dataset
        xarray 数据。 xarray data.
    indexers : dict, optional
        选取索引，与 xarray.sel 的 indexers 参数一致。Selection index,
        consistent with the indexers parameter of xarray.sel, by default None
    method : Literal[None, "nearest", "pad", "ffill", "backfill", "bfill"], optional
        选择数据时的插值方法，与 xarray.sel 的 method 参数一致。The interpolation
        method when selecting data, consistent with the method parameter of
        xarray.sel, by default None
    tolerance : None, optional
        选择数据时的容差，与 xarray.sel 的 tolerance 参数一致。The tolerance when
        selecting data, consistent with the tolerance parameter of xarray.sel,
        by default None
    drop : bool, optional
        是否删除选取后的空维度。Whether to delete the empty dimension after selection,
        by default False
    **kwargs :
        选取的维度和选取方式。The dimensions and selection methods.

    Example
    -------

    ```python
    data = xr.DataArray(np.arange(0, 10), dims='x', coords={'x': np.arange(0, 10)})
    new_data = safe_sel(data, x=slice(0, 5))  # 使用方法与 xarray.sel 一致
    ```

    Returns
    -------
    DataArray | Dataset
        新的数据对象。The new data object.
    """

    if not isinstance(indexers, dict) and indexers is not None: 
        raise ValueError('indexers must be a dict.')

    if indexers is None:
        indexers = {}

    for key, value in kwargs.items():
        indexers[key] = value

    # 识别处理
    for key, value in indexers.items():
        if key not in data.dims:
            raise ValueError(f'The dimension "{key}" is not in the data.')
        if isinstance(value, slice):
            if value.start is None or value.stop is None:
                continue

            dim = data[key].values
            # 检查单调性
            diffs = np.ediff1d(dim)
            if np.all(diffs >= 1e-8):
                # 升序
                if value.start > value.stop:
                    value = slice(value.stop, value.start, value.step)
            elif np.all(diffs <= -1e-8):
                # 降序
                if value.start < value.stop:
                    value = slice(value.stop, value.start, value.step)
            else:
                raise ValueError(f'The dimension "{key}" is not monotonic.')

            indexers[key] = value

    return data.sel(indexers, method=method, tolerance=tolerance, drop=drop)


def moving_average(data: DataArray , window: float,
                   dims: str | list[str]=None,
                   window_units: str='days', nan_edge: bool=False) -> DataArray:
    """
    计算滑动平均值，支持时间和空间维度。
    Calculate the moving average, supports time and space dimensions.

    Parameters
    ----------
    data : DataArray
        要计算滑动平均值的数据。The data to calculate the moving average.
    window : float
        滑动窗口大小，单位与数据维度一致，而不是数量。在时间上滑动平均，
        需要指定 `window_units` 为 `window` 的时间单位。
        例如在经度上滑动平均， 数据分辨率为 0.5 度, `window = 2` 表示以 2 度
        滑动平均，实际计算的窗口为 2/0.5=4 个数值。

        The size of the moving window, the unit is consistent with the data
        dimension, not the number.
        For moving average in time, you need to specify `window_units` as the
        time unit of `window`.
        For example, in longitude moving average, the data resolution is 0.5
        degrees, `window = 2` means moving average with 2 degrees, the actual
        calculation window is 2/0.5=4 values.
    dims : str | list[str], optional
        计算的维度名，支持多个，如果数据只有一个维度，可以不填。

        The dimension name to calculate, supports multiple. If the data has only
        one dimension, you can not fill it.
    window_units : str, optional
        滑动窗口的时间单位，只有维度是时间时有效，支持所有 Pandas 的字符时间单位。

        The time unit of the moving window, only valid when the dimension is time,
        supports all Pandas string time units.
    nan_edge : bool, optional
        数据两边小于半个窗口的值是否使用 NaN 填充，默认为 False。
        如果为 `False`，则两边会缩小窗口大小来计算平均值。

        Whether to fill the values less than half of the window with NaN,
        default is False. If `False`, the window size will be reduced to
        calculate the average value.

    Returns
    -------
    DataArray
        滑动平均后的数据。The data after moving average.

    """
    from pandas import Timedelta

    # 空间或时间的滑动平均
    if dims is None:
        if len(data.dims) == 1:
            dims = data.dims[0]
        else:
            raise ValueError(
                'dim must be specified when data has more than 1 dimension.'
            )

    if isinstance(dims, str):
        dims = [dims]

    idx_windows = []
    for _d in dims:
        dim_var = data[_d]
        if dim_var.size <= 3:
            raise ValueError(
                f'The dimension "{_d}" has only {dim_var.size} values, '
                'cannot calculate moving average.'
            )
        # 检查是否为时间维度
        if dim_var.dtype.kind == 'M':
            window = Timedelta(window, unit=window_units).total_seconds()
            res = Timedelta(dim_var.values[1] - dim_var.values[0]).total_seconds()
        else:
            res = dim_var.values[1] - dim_var.values[0]

        # 检查窗口是否为分辨率的整数倍
        if window % res != 0:
            warnings.warn(
                f'The window {window} is not a multiple of the resolution {res}'
                f' in dimension "{_d}". The window in calculation will be '
                f'rounded to {int(window / res)}.'
            )
        idx_windows.append(int(window / res))


    data = data.rolling(
        {d: idx_windows[i] for i, d in enumerate(dims)},
        center=True, min_periods=None if nan_edge else 1
    ).mean()

    return data


def multi_sel(*variables: DataArray|Dataset, **kwargs) -> List[DataArray|Dataset]:
    """对多个变量进行选择的包装器，并返回对应变量

    Select multiple variables and return the corresponding variables.

    Examples
    --------
        >>> from moisten.calc._xr import multi_sel
        >>> u = xr.open_dataarray('u.nc')
        >>> v = xr.open_dataarray('v.nc')
        >>> w = xr.open_dataarray('w.nc')
        >>> # 对 u, v, w 进行相同的选取
        >>> u, v, w = multi_sel(u, v, w, level=500, lon=slice(100, 150))
        >>> # 等同于
        >>> u = u.sel(level=500, lon=slice(100, 150))
        >>> v = v.sel(level=500, lon=slice(100, 150))
        >>> w = w.sel(level=500, lon=slice(100, 150))

    Parameters
    ----------
    *variables : DataArray | Dataset
        要进行选择的对象

    **kwargs:
        传入到 sel() 中的参数，可以是维度的选取，也可以是其他参数

    Returns
    -------
    _type_
        _description_
    """
    result = []
    for i in range(len(variables)):
        result.append(variables[i].sel(**kwargs))
    return result


def multi_isel(*variables: DataArray|Dataset, **kwargs) -> List[DataArray|Dataset]:
    """对多个变量进行选择的包装器，并返回对应变量

    Select multiple variables and return the corresponding variables.

    Examples
    --------
        >>> from moisten.calc._xr import multi_isel
        >>> u = xr.open_dataarray('u.nc')
        >>> v = xr.open_dataarray('v.nc')
        >>> w = xr.open_dataarray('w.nc')
        >>> # 对 u, v, w 进行相同的选取
        >>> u, v, w = multi_isel(u, v, w, level=2, lon=slice(0, 100))
        >>> # 等同于
        >>> u = u.isel(level=2, lon=slice(0, 100))
        >>> v = v.isel(level=2, lon=slice(0, 100))
        >>> w = w.isel(level=2, lon=slice(0, 100))

    Parameters
    ----------
    *variables : DataArray | Dataset
        要进行选择的对象

    **kwargs:
        传入到 isel() 中的参数，可以是维度的选取，也可以是其他参数

    Returns
    -------
    _type_
        _description_
    """
    result = []
    for i in range(len(variables)):
        result.append(variables[i].isel(**kwargs))
    return result


def xr_compress_encoding(data_or_names: DataArray | Dataset | str | List[str],
                        compress_level: int = 4) -> dict:
    """
    生成 xarray.to_netcdf() 保存时的压缩编码参数。

    Generate compression encoding parameters for xarray.to_netcdf() saving.

    Examples
    --------
    Compress all variables when saving:

        >>> myData.to_netcdf("myData.nc", encoding=xr_compress_encoding(myData))

    Compress only specific variables:

        >>> myDataset.to_netcdf("myDataset.nc", encoding=xr_compress_encoding(["var1", "var2"]))

    Parameters
    ----------
    data_or_names : DataArray | Dataset | str | List[str]
        可以传入要压缩的 DataArray 或 Dataset 对象，或者要压缩的 DataArray 名称列表。

        DataArray or Dataset object, or variable name(s) to compress.
        When passing a Dataset, all data variables will be compressed.
    compress_level : int, optional
        压缩等级，有效值为 1-9，越大压缩率越高，默认为 4。

        Compression level, valid values are 1-9, by default 4.

    Returns
    -------
    dict
        返回用于 `to_netcdf` 的 `encoding` 参数字典。
        Dictionary with encoding parameters.

    """

    if isinstance(data_or_names, DataArray):
        var_names = [data_or_names.name]
    elif isinstance(data_or_names, Dataset):
        var_names = list(data_or_names.data_vars)
    elif isinstance(data_or_names, str):
        var_names = [data_or_names]
    else:
        var_names = data_or_names

    encoding = {}
    for name in var_names:
        encoding[name] = {'zlib': True, 'complevel': compress_level}

    return encoding


def xr_int16_compress(data: DataArray | Dataset, names: str | list[str] | None = None,
                   compress_level: int | bool = 4
                   ) -> tuple[DataArray | Dataset, dict]:
    """
    将数据转换为 int16 类型并进行压缩。将数据从浮点转为 int16 后保存，
    可以大幅减少需要的储存空间，但精度会降低到 5 位有效数字。
    返回一个转换后的 DataArray 或 Dataset，以及对应的 encoding 字典。

    Convert data to int16 type and compress it. Converting data from float to int16
    can significantly reduce storage space, but the precision will be reduced
    to 5 significant digits.

    Examples
    --------
    Compress all variables when saving:
        >>> myData, encoding = xr_int16_compress(myData)
        >>> myData.to_netcdf("myData.nc", encoding=encoding)

    Compress only specific variables:
        >>> myDataset, encoding = xr_int16_compress(myDataset, names=["var1", "var2"])
        >>> myDataset.to_netcdf("myDataset.nc", encoding=encoding)


    Parameters
    ----------
    data : DataArray | Dataset
        需要压缩的数据对象，可以是 DataArray 或 Dataset。

        The data object to compress, can be DataArray or Dataset.
    names : str | list[str] | None, optional
        需要指定压缩的 DataArray 名称列表，如果为 None，则压缩所有 DataArray。

        The list of DataArray names to compress, if None, compress all DataArrays.
    compress_level : int | bool, optional
        压缩等级，有效值为 1-9，越大压缩率越高，默认为 4。

        Compression level, valid values are 1-9, by default 4.
    Returns
    -------
    tuple[DataArray | Dataset, dict]
        返回压缩后的数据对象和编码参数字典。

        Returns the compressed data object and encoding parameters dictionary.

    """
    encoding = {}
    encodind_template = {
        '_FillValue': -32768,
        'zlib': compress_level is not False,
        'complevel': compress_level
    }

    def one_dataarray(da: DataArray) -> DataArray:
        attrs = da.attrs.copy()
        d_max = da.max().values
        d_min = da.min().values

        offset = ((d_max + d_min) / 2)
        scale = (d_max - d_min) / 65534 # 缩放到 -32767 ~ 32767

        encode_data = (da - offset) / scale
        encode_data = encode_data.fillna(-32768)  # 将 NaN 转换为 -32768
        encode_data = encode_data.astype(np.int16)

        attrs['scale_factor'] = scale
        attrs['add_offset'] = offset

        encode_data = encode_data.assign_attrs(attrs)

        return encode_data

    if isinstance(data, DataArray):
        data = one_dataarray(data)
        encoding[data.name] = encodind_template.copy()
        return data, encoding

    elif isinstance(data, Dataset):
        if names is None:
            names = list(data.data_vars)
        elif isinstance(names, str):
            names = [names]

        for name in names:
            if name not in data.data_vars:
                raise ValueError(f'Variable "{name}" not found in Dataset.')
            da = one_dataarray(data[name])
            encoding[name] = encodind_template.copy()
            data[name] = da

        return data, encoding


def extend_lon(data: DataArray | Dataset, lon_name: str='longitude',
               extend_degrees: float=60) -> DataArray | Dataset:
    """将数据在经度轴上头尾循环填充，类似 np.pad 的 mode='wrap'。
    请确保数据在经度上是全球的，即 -180 到 180 或 0 到 360。
    新的数据的经度值将会拓展，例如从 0-360 拓展到 -60 到 420。

    Parameters
    ----------
    data : DataArray | Dataset
        需要扩展的数据对象，可以是 DataArray 或 Dataset。

        The data object to extend, can be DataArray or Dataset.
    lon_name : str, optional
        经度的名称, by default 'longitude'

        The name of longitude dimension, by default 'longitude'.
    extend_degrees : float, optional
        单边拓展的经度范围，以度为单位, by default 60

    Returns
    -------
    DataArray | Dataset
        返回拓展后的数据对象。
    """

    dx = data[lon_name].values[1] - data[lon_name].values[0]
    warp_num = int(extend_degrees / dx)
    if warp_num < 1:
        raise ValueError('extend_degrees is too small.')

    lon = data[lon_name]
    new_lon = np.concatenate([
        lon.values[-warp_num:] - 360,
        lon.values,
        lon.values[:warp_num] + 360
    ])
    data = data.pad({lon_name: (warp_num, warp_num)}, mode='wrap')
    data = data.assign_coords({lon_name: new_lon})
    return data
