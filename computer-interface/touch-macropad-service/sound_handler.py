import argparse
import subprocess
import logging
from datetime import datetime
import time
from pathlib import Path
import os
from pprint import pformat
from enums import SoundAction

class SoundHandler():
    ''' Maintains a list of Sound objects, acts as interface with service. '''

    def __init__(self, logger, base_dir):
        self.logger = logger
        self.base_dir = base_dir
        self.sounds = {} # maps string sound file path to Sound object

        # the sounds that can exist are the ones in base_dir
        sound_paths = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                sound_path = os.path.join(root, file)
                self.sounds[sound_path] = Sound(sound_path, logger)
        
        logger.info(f"SoundHandler loaded sounds:\n{pformat(list(self.sounds.keys()))}")

    def handle(self, sound_action, sound_rel_file):
        # check sound exists
        sound_file = os.path.join(self.base_dir, sound_rel_file)
        if str(sound_file) not in self.sounds:
            raise Exception(f"Sound file doesn't exist: {sound_file}")
        
        if sound_action == SoundAction.PLAY:
            self.sounds[sound_file].play()
        elif sound_action == SoundAction.KILL:
            self.sounds[sound_file].kill()

    def close(self):
        # have each sound handle its own process
        for sound in self.sounds.values():
            sound.close()


class Sound():
    def __init__(self, file, logger):
        self.file = file
        self.proc = None
        self.logger = logger

    def __str__(self):
        if self.is_playing():
            return f'[SOUND={self.file} PID={self.proc.pid}]'
        else:
            return f'[SOUND={self.file}]'

    def is_playing(self):
        if self.proc == None:
            return False
        elif self.proc.poll() != None:
            # process exited with a return code
            return False
        else:
            # process has not exited with a return code
            return True

    def play(self):
        ''' Launch a new pipewire process to play the sound '''
        if self.is_playing():
            self.logger.info(f'{self} failed to play because it is already playing')
        else:
            # play and don't schedule repeats
            self.proc = subprocess.Popen(['pw-play', self.file])
            self.logger.info(f'Now playing {self}')

    def kill(self):
        ''' Kill our running pipewire process '''
        if not self.is_playing():
            self.logger.info(f'Could not kill {self} because it is already dead')
        else:
            # kill process
            self.proc.terminate()
            self.logger.info(f'Sent SIGTERM to {self}')

    def loop(self):
        if self.is_playing():
            self.logger.info(f'{self} failed to loop because it is already playing')
        # todo...

if __name__ == '__main__':

    logname = datetime.now().strftime('logs/%Y-%m-%d_%H-%M-%S.log')
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()
        ]
    )
    log = logging.getLogger()

    h = SoundHandler(log, Path("/data/Code/touchscreen-macropad/sounds"))
    h.handle(SoundAction.PLAY, 'distorted-beep.mp3')

    time.sleep(0.5)

    h.handle(SoundAction.KILL, 'distorted-beep.mp3')

