from f1_unicorn.config import load_config
from f1_unicorn.network_manager import is_connected
from f1_unicorn.render import WHITE, BLACK
import time


def menu_page(graphics, state):
    config = load_config()
    graphics.set_pen(WHITE)
    graphics.rectangle(0, 0, 32, 9)
    graphics.set_font("bitmap8")

    graphics.set_pen(BLACK)
    graphics.text("FLAGS", 2, 1, -1, 1, 0, 2)
    graphics.rectangle(0, 9, 32, 23)

    graphics.set_pen(WHITE)
    if is_connected(config["wifi"]["country"]):
        graphics.text("Ready", 2, 16, -1, 1, 0, 2)
    else:
        tick = time.ticks_ms()
        step = (tick // 1000) % 4

        graphics.rectangle(15, 24, 2, 2)

        if step >= 1:
            graphics.rectangle(14, 22, 4, 1)
            graphics.rectangle(13, 23, 1, 2)
            graphics.rectangle(18, 23, 1, 2)

        if step >= 2:
            graphics.rectangle(13, 20, 6, 1)
            graphics.pixel(12, 21)
            graphics.pixel(19, 21)
            graphics.rectangle(11, 22, 1, 2)
            graphics.rectangle(20, 22, 1, 2)

        if step >= 3:
            graphics.rectangle(12, 18, 8, 1)
            graphics.pixel(11, 19)
            graphics.pixel(20, 19)
            graphics.pixel(10, 20)
            graphics.pixel(21, 20)
            graphics.rectangle(9, 21, 1, 2)
            graphics.rectangle(22, 21, 1, 2)

    return graphics
