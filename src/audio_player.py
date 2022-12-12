from pygame import mixer
from pygame.mixer import music as m

mixer.init()

absolute_pos_offset = 0.0

current_song_idx = -1
playing = False
queue = []
history = []


def get_state():
    return {
        "idx": current_song_idx,
        "playing": playing,
        "queue": queue,
        "history": history
    }


def play_new(db_id):
    global current_song_idx, playing

    stop()
    filepath, = FUNCTIONS['db_get_songs']('filepath', 'id={}'.format(db_id))[0]
    m.load(filepath)
    m.play()

    current_song_idx = db_id
    playing = True

    return 0


def play():
    global playing
    m.unpause()
    playing = True
    return 0


def pause():
    global playing
    m.pause()
    playing = False
    return 0


def stop():
    global playing
    m.rewind()
    m.pause()
    playing = False
    return 0


def get_pos():
    return m.get_pos() / 1000.0 - absolute_pos_offset


def set_pos(time):
    global absolute_pos_offset
    m.set_pos(time)
    absolute_pos_offset += get_pos() - time


FUNCTIONS = {
    "audio_get_state": get_state,
    "audio_play_new": play_new,
    "audio_play": play,
    "audio_pause": pause,
    "audio_stop": stop,
    "audio_get_pos": get_pos,
    "audio_set_pos": m.set_pos
}

CLI_FUNCTIONS = {
    "audio_set_pos": lambda x: set_pos(float(x)),
    "audio_play_new": lambda db_id: play_new(int(db_id))
}


def link_functions(fun_map):
    global FUNCTIONS
    FUNCTIONS = fun_map
