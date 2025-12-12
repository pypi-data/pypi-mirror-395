import os
import time
import subprocess
from pathlib import Path
from just_playback.playback import Playback as PlaybackBase, MiniaudioError


class Playback(PlaybackBase):
    def play_sync(self):
        self.play()
        self.waiting()

    def waiting(self):
        while self.playing:
            time.sleep(0)


def play_file(filepath, ignore=True):
    if ignore:
        if not is_device_supported():
            return
    try:
        playback = Playback()
    except MiniaudioError:
        if ignore:
            return
        else:
            raise
    playback.load_file(filepath)
    playback.play_sync()


path_res = Path(__file__).resolve().parent / 'res'


def play_res(name, path=None, ignore=True):
    path = path or path_res
    for file in os.listdir(path):
        if os.path.splitext(file)[0] == name:
            play_file(os.path.join(path, file), ignore)


def is_device_supported():
    if os.name != 'nt':
        result = subprocess.getoutput('lspci')
        desc_list = [x.rsplit(':', 1)[0].split(' ', 1)[-1].strip() for x in result.split('\n')]
        return 'Audio device' in desc_list
    return True
