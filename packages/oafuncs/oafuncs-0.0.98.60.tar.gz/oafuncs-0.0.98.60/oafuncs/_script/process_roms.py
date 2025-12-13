#!/usr/bin/env python3
"""
process_roms_uv_fixed.py

ROMS -> lon/lat remapping with correct u/v handling following Fortran workflow:
  - Average u/v to rho points (pad both ends then average)
  - Vertical interpolate on SOURCE rho depths to standard target depths (spline fallback linear)
  - Horizontal remap each target level to output lon/lat (xESMF)
Robust Cs handling, no silent NaN propagation, endpoint handling like Fortran splint.

Usage: edit __main__ input_nc/output_nc/varnames/target_lon/target_lat/target_depth.
Dependencies: numpy, xarray, scipy, xesmf
"""

from typing import Optional, Sequence, Dict, Any, Tuple
import numpy as np
import xarray as xr
from scipy.interpolate import interp1d, CubicSpline
from rich import print

# Verbose toggles
VERBOSE = True
VERBOSE_DEBUG = False

# -------------------------
# Utilities
# -------------------------
def safe_nanmin(a):
    a = np.asarray(a)
    if np.isfinite(a).any():
        return np.nanmin(a)
    return np.nan


def safe_nanmax(a):
    a = np.asarray(a)
    if np.isfinite(a).any():
        return np.nanmax(a)
    return np.nan


def avg_to_rho_axis_padboth(arr: np.ndarray, axis: int) -> np.ndarray:
    """
    Pad both ends with edge values and average adjacent pairs along axis.
    Input length n -> output length n+1. Works for N-D arrays.
    """
    arr = np.asarray(arr)
    if arr.size == 0:
        return arr
    arr = arr.astype(np.float64, copy=False)
    axis = axis if axis >= 0 else arr.ndim + axis
    pad = [(0, 0)] * arr.ndim
    pad[axis] = (1, 1)
    arr_pad = np.pad(arr, pad, mode='edge')
    # average adjacent pairs
    slic_l = [slice(None)] * arr.ndim
    slic_r = [slice(None)] * arr.ndim
    slic_l[axis] = slice(0, arr_pad.shape[axis] - 1)
    slic_r[axis] = slice(1, arr_pad.shape[axis])
    left = arr_pad[tuple(slic_l)]
    right = arr_pad[tuple(slic_r)]
    out = 0.5 * (left + right)
    return np.ascontiguousarray(out)


def _need_periodic(lon1d: np.ndarray, tol: float = 1.0) -> bool:
    lon1d = np.asarray(lon1d, dtype=np.float64)
    if lon1d.size == 0:
        return False
    span = np.nanmax(lon1d) - np.nanmin(lon1d)
    return span > (360 - tol)


# -------------------------
# Vertical stretching helpers (Cs)
# -------------------------
def _compute_C_from_vstretching(s: np.ndarray, theta_s: float, theta_b: float, vstretching: int) -> np.ndarray:
    s = np.asarray(s, dtype=np.float64)
    vstretching = int(vstretching)
    theta_s = float(theta_s)
    theta_b = float(theta_b)
    if vstretching == 1:
        return (1 - theta_b) * (np.sinh(theta_s * s) / np.sinh(theta_s)) + \
               theta_b * (-0.5 + 0.5 * np.tanh(theta_s * (s + 0.5)) / np.tanh(0.5 * theta_s))
    elif vstretching == 2:
        Csur = (1 - np.cosh(theta_s * s)) / (np.cosh(theta_s) - 1)
        Cbot = -1 + (1 - np.sinh(theta_b * (s + 1))) / np.sinh(theta_b)
        alpha, beta = 3.0, 3.0
        Cweight = (s + 1) ** alpha * (1 + (alpha / beta) * (1 - (s + 1) ** beta))
        return Cweight * Csur + (1 - Cweight) * Cbot
    else:
        # 4
        Ctemp = (1 - np.cosh(theta_s * s)) / (np.cosh(theta_s) - 1)
        denom = (1 - np.exp(-theta_b))
        denom = denom if denom != 0 else 1e-12
        return (np.exp(theta_b * Ctemp) - 1) / denom


# -------------------------
# Compute source z (vectorized), validate Cs
# -------------------------
def get_roms_depths(ds: xr.Dataset, is_w: bool = False, time_index: Optional[int] = None,
                    eps: float = 1e-8) -> xr.DataArray:
    vtransform = int(getattr(ds, 'Vtransform', ds.attrs.get('Vtransform', 2)))
    vstretching = int(getattr(ds, 'Vstretching', ds.attrs.get('Vstretching', 4)))
    theta_s = float(ds.attrs.get('theta_s', getattr(ds, 'theta_s', 5.0)))
    theta_b = float(ds.attrs.get('theta_b', getattr(ds, 'theta_b', 0.4)))

    h = ds['h'].astype('f8').values
    if 'mask_rho' in ds.variables:
        mask_rho = ds['mask_rho'].astype('f8').values
        h = h.copy()
        h[mask_rho == 0] = np.nan

    hc = None
    if 'hc' in ds.variables:
        try:
            hc = float(np.array(ds['hc'].values))
        except Exception:
            hc = None
    if hc is None:
        hc = float(ds.attrs.get('hc', 1.0))
    hc = float(hc)

    # zeta
    if 'zeta' in ds.variables:
        zeta_da = ds['zeta']
        if 'ocean_time' in zeta_da.dims:
            if time_index is None:
                zeta = zeta_da.astype('f8').values
            else:
                zeta = zeta_da.isel(ocean_time=int(time_index)).astype('f8').values
        else:
            zeta = zeta_da.astype('f8').values
    else:
        if time_index is None and 'ocean_time' in ds.dims:
            ntime = int(ds.sizes.get('ocean_time', 1))
            zeta = np.zeros((ntime,) + h.shape, dtype=np.float64)
        else:
            zeta = np.zeros_like(h, dtype=np.float64)

    if is_w:
        Ns = int(ds.sizes.get('s_w', 0))
        sc_name, Cs_name = 'sc_w', 'Cs_w'
        s_dim = 's_w'
    else:
        Ns = int(ds.sizes.get('s_rho', 0))
        sc_name, Cs_name = 'sc_r', 'Cs_r'
        s_dim = 's_rho'

    if sc_name in ds.variables:
        s = np.asarray(ds[sc_name].values, dtype=np.float64).ravel()
    else:
        if is_w:
            s = (np.arange(0, Ns) - Ns) / float(Ns)
        else:
            s = (np.arange(1, Ns + 1) - Ns - 0.5) / float(Ns)

    # Cs read + validate
    if Cs_name in ds.variables:
        try:
            C_read = np.asarray(ds[Cs_name].values, dtype=np.float64).ravel()
        except Exception:
            C_read = None
    else:
        C_read = None

    if C_read is None:
        C = _compute_C_from_vstretching(s, theta_s, theta_b, vstretching)
    else:
        cmin = safe_nanmin(C_read)
        cmax = safe_nanmax(C_read)
        if (not np.isfinite(cmin)) or (not np.isfinite(cmax)) or (cmax > 5.0) or (cmin < -50.0):
            if VERBOSE:
                print(f"[get_roms_depths] Cs suspicious (min={cmin}, max={cmax}), recomputing")
            C = _compute_C_from_vstretching(s, theta_s, theta_b, vstretching)
        else:
            C = C_read

    s = np.asarray(s, dtype=np.float64).ravel()
    C = np.asarray(C, dtype=np.float64).ravel()

    # prepare h arr
    h_arr = np.asarray(h, dtype=np.float64).copy()
    h_arr[~np.isfinite(h_arr)] = np.nan
    h_arr[h_arr <= 0] = np.nan

    s3 = s[:, None, None]
    C3 = C[:, None, None]
    h3 = h_arr[None, :, :]

    if zeta.ndim == 3:
        zeta3 = zeta[:, None, :, :]
        if vtransform == 1:
            Zo = hc * s3 + (h3 - hc) * C3
            denom_safe = np.where(np.abs(h3) > eps, h3, np.nan)
            z = Zo[None, ...] + zeta3 * (1.0 + Zo[None, ...] / denom_safe[None, ...])
        else:
            denom_safe = np.where(np.abs(hc + h3) > eps, (hc + h3), np.nan)
            Zo = (hc * s3 + h3 * C3) / denom_safe
            z = zeta3 + (zeta3 + h3[None, ...]) * Zo[None, ...]
        time_dim = 'ocean_time'
    else:
        zeta3 = zeta[None, :, :]
        if vtransform == 1:
            Zo = hc * s3 + (h3 - hc) * C3
            denom_safe = np.where(np.abs(h3) > eps, h3, np.nan)
            z = Zo + zeta3 * (1.0 + Zo / denom_safe)
        else:
            denom_safe = np.where(np.abs(hc + h3) > eps, (hc + h3), np.nan)
            Zo = (hc * s3 + h3 * C3) / denom_safe
            z = zeta3 + (zeta3 + h3) * Zo
        time_dim = None

    # bounds
    if z.ndim == 4:
        zeta_b = zeta3; h_b = h3[None, ...]
    else:
        zeta_b = zeta3; h_b = h3
    z_max_allowed = zeta_b
    z_min_allowed = zeta_b - h_b
    z = np.where((z <= (z_max_allowed + 1e-6)) & (z >= (z_min_allowed - 1e-6)), z, np.nan)
    z = np.where(np.abs(z) >= 2e4, np.nan, z)

    # build DataArray
    if time_dim is not None:
        dims = (time_dim, s_dim, 'eta_rho', 'xi_rho')
        coords = {time_dim: ds['ocean_time'] if 'ocean_time' in ds.coords else np.arange(z.shape[0])}
    else:
        dims = (s_dim, 'eta_rho', 'xi_rho')
        coords = {}
    coords[s_dim] = s
    coords['eta_rho'] = ds['eta_rho'] if 'eta_rho' in ds.coords else np.arange(h_arr.shape[0])
    coords['xi_rho'] = ds['xi_rho'] if 'xi_rho' in ds.coords else np.arange(h_arr.shape[1])

    z_da = xr.DataArray(data=z, dims=dims, coords=coords)
    if VERBOSE:
        try:
            if time_dim is not None:
                zk = z_da.isel({time_dim: 0})
                print(f"[get_roms_depths] sample z min/max (time0): {safe_nanmin(zk.values):.3f}/{safe_nanmax(zk.values):.3f}")
            else:
                print(f"[get_roms_depths] sample z min/max: {safe_nanmin(z):.3f}/{safe_nanmax(z):.3f}")
        except Exception:
            pass
    return z_da


# -------------------------
# vertical interpolation per-column with Fortran endpoint policy
# -------------------------
def vertical_interp_with_endpoints(depths: np.ndarray, data: np.ndarray, target_depth: Sequence[float],
                                   allow_extrapolation: bool = False, cubic_min_points: int = 4) -> np.ndarray:
    """
    Column-wise interpolation similar to Fortran spline+splint behavior:
      - if n_valid >= cubic_min_points: cubic spline; for target outside source range assign endpoint value
      - elif n_valid >=2: linear interpolation; for outside assign endpoint value
      - else: NaN
    depths: (Ns, eta, xi)
    data:   (Ns, eta, xi)
    target_depth: 1D (negative depths)
    """
    depths = np.asarray(depths, dtype=np.float64)
    data = np.asarray(data, dtype=np.float64)
    target_depth = np.asarray(target_depth, dtype=np.float64)
    nt = len(target_depth)
    eta = data.shape[1]
    xi = data.shape[2]
    out = np.full((nt, eta, xi), np.nan, dtype=np.float64)

    # compute h_actual to mask deeper than local depth
    if np.isfinite(depths).any():
        h_actual = np.abs(np.nanmin(depths, axis=0))
    else:
        h_actual = np.zeros((eta, xi), dtype=np.float64)
    h_actual = np.where(np.isfinite(h_actual), h_actual, 0.0)

    for i in range(eta):
        for j in range(xi):
            dcol = depths[:, i, j]
            vcol = data[:, i, j]
            ok = np.isfinite(dcol) & np.isfinite(vcol)
            n_ok = int(ok.sum())
            if n_ok < 2:
                continue
            d_valid = dcol[ok]
            v_valid = vcol[ok]
            # sort ascending depth for interp
            order = np.argsort(d_valid)
            d_valid = d_valid[order]
            v_valid = v_valid[order]
            # unique depths
            d_u, idx = np.unique(d_valid, return_index=True)
            v_u = v_valid[idx]
            if d_u.size < 2:
                continue
            try:
                if d_u.size >= cubic_min_points:
                    cs = CubicSpline(d_u, v_u, extrapolate=False)
                    y = cs(target_depth)
                    # handle endpoints: where target < d_u[0] -> assign v_u[0]; where > d_u[-1] -> v_u[-1]
                    left_mask = target_depth < d_u[0]
                    right_mask = target_depth > d_u[-1]
                    if left_mask.any():
                        y[left_mask] = v_u[0]
                    if right_mask.any():
                        y[right_mask] = v_u[-1]
                    out[:, i, j] = y
                else:
                    f = interp1d(d_u, v_u, bounds_error=False, fill_value=np.nan, assume_sorted=True)
                    y = f(target_depth)
                    # fill outside with endpoints
                    left_mask = target_depth < d_u[0]
                    right_mask = target_depth > d_u[-1]
                    if left_mask.any():
                        y[left_mask] = v_u[0]
                    if right_mask.any():
                        y[right_mask] = v_u[-1]
                    out[:, i, j] = y
            except Exception:
                # fallback linear
                try:
                    f = interp1d(d_u, v_u, bounds_error=False, fill_value=np.nan, assume_sorted=True)
                    y = f(target_depth)
                    left_mask = target_depth < d_u[0]
                    right_mask = target_depth > d_u[-1]
                    if left_mask.any():
                        y[left_mask] = v_u[0]
                    if right_mask.any():
                        y[right_mask] = v_u[-1]
                    out[:, i, j] = y
                except Exception:
                    if VERBOSE_DEBUG:
                        print(f"[vertical_interp] interpolation failed at col {i},{j}")
                    continue
            # ensure target deeper than local bathymetry get NaN
            deeper = np.abs(target_depth) > h_actual[i, j]
            if np.isfinite(h_actual[i, j]) and deeper.any():
                out[deeper, i, j] = np.nan

    if VERBOSE_DEBUG:
        print("[vertical_interp] done; out nan_frac=", np.isnan(out).mean())
    return out


# -------------------------
# xESMF regridder helpers
# -------------------------
def _make_src_dataset_for_grid(ds: xr.Dataset, grid: str) -> xr.Dataset:
    # grid: 'rho','u','v'
    if grid == 'rho':
        lon2, lat2 = ds['lon_rho'].values, ds['lat_rho'].values
        dims = ('eta_rho', 'xi_rho')
    elif grid == 'u':
        lon2, lat2 = ds['lon_u'].values, ds['lat_u'].values
        dims = ('eta_u', 'xi_u')
    elif grid == 'v':
        lon2, lat2 = ds['lon_v'].values, ds['lat_v'].values
        dims = ('eta_v', 'xi_v')
    else:
        raise ValueError("Unknown grid")
    return xr.Dataset({'lon': (dims, lon2), 'lat': (dims, lat2)})


def _make_dst_dataset(target_lon: Sequence[float], target_lat: Sequence[float]) -> xr.Dataset:
    return xr.Dataset({'lon': (('lon',), np.asarray(target_lon, dtype=np.float64)),
                       'lat': (('lat',), np.asarray(target_lat, dtype=np.float64))})


def _make_regridder_safe(src_ds: xr.Dataset, dst_ds: xr.Dataset, method: str, fname: str, periodic: bool, reuse: bool):
    try:
        import xesmf as xe
    except Exception as e:
        raise ImportError("xesmf required. Install: conda install --solver=classic -c conda-forge xesmf esmpy. Error: " + str(e))
    try:
        reb = xe.Regridder(src_ds, dst_ds, method=method, periodic=periodic, filename=fname, reuse_weights=reuse)
    except OSError:
        reb = xe.Regridder(src_ds, dst_ds, method=method, periodic=periodic, reuse_weights=False)
        try:
            reb.to_netcdf(fname)
        except Exception:
            pass
    return reb


# -------------------------
# Main processing function (implements Fortran logic for u/v)
# -------------------------
def process_roms_file(input_nc: str, output_nc: str, varnames: Sequence[str],
                      target_lon: Sequence[float], target_lat: Sequence[float], target_depth: Sequence[float],
                      overwrite_weights: bool = False):
    ds = xr.open_dataset(input_nc, decode_cf=True, mask_and_scale=True)
    times = np.asarray(ds['ocean_time'].values) if 'ocean_time' in ds.dims else np.array([0])

    # dst ds for xESMF
    dst_ds = _make_dst_dataset(target_lon, target_lat)
    periodic = _need_periodic(np.asarray(target_lon))

    # create rho regridder (final remap uses rho grid)
    src_rho = _make_src_dataset_for_grid(ds, 'rho')
    fname_rho = f"weights_bilin_rho_{src_rho['lon'].shape[0]}x{src_rho['lon'].shape[1]}_dst{len(target_lat)}x{len(target_lon)}.nc"
    reb_rho = _make_regridder_safe(src_rho, dst_ds, method='bilinear', fname=fname_rho, periodic=periodic, reuse=not overwrite_weights)
    reb_mask_rho = _make_regridder_safe(src_rho, dst_ds, method='nearest_s2d', fname=fname_rho.replace('.nc', '_mask.nc'), periodic=periodic, reuse=not overwrite_weights)

    interp_results = {}

    for var in varnames:
        if VERBOSE:
            print(f"**[main]** processing {var}")
        
        if var not in ds.variables:
            raise RuntimeError(f"{var} not found in dataset")
        
        is_w_kind = True if 's_w' in ds[var].dims else False
        is_rho_kind = True if 's_rho' in ds[var].dims or 'eta_rho' in ds[var].dims or 'xi_rho' in ds[var].dims else False
        is_u_kind = True if 'eta_u' in ds[var].dims or 'xi_u' in ds[var].dims else False
        is_v_kind = True if 'eta_v' in ds[var].dims or 'xi_v' in ds[var].dims else False

        if is_u_kind:
            u_da = ds[var].astype('f8')
            u_vals = np.where(np.isfinite(u_da.values), u_da.values, np.nan)  # (time, s_rho, eta_u, xi_u)
            # average to rho grid:
            u_rho = avg_to_rho_axis_padboth(u_vals, axis=-1)  # -> shape (time, s, eta_u, xi_u+1) ; eta_u == eta_rho
            eta_rho_len = ds.sizes['eta_rho']; xi_rho_len = ds.sizes['xi_rho']
            if u_rho.shape[-2] != eta_rho_len or u_rho.shape[-1] != xi_rho_len:
                raise RuntimeError(f"u_rho shape mismatch {u_rho.shape[-2:]} vs rho ({eta_rho_len},{xi_rho_len})")
            # 旋转到东向分量（如果有angle）
            angle = ds['angle'].values if 'angle' in ds.variables else np.zeros((eta_rho_len, xi_rho_len))
            nt = u_rho.shape[0]; ns = u_rho.shape[1]
            u_east = np.full_like(u_rho, np.nan)
            for t in range(nt):
                print(f'Processing time step {t+1}/{nt} for variable {var} (u-component)')
                for k in range(ns):
                    print(f'  Processing vertical level {k+1}/{ns} for variable {var} (u-component)')
                    ur = u_rho[t, k, :, :]
                    ang = angle
                    if ang.shape != ur.shape:
                        ang = np.broadcast_to(angle, ur.shape)
                    cosA = np.cos(ang)
                    sinA = np.sin(ang)
                    # 只处理u分量（东向）
                    u_east[t, k, :, :] = ur * cosA
            # vertical interpolation ON SOURCE (rho) grid using z_rho
            if 'z_rho' in ds.variables:
                z_rho_da = ds['z_rho'].astype('f8')
                z_rho = np.where(np.isfinite(z_rho_da.values), z_rho_da.values, np.nan)
            else:
                z_rho = get_roms_depths(ds, is_w=is_w_kind).values
            res_u_time = []
            for t in range(nt):
                print(f'Processing time step {t+1}/{nt} for variable {var} (vertical interpolation)')
                zcol = z_rho[t] if z_rho.ndim == 4 else z_rho
                ue_src = u_east[t]
                ue_vert = vertical_interp_with_endpoints(zcol, ue_src, target_depth)
                levels_u = []
                for k in range(ue_vert.shape[0]):
                    da_u = xr.DataArray(ue_vert[k], dims=('eta_rho', 'xi_rho'),
                                        coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                'lon': (('eta_rho', 'xi_rho'), ds['lon_rho'].values),
                                                'lat': (('eta_rho', 'xi_rho'), ds['lat_rho'].values)})
                    ru = reb_rho(da_u)
                    if 'mask_rho' in ds.variables:
                        da_mask_src = xr.DataArray(ds['mask_rho'].astype(np.float64).values, dims=('eta_rho', 'xi_rho'),
                                                   coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                           'lon': (('eta_rho', 'xi_rho'), ds['lon_rho'].values),
                                                           'lat': (('eta_rho', 'xi_rho'), ds['lat_rho'].values)})
                        mask_dst = reb_mask_rho(da_mask_src)
                        ru = ru.where(mask_dst >= 0.5, np.nan)
                    levels_u.append(ru.values)
                res_u_time.append(np.array(levels_u))
            interp_results[var] = np.array(res_u_time)

        elif is_v_kind:
            v_da = ds[var].astype('f8')
            v_vals = np.where(np.isfinite(v_da.values), v_da.values, np.nan)  # (time, s_rho, eta_v, xi_v)
            v_rho = avg_to_rho_axis_padboth(v_vals, axis=-2)  # -> shape (time, s, eta_v+1, xi_v) ; xi_v == xi_rho
            eta_rho_len = ds.sizes['eta_rho']; xi_rho_len = ds.sizes['xi_rho']
            if v_rho.shape[-2] != eta_rho_len or v_rho.shape[-1] != xi_rho_len:
                raise RuntimeError(f"v_rho shape mismatch {v_rho.shape[-2:]} vs rho ({eta_rho_len},{xi_rho_len})")
            # 旋转到北向分量（如果有angle）
            angle = ds['angle'].values if 'angle' in ds.variables else np.zeros((eta_rho_len, xi_rho_len))
            nt = v_rho.shape[0]; ns = v_rho.shape[1]
            v_north = np.full_like(v_rho, np.nan)
            for t in range(nt):
                print(f'Processing time step {t+1}/{nt} for variable {var} (v-component)')
                for k in range(ns):
                    print(f'  Processing vertical level {k+1}/{ns} for variable {var} (v-component)')
                    vr = v_rho[t, k, :, :]
                    ang = angle
                    if ang.shape != vr.shape:
                        ang = np.broadcast_to(angle, vr.shape)
                    cosA = np.cos(ang)
                    sinA = np.sin(ang)
                    # 只处理v分量（北向）
                    v_north[t, k, :, :] = vr * cosA
            if 'z_rho' in ds.variables:
                z_rho_da = ds['z_rho'].astype('f8')
                z_rho = np.where(np.isfinite(z_rho_da.values), z_rho_da.values, np.nan)
            else:
                z_rho = get_roms_depths(ds, is_w=is_w_kind).values
            res_v_time = []
            for t in range(nt):
                print(f'Processing time step {t+1}/{nt} for variable {var} (vertical interpolation)')
                zcol = z_rho[t] if z_rho.ndim == 4 else z_rho
                vn_src = v_north[t]
                vn_vert = vertical_interp_with_endpoints(zcol, vn_src, target_depth)
                levels_v = []
                for k in range(vn_vert.shape[0]):
                    da_v = xr.DataArray(vn_vert[k], dims=('eta_rho', 'xi_rho'),
                                        coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                'lon': (('eta_rho', 'xi_rho'), ds['lon_rho'].values),
                                                'lat': (('eta_rho', 'xi_rho'), ds['lat_rho'].values)})
                    rv = reb_rho(da_v)
                    if 'mask_rho' in ds.variables:
                        da_mask_src = xr.DataArray(ds['mask_rho'].astype(np.float64).values, dims=('eta_rho', 'xi_rho'),
                                                   coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                           'lon': (('eta_rho', 'xi_rho'), ds['lon_rho'].values),
                                                           'lat': (('eta_rho', 'xi_rho'), ds['lat_rho'].values)})
                        mask_dst = reb_mask_rho(da_mask_src)
                        rv = rv.where(mask_dst >= 0.5, np.nan)
                    levels_v.append(rv.values)
                res_v_time.append(np.array(levels_v))
            interp_results[var] = np.array(res_v_time)
            
        elif is_rho_kind:
            # scalar processing: temp/salt/zeta (vertical-first -> horizontal remap)
            da = ds[var].astype('f8')
            vals = np.where(np.isfinite(da.values), da.values, np.nan)
            if da.ndim == 4:
                nt = vals.shape[0]
                out_time = []
                for t in range(nt):
                    print(f'Processing time step {t+1}/{nt} for variable {var} (vertical interpolation)')
                    src = vals[t]
                    if is_w_kind and 'z_w' in ds.variables:
                        zsrc = np.where(np.isfinite(ds['z_w'].values), ds['z_w'].values, np.nan)
                        zcol = zsrc[t] if zsrc.ndim == 4 else zsrc
                    elif not is_w_kind and 'z_rho' in ds.variables:
                        zsrc = np.where(np.isfinite(ds['z_rho'].values), ds['z_rho'].values, np.nan)
                        zcol = zsrc[t] if zsrc.ndim == 4 else zsrc
                    else:
                        zcol = get_roms_depths(ds, is_w=is_w_kind, time_index=t).values
                    vert = vertical_interp_with_endpoints(zcol, src, target_depth)
                    levels = []
                    for k in range(vert.shape[0]):
                        print(f'  Processing vertical level {k+1}/{vert.shape[0]} for variable {var} (vertical interpolation)')
                        da_l = xr.DataArray(vert[k], dims=('eta_rho', 'xi_rho'),
                                            coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                    'lon': (('eta_rho', 'xi_rho'), ds['lon_rho'].values),
                                                    'lat': (('eta_rho', 'xi_rho'), ds['lat_rho'].values)})
                        rt = reb_rho(da_l)
                        if 'mask_rho' in ds.variables:
                            da_mask_src = xr.DataArray(ds['mask_rho'].astype(np.float64).values, dims=('eta_rho','xi_rho'),
                                                       coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                               'lon': (('eta_rho','xi_rho'), ds['lon_rho'].values),
                                                               'lat': (('eta_rho','xi_rho'), ds['lat_rho'].values)})
                            mask_dst = reb_mask_rho(da_mask_src)
                            rt = rt.where(mask_dst >= 0.5, np.nan)
                        levels.append(rt.values)
                    out_time.append(np.array(levels))
                interp_results[var] = np.array(out_time)
            elif da.ndim == 3:
                nt = vals.shape[0]
                out = []
                for t in range(nt):
                    print(f'Processing time step {t+1}/{nt} for variable {var} (horizontal remap)')
                    da_l = xr.DataArray(vals[t], dims=('eta_rho', 'xi_rho'),
                                        coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                'lon': (('eta_rho','xi_rho'), ds['lon_rho'].values),
                                                'lat': (('eta_rho','xi_rho'), ds['lat_rho'].values)})
                    rt = reb_rho(da_l)
                    if 'mask_rho' in ds.variables:
                        da_mask_src = xr.DataArray(ds['mask_rho'].astype(np.float64).values, dims=('eta_rho','xi_rho'),
                                                   coords={'eta_rho': ds['eta_rho'], 'xi_rho': ds['xi_rho'],
                                                           'lon': (('eta_rho','xi_rho'), ds['lon_rho'].values),
                                                           'lat': (('eta_rho','xi_rho'), ds['lat_rho'].values)})
                        mask_dst = reb_mask_rho(da_mask_src)
                        rt = rt.where(mask_dst >= 0.5, np.nan)
                    out.append(rt.values)
                interp_results[var] = np.array(out)
            else:
                raise ValueError(f"Unsupported variable dims for {var}")
        else:
            raise ValueError(f"Unknown grid type for variable {var}")

    # write netcdf output - simple writer for (time,depth,lat,lon) or (time,lat,lon)
    times_out = times
    data_vars = {}
    coords = {'time': ('time', times_out), 'lat': ('lat', target_lat), 'lon': ('lon', target_lon)}
    if target_depth is not None:
        coords['depth'] = ('depth', target_depth)

    for vname, arr in interp_results.items():
        a = np.asarray(arr)
        if a.ndim == 4:
            data_vars[vname] = (('time', 'depth', 'lat', 'lon'), a)
        elif a.ndim == 3:
            data_vars[vname] = (('time', 'lat', 'lon'), a)
        else:
            raise ValueError(f"Unexpected ndim for output {vname}: {a.ndim}")

    ds_out = xr.Dataset(data_vars=data_vars, coords=coords)
    encoding = {name: {'zlib': True, 'complevel': 4} for name in data_vars.keys()}
    ds_out.to_netcdf(output_nc, encoding=encoding)
    if VERBOSE:
        print(f"[main] wrote {output_nc} variables: {list(data_vars.keys())}")


# -------------------------
# __main__ example
# -------------------------
if __name__ == "__main__":
    input_nc = "./2024090100/nwa_his_0001.nc"
    output_nc = "roms_interp.nc"
    varnames = ['temp', 'zeta', 'w', 'u', 'v', 'salt']
    target_lon = np.linspace(108, 140, 641)
    target_lat = np.linspace(15, 40, 501)
    target_depth = [-5, -10, -20, -30, -50, -75, -100, -125, -150, -200,
                    -250, -300, -400, -500, -600, -700, -800, -900, -1000]
    process_roms_file(input_nc, output_nc, varnames, target_lon, target_lat, target_depth, overwrite_weights=False)