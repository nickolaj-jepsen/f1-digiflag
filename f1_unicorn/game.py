import socket
import time

from f1_unicorn.parser.event import event_type, start_light_event
from f1_unicorn.parser.participant import build_participant
from f1_unicorn.parser.header import build_header
from f1_unicorn.parser.lap import build_lap_data
from f1_unicorn.parser.session import build_session
from f1_unicorn.parser.car import build_car
from f1_unicorn.udp import open_connection


HEADER_LENGTH = 29
LARGEST_PACKET_SIZE = 1460


async def connect(result):
    connection = open_connection()

    session = None
    lap = None
    car = None
    participant = None
    start_light = 0
    start_light_time = 0

    red_flag_time = 0
    chequered_flag_time = 0
    connection = open_connection()
    while True:
        data = await connection.read(2048)

        header = build_header(data)

        if header.m_packetId == 1:
            session = build_session(data[29:])

        if header.m_packetId == 2:
            lap = build_lap_data(data[29:])

        if header.m_packetId == 3:
            event = event_type(data[29:])

            if event == "STLG":
                start_light = start_light_event(data[29:])
                start_light_time = time.ticks_ms()
            elif event == "LGOT":
                start_light_time = 0
            elif event == "RDFL":
                red_flag_time = time.ticks_ms()
            elif event == "CHQF":
                chequered_flag_time = time.ticks_ms()

        if header.m_packetId == 4:
            participant = build_participant(data[29:], header.m_playerCarIndex)

        if header.m_packetId == 7:
            car = build_car(data[29:], header.m_playerCarIndex)

        if session and lap:
            active_flag = car.m_vehicleFiaFlags if car else 0
            safety_car = session.m_safetyCarStatus
            player_number = str(participant.m_raceNumber) if participant else "00"

            if (time.ticks_ms() - red_flag_time) < 10000:
                result["flag"] = "red_flag"
            elif (time.ticks_ms() - chequered_flag_time) < 10000:
                result["flag"] = "chequered_flag"
            elif safety_car == 1:
                result["flag"] = "safety_car"
            elif safety_car == 2:
                result["flag"] = "virtual_safety_car"
            elif active_flag == 3:
                result["flag"] = "yellow_flag"
            elif active_flag == 2:
                result["flag"] = "blue_flag"
                result["flag_extra"] = {"number": player_number}
            elif active_flag == 1:
                result["flag"] = "green_flag"
            elif (time.ticks_ms() - start_light_time) < 10000:
                result["flag"] = "lights_out"
                result["flag_extra"] = {"count": start_light}
            else:
                result["flag"] = None


async def connect_sync(result):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(("", 20777))

    session = None
    lap = None
    car = None
    participant = None
    start_light = 0
    start_light_time = 0

    red_flag_time = 0
    chequered_flag_time = 0
    while True:
        data, addr = client.recvfrom(2048)

        header = build_header(data)

        if header.m_packetId == 1:
            session = build_session(data[29:])

        if header.m_packetId == 2:
            lap = build_lap_data(data[29:])

        if header.m_packetId == 3:
            event = event_type(data[29:])

            if event == "STLG":
                start_light = start_light_event(data[29:])
                start_light_time = time.ticks_ms()
            elif event == "LGOT":
                start_light_time = 0
            elif event == "RDFL":
                red_flag_time = time.ticks_ms()
            elif event == "CHQF":
                chequered_flag_time = time.ticks_ms()

        if header.m_packetId == 4:
            participant = build_participant(data[29:], header.m_playerCarIndex)

        if header.m_packetId == 7:
            car = build_car(data[29:], header.m_playerCarIndex)

        if session and lap:
            active_flag = car.m_vehicleFiaFlags if car else 0
            safety_car = session.m_safetyCarStatus
            player_number = str(participant.m_raceNumber) if participant else "00"

            if (time.ticks_ms() - red_flag_time) < 10000:
                result["flag"] = "red_flag"
            elif (time.ticks_ms() - chequered_flag_time) < 10000:
                result["flag"] = "chequered_flag"
            elif safety_car == 1:
                result["flag"] = "safety_car"
            elif safety_car == 2:
                result["flag"] = "virtual_safety_car"
            elif active_flag == 3:
                result["flag"] = "yellow_flag"
            elif active_flag == 2:
                result["flag"] = "blue_flag"
                result["flag_extra"] = {"number": player_number}
            elif active_flag == 1:
                result["flag"] = "green_flag"
            elif (time.ticks_ms() - start_light_time) < 10000:
                result["flag"] = "lights_out"
                result["flag_extra"] = {"count": start_light}
            else:
                result["flag"] = None
