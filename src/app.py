import dogify_cli as c
import audio_player
import local_data
import tkinter.filedialog as f
import GUI as gui
import re


APP_FUNCTIONS: dict = {
    "open_filedialog": lambda: f.askopenfilename(),
    "quit": lambda: local_data.close(),
    "echo": lambda s: print(s)
}


def register_functions(functions_map: dict):
    global APP_FUNCTIONS
    for name, fun in functions_map.items():
        APP_FUNCTIONS[name] = fun
    for name, fun in APP_FUNCTIONS.items():
        functions_map[name] = fun
    c.register_cmds(functions_map)


if __name__ == '__main__':
    register_functions(APP_FUNCTIONS)

    register_functions(local_data.FUNCTIONS)
    c.register_cmds(local_data.CLI_FUNCTIONS)
    register_functions(audio_player.FUNCTIONS)
    c.register_cmds(audio_player.CLI_FUNCTIONS)
    register_functions(gui.FUNCTIONS)
    c.register_cmds(gui.CLI_FUNCTIONS)

    local_data.link_functions(APP_FUNCTIONS)
    audio_player.link_functions(APP_FUNCTIONS)
    gui.link_functions(APP_FUNCTIONS)

    gui.init()
    c.run_cli()

