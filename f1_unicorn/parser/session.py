from collections import namedtuple
import struct

MarshalZone = namedtuple("MarshalZone", "m_zoneStart m_zoneFlag")
WeatherForecastSample = namedtuple(
    "WeatherForecastSample",
    "m_sessionType m_timeOffset m_weather m_trackTemperature m_trackTemperatureChange m_airTemperature m_airTemperatureChange m_rainPercentage",
)
Session = namedtuple(
    "Session",
    "m_weather m_trackTemperature m_airTemperature m_totalLaps m_trackLength m_sessionType m_trackId m_formula m_sessionTimeLeft m_sessionDuration m_pitSpeedLimit m_gamePaused m_isSpectating m_spectatorCarIndex m_sliProNativeSupport m_numMarshalZones m_marshalZones m_safetyCarStatus m_networkGame m_numWeatherForecastSamples m_weatherForecastSamples m_forecastAccuracy m_aiDifficulty m_seasonLinkIdentifier m_weekendLinkIdentifier m_sessionLinkIdentifier m_pitStopWindowIdealLap m_pitStopWindowLatestLap m_pitStopRejoinPosition m_steeringAssist m_brakingAssist m_gearboxAssist m_pitAssist m_pitReleaseAssist m_ERSAssist m_DRSAssist m_dynamicRacingLine m_dynamicRacingLineType m_gameMode m_ruleSet m_timeOfDay m_sessionLength m_speedUnitsLeadPlayer m_temperatureUnitsLeadPlayer m_speedUnitsSecondaryPlayer m_temperatureUnitsSecondaryPlayer m_numSafetyCarPeriods m_numVirtualSafetyCarPeriods m_numRedFlagPeriods",
)

part1 = "<BbbBHBbBHHBBBBBB"
marshals = "<fb"
part2 = "<BBB"
weather = "<BBBbbbbB"
part3 = "<BBLLLBBBBBBBBBBBBBBLBBBBBBBB"

part1_size = struct.calcsize(part1)
marshals_size = struct.calcsize(marshals)
part2_size = struct.calcsize(part2)
weather_size = struct.calcsize(weather)
part3_size = struct.calcsize(part3)

marshal_amount = 21
weather_forecast_sample_amount = 56


def build_session(data):
    # Builds session data from the given data

    # Part 1
    part1_data = data[:part1_size]
    data = data[part1_size:]
    part1_values = struct.unpack(part1, part1_data)

    # Marshal zones
    marshal_zones = []
    for i in range(marshal_amount):
        marshal_data = data[:marshals_size]
        data = data[marshals_size:]
        marshal_values = struct.unpack(marshals, marshal_data)
        marshal_zones.append(MarshalZone(*marshal_values))

    # Part 2
    part2_data = data[:part2_size]
    data = data[part2_size:]
    part2_values = struct.unpack(part2, part2_data)

    # Weather forecast samples
    weather_forecast_samples = []
    for i in range(weather_forecast_sample_amount):
        weather_data = data[:weather_size]
        data = data[weather_size:]
        weather_values = struct.unpack(weather, weather_data)
        weather_forecast_samples.append(WeatherForecastSample(*weather_values))

    # Part 3
    part3_data = data[:part3_size]
    data = data[part3_size:]
    part3_values = struct.unpack(part3, part3_data)

    res = (
        list(part1_values)
        + [marshal_zones]
        + list(part2_values)
        + [weather_forecast_samples]
        + list(part3_values)
    )

    return Session(*res)
