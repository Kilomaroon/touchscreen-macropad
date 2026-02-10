from service import Action
from sound_handler import SoundAction
from evdev_handler import ecodes

# location of sound files
sound_dir=Path("/data/Code/touchscreen-macropad/sounds")

# actions to do on touchscreen button press
actions = {
    # example:
    # "0+": (Action.KEYS, [ecodes.KEY_LEFTCTRL, ecodes.KEY_C])
    
    "0+": (Action.KEYS, [ecodes.KEY_A]),
    "1+": (Action.SOUND, SoundAction.PLAY, 'distorted-beep.mp3'),
}