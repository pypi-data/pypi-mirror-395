from typing import Union, Literal

import numpy as np
import xarray as xr
from rich import print


__all__ = ["earth_distance", "mask_shapefile", "mask_land_ocean", "is_land", "is_ocean"]


def earth_distance(lon1, lat1, lon2, lat2):
    """
    计算两点间的距离（km）
    """
    from math import asin, cos, radians, sin, sqrt
    # 将经纬度转换为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球半径（公里）
    return c * r


def mask_shapefile(
    data_array: np.ndarray,
    longitudes: np.ndarray,
    latitudes: np.ndarray,
    shapefile_path: str,
) -> Union[xr.DataArray, None]:
    """
    Mask a 2D data array using a shapefile.

    Args:
        data_array (np.ndarray): 2D array of data to be masked.
        longitudes (np.ndarray): 1D array of longitudes.
        latitudes (np.ndarray): 1D array of latitudes.
        shapefile_path (str): Path to the shapefile used for masking.

    Returns:
        Union[xr.DataArray, None]: Masked xarray DataArray or None if an error occurs.

    Raises:
        FileNotFoundError: If the shapefile does not exist.
        ValueError: If the data dimensions do not match the coordinates.

    Examples:
        >>> data_array = np.random.rand(10, 10)
        >>> longitudes = np.linspace(-180, 180, 10)
        >>> latitudes = np.linspace(-90, 90, 10)
        >>> shapefile_path = "path/to/shapefile.shp"
        >>> masked_data = mask_shapefile(data_array, longitudes, latitudes, shapefile_path)
        >>> print(masked_data)  # Expected output: Masked DataArray

    """
    import salem
    try:
        shp_f = salem.read_shapefile(shapefile_path)
        data_da = xr.DataArray(data_array, coords=[("latitude", latitudes), ("longitude", longitudes)])
        masked_data = data_da.salem.roi(shape=shp_f)
        return masked_data
    except Exception as e:
        print(f"[red]An error occurred: {e}[/red]")
        return None


def _normalize_lon(lon: np.ndarray) -> np.ndarray:
    """将经度转换到 [-180, 180)。"""
    lon = np.asarray(lon, dtype=float)
    return np.where(lon >= 180, lon - 360, lon)


def _land_sea_mask(
    lon: np.ndarray,
    lat: np.ndarray,
    keep: Literal["land", "ocean"],
) -> np.ndarray:
    """
    根据 1-D 或 2-D 经纬度返回布尔掩膜。
    True 表示该位置 *保留*，False 表示该位置将被掩掉。
    """
    from global_land_mask import globe
    
    lon = _normalize_lon(lon)
    lat = np.asarray(lat, dtype=float)

    # 如果输入是 1-D，则网格化；2-D 则直接使用
    if lon.ndim == 1 and lat.ndim == 1:
        lon_2d, lat_2d = np.meshgrid(lon, lat)
    elif lon.ndim == 2 and lat.ndim == 2:
        lon_2d, lat_2d = lon, lat
    else:
        raise ValueError("经纬度必须是同维度的 1-D 或 2-D 数组")

    is_ocean = globe.is_ocean(lat_2d, lon_2d)

    if keep == "land":
        mask = ~is_ocean
    elif keep == "ocean":
        mask = is_ocean
    else:
        raise ValueError("keep 只能是 'land' 或 'ocean'")

    return mask


def mask_land_ocean(
    data: xr.DataArray | xr.Dataset,
    lon: np.ndarray,
    lat: np.ndarray,
    *,  # 强制关键字参数
    keep: Literal["land", "ocean"] = "land",
) -> xr.DataArray | xr.Dataset:
    """
    根据海陆分布掩膜 xarray 对象。

    Parameters
    ----------
    data : xr.DataArray 或 xr.Dataset
        至少包含 'lat' 和 'lon' 维度/坐标的数组。
    lon : array_like
        经度，可以是 1-D 或 2-D。
    lat : array_like
        纬度，可以是 1-D 或 2-D。
    keep : {'land', 'ocean'}, optional
        指定要保留的部分，默认为 'land'。

    Returns
    -------
    掩膜后的 xr.DataArray / xr.Dataset
    """
    mask = _land_sea_mask(lon, lat, keep)

    # 将布尔掩膜转换为 xarray.DataArray
    mask_da = xr.DataArray(mask, dims=("lat", "lon"))

    # 如果输入已经是 xarray 对象，直接使用 where
    if isinstance(data, (xr.DataArray, xr.Dataset)):
        return data.where(mask_da)

    # 如果输入是 numpy 数组，则假定最后两个维度是 (lat, lon)
    if isinstance(data, np.ndarray):
        arr = data
        if arr.ndim < 2:
            raise ValueError("numpy array 数据至少应包含 2 个维度 (lat, lon)")

        if arr.ndim == 2:
            lat_arr = np.asarray(lat)
            lon_arr = np.asarray(lon)
            # 支持 lat/lon 为 1D 或 2D
            if lat_arr.ndim == 1 and lon_arr.ndim == 1:
                da = xr.DataArray(arr, dims=("lat", "lon"), coords={"lat": lat_arr, "lon": lon_arr})
            elif lat_arr.ndim == 2 and lon_arr.ndim == 2:
                if lat_arr.shape != arr.shape or lon_arr.shape != arr.shape:
                    raise ValueError("提供的二维经纬度数组形状必须匹配数据的 (lat, lon) 维度")
                da = xr.DataArray(arr, dims=("lat", "lon"), coords={"lat": (("lat", "lon"), lat_arr), "lon": (("lat", "lon"), lon_arr)})
            else:
                raise ValueError("lat/lon 必须同时为 1D 或同时为 2D")
        else:
            # 为前面的维度生成占位名称，例如 dim_0, dim_1, ...
            leading_dims = [f"dim_{i}" for i in range(arr.ndim - 2)]
            dims = leading_dims + ["lat", "lon"]
            coords = {f"dim_{i}": np.arange(arr.shape[i]) for i in range(arr.ndim - 2)}

            lat_arr = np.asarray(lat)
            lon_arr = np.asarray(lon)
            # 如果 lat/lon 为 1D
            if lat_arr.ndim == 1 and lon_arr.ndim == 1:
                if lat_arr.shape[0] != arr.shape[-2] or lon_arr.shape[0] != arr.shape[-1]:
                    raise ValueError("一维 lat/lon 长度必须匹配数据的最后两个维度")
                coords.update({"lat": lat_arr, "lon": lon_arr})
            # 如果 lat/lon 为 2D，要求其形状与数据最后两个维度一致
            elif lat_arr.ndim == 2 and lon_arr.ndim == 2:
                if lat_arr.shape != (arr.shape[-2], arr.shape[-1]) or lon_arr.shape != (arr.shape[-2], arr.shape[-1]):
                    raise ValueError("二维 lat/lon 的形状必须匹配数据的最后两个维度")
                coords.update({"lat": (("lat", "lon"), lat_arr), "lon": (("lat", "lon"), lon_arr)})
            else:
                raise ValueError("lat/lon 必须同时为 1D 或同时为 2D")

            da = xr.DataArray(arr, dims=dims, coords=coords)

        masked = da.where(mask_da)
        # 返回与输入相同的类型：numpy -> numpy
        return masked.values

    # 其他类型尝试转换为 DataArray
    try:
        da = xr.DataArray(data)
        return da.where(mask_da)
    except Exception:
        raise TypeError("data must be xr.DataArray, xr.Dataset, or numpy.ndarray")


def is_land(lat: float, lon: float) -> bool:
    """
    判断给定经纬度点是否在陆地上。

    参数:
        lat (float): 纬度
        lon (float): 经度

    返回:
        bool: 如果点在陆地上则返回 True，否则返回 False
    """
    from global_land_mask import globe
    lon = lon if lon <= 180 else lon - 360
    return globe.is_land(lat, lon)


def is_ocean(lat: float, lon: float) -> bool:
    """
    判断给定经纬度点是否在海洋上。

    参数:
        lat (float): 纬度
        lon (float): 经度

    返回:
        bool: 如果点在海洋上则返回 True，否则返回 False
    """
    from global_land_mask import globe
    lon = lon if lon <= 180 else lon - 360
    return globe.is_ocean(lat, lon)

if __name__ == "__main__":
    pass
