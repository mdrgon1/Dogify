from pygame import mixer as m

m.init()
channel = None


def play_new(filepath):
    global channel
    stop()
    channel = m.Sound(file=filepath).play()
    return channel


def play():
    global channel
    if channel:
        return channel.unpause()
    else:
        print("no song currently playing")
        return -1


def pause():
    global channel
    if channel:
        return channel.pause()
    return 0


def stop():
    global channel
    if channel:
        return channel.stop()
    return 0
