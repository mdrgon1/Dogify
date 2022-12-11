from pygame import mixer
from pygame.mixer import music as m

mixer.init()

absolute_pos_offset = 0.0


def play_new(filepath):
    stop()
    m.load(filepath)
    m.play()
    return 0


def play():
    m.unpause()
    return 0


def pause():
    m.pause()
    return 0


def stop():
    m.rewind()
    m.pause()
    return 0


def get_pos():
    return m.get_pos() / 1000.0 - absolute_pos_offset


def set_pos(time):
    global absolute_pos_offset
    m.set_pos(time)
    absolute_pos_offset += get_pos() - time


FUNCTIONS = {
    "audio_play_new": play_new,
    "audio_play": play,
    "audio_pause": pause,
    "audio_stop": stop,
    "audio_get_pos": get_pos,
    "audio_set_pos": m.set_pos
}

CLI_FUNCTIONS = {
    "audio_set_pos": lambda x: set_pos(float(x))
}


def link_functions(fun_map):
    global FUNCTIONS
    FUNCTIONS = fun_map
