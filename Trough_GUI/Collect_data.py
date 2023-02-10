import Trough_GUI
from Trough_GUI.status_widgets import Bar_Sep,Bar_Area,Bar_Area_per_Molec, \
    degC, surf_press, zero_press, plate_circumference, moles_molec
from Trough_GUI.command_widgets import Barr_Units, Barr_Speed, Barr_Target
from IPython import get_ipython
cmdsend = get_ipython().user_ns["Trough_Control"].cmdsend
datarcv = get_ipython().user_ns["Trough_Control"].datarcv
trough_lock = get_ipython().user_ns["Trough_Control"].trough_lock

# Boilerplate style for long descriptions on ipywidget
longdesc = {'description_width': 'initial'}

class trough_run():
    def __init__(self, id, filename, title, units, target, speed, moles,
                 plate_circ, dataframe=None):
        """Create a new run object
        Parameters
        ----------
        id: int
            0 based index of run in current notebook
        filename: str
            String representation of the filename used to store the data,
            with not type extension. This probably should not contain a path.
        title: str
            User friendly title (suggested default is same as filename).
        units: str
            Units for the displayed barrier positions (cm, cm^2 or Ang^2/molec).
        target: float
            Numerical value in units for the targeted final trough area.
        speed: float
            Numerical value in units for the speed to move the barriers.
        moles: float
            moles of molecules initially spread in the trough.
        plate_circ: float
            circumference of the Whilhelmy plate in mm.
        dataframe: None or DataFrame
        """
        from plotly import graph_objects as go
        self.id = id
        self.filename = filename
        self.title = title
        self.units = units
        self.target = target
        self.speed = speed
        self.moles = moles
        self.plate_circ = plate_circ
        self.livefig = go.FigureWidget(layout_template='simple_white')
        self.df = dataframe
        # TODO load data into livefig if there is any?

    @classmethod
    def from_html(self, html):
        """Create a run from an html representation"""
        id = None
        filename = None
        title = None
        units = None
        target = None
        speed = None
        moles = None
        plate_circ = None
        dataframe = None
        # TODO convert html representation of a run to a run object
        return trough_run(id, filename, title, units, target, speed, moles,
                 plate_circ, dataframe)

    def to_html(self):
        """Create an html string representing a run"""
        from AdvancedHTMLParser import AdvancedTag as Domel
        from datetime import datetime
        htmlstr = ""
        # TODO create the htmlstr
        return htmlstr

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
    from ipywidgets import Text, Dropdown, HBox, VBox, Accordion, Label, Button
    from IPython.display import display
    from IPython import get_ipython
    user_ns = get_ipython().user_ns
    name_to_run = {}
    completed_runs = []
    for k in user_ns["Trough_GUI"].runs:
        name_to_run[k.title]= k
        completed_runs.append(k.title)
    # TODO Check if run completed, if so reload data, display and exit
    datafilepath = Path.cwd()/Path(str(run_name) + '.html') # or should it be gz
    if datafilepath.exists():
        # TODO display the data as a live plotly plot.
        return
    # TODO Build run setup GUI
    run_title = Text(description = "Run Title",
                     value = str(run_name),
                     disabled = False)
    def changed_base_on(change):
        # TODO update settings to match the chosen run
        pass
    base_on = Dropdown(description = "Base on",
                       options=['None'] + completed_runs)
    base_on.observe(changed_base_on)
    top_HBox = HBox([run_title, base_on])
    # Displayed status widgets
    status_HBox1 = HBox([Bar_Sep, Bar_Area, Bar_Area_per_Molec])
    status_HBox2 = HBox([surf_press, degC])
    status_VBox = VBox([status_HBox1, status_HBox2])
    status_Acc = Accordion([status_VBox])
    status_Acc.set_title(0,"Status")
    status_Acc.selected_index = 0
    # Displayed settings widgets
    settings_HBox1 = HBox([zero_press, plate_circumference, moles_molec])
    settings_HBox2 = HBox([Barr_Units, Barr_Speed])
    store_settings = Button(description="Fix Settings")
    # Run control button
    def on_run_start_stop(change):
        # Check if we are stopping a run
        if run_start_stop.description == "Stop":
            on_stop_run()
            return
        # TODO take over status updating
        # First shutdown currently running updater
        if Trough_GUI.updater_running.value:
            Trough_GUI.run_updater.value = False
            while Trough_GUI.updater_running.value:
                # wait
                pass
        # TODO Start run
        # Convert "Start" to "Stop" button
        run_start_stop.description = "Stop"
        run_start_stop.button_style = "danger"
        # TODO display data as collected and periodically update status widgets
        # spawn updater thread that updates both status widgets and the figure.
        return

    def on_stop_run():
        # TODO Stop run
        # TODO Store data
        # TODO Display final data
        # TODO release status updating
        return
    run_start_stop = Button(description="Run",
                            button_style="success")
    run_start_stop.on_click(on_run_start_stop)
    def on_store_settings(change):
        from IPython.display import HTML, clear_output
        # create the run object
        id = len(Trough_GUI.runs)
        Trough_GUI.runs.append(trough_run(id,run_name, run_title.value,
                                          Barr_Units.value,
                                          float(Barr_Target.value),
                                          float(Barr_Speed.value),
                                          float(moles_molec.value),
                                          float(plate_circumference.value)))
        # Create the collection display
        headerhtmlstr = ''
        headerhtmlstr += '<table><tr><th>Run ID</th><th>Title</th>'
        headerhtmlstr += '<th>Storage File Name</th></tr>'
        headerhtmlstr += '<tr><td>'+str(id)+ '</td>'
        headerhtmlstr += '<td>'+run_title.value+'</td>'
        headerhtmlstr += '<td>'+run_name+'</td></tr></table>'
        headerhtmlstr += '<table><tr><th>Target ('+Barr_Units.value + ')</th>'
        headerhtmlstr += '<th>Speed ('+Barr_Units.value + '/min)</th>'
        headerhtmlstr += '<th>Moles</th><th>Plate Circumference (mm)</th></tr>'
        headerhtmlstr += '<tr><td>' +str(Barr_Target.value)+'</td>'
        headerhtmlstr += '<td>' + str(Barr_Speed.value)+ '</td>'
        headerhtmlstr += '<td>' + str(moles_molec.value)+ '</td>'
        headerhtmlstr += '<td>' +str(plate_circumference.value) + '</td></tr>'
        headerhtmlstr += '</table>'
        collect_control1 = HBox([surf_press, run_start_stop])
        position = None
        if Barr_Units.value == 'cm':
            position = Bar_Sep
        elif Barr_Units.value == 'cm^2':
            position = Bar_Area
        elif Barr_Units.value == 'Angstrom^2/molec':
            position = Bar_Area_per_Molec
        collect_control2 = HBox([degC, position])
        collect_control = VBox([collect_control1, collect_control2])
        x_units = Barr_Units.value
        x_min = 0
        x_max = 1
        if float(Barr_Target.value) < float(position.value):
            x_min = float(Barr_Target.value)
            x_max = float(position.value)
        else:
            x_min = float(position.value)
            x_max = float(Barr_Target.value)
        if float(Barr_Speed.value) == 0:
            x_units = 'Time (s)'
            x_min = 0
            x_max = 5
        Trough_GUI.runs[id].livefig.update_yaxes(title = "$\Pi\,(mN/m)$",
                                                 range=[0, 60])
        Trough_GUI.runs[id].livefig.update_xaxes(title=x_units,
                                                 range=[x_min,x_max])
        # Clear output and display collection
        #   with fixed param and start run button.
        clear_output()
        display(HTML(headerhtmlstr))
        display(Trough_GUI.runs[id].livefig)
        display(collect_control)
        return

    store_settings.on_click(on_store_settings)
    settings_HBox3 = HBox([Label("Target", style=longdesc), Barr_Target,
                           store_settings])
    settings_VBox = VBox([settings_HBox1,settings_HBox2, settings_HBox3])
    settings_Acc = Accordion([settings_VBox])
    settings_Acc.set_title(0, "Settings")
    status_Acc.selected_index = 0
    Barr_Target.disabled = False
    display(top_HBox, status_Acc, settings_Acc)

    return

def collect_data_updater(trough_lock, cmdsend, datarcv, cals, lastdirection,
                   run_updater, updater_running, run):
    """This is run in a separate thread and will update the figure and
    all status widgets every 2 seconds or when it can get access to the pipes
    to talk to the trough.

    Parameters
    ----------
    trough_lock: threading.lock
        When acquired this routine will talk to the trough. Releases it for
        other processes after every update.

    cmdsend: Pipe
        End of Pipe to send commands to the Trough.

    datarcv: Pipe
        End of Pipe to receive data from the Trough.

    cals: Trough_GUI.calibrations
        Used to convert the data to user units.

    lastdirection: multiprocessing.Value
        Of type 'i' to indicate last direction the barriers moved.

    run_updater: multiprocessing.Value
        Of type 'c_bool'. True if this updater should keep running.

    updater_running: multiprocessing.Value
        Of type 'c_bool'. Set to True by this process when it starts
        and set to False before exiting.

    run: trough_run
        This object contains the live figure and the place to store the data.
    """
    import time
    # Set the shared I'm running flag.
    updater_running.value = True
    trough_lock.acquire()
    while run_updater.value:
        min_next_time = time.time() + 2.0
        cmdsend.send(['Send',''])
        waiting = True
        while waiting:
            if datarcv.poll():
                datapkg =datarcv.recv()
                # TODO change to update figure and then call update_status
                if len(datapkg[1]) >= 1:
                    update_collection(datapkg, cals, lastdirection, run)
                    update_dict = {'barr_raw':datapkg[1][-1],
                                   'barr_dev':datapkg[2][-1],
                                   'bal_raw':datapkg[3][-1],
                                   'bal_dev':datapkg[4][-1],
                                   'temp_raw':datapkg[5][-1],
                                   'temp_dev':datapkg[6][-1],
                                   'messages':datapkg[7]}
                else:
                    # No updated data, so just pass messages
                    update_dict = {'messages':datapkg[7]}
                update_status(update_dict, cals, lastdirection)
                waiting = False
        if time.time()< min_next_time:
            time.sleep(min_next_time - time.time())
    # Release lock and set the shared I'm running flag to False before exiting.
    trough_lock.release()
    updater_running.value = False
    return

def update_collection(datapkg, cals, lastdirection, run):
    """Updates the graph and the data storage"""
    from pandas import DataFrame
    import numpy as np
    # TODO do all the calculations on the new data
    time_stamp = np.array(datapkg[0])
    pos_raw = np.array(datapkg[1])
    pos_raw_stdev = np.array(datapkg[2])
    bal_raw = np.array(datapkg[3])
    bal_raw_stdev = np.array(datapkg[4])
    temp_raw = np.array(datapkg[5])
    temp_raw_stdev = np.array(datapkg[6])
    sep_cm = None
    sep_cm_stdev = None
    if lastdirection.value < 0:
        sep_cm, sep_cm_stdev = cals.barriers_close.cal_apply(pos_raw,
                                                             pos_raw_stdev)
    else:
        sep_cm, sep_cm_stdev = cals.barriers_close.cal_apply(pos_raw,
                                                             pos_raw_stdev)
    area_sqcm = sep_cm*float(cals.barriers_open.additional_data[ \
                               "trough width (cm)"])
