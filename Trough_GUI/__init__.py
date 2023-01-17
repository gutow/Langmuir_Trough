from Trough_GUI import calibration_utils, status_widgets,\
    command_widgets

calibrations = calibration_utils.Calibrations()

# TODO maybe we now start up the trough if necessary?
import Trough_Control
from threading import Lock, Thread
from IPython import get_ipython
user_ns = get_ipython().user_ns
user_ns["trough_lock"] = Lock()
if not Trough_Control.trough_util.is_trough_initialized():
    user_ns["cmdsend"], user_ns["datarcv"], user_ns["TROUGH]"] = \
        Trough_Control.trough_util.init_trough()

# Now we should be able to import Monitor_Calibrate
from Trough_GUI import Monitor_Calibrate

status_update_thread = Thread(target=status_widgets.status_updater,
                                        args=(user_ns["trough_lock"],
                                              user_ns["cmdsend"],
                                              user_ns["datarcv"],
                                              calibrations,))
status_update_thread.start()
