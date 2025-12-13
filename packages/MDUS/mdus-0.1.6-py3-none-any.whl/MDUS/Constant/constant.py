import numpy as np

# Radius of Mercury
Rm = 2439.7 # km
# velocity of solar wind
vsw = 400 # km/s
# semi-major axis of Mercury
smaxis = 57.91e6 #km
# gravitational constant
G = 6.67430e-11 # m^3/kg/s^2
# mass of Mercury
M = 1.989e30 # kg
# astronomical unit
au = 149597870.7 # km
# Jule of 1 eV[J/eV]
ev = 1.6e-19
# mass of proton
mass = 1.67e-27
# conversion constant [1/e]
C = 1.6022e-20 # 変換定数[1/e]
# 立体角，1.15piかも
omega = 4*np.pi
# magic number
magicnumber_p = 1e-1
magicnumber_t = 2
# boltzman constant [m^2*kg*s^-2*K^-1]
kb = 1.38e-23
# magnetic constant
mu0 = 1.26e-6
# EQTAB
EQTAB = np.array([ 0.0464,  0.0511,  0.0564,  0.062 ,  0.0683,  0.0754, 0.0829,
         0.0913,  0.1004,  0.1107,  0.1219,  0.134 ,  0.1478, 0.1627,
         0.1789,  0.197 ,  0.217 ,  0.2388,  0.2631,  0.2896, 0.3189,
         0.351 ,  0.3863,  0.4255,  0.4682,  0.5156,  0.5677, 0.6251,
         0.688 ,  0.7576,  0.8343,  0.9184,  1.011 ,  1.1133, 1.2255,
         1.3493,  1.4855,  1.6358,  1.8007,  1.9828,  2.183 , 2.4034,
         2.6459,  2.9131,  3.2074,  3.531 ,  3.8877,  4.2802, 4.7126,
         5.1884,  5.7121,  6.2892,  6.9243,  7.6233,  8.393 , 9.2407,
        10.1738, 11.2011, 12.3322, 13.5774, 14.9482, 16.4578, 18.1198,
        19.9492])