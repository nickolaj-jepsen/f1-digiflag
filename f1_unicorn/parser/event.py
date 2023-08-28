import struct

event_format = "<4s"
event_size = struct.calcsize(event_format)

start_light_event_format = "<B"
start_light_event_size = struct.calcsize(start_light_event_format)


def event_type(data):
    return struct.unpack(event_format, data[:event_size])[0].decode("utf-8")


def start_light_event(data):
    return struct.unpack(
        start_light_event_format, data[event_size : event_size + start_light_event_size]
    )[0]
