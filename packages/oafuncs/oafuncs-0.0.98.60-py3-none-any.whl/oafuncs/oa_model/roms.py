from typing import Sequence

__all__ = ['interp']


def interp(input_nc: str, output_nc: str, varnames: Sequence[str],
                      target_lon: Sequence[float], target_lat: Sequence[float], target_depth: Sequence[float],
                      overwrite_weights: bool = False):
    """
    Perform vertical interpolation and horizontal remapping of ROMS model data.
    
    Parameters
    ----------
    input_nc : str
        Path to the input ROMS NetCDF file.
    output_nc : str
        Path to the output NetCDF file.
    varnames : Sequence[str]
        List of variable names to process.
    target_lon : Sequence[float]
        Target longitudes for horizontal remapping.
    target_lat : Sequence[float]
        Target latitudes for horizontal remapping.
    target_depth : Sequence[float]
        Target depths for vertical interpolation. Should be negative values (e.g., -5 for 5m depth).
    overwrite_weights : bool, optional
        Whether to overwrite existing regridding weights files. Default is False.
    
    Examples
    --------
    input_nc = "./2024090100/nwa_his_0001.nc"
    output_nc = "roms_interp.nc"
    varnames = ['temp', 'zeta', 'w', 'u', 'v', 'salt']
    target_lon = np.linspace(108, 140, 641)
    target_lat = np.linspace(15, 40, 501)
    target_depth = [-5, -10, -20, -30, -50, -75, -100, -125, -150, -200,
                    -250, -300, -400, -500, -600, -700, -800, -900, -1000]
    """
    
    from oafuncs._script.process_roms import process_roms_file
    process_roms_file(input_nc, output_nc, varnames, target_lon, target_lat, target_depth,
                      overwrite_weights=overwrite_weights)