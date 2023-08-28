import socket
import time

from f1_unicorn.parser.event import event_type, start_light_event
from f1_unicorn.parser.participant import build_participant
from f1_unicorn.parser.header import build_header
from f1_unicorn.parser.lap import build_lap_data
from f1_unicorn.parser.session import build_session
from f1_unicorn.parser.car import build_car
from f1_unicorn.render import (
    render_blank,
    render_yellow_flag,
    render_green_flag,
    render_blue_flag,
    render_red_flag,
    render_safety_car,
    render_virtual_safety_car,
    render_chequered_flag,
    render_lights_out,
    render_waiting,
)


def legacy(graphics, state, update):
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
    update(render_waiting(graphics))

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

            if time.ticks_ms() - red_flag_time < 10000:
                update(render_red_flag(graphics))
            elif time.ticks_ms() - chequered_flag_time < 10000:
                update(render_chequered_flag(graphics))
            elif safety_car == 1:
                update(render_safety_car(graphics))
            elif safety_car == 2:
                update(render_virtual_safety_car(graphics))
            elif active_flag == 3:
                update(render_yellow_flag(graphics))
            elif active_flag == 2:
                update(render_blue_flag(graphics, player_number))
            elif active_flag == 1:
                update(render_green_flag(graphics))
            elif time.ticks_ms() - start_light_time < 10000:
                update(render_lights_out(graphics, start_light))
            else:
                update(render_blank(graphics))
