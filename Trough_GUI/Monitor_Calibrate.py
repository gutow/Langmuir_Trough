def Monitor_Setup_Trough():
    """
    This produces a user interface in jupyter notebooks using ipywidgets. The
    interface allows monitoring of the trough barrier positions, balance
    signal, and temperature signal. The barrier positions can be
    adjusted using this interface. Calibrations of all the signals are
    performed using this interface.

    Calibrations are stored in the file "calibXXXX.html" in the .Trough
    directory of the current user. The latest file is used. If none exists
    one is created using default parameters. Users should calibrate all
    signals before using the trough.
    """
    from ipywidgets import Layout, Box, HBox, VBox, GridBox, Tab, Accordion, \
        Dropdown, Label, Text, Button, Checkbox, FloatText, RadioButtons, \
        BoundedIntText
    from ipywidgets import HTML as richLabel
    from ipywidgets import HTMLMath as texLabel
    from IPython.display import display, HTML
    from IPython.display import Javascript as JS

    # Boilerplate layout for long descriptions on ipywidget
    longdesc = {'description_width': 'initial'}

    # Balance Monitoring
    balance_label = Label(value="BALANCE:")
    mg = Text(description = "mg",
                disabled = True,
                style =longdesc)
    surf_press = Text(description = "$\pi$ (mN/m)",
                        disabled = True,
                        style =longdesc)
    plate_circumference = FloatText(description = "Plate circumference (mm)",
                                    value = 21.5,
                                    style =longdesc)
    zero_press = Button(description = "Zero Pressure")
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
    degC = Text(description = "$^o C$",
                disabled = True,
                style =longdesc)
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
    barrier_label = Label(value = "BARRIERS:")
    Bar_Frac = Text(description = "% open", disabled = True, style = longdesc)
    Bar_Sep = Text(description = "Separation (cm)", disabled = True,
                   style = longdesc)
    Bar_Area = Text(description = "Area", disabled = True, style = longdesc)
    Bar_Area_per_Molec = Text(description = "$\mathring{A^2}$/molecule",
                              disabled = True, style = longdesc)
    moles_molec = FloatText(description = "moles of molecules",
                            value = 3.00e-8, style = longdesc)
    Barrier = HBox(children = [barrier_label,
                               VBox(children=[Bar_Frac,Bar_Sep,Bar_Area]),
                               VBox(children=[moles_molec,
                                              Bar_Area_per_Molec])],
                               layout = Layout(border="solid"))
    # Manual Barrier Control
    Barr_Units = Dropdown(description = "Units",
                          options = ["% of max", "cm", "cm^2",
                                     "Angstrom^2/molec"])
    Barr_Direction = RadioButtons(options=["Open", "Close", "Move To"])
    Barr_Target = FloatText(value = 100.0, disabled = True)
    Barr_Speed = FloatText(description = "Speed (/min)", value = 100.0,
                           disabled = False)
    Barr_Start = Button(description = "Start")
    Barr_Start.button_style = "success"
    Barr_Stop = Button(description = "Stop")
    Barr_Stop.button_style = "danger"
    Move_Barrier = HBox(children =[VBox(children=[Barr_Direction, Barr_Target]),
                        VBox(children=[Barr_Units, Barr_Speed]),
                                   VBox(children=[Barr_Start,Barr_Stop])])
    # Barrier Calibration
    Barr_Raw = Text(description = "Barrier Raw (V)", disabled = True,
                   style=longdesc)
    Barr_Cal_Val = FloatText(description = "Measured Barrier Separation (cm)",
                            disabled = False, style = longdesc)
    Trough_Width = FloatText(description = "Trough width (cm)", value = 9.525,
                             disabled = False, style = longdesc)
    Skimer_Correction = FloatText(description = "Skimmer Correction ($cm^2$)",
                                  value = -0.5, disabled = False,
                                  style = longdesc)
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

    # Status
    Status = richLabel(layout = Layout(border="solid"), value =
    '<p>Status messages will appear here.</p>')

    # Monitor, Control and Calibrate widget
    Mon_Ctl_Calib = VBox(children=[Balance, Cal_Bal, Temperature, Cal_Temp,
                                   Barrier, Barrier_Accord, Status])
    display(Mon_Ctl_Calib)
    pass