from Trough_GUI import calibration_utils, status_widgets,\
    command_widgets

calibrations = calibration_utils.Calibrations()

# TODO maybe we now start up the trough if necessary?
import Trough_Control
from threading import Thread
from IPython import get_ipython
user_ns = get_ipython().user_ns
user_ns["Trough_Control"] = Trough_Control
if not Trough_Control.trough_util.is_trough_initialized():
    Trough_Control["cmdsend"], Trough_Control["datarcv"], \
    Trough_Control["TROUGH]"] = Trough_Control.trough_util.init_trough()

# Now we should be able to import Monitor_Calibrate
from Trough_GUI import Monitor_Calibrate

status_update_thread = Thread(target=status_widgets.status_updater,
                                        args=(Trough_Control["trough_lock"],
                                              Trough_Control["cmdsend"],
                                              Trough_Control["datarcv"],
                                              calibrations,))
status_update_thread.start()
