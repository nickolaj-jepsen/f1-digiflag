import time
from f1_unicorn.render import (
    render_blank,
    render_yellow_flag,
    render_green_flag,
    render_blue_flag,
    render_red_flag,
    render_safety_car,
    render_virtual_safety_car,
    render_lights_out,
    render_chequered_flag,
)


def demo_page(graphics, state):
    tick = time.ticks_ms()

    # each of the 7 variant should last 5 seconds, with one second of black in between
    variant = (tick // 6000) % 9

    if variant == 0:
        return render_yellow_flag(graphics)
    elif variant == 1:
        return render_safety_car(graphics)
    elif variant == 2:
        return render_virtual_safety_car(graphics)
    elif variant == 3:
        return render_red_flag(graphics)
    elif variant == 4:
        return render_blue_flag(graphics, "99")
    elif variant == 5:
        return render_green_flag(graphics)
    elif variant == 6:
        return render_lights_out(graphics, ((tick // 1000) % 6) + 1)
    elif variant == 7:
        return render_chequered_flag(graphics)
    elif variant == 8:
        return render_blank(graphics)
