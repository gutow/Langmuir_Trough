import Trough_GUI.status_widgets
from Trough_GUI.status_widgets import *
from Trough_GUI.command_widgets import *
from Trough_GUI import trough_lock
from IPython import get_ipython
cmdsend = get_ipython().user_ns["cmdsend"]
datarcv = get_ipython().user_ns["datarcv"]
def Monitor_Setup_Trough(calibrations):
    """
    This produces a user interface in jupyter notebooks using ipywidgets. The
    interface allows monitoring of the trough barrier positions, balance
    signal, and temperature signal. The barrier positions can be
    adjusted using this interface. Calibrations of all the signals are
    performed using this interface.

    Calibrations are stored in the calibration files in the .Trough/calibrations
    directory of the current user. The latest file is used. If none exists
    one is created using default parameters. Users should calibrate all
    signals before using the trough.

    NOTE: some objects used here are global and created by importing from
    status_widgets.py and command_widgets.py.

    Parameters
    ----------
    calibrations: Calibrations
        The object containing the calibrations be used and modified. See
        `Trough_GUI.calibration_utils`.
    """
    from ipywidgets import Layout, Box, HBox, VBox, GridBox, Tab, Accordion, \
        Dropdown, Label, Text, Button, Checkbox, FloatText, RadioButtons, \
        BoundedIntText, BoundedFloatText
    from ipywidgets import HTML as richLabel
    from ipywidgets import HTMLMath as texLabel
    from IPython.display import display, HTML
    from IPython.display import Javascript as JS

    # Boilerplate style for long descriptions on ipywidget
    longdesc = {'description_width': 'initial'}

    # Balance Monitoring
    balance_label = Label(value="BALANCE:")
    Balance = HBox(children = [balance_label,VBox(children =[
        mg, surf_press]), VBox(children = [plate_circumference,zero_press])],
                   layout = Layout(border="solid"))
    # Balance Calibration
    Bal_Cal_Butt = Button(description = "Start Calibration")
    Bal_Raw = Text(description = 'Balance Raw (V):',
                   disabled = True,
                   style = longdesc)
    Bal_Cal_Mass = FloatText(description = 'Mass (mg):',
                             value = 120.0,
                             disabled = False,
                             style = longdesc)
    Bal_Cal_Instr = richLabel(value = '<ol><li>Collect 5 calibration masses of'
                                      ' 120 mg or less.</li>'
                                      '<li>Click "Start Calibration".</li> '
                                      '<li>Place the'
                                      ' first mass on the balance and '
                                      'enter its mass.</li>'
                                      '<li>When the raw reading is stable click'
                                      ' "keep".</li>'
                                      '<li>Repeat for each calibration '
                                      'mass.</li></ol>'
                                      'The button will revert to "Start '
                                      'Calibration" when done.')
    Bal_Cal_Box = VBox(children = [Bal_Cal_Instr,HBox(children=[Bal_Raw,
                                                                Bal_Cal_Mass,
                                                                Bal_Cal_Butt])])
    Cal_Bal = Accordion(children = [Bal_Cal_Box])
    Cal_Bal.set_title(0,'Calibrate Balance')
    Cal_Bal.selected_index = None

    # Temperature Monitoring
    temp_label = Label(value = "TEMPERATURE:")
    Temperature = HBox(children=[temp_label,degC],
                   layout = Layout(border="solid"))
    # Temperature Calibration
    Temp_Raw = Text(description ="Temperature Raw (V)", disabled = True,
                    style = longdesc)
    Temp_Cal_Val = FloatText(description = "Actual $^o C$", disabled = False,
                             style = longdesc)
    Temp_Cal_Butt = Button(description = "Start Calibration")
    Temp_Cal_Instr = richLabel(value = '<ol><li>Gather 5 liquid temperature '
                                       'references.</li>'
                                       '<li>Click "Start Calibration".</li>'
                                       '<li>Place the temperature probe in '
                                       'the first reference.</li>'
                                       '<li>When the raw reading is stable '
                                       'click "keep".</li>'
                                       '<li>Repeat for each temperature '
                                       'reference.</li></ol>'
                                       'The button will revert to "Start '
                                       'Calibration" when done.')
    Temp_Cal_Box = VBox(children = [Temp_Cal_Instr,HBox(children = [Temp_Raw,
                                                                Temp_Cal_Val,
                                                                Temp_Cal_Butt
                                                                    ])])
    Cal_Temp = Accordion(children = [Temp_Cal_Box])
    Cal_Temp.set_title(0,'Calibrate Temperature')
    Cal_Temp.selected_index = None

    # Barrier Monitoring
    barrier_label = Label(value="BARRIERS:")
    Barrier = HBox(children = [barrier_label,
                               VBox(children=[Bar_Frac,Bar_Sep,Bar_Area]),
                               VBox(children=[moles_molec,
                                              Bar_Area_per_Molec])],
                               layout=Layout(border="solid"))



    Move_Barrier = HBox(children=[VBox(children=[Barr_Direction, Barr_Target]),
                        VBox(children=[Barr_Units, Barr_Speed]),
                                   VBox(children=[Barr_Start,Barr_Stop])])
    # Barrier Calibration
    open_steps = [{"speed":0.1, "target":0.5, "speed_data":True, "position":False},
                   {"speed":1.0, "target":0.10, "speed_data":True, "position":True},
                   {"speed": 0.2, "target": 0.15, "speed_data": True, "position": False},
                   {"speed": 0.9, "target": 0.30, "speed_data": True, "position": True},
                   {"speed": 0.3, "target": 0.35, "speed_data": True, "position": False},
                   {"speed": 0.8, "target": 0.50, "speed_data": True, "position": True},
                   {"speed": 0.4, "target": 0.55, "speed_data": True, "position": False},
                   {"speed": 0.7, "target": 0.70, "speed_data": True, "position": True},
                   {"speed": 0.5, "target": 0.85, "speed_data": True, "position": False},
                   {"speed": 0.6, "target": 1.0, "speed_data": True, "position": True}]
    close_steps = [{"speed":0.1, "target":0.95, "speed_data":True, "position":False},
                   {"speed":1.0, "target":0.80, "speed_data":True, "position":True},
                   {"speed": 0.2, "target": 0.75, "speed_data": True, "position": False},
                   {"speed": 0.9, "target": 0.60, "speed_data": True, "position": True},
                   {"speed": 0.3, "target": 0.55, "speed_data": True, "position": False},
                   {"speed": 0.8, "target": 0.40, "speed_data": True, "position": True},
                   {"speed": 0.4, "target": 0.45, "speed_data": True, "position": False},
                   {"speed": 0.7, "target": 0.20, "speed_data": True, "position": True},
                   {"speed": 0.5, "target": 0.10, "speed_data": True, "position": False},
                   {"speed": 0.6, "target": 0.0, "speed_data": True, "position": True}
                   ]
    calibrating_barr_direction = "close"
    calibrating_barr_step = 0
    def on_calib_barr(change):
        nonlocal calibrating_barr_direction
        nonlocal calibrating_barr_step
        steps = None
        if Barr_Cal_Butt.description == 'Start Calibration':
            # begin the calibration by opening the trough
            Barr_Cal_Butt.description = 'Moving...'
            Barr_Cal_Butt.disabled = True
            trough_lock.acquire()
            cmdsend.send(['Speed', 1.0])
            cmdsend.send(['Direction', 1.0])
            cmdsend.send(['Start', ''])
            trough_lock.release()
            while Trough_GUI.status_widgets.Bar_Frac.value < 100.0:
                # We wait
                pass
        if Barr_Cal_Butt.description == 'Keep':
            # we need to keep the position data
            pass
        if calibrating_barr_direction == 'open':
            steps = open_steps
        elif calibrating_barr_direction == 'close':
            steps = close_steps
        # Move barriers according to step and collect some data

        # Update step information
        if calibrating_barr_step == len(steps) - 1:
            # next time we will go the other way
            if calibrating_barr_direction == 'open':
                calibrating_barr_direction = 'done'
            elif calibrating_barr_direction == 'close':
                calibrating_barr_direction = 'open'
            calibrating_barr_step = 0
        else:
            calibrating_barr_step += 1

        # If we are done clean up and reset the buttons
        if calibrating_barr_direction == 'done':
            Barr_Cal_Butt.description = 'Start Calibration'
            calibrating_barr_direction == 'close'
            calibrating_barr_step = 0
            # do the fitting and save the data
        pass

    Barr_Raw = Text(description = "Barrier Raw (V)", disabled = True,
                   style=longdesc)
    Barr_Cal_Val = FloatText(description = "Measured Barrier Separation (cm)",
                            disabled = False, style = longdesc)
    Trough_Width = FloatText(description="Trough width (cm)",
                                value=calibrations.barriers.\
                                additional_data['trough width (cm)'],
                                disabled = False, style = longdesc)
    Skimer_Correction = FloatText(description = "Skimmer Correction ($cm^2$)",
                                value= calibrations.barriers.\
                                additional_data['skimmer correction (cm^2)'],
                                disabled=False, style=longdesc)
    Barr_Cal_Butt = Button(description = "Start Calibration")
    Barr_Cal_Instr = richLabel(value = '<span style="color:red;">Do Not '
                                       'adjust the trough width or skimmer '
                                       'corrections without accounting for '
                                       'curvature of the surface and the '
                                       'skimmers.</span>'
                                       '<ol><li>Get a ruler with a precision '
                                       'of 0.1 cm or better that is long '
                                       'enough to measure the distance '
                                       'between the barriers when they are '
                                       'fully open.</li>'
                                       '<li>Click on "Start Calibration".</li>'
                                       '<li>When the button converts to '
                                       '"keep" measure the distance between '
                                       'the barriers.</li>'
                                       '<li>Enter the measured value. '
                                       'Make sure the raw value is stable. '
                                       'Then click "keep".</li>'
                                       '<li>Repeat.</li></ol>'
                                       'The button will revert to "Start '
                                       'Calibration" when done.')
    Barr_Adjust_Rarely = VBox(children =[Trough_Width, Skimer_Correction])
    Barr_Adjust_Box = VBox(children = [Barr_Raw, Barr_Cal_Val])
    Barr_Cal_Box = VBox(children = [Barr_Cal_Instr,
                                    HBox(children = [ Barr_Adjust_Rarely,
                                                      Barr_Adjust_Box,
                                                      Barr_Cal_Butt])])
    Barrier_Accord = Accordion(children=[Move_Barrier,Barr_Cal_Box])
    Barrier_Accord.set_title(0, "Manual Barrier Control")
    Barrier_Accord.set_title(1, "Calibrate Barriers")
    Barrier_Accord.selected_index = None

    # Monitor, Control and Calibrate widget
    Mon_Ctl_Calib = VBox(children=[Balance, Cal_Bal, Temperature, Cal_Temp,
                                   Barrier, Barrier_Accord, Status])
    display(Mon_Ctl_Calib)
    pass