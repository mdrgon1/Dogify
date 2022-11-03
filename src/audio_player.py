import vlc

player = None


def play_new(filepath):
    global player
    stop()
    player = vlc.MediaPlayer(filepath)
    player.play()


def play():
    global player
    if player:
        player.play()
    else:
        print("no song currently playing")


def pause():
    global player
    if player:
        player.pause()


def stop():
    global player
    if player:
        player.stop()