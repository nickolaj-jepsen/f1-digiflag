from collections import namedtuple
import struct

Lap = namedtuple(
    "Lap",
    "m_lastLapTimeInMS m_currentLapTimeInMS m_sector1TimeInMS m_sector1TimeMinutes m_sector2TimeInMS m_sector2TimeMinutes m_deltaToCarInFrontInMS m_deltaToRaceLeaderInMS m_lapDistance m_totalDistance m_safetyCarDelta m_carPosition m_currentLapNum m_pitStatus m_numPitStops m_sector m_currentLapInvalid m_penalties m_totalWarnings m_cornerCuttingWarnings m_numUnservedDriveThroughPens m_numUnservedStopGoPens m_gridPosition m_driverStatus m_resultStatus m_pitLaneTimerActive m_pitLaneTimeInLaneInMS m_pitStopTimerInMS m_pitStopShouldServePen",
)
LapData = namedtuple("LapData", "m_lapData m_timeTrialPBCarIdx m_timeTrialRivalCarIdx")

lap_format = "<LLHBHBHHfffBBBBBBBBBBBBBBBHHB"
lap_size = struct.calcsize(lap_format)

lap_data_format = "<BB"
lap_data_size = struct.calcsize(lap_data_format)

lap_data_amount = 22


def build_lap_data(data):
    # Builds lap data from the given data

    # Lap data
    lap_data = []
    for i in range(lap_data_amount):
        lap_data_data = data[:lap_size]
        data = data[lap_size:]
        lap_data_values = struct.unpack(lap_format, lap_data_data)
        lap_data.append(Lap(*lap_data_values))

    # Time trial data
    time_trial_data = data[:lap_data_size]
    data = data[lap_data_size:]
    time_trial_data_values = struct.unpack(lap_data_format, time_trial_data)

    return LapData(lap_data, *time_trial_data_values)
