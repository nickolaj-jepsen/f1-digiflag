import time


def is_on(hz):
    return time.ticks_ms() % (1000 // hz) < (500 // hz)
