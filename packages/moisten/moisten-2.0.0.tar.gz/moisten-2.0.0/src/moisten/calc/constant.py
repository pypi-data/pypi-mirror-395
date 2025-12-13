"""
物理常量

Physical Constants
"""
import numpy as np

# 地球形状参数，来自于 WGS-84 https://en.wikipedia.org/wiki/World_Geodetic_System

EARTH_MAJOR_AXIS = 6378137.0
"""地球长半轴(m)"""

EARTH_MINOR_AXIS = 6356752.314245
"""地球短半轴(m)"""

EARTH_RADIUS = EARTH_MAJOR_AXIS
"""地球半径（长半轴）(m)"""

EARTH_INVERSE_FLATTENING = 298.257223563
"""地球扁率倒数"""

EARTH_FLATTENING = 1 / EARTH_INVERSE_FLATTENING
"""地球扁率"""

# 地球物理常量
EARTH_GRAVITY = 9.80665
"""标准重力加速度(m/s^2) https://en.wikipedia.org/wiki/Gravity_of_Earth"""

SOLAR_DAY = 86400
"""太阳日(s)"""

SIDEREAL_DAY = 86164.0905
"""恒星日(s) https://en.wikipedia.org/wiki/Sidereal_time"""

EARTH_ROTATION_ANGULAR_VELOCITY = 2 * np.pi / SIDEREAL_DAY
"""地球自转角速度 Omega (rad/s)"""

ROSSBY_PARAMETER_ON_EQUATOR = 2 * EARTH_ROTATION_ANGULAR_VELOCITY / EARTH_RADIUS
"""赤道上的罗斯贝参数 (1/(m·s))"""

EARTH_EQUATOR_LENGTH = 2 * np.pi * EARTH_RADIUS
"""地球赤道长度(m)"""

LENGTH_PRE_LATITUDE = EARTH_EQUATOR_LENGTH / 360
"""一度纬度的长度(m)"""