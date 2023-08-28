from f1_unicorn.color import BLACK
from f1_unicorn.config import load_config, save_config
from f1_unicorn.game import connect
from f1_unicorn.legacy import legacy
from f1_unicorn.network_manager import connect_wifi, is_connected
from f1_unicorn.pages.demo import demo_page
from f1_unicorn.pages.main import main_page
from f1_unicorn.pages.menu import menu_page
import uasyncio
from f1_unicorn.globals import cu, graphics
from cosmic import CosmicUnicorn
import math
from machine import Pin

REFRESH_RATE = 10
INPUT_RATE = 60
_active_page = "menu"


def _update_brightness(delta):
    new_brightness = max(min(cu.get_brightness() + delta, 1.0), 0.1)
    config = load_config()
    config["brightness"] = math.ceil(new_brightness * 100)
    save_config(config)
    cu.set_brightness(new_brightness)


def _update_sleep():
    if cu.get_brightness() > 0.0:
        cu.set_brightness(0.0)
    else:
        config = load_config()
        cu.set_brightness(config["brightness"] / 100.0)


def _register_button(button_id, callback):
    button = Pin(button_id, Pin.IN, Pin.PULL_UP)
    button.irq(callback, Pin.IRQ_RISING)


def _switch_page(config, page):
    if not is_connected(config["wifi"]["country"]):
        return
    print("Switching to {}".format(page))
    global _active_page
    _active_page = page


break_loop = False


async def render(state):
    while True:
        if break_loop:
            break
        result = graphics

        result.clear()
        result.set_pen(BLACK)
        result.rectangle(0, 0, 32, 32)

        if _active_page == "main":
            result = main_page(result, state)
        elif _active_page == "demo":
            result = demo_page(result, state)
        elif _active_page == "menu":
            result = menu_page(result, state)
        cu.update(result)

        await uasyncio.sleep_ms(1000 // 5)


async def main():
    config = load_config()
    cu.set_brightness(config["brightness"] / 100.0)
    state = {"game": {}}
    global _active_page

    def switch_legacy(_):
        if not is_connected(config["wifi"]["country"]):
            return

        global break_loop
        network_task.cancel()
        break_loop = True

    uasyncio.create_task(
        connect_wifi(
            config["wifi"]["country"],
            config["wifi"]["ssid"],
            config["wifi"]["password"],
        )
    )
    network_task = uasyncio.create_task(connect(state))
    render_task = uasyncio.create_task(render(state))

    _register_button(
        CosmicUnicorn.SWITCH_BRIGHTNESS_UP, lambda _: _update_brightness(0.1)
    )
    _register_button(
        CosmicUnicorn.SWITCH_BRIGHTNESS_DOWN, lambda _: _update_brightness(-0.1)
    )
    _register_button(CosmicUnicorn.SWITCH_SLEEP, lambda _: _update_sleep())
    _register_button(CosmicUnicorn.SWITCH_A, lambda _: _switch_page(config, "main"))
    _register_button(CosmicUnicorn.SWITCH_B, switch_legacy)
    _register_button(CosmicUnicorn.SWITCH_C, lambda _: _switch_page(config, "demo"))
    _register_button(CosmicUnicorn.SWITCH_D, lambda _: _switch_page(config, "menu"))

    await render_task
    # If we get here, it means the user is trying to access the legacy app
    legacy(graphics, state, cu.update)
