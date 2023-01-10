from Trough_GUI import calibration_utils, status_widgets,\
    command_widgets, Monitor_Calibrate

# TODO should I put shared variable used to control/update GUI elements into a
#   common structure (e.g. Trough_GUI_Common.X...)? This would allow it to be
#   placed in the global namespace while lowering the chance that the user
#   would change them by accident.
#   An alternative is simply to initialize the trough when Trough_GUI is
#   imported. Then calibrations would be inside the Trough_GUI namespace.

class Trough_GUI_Common():
    def __init__(self):
        """This is a structure to hold values, variables and objects used in
        common by the Trough_GUI"""
        #self.calibrations = calibration_utils.Calibrations()

        pass

calibrations = calibration_utils.Calibrations()

# TODO maybe we now start up the trough if necessary?