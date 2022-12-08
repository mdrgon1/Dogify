import dogify_cli as c
import audio_player
import local_data
import tkinter.filedialog as f
import re


APP_FUNCTIONS: dict = {}


def register_functions(name, fun, *d):
    APP_FUNCTIONS[name] = fun
    c.register_cmds(name, fun)
    if d:
        register_functions(*d)


register_functions(
    "open_filedialog", lambda: f.askopenfilename(),
    "quit", lambda: local_data.close(),
)


if __name__ == '__main__':
    register_functions(*local_data.FUNCTIONS)
    c.register_cmds(*local_data.CLI_FUNCTIONS)
    register_functions(*audio_player.FUNCTIONS)
    c.register_cmds(*audio_player.CLI_FUNCTIONS)

    c.run_cli()
