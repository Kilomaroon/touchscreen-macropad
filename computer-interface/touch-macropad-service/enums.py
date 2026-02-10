from enum import Enum

# used by service to select handler
class Action(Enum):
    KEYS = 1
    SOUND = 2

# used by sound_handler to select operation
class SoundAction(Enum):
    PLAY = 1
    LOOP = 2
    HOLD = 3
    KILL = 4
