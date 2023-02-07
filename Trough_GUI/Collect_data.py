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
    run_start_stop = Button(description="Run",
                            button_style="success")
    def on_store_settings(change):
        # TODO create the run object
        # TODO Create the collection display
        # TODO clear output and display collection
        #   with fixed param and start run button.
        pass
    store_settings.on_click(on_store_settings)
    settings_HBox3 = HBox([Label("Target", style=longdesc), Barr_Target,
                           store_settings])
    settings_VBox = VBox([settings_HBox1,settings_HBox2, settings_HBox3])
    settings_Acc = Accordion([settings_VBox])
    settings_Acc.set_title(0, "Settings")
    status_Acc.selected_index = 0
    Barr_Target.disabled = False
    display(top_HBox, status_Acc, settings_Acc)
    def on_run_start_stop(change):
        # TODO take over status updating
        # TODO Start run (show or convert to stop button)
        run_start_stop.description = "Stop"
        run_start_stop.button_style = "danger"
        # TODO display data as collected
        pass

    def on_stop_run():
        # TODO Stop run
        # TODO Store data
        # TODO Display final data
        # TODO release status updating
        pass
    return