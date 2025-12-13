"""
计算函数
"""
import numpy as np
import xarray as xr
from typing import Literal
from .constant import LENGTH_PRE_LATITUDE as _LENGTH_PRE_LATITUDE

def lon_lat_distance(lon: np.ndarray, lat: np.ndarray
                     ) -> tuple[np.ndarray, np.ndarray]:
    """根据等间距经纬度，生成实际经纬网格间距。使用球形模型，地球半径来自WGS84.

    Generate the actual grid spacing of latitude and longitude based on latitude and longitude.
    The spherical model is used, and the radius of the earth comes from WGS84.

    Example
    -------
        >>> from moisten.calc import lon_lat_distance
        >>> import numpy as np
        >>> lon = np.arange(0, 360, 1.0)
        >>> lat = np.arange(-90, 91, 1.0)
        >>> dx, dy = lon_lat_distance(lon, lat)

    Parameters
    ----------
    lon : np.ndarray
        经度  longitude
    lat : np.ndarray
        纬度  latitude

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        返回纬向（x）和经向（y）的网格间距数组，单位为米

        return the grid spacing array of latitude (x) and longitude (y), in meters
    """

    # 验证输入是否为1维
    if lon.ndim != 1 or lat.ndim != 1:
        raise ValueError("lon and lat must be 1D arrays")

    # 验证是否等间距
    if not np.all(np.isclose(np.diff(lon), np.diff(lon)[0])):
        raise ValueError("Longitude is not equidistant")
    if not np.all(np.isclose(np.diff(lat), np.diff(lat)[0])):
        raise ValueError("Latitude is not equidistant")

    resolutionX: float = np.abs(lon[1] - lon[0])
    resolutionY: float = np.abs(lat[1] - lat[0])

    dy = np.ones((len(lat), len(lon))) * _LENGTH_PRE_LATITUDE * resolutionY
    dx = np.ones((len(lat))) * _LENGTH_PRE_LATITUDE * \
        np.cos(lat * np.pi / 180) * resolutionX
    dx = np.expand_dims(dx, axis=1).repeat(len(lon), axis=1)
    return dx, dy


def derivative(data: xr.DataArray, coord: str,
                dim_type: Literal["auto", "lonlat", "other"] = "auto",
                lon_name: str = "longitude", lat_name: str = "latitude",
                datetime_unit: Literal["W", "D", "h", "m", "s", "ms", "us",
                                       "ns", "ps", "fs", "as", None] = None,
                edge_order: Literal[1, 2] = 2
                ) -> xr.DataArray:
    """计算物理量在指定坐标上的一阶导数/梯度，支持空间维度和时间/其他维度的导数计算。

    Parameters
    ----------
    data : xr.DataArray
        要计算的数据，目前仅支持 `DataArray` 类型

        The data to be calculated, currently only supports `DataArray` type
    coord : str
        要求导数的维度名称

        The name of the dimension to be differentiated

    dim_type : Literal["auto", "lonlat", "other"], optional
        维度的类型，如果需要在经纬度坐标上求水平梯度，则设为 "lonlat"；
        如果是时间或其他维度，则设为 "other"。默认自动检测。

        The type of dimension. If you need to calculate the horizontal gradient
        on the latitude and longitude coordinates, set it to "lonlat"; if it is
        time or other dimensions, set it to "other". Default is auto-detect.

    lon_name, lat_name : str, optional
        数据中经纬度维度的名称(如果计算经纬度维度的梯度），
        默认为 "longitude" 和 "latitude"。

        The names of the longitude and latitude dimensions in the data
        (if calculating the gradient of latitude and longitude dimensions),
        default is "longitude" and "latitude".

    datetime_unit : Literal["W", "D", "h", "m", "s", "ms", "us",
                             "ns", "ps", "fs", "as", None], optional
        计算时间变化率时使用的时间单位，为 xr.differentiate 的参数。

        The time unit used when calculating the rate of change of time,
        which is a parameter of xr.differentiate.

    edge_order : Literal[1, 2], optional
        计算导数时，使用的边界处理方式，默认为2阶

        The boundary handling method used when calculating the derivative,
        the default is 2nd order.

    Returns
    -------
    xr.DataArray
        返回计算后的导数数据

        Return the calculated derivative data
    """
    data = data.copy(deep=False)

    if dim_type == "auto":
        if coord in ["lon", "lat", "longitude", "latitude", lon_name, lat_name]:
            dim_type = "lonlat"
        else:
            dim_type = "other"

    if dim_type == "lonlat":
        dx, dy = lon_lat_distance(data[lon_name].values, data[lat_name].values)
        axis = data.get_axis_num(coord)
        data.values = np.gradient(data.values, axis=axis, edge_order=edge_order)

        if coord == lon_name:
            data.values /= dx
        else:
            if data[lat_name].values[0] > data[lat_name].values[-1]:
                dy *= -1
            data.values /= dy

        return data

    elif dim_type == "other":
        return data.differentiate(coord, edge_order=edge_order,
                                    datetime_unit=datetime_unit)

    else:
        raise ValueError("dim_type must be 'auto', 'lonlat' or 'other'")


def coriolis_parameter(latitude: np.ndarray | float) -> np.ndarray | float:
    """
    计算科里奥利参数，需要传入纬度。
    如果是 Numpy 数组，返回的也是相同 Shape 的 Numpy 数组。
    计算公式为：
        f = 2 * Omega * sin(latitude)
    其中 Omega 为地球自转角速度。

    Calculate the Coriolis parameter, which is a function of latitude.
    If the input latitude does not have a unit, it is assumed to be in degrees.
    The formula is:
        f = 2 * Omega * sin(latitude)
    where Omega is the angular velocity of the Earth.

    Parameters
    ----------
    latitude : ndarray | float
        纬度，以度为单位。
        Latitude in degrees.

    Returns
    -------
    Quantity
        科里奥利参数，单位为 rad/s。

        The Coriolis parameter corresponding to the input latitude.

    """
    from .constant import EARTH_ROTATION_ANGULAR_VELOCITY

    latitude = np.deg2rad(latitude)
    f = 2 * EARTH_ROTATION_ANGULAR_VELOCITY * np.sin(latitude)
    return f


def rossby_parameter(latitude: np.ndarray | float) -> np.ndarray | float:
    """
    计算罗斯贝参数，需要传入纬度。
    如果是 Numpy 数组，返回的也是相同 Shape 的 Numpy 数组。
    计算公式为：
        beta = 2 * Omega * cos(latitude) / a
    其中 Omega 为地球自转角速度，a 为地球半径。

    Calculate the rossby parameter, which is a function of latitude.
    If the input latitude does not have a unit, it is assumed to be in degrees.
    The formula is:
        beta = 2 * Omega * cos(latitude) / a
    where Omega is the angular velocity of the Earth and a is the radius of the Earth.

    Parameters
    ----------
    latitude : np.ndarray | float
        纬度，以度为单位。
        Latitude in degrees.

    Returns
    -------
    Quantity
        罗斯贝参数，单位为 rad/s/m。

        The Rossby parameter corresponding to the input latitude.

    """
    from .constant import EARTH_ROTATION_ANGULAR_VELOCITY, EARTH_RADIUS
    latitude = np.deg2rad(latitude)
    b = 2 * EARTH_ROTATION_ANGULAR_VELOCITY * np.cos(latitude) / EARTH_RADIUS
    return b


def downsample(v: np.ndarray | xr.DataArray, interval:int,
               dims: int | str | list[int] | list[str]=None):
    """对 n 维数据进行间隔降采样，可以指的定降采样的维度，默认全部维度。

    Downsample n-dimensional data at intervals,
    you can specify the dimensions to downsample,
    the default is all dimensions.

    Parameters
    ----------
    v : np.ndarray | xr.DataArray
        要降采样的数据

        The data to be downsampled.

    interval : int
        降采样的间隔，每隔 interval 取一个值

        The interval of downsampling, take one value every interval.

    dims : int | str | list[int] | list[str]
        要降采样的维度，默认全部维度。
        可以是一个整数或者一组整数，如果数据是 DataArray， 还可以是维度的名称。

        The dimensions to be downsampled, default is all dimensions.
        It can be an integer or a group of integers,
        and if the data is DataArray, it can also be the names of the dimensions.
    """
    if isinstance(dims, (list, tuple)):
        if (not all(isinstance(i, int) for i in dims)) and \
                (not all(isinstance(i, str) for i in dims)):
            raise ValueError("dims must be list of int or str")

    if dims is None:
        slices = tuple(slice(None, None, interval) for _ in range(v.ndim))
        return v[slices]
    elif isinstance(dims, int):
        slices = tuple(slice(None, None, interval) if i == dims else slice(None)
                        for i in range(v.ndim))
        return v[slices]
    elif isinstance(dims, str):
        if isinstance(v, xr.DataArray):
            slices = {dims: slice(None, None, interval)}
            return v.isel(slices)
        else:
            raise ValueError("only DataArray support `str` dims")
    elif isinstance(dims, (list, tuple)):
        if isinstance(dims[0], int):
            slices = tuple(slice(None, None, interval) if i in dims else slice(None)
                            for i in range(v.ndim))
            return v[slices]
        elif isinstance(dims[0], str):
            if isinstance(v, xr.DataArray):
                slices = {i: slice(None, None, interval) for i in dims}
                return v.isel(slices)
            else:
                raise ValueError("only DataArray support str dims")
    else:
        raise ValueError("dims must be int, list of int or str")
