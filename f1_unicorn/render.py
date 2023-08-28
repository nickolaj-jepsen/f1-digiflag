from f1_unicorn.color import BLACK, WHITE, YELLOW, GREEN, RED, BLUE
from f1_unicorn.util import is_on


def render_blank(graphics):
    graphics.set_pen(BLACK)
    graphics.rectangle(0, 0, 32, 32)
    return graphics


def render_waiting(graphics):
    graphics.set_pen(BLACK)
    graphics.rectangle(0, 0, 32, 32)
    graphics.set_pen(WHITE)
    return _render_centered_text(graphics, "??")


def render_yellow_flag(graphics):
    on = is_on(2)
    if on:
        graphics.set_pen(YELLOW)
    else:
        graphics.set_pen(BLACK)
    graphics.rectangle(0, 0, 32, 32)
    return graphics


def render_double_yellow(graphics):
    on = is_on(2)
    graphics.set_pen(BLACK)
    graphics.rectangle(0, 0, 32, 32)
    graphics.set_pen(YELLOW)
    if on:
        graphics.triangle(0, 0, 32, 0, 0, 32)
    else:
        graphics.triangle(32, 0, 32, 32, 0, 32)
    return graphics


def render_green_flag(graphics):
    graphics.set_pen(GREEN)
    graphics.rectangle(0, 0, 32, 32)
    return graphics


def render_blue_flag(graphics, number: str):
    if is_on(1):
        _render_frame(graphics, BLUE)
    else:
        graphics.set_pen(BLACK)
        graphics.rectangle(0, 0, 32, 32)

    graphics.set_pen(WHITE)
    _render_centered_text(graphics, number, spacing=1)

    return graphics


def render_red_flag(graphics):
    graphics.set_pen(RED)
    graphics.rectangle(0, 0, 32, 32)
    return graphics


def _render_frame(graphics, color):
    graphics.set_pen(color)
    graphics.rectangle(0, 0, 32, 32)

    graphics.set_pen(BLACK)
    graphics.rectangle(3, 3, 26, 26)

    graphics.set_pen(color)
    graphics.triangle(2, 2, 2, 6, 6, 2)
    graphics.triangle(30, 2, 24, 2, 29, 7)
    graphics.triangle(2, 30, 2, 25, 6, 29)
    graphics.triangle(30, 30, 30, 23, 25, 28)
    return graphics


def _render_centered_text(graphics, text, spacing=1):
    graphics.set_font("bitmap8")
    width = graphics.measure_text(text, spacing=spacing)
    graphics.text(text, 16 - (width // 2) + 1, 9, spacing=spacing)
    return graphics


def render_safety_car(graphics):
    if is_on(1):
        graphics = _render_frame(graphics, YELLOW)
    else:
        graphics.set_pen(BLACK)
        graphics.rectangle(0, 0, 32, 32)

    graphics.set_pen(WHITE)
    return _render_centered_text(graphics, "SC", spacing=1)


def render_virtual_safety_car(graphics):
    if is_on(1):
        graphics = _render_frame(graphics, YELLOW)
    else:
        graphics.set_pen(BLACK)
        graphics.rectangle(0, 0, 32, 32)

    graphics.set_pen(WHITE)
    graphics.set_font("bitmap6")

    # V
    graphics.rectangle(4, 11, 2, 4)
    graphics.rectangle(5, 15, 2, 4)
    graphics.rectangle(7, 19, 2, 2)
    graphics.rectangle(9, 15, 2, 4)
    graphics.rectangle(10, 11, 2, 4)

    # S
    graphics.rectangle(13, 11, 6, 2)
    graphics.rectangle(13, 13, 2, 4)
    graphics.rectangle(15, 15, 4, 2)
    graphics.rectangle(17, 17, 2, 4)
    graphics.rectangle(13, 19, 6, 2)

    # C
    graphics.rectangle(20, 13, 2, 6)
    graphics.rectangle(22, 11, 4, 2)
    graphics.rectangle(22, 19, 4, 2)
    graphics.rectangle(26, 13, 2, 2)
    graphics.rectangle(26, 17, 2, 2)

    return graphics


def render_chequered_flag(graphics):
    graphics.set_pen(BLACK)
    graphics.rectangle(0, 0, 32, 32)

    graphics.set_pen(WHITE)
    graphics.rectangle(0, 0, 8, 8)
    graphics.rectangle(16, 0, 8, 8)
    graphics.rectangle(8, 8, 8, 8)
    graphics.rectangle(24, 8, 8, 8)
    graphics.rectangle(0, 16, 8, 8)
    graphics.rectangle(16, 16, 8, 8)
    graphics.rectangle(8, 24, 8, 8)
    graphics.rectangle(24, 24, 8, 8)

    return graphics


def render_lights_out(graphics, count):
    graphics.set_pen(BLACK)
    graphics.rectangle(0, 0, 32, 32)

    graphics.set_pen(RED)

    if count > 0:
        graphics.rectangle(2, 2, 4, 28)
    if count > 1:
        graphics.rectangle(8, 2, 4, 28)
    if count > 2:
        graphics.rectangle(14, 2, 4, 28)
    if count > 3:
        graphics.rectangle(20, 2, 4, 28)
    if count > 4:
        graphics.rectangle(26, 2, 4, 28)

    return graphics
