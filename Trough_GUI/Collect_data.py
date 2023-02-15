from ipywidgets import Button
from IPython import get_ipython
cmdsend = get_ipython().user_ns["Trough_Control"].cmdsend
datarcv = get_ipython().user_ns["Trough_Control"].datarcv
trough_lock = get_ipython().user_ns["Trough_Control"].trough_lock

# Boilerplate style for long descriptions on ipywidget
longdesc = {'description_width': 'initial'}

class trough_run():
    def __init__(self, id, filename, title, units, target, speed, moles,
                 plate_circ, dataframe=None, timestamp=None):
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
        timestamp: None or int
        """
        from plotly import graph_objects as go
        import time
        from datetime import datetime
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
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()
        self.datestr = (datetime.fromtimestamp(self.timestamp)).isoformat()
        # TODO load data into livefig if there is any?

    @classmethod
    def from_html(self, html):
        """Create a run from an html representation
        Parameters
        ----------
        html: str
            The html to be parsed to create the run object

        Returns
        -------
        trough_run: trough_run
            A trough_run object
        """
        from AdvancedHTMLParser import AdvancedHTMLParser as Parser
        from pandas import read_html
        # parse the document
        document = Parser()
        document.parseStr(html)
        id = document.getElementById('id').text
        filename = document.getElementById('filename').text
        title = document.getElementById('title').text
        units = document.getElementById('units').text
        target = document.getElementById('target').text
        speed = document.getElementById('speed').text
        moles = document.getElementById('moles').text
        plate_circ = document.getElementById('plate_circ').text
        data_table_html = document.getElementById('run_data')
        dataframe = read_html(data_table_html, index_col=0)[0]
        timestamp = document.getElementById('timestamp').text
        # return as run object
        return trough_run(id, filename, title, units, target, speed, moles,
                 plate_circ, dataframe, timestamp)

    def to_html(self):
        """Create an html string representing a run"""
        from AdvancedHTMLParser import AdvancedTag as Domel
        # create the html
        run_div = Domel('div')
        run_info = Domel('table')
        run_info.setAttributes('class','run_info')
        run_info.setAttributes('id','run_info')
        run_info.setAttributes('border','1')
        tr = Domel('tr')
        tr.appendInnerHTML('<th>ID</th><th>Filename</th><th>Title</th><th>Units'
                       '</th><th>Target</th><th>Speed</th><th>Moles</th>'
                       '<th>Plate Circumference (mm)</th><th>Time</th><th>Time '
                       'Stamp</th>')
        run_info.appendChild(tr)
        tr = Domel('tr')
        tr.appendInnerHTML('<td id="id">'+str(self.id)+'</td>'
                           '<td id="filename">'+str(self.filename) + '</td>'
                           '<td id="title">'+str(self.title) + '</td>'
                           '<td id="units">' + str(self.units)+'</td>'
                           '<td id="target">'+str(self.target) +'</td>'
                           '<td id="speed">'+str(self.speed)+'</td>'
                           '<td id="moles">' + str(self.moles)+'</td>'
                           '<td id="plate_circ">'+str(self.plate_circ) + '</td>'
                           '<td id="datestr">'+str(self.datestr)+'</td>'
                           '<td id="timestamp">' + str(self.timestamp)+'</td>')
        run_info.appendChild(tr)
        run_div.appendChild(run_info)
        run_div.appendInnerHTML(self.df.to_html(table_id="run_data"))
        return run_div.asHTML()

def on_run_start_stop(change):
    from threading import Thread
    from numpy import sign
    from IPython import get_ipython
    Trough_GUI = get_ipython().user_ns["Trough_GUI"]
    Bar_Sep = Trough_GUI.status_widgets.Bar_Sep
    Bar_Area = Trough_GUI.status_widgets.Bar_Area
    Bar_Area_per_Molec = Trough_GUI.status_widgets.Bar_Area_per_Molec
    moles_molec = Trough_GUI.status_widgets.moles_molec
    Barr_Units = Trough_GUI.command_widgets.Barr_Units
    Barr_Speed = Trough_GUI.command_widgets.Barr_Speed
    Barr_Target = Trough_GUI.command_widgets.Barr_Target
    # Check if we are stopping a run
    if run_start_stop.description == "Stop":
        on_stop_run()
        return
    # take over status updating
    # First shutdown currently running updater
    if Trough_GUI.updater_running.value:
        Trough_GUI.run_updater.value = False
        while Trough_GUI.updater_running.value:
            # wait
            pass
    # Start run
    # Convert "Start" to "Stop" button
    Trough_GUI.run_updater.value = True
    run_start_stop.description = "Stop"
    run_start_stop.button_style = "danger"
    # start barriers
    trough_lock.acquire()
    direction = 0
    tempspeed = 0
    speed = 0
    skimmer_correction = float(Trough_GUI.calibrations.barriers_open.additional_data["skimmer correction (cm^2)"])
    width = float(Trough_GUI.calibrations.barriers_open.additional_data["trough width (cm)"])
    target_speed = float(Barr_Speed.value)
    if Barr_Units.value == 'cm':
        direction = int(sign(float(Barr_Target.value)-float(Bar_Sep.value)))
        tempspeed = target_speed
    elif Barr_Units.value == "cm^2":
        direction = int(sign(float(Barr_Target.value)-float(Bar_Area.value)))
        tempspeed = (target_speed - skimmer_correction) / width
    elif Barr_Units.value == "Angstrom^2/molec":
        direction = int(sign(float(Barr_Target.value)-float(Bar_Area_per_Molec.value)))
        tempspeed = (target_speed - skimmer_correction) / width / 1e16 * moles_molec * 6.02214076e23
    if direction < 0:
        target = Trough_GUI.calibrations.barriers_close.cal_inv(float(Barr_Target.value),0)[0]
        speed = Trough_GUI.calibrations.speed_close.cal_inv(tempspeed,0)[0]
    else:
        target = Trough_GUI.calibrations.barriers_open.cal_inv(float(Barr_Target.value), 0)[0]
        speed = Trough_GUI.calibrations.speed_open.cal_inv(tempspeed, 0)[0]
    cmdsend.send(['Speed', speed])
    cmdsend.send(['Direction', direction])
    cmdsend.send(['MoveTo', target])
    trough_lock.release()
    # display data as collected and periodically update status widgets
    # spawn updater thread that updates both status widgets and the figure.
    updater = Thread(target=collect_data_updater, args=(trough_lock, cmdsend,
                                                datarcv,
                                                Trough_GUI.calibrations,
                                                Trough_GUI.lastdirection,
                                                Trough_GUI.run_updater,
                                                Trough_GUI.updater_running,
                                                Trough_GUI.runs[-1]))
    updater.start()
    return

def end_of_run():
    from IPython import get_ipython
    Trough_GUI = get_ipython().user_ns["Trough_GUI"]
    # update the stop button
    run_start_stop.description = "Done"
    run_start_stop.button_style = ""
    run_start_stop.disabled = True
    # TODO Store data
    # TODO Display final data
    # start background updating
    if not Trough_GUI.updater_running.value:
        Trough_GUI.run_updater.value = True
        Trough_GUI.start_status_updater()
    return

def on_stop_run():
    from IPython import get_ipython
    Trough_GUI = get_ipython().user_ns["Trough_GUI"]
    # Stop run
    if Trough_GUI.updater_running.value:
        Trough_GUI.run_updater.value = False
    # when collection stops it will call end_of_run above.
    return

run_start_stop = Button(description="Run",
                        button_style="success")
run_start_stop.on_click(on_run_start_stop)

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
    Trough_GUI = get_ipython().user_ns["Trough_GUI"]
    Bar_Sep = Trough_GUI.status_widgets.Bar_Sep
    Bar_Area = Trough_GUI.status_widgets.Bar_Area
    Bar_Area_per_Molec = Trough_GUI.status_widgets.Bar_Area_per_Molec
    degC = Trough_GUI.status_widgets.degC
    surf_press = Trough_GUI.status_widgets.surf_press
    zero_press = Trough_GUI.status_widgets.zero_press
    plate_circumference = Trough_GUI.status_widgets.plate_circumference
    moles_molec = Trough_GUI.status_widgets.moles_molec
    Barr_Units = Trough_GUI.command_widgets.Barr_Units
    Barr_Speed = Trough_GUI.command_widgets.Barr_Speed
    Barr_Target = Trough_GUI.command_widgets.Barr_Target
    name_to_run = {}
    completed_runs = []
    for k in Trough_GUI.runs:
        name_to_run[k.title]= k
        completed_runs.append(k.title)
    # TODO Check if run completed, if so reload data, display and exit
    datafilepath = Path.cwd()/Path(str(run_name) + '.html') # or should it be gz
    if datafilepath.exists():
        # TODO display the data as a live plotly plot.
        return
    # Build run setup GUI
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
    store_settings = Button(description="Store Settings")

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
        headerhtmlstr += '<th>Storage File Name</th>'
        headerhtmlstr += '<th>Target (' + Barr_Units.value + ')</th>'
        headerhtmlstr += '<th>Speed (' + Barr_Units.value + '/min)</th>'
        headerhtmlstr += '<th>Moles</th><th>Plate Circumference (mm)</th></tr>'
        headerhtmlstr += '<tr><td>'+str(id)+ '</td>'
        headerhtmlstr += '<td>'+run_title.value+'</td>'
        headerhtmlstr += '<td>'+run_name+'</td>'
        headerhtmlstr += '<td>' +str(Barr_Target.value)+'</td>'
        headerhtmlstr += '<td>' + str(Barr_Speed.value)+ '</td>'
        headerhtmlstr += '<td>' + str(moles_molec.value)+ '</td>'
        headerhtmlstr += '<td>' +str(plate_circumference.value) + '</td></tr>'
        headerhtmlstr += '</table>'
        run_start_stop.description = "Run"
        run_start_stop.disabled = False
        run_start_stop.button_style = "success"
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
            x_min = 0.98*float(Barr_Target.value)
            x_max = 1.02*float(position.value)
        else:
            x_min = 0.98*float(position.value)
            x_max = 1.02*float(Barr_Target.value)
        if float(Barr_Speed.value) == 0:
            x_units = 'Time (s)'
            x_min = 0
            x_max = 5
        Trough_GUI.runs[id].livefig.update_yaxes(title = "$\Pi\,(mN/m)$",
                                                 range=[0, 60])
        Trough_GUI.runs[id].livefig.update_xaxes(title=x_units,
                                                 range=[x_min,x_max])
        Trough_GUI.runs[id].livefig.add_scatter(x=[],y=[])
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
    all status widgets at an interval of 2 seconds or a little longer. While
    this is running nothing else will be able to talk to the trough.

    Parameters
    ----------
    trough_lock: threading.lock
        When acquired this routine will talk to the trough. It is not
        released until the routine exits to avoid any data loss. It does
        call the status_widgets updater as often as it can while collecting
        the data.

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
    from IPython import get_ipython
    Trough_GUI = get_ipython().user_ns["Trough_GUI"]
    # Set the shared I'm running flag.
    updater_running.value = True
    print("collect_data_updater started")
    trough_lock.acquire()
    # TODO decide how to determine if target reached. If so exit.
    while run_updater.value:
        min_next_time = time.time() + 2.0
        cmdsend.send(['Send',''])
        waiting = True
        while waiting:
            if datarcv.poll():
                datapkg =datarcv.recv()
                # update figure and then call update_status
                if len(datapkg[1]) >= 1:
                    update_collection(datapkg, cals, lastdirection, run_updater, updater_running, run)
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
                Trough_GUI.status_widgets.update_status(update_dict, cals,
                                                        lastdirection)
                waiting = False
        if time.time()< min_next_time:
            time.sleep(min_next_time - time.time())
    # Release lock and set the shared I'm running flag to False before exiting.
    print("collect_data_updater releasing lock")
    trough_lock.release()
    updater_running.value = False
    Trough_GUI.Collect_data.end_of_run()
    print("collect_data_updater done")
    return

def update_collection(datapkg, cals, lastdirection, run_updater, updater_running, run):
    """Updates the graph and the data storage"""
    from pandas import DataFrame, concat
    import numpy as np
    from IPython import get_ipython
    Trough_GUI = get_ipython().user_ns["Trough_GUI"]
    plate_circumference = Trough_GUI.status_widgets.plate_circumference
    moles_molec = Trough_GUI.status_widgets.moles_molec
    on_stop_run = Trough_GUI.Collect_data.on_stop_run
    # do all the calculations on the new data
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
    sep_cm = np.array(sep_cm)
    sep_cm_stdev = np.array(sep_cm_stdev)
    area_sqcm = sep_cm*float(cals.barriers_open.additional_data[ \
                               "trough width (cm)"])
    area_sqcm_stdev = sep_cm_stdev*float(cals.barriers_open.additional_data[ \
                               "trough width (cm)"])


    area_per_molec_ang_sq_stdev = area_sqcm_stdev * 1e16 / moles_molec.value / 6.02214076e23
    area_per_molec_ang_sq = area_sqcm * 1e16 / moles_molec.value / 6.02214076e23
    mgrams, mgrams_err = cals.balance.cal_apply(bal_raw,bal_raw_stdev)
    mgrams = np.array(mgrams)
    mgrams_err = np.array(mgrams_err)
    surf_press_err = mgrams_err * 9.80665 / plate_circumference.value
    surf_press_data = (Trough_GUI.status_widgets.tare_pi-mgrams)*9.80665\
                      /plate_circumference.value
    tempC, tempC_stdev = cals.temperature.cal_apply(temp_raw, temp_raw_stdev)

    # add data to the dataframe
    newdata = DataFrame({"time_stamp":time_stamp,
                         "position_raw": pos_raw,
                         "postion_raw_stdev":pos_raw_stdev,
                         "balance_raw":bal_raw,
                         "balance_raw_stdev":bal_raw_stdev,
                         "temperature_raw":temp_raw,
                         "temperature_raw_stdev":temp_raw_stdev,
                         "Separation (cm)":sep_cm,
                         "Separation stdev":sep_cm_stdev,
                         "Area (cm^2)":area_sqcm,
                         "Area stdev":area_sqcm_stdev,
                         "Area per molecule (A^2)":area_per_molec_ang_sq,
                         "Area per molec stdev": area_per_molec_ang_sq_stdev,
                         "mg":mgrams,
                         "mg stdev":mgrams_err,
                         "Surface Pressure (mN/m)":surf_press_data,
                         "Surface Pressure stdev":surf_press_err,
                         "Deg C":tempC,
                         "Deg C stdev":tempC_stdev})
    if not isinstance(run.df, DataFrame):
        run.df = newdata.copy()
    else:
        run.df = concat([run.df,newdata], ignore_index=True) # This may be
        # costly. If so make the data frame only at the end.
        # TODO should I lock the dataframe or only make np.arrays until done.
    # update the graph
    x_data =[]
    y_data = run.df["Surface Pressure (mN/m)"]
    lastpos = None
    initpos = None
    if run.speed == 0:
        x_data = run.df["time_stamp"]-run.df["time_stamp"][0]
    else:
        if run.units == "cm":
            x_data = run.df["Separation (cm)"]
            lastpos = run.df["Separation (cm)"][len(run.df["Separation (cm)"])-1]
            initpos = run.df["Separation (cm)"][0]
        if run.units == "cm^2":
            x_data = run.df["Area (cm^2)"]
            lastpos = run.df["Area (cm^2)"][len(run.df["Area (cm^2)"])-1]
            initpos = run.df["Area (cm^2)"][0]
        if run.units == "Angstrom^2/molec":
            x_data = run.df["Area per molecule (A^2)"]
            lastpos = run.df["Area per molecule (A^2)"][len(run.df["Area per molecule (A^2)"])-1]
            initpos = run.df["Area per molecule (A^2)"][0]
    run.livefig.data[0].x = x_data
    run.livefig.data[0].y = y_data
    if (lastpos < initpos) and (lastpos <= run.target):
        # Stop collecting
        run_updater.value = False
    if (lastpos > initpos) and (lastpos >= run.target):
        # Stop collecting
        run_updater.value = False
    return