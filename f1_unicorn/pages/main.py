from f1_unicorn.render import (
    render_yellow_flag,
    render_green_flag,
    render_blue_flag,
    render_red_flag,
    render_safety_car,
    render_virtual_safety_car,
    render_chequered_flag,
    render_lights_out,
)


def main_page(graphics, state):
    flag = state["game"].get("flag")
    flag_extra = state["game"].get("flag_extra", {})
    # flag = None
    # flag_extra = {}

    if flag == "red_flag":
        return render_red_flag(graphics)
    elif flag == "chequered_flag":
        return render_chequered_flag(graphics)
    elif flag == "safety_car":
        return render_safety_car(graphics)
    elif flag == "virtual_safety_car":
        return render_virtual_safety_car(graphics)
    elif flag == "yellow_flag":
        return render_yellow_flag(graphics)
    elif flag == "blue_flag":
        return render_blue_flag(graphics, flag_extra.get("number", "??"))
    elif flag == "green_flag":
        return render_green_flag(graphics)
    elif flag == "lights_out":
        return render_lights_out(graphics, flag_extra.get("count", 1))
    return graphics
