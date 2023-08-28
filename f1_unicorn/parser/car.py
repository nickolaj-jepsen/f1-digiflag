from collections import namedtuple
import struct

Car = namedtuple(
    "Car",
    "m_tractionControl m_antiLockBrakes m_fuelMix m_frontBrakeBias m_pitLimiterStatus m_fuelInTank m_fuelCapacity m_fuelRemainingLaps m_maxRPM m_idleRPM m_maxGears m_drsAllowed m_drsActivationDistance m_actualTyreCompound m_visualTyreCompound m_tyresAgeLaps m_vehicleFiaFlags m_enginePowerICE m_enginePowerMGUK m_ersStoreEnergy m_ersDeployMode m_ersHarvestedThisLapMGUK m_ersHarvestedThisLapMGUH m_ersDeployedThisLap m_networkPaused",
)

car_format = "<BBBBBfffHHBBHBBBbfffBfffB"
car_size = struct.calcsize(car_format)


def build_car(data, index):
    return Car(
        *struct.unpack(car_format, data[car_size * index : car_size * (index + 1)])
    )
