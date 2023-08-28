from collections import namedtuple
import struct

Header = namedtuple(
    "Header",
    "m_packetFormat m_gameYear m_gameMajorVersion m_gameMinorVersion m_packetVersion m_packetId m_sessionUID m_sessionTime m_frameIdentifier m_overallFrameIdentifier m_playerCarIndex m_secondaryPlayerCarIndex",
)


def build_header(data):
    return Header(*struct.unpack("<HBBBBBQfLLBB", data[:29]))
