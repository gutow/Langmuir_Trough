from Trough_Control import trough_util, message_utils
from threading import Lock
trough_lock = Lock()
#  last direction barriers moved -1 closing, 0 unknown, 1 opening
lastdirection = 0