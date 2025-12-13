import win32com.client
import datetime

# Get reference to running STK instance
uiApplication = win32com.client.Dispatch('STK11.Application')
uiApplication.Visible = True

# Get our IAgStkObjectRoot interface
root = uiApplication.Personality2



# 选择卫星
def sat_propagate(name: str, orbit_epoch: datetime.datetime, orbit_rv_fix_m: list):
    satellite = root.CurrentScenario.Children.new(18, name)  # eSatellite

    # 设置递推类型 HPOP
    satellite.SetPropagatorType(0) # 0: ePropagatorHPOP
    print(satellite.PropagatorSupportedTypes)
    print(satellite.PropagatorType)

    # 设置 HPOP 摄动力
    forceModel = satellite.Propagator.ForceModel
    forceModel.CentralBodyGravity.File = r'C:\Program Files\AGI\STK 11\STKData\CentralBodies\Earth\WGS84_EGM96.grv'
    forceModel.CentralBodyGravity.MaxDegree = 21
    forceModel.CentralBodyGravity.MaxOrder = 21
    forceModel.Drag.Use=0
    forceModel.SolarRadiationPressure.Use=0

    # 设置递推初始时间与rv
    satellite.Propagator.InitialState.OrbitEpoch.SetExplicitTime(
        orbit_epoch.strftime('%d %b %Y %H:%M:%S.%f'))
    
    orbit_rv_fix_km = [x/1e3 for x in orbit_rv_fix_m] # 单位转换
    satellite.Propagator.InitialState.Representation.AssignCartesian(
        2, 
        orbit_rv_fix_km[0], 
        orbit_rv_fix_km[1], 
        orbit_rv_fix_km[2], 
        orbit_rv_fix_km[3], 
        orbit_rv_fix_km[4], 
        orbit_rv_fix_km[5])  # 2: eCoordinateSystemFixed

    # 递推计算
    satellite.Propagator.Propagate()

    return satellite


# Get reference to running STK instance
uiApplication = win32com.client.Dispatch('STK11.Application')
uiApplication.Visible = True

# Get our IAgStkObjectRoot interface
root = uiApplication.Personality2


GNSS_A_data = [
    1728863912,
    799616.31,
    3015870.75,
    6147789.00,
    675.43,
    -6897.96,
    3288.37]

GNSS_B_data = [
    1728863903,
    793314.56,
    3077794.00,
    6117463.00,
    693.34,
    -6864.36,
    3355.6]

GNSS_C_data = [
    1728863919,
    804203.00,
    2968066.75,
    6170752.50,
    661.47,
    -6923.44,
    3236.07
]

GNSS_D_data = [
    1728863913,
    800546.13,
    3008147.75,
    6151491.00,
    673.33,
    -6901.90,
    3280.39,
]

satellite_A = sat_propagate('A', datetime.datetime.fromtimestamp(GNSS_A_data[0] - 8*3600), GNSS_A_data[1:])
satellite_B = sat_propagate('B', datetime.datetime.fromtimestamp(GNSS_B_data[0] - 8*3600), GNSS_B_data[1:])
satellite_C = sat_propagate('C', datetime.datetime.fromtimestamp(GNSS_C_data[0] - 8*3600), GNSS_C_data[1:])
satellite_D = sat_propagate('D', datetime.datetime.fromtimestamp(GNSS_D_data[0] - 8*3600), GNSS_D_data[1:])

