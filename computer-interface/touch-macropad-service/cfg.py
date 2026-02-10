from evdev import ecodes
from enums import Action, SoundAction
from pathlib import Path

# actions to do on touchscreen button press
actions = {
    # example:
    # "0+": (Action.KEYS, [ecodes.KEY_LEFTCTRL, ecodes.KEY_C])
    
    "0+": (Action.KEYS, [ecodes.KEY_A]),
    "1+": (Action.SOUND, SoundAction.PLAY, 'distorted-beep.mp3'),
    "1-": (Action.SOUND, SoundAction.KILL, 'distorted-beep.mp3'),
    "2+": (Action.SOUND, SoundAction.PLAY, 'tracks/censor.mp3'),
    "2-": (Action.SOUND, SoundAction.KILL, 'tracks/censor.mp3'),
}

# location of sound files
sound_dir = Path("/usr/local/bin/touch-macropad/sounds")
