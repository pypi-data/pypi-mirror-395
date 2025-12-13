from scipy import interpolate
from . import igrf_utils as iut
import os, sys

def get_mag_field(date: float, lon: float, lat: float, alt: float):
    """
        Compute the magnetic filed of given location, use igrf-14.

        Parameters
        ----------
        date: decimal date in years 1900-2030
        alt: altitude in km
        lat, lon: latitude & longitude in decimal degrees

        alt, lat, lon in geodetic (shape of Earth using the WGS-84 ellipsoid)

        Returns
        -------
        list [x, y, z]
        X: north component : nT
        Y: east component : nT
        Z: vertical component : nT
    """

    # Load in the file of coefficients
    IGRF_FILE = r'SHC_files/IGRF' + '14' + '.SHC'
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), IGRF_FILE))
    print(dir)

    igrf = iut.load_shcfile(dir, None)
    
    colat = 90-lat
    alt, colat, sd, cd = iut.gg_to_geo(alt, colat)

    # Interpolate the geomagnetic coefficients to the desired date(s)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    f = interpolate.interp1d(igrf.time, igrf.coeffs, fill_value='extrapolate')
    coeffs = f(date)    
    
    # Compute the main field B_r, B_theta and B_phi value for the location(s) 
    Br, Bt, Bp = iut.synth_values(coeffs.T, alt, colat, lon,
                              igrf.parameters['nmax'])

    # Rearrange to X, Y, Z components 
    X = -Bt; Y = Bp; Z = -Br

    # Rotate back to geodetic coords if needed
    t = X; X = X*cd + Z*sd;  Z = Z*cd - t*sd
        
    # Compute the four non-linear components 
    dec, hoz, inc, eff = iut.xyz2dhif(X,Y,Z)

    return [X,Y,Z]


if __name__ == '__main__':
    mag = get_mag_field(2024.9, 45, 45, 10)
    print(mag)

    # Geomagnetic field values at:  45.0° / 45.0°, at altitude 10.0 for 2024.9 using IGRF-14
    # Declination (D):  8.110 °
    # Inclination (I):  64.038 °
    # Horizontal intensity (H):  22327.7 nT
    # Total intensity (F)     :  51003.3 nT
    # North component (X)     :  22104.4 nT
    # East component (Y)      :  3149.8 nT
    # Vertical component (Z)  :  45856.4 nT
    # Declination SV (D):  2.51 arcmin/yr
    # Inclination SV (I):  1.69 arcmin/yr
    # Horizontal SV (H):  5.2 nT/yr
    # Total SV (F)     :  62.7 nT/yr
    # North SV (X)     :  2.9 nT/yr
    # East SV (Y)      :  16.9 nT/yr
    # Vertical SV (Z)  :  67.2 nT/yr
