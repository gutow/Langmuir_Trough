import Trough_GUI
from Trough_GUI.status_widgets import Bar_Sep,Bar_Area,Bar_Area_per_Molec, \
    degC, surf_press, set_zero_pressure, plate_circumference, moles_molec
from Trough_GUI.command_widgets import Barr_Units, Barr_Speed, Barr_Target
from IPython import get_ipython
cmdsend = get_ipython().user_ns["Trough_Control"].cmdsend
datarcv = get_ipython().user_ns["Trough_Control"].datarcv
trough_lock = get_ipython().user_ns["Trough_Control"].trough_lock

def Run(run_name):
    """
    This routine creates a GUI for initializing, starting, collecting and
    completing a run. If the run has been completed it will simply reload it
    from the local datafile.

    Parameters
    ----------
    run_name: str or Path
    This should generally be the name for the file the data will be stored in
    without a file type extension. Recommend a naming scheme that produces
    Unique filenames, such as `Trough_run_<username>_<timestamp>`.
    """
    from pathlib import Path
    # TODO Check if run completed, if so reload data, display and exit
    datafilepath = Path.cwd()/Path(str(run_name) + '.html') # or should it be gz
    if datafilepath.exists():
        # TODO display the data as a live plotly plot.
        return
    # TODO Build run setup GUI

    # TODO take over status updating

    # TODO Start run

    # TODO Stop run

    # TODO Store data

    # TODO Display final data

    # TODO release status updating

    return