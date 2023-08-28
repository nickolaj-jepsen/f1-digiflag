from collections import namedtuple
import struct

Participant = namedtuple(
    "Participant",
    "m_aiControlled m_driverId m_networkId m_teamId m_myTeam m_raceNumber m_nationality m_name m_yourTelemetry m_showOnlineNames m_platform",
)

participant_format = "<BBBBBBB48sBBB"
participant_size = struct.calcsize(participant_format)


def build_participant(data, index):
    # skip first byte
    data = data[1:]
    return Participant(
        *struct.unpack(
            participant_format,
            data[participant_size * index : participant_size * (index + 1)],
        )
    )
