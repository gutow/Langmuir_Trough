from ipywidgets import Layout, Box, HBox, VBox, GridBox, Tab, Accordion, \
    Dropdown, Label, Text, Button, Checkbox, FloatText, RadioButtons, \
    BoundedIntText, BoundedFloatText
from ipywidgets import HTML as richLabel
from ipywidgets import HTMLMath as texLabel
from IPython.display import display, HTML
from IPython.display import Javascript as JS

# Boilerplate style for long descriptions on ipywidget
longdesc = {'description_width': 'initial'}

# Barriers
# Manual Barrier Control
Barr_Target_Frac = 1.0
def on_change_Barr_Units(change):
    print(change)
    if change['new'] == 'cm':
        Barr_Target.min = calibrations.barriers.cal_apply(0.0,0.0)[0]
        Barr_Target.max = calibrations.barriers.cal_apply(1.0, 0.0)[0]
        Barr_Target.value = calibrations.barriers.cal_apply(Barr_Target_Frac,
                                                            0.0)[0]
    if change['new'] == 'cm^2':
        temptarg = calibrations.barriers.cal_apply(Barr_Target_Frac,0.0)[0]*\
                            float(Trough_Width.value) + float(Skimer_Correction.value)
        max = calibrations.barriers.cal_apply(1.0, 0.0)[0]*float(Trough_Width.value) +\
                          float(Skimer_Correction.value)
        min = calibrations.barriers.cal_apply(0.0,0.0)[0]*float(Trough_Width.value) +\
                          float(Skimer_Correction.value)
        Barr_Target.max = max
        Barr_Target.min = min
        Barr_Target.value = temptarg
    if change['new'] == 'Angstrom^2/molec':
        temptarg = calibrations.barriers.cal_apply(Barr_Target_Frac,0.0)[0]*\
                            float(Trough_Width.value) + \
                            float(Skimer_Correction.value)*\
                            1e16/moles_molec.value/6.02214076e23
        max = calibrations.barriers.cal_apply(1.0,0.0)[0]*\
                            float(Trough_Width.value) + \
                            float(Skimer_Correction.value)*\
                            1e16/moles_molec.value/6.02214076e23
        min = calibrations.barriers.cal_apply(0.0,0.0)[0]*\
                            float(Trough_Width.value) + \
                            float(Skimer_Correction.value)*\
                            1e16/moles_molec.value/6.02214076e23
        Barr_Target.max = max
        Barr_Target.min = min
        Barr_Target.value = temptarg
        pass
    # TODO Remove below after testing
    if change['new'] == '% of max':
        Barr_Target.min = 0.0
        Barr_Target.max = 1.0
        Barr_Target.value = Barr_Target_Frac
    pass

Barr_Units = Dropdown(description="Units",
                      options=["cm", "cm^2", "Angstrom^2/molec"])

Barr_Units.observe(on_change_Barr_Units, names='value')

def on_change_Barr_Direction(changed):
    if Barr_Direction.value == 'Move To':
        Barr_Target.disabled = False
    else:
        Barr_Target.disabled = True
    pass

Barr_Direction = RadioButtons(options=["Open", "Close", "Move To"])
Barr_Direction.observe(on_change_Barr_Direction, names='value')
Barr_Target = BoundedFloatText(value=Barr_Target_Frac, min=0.0, max=1.0,
                               step=0.1, disabled=True)
Barr_Speed = FloatText(description="Speed (/min)", value=1.0,
                       disabled=False)
def on_click_Start(change):
    from IPython import get_ipython
    cmdsend = get_ipython().user_ns["cmdsend"]
    speed = Barr_Speed.value / 100.0
    cmdsend.send(['Speed', speed])
    if Barr_Direction.value != 'Move To':
        direction = 0
        if Barr_Direction.value == 'Close':
            direction = -1
        elif Barr_Direction.value == 'Open':
            direction = 1
        cmdsend.send(['Direction', direction])
        cmdsend.send(['Start', ''])
    else:
        # TODO need to get cal_inv() working
        if Barr_Units.value == 'cm':
            Barr_Target_Frac =
        pass

Barr_Start = Button(description="Start")
Barr_Start.button_style = "success"
Barr_Start.on_click(on_click_Start)

def on_click_Stop(change):
    from IPython import get_ipython
    cmdsend = get_ipython().user_ns["cmdsend"]
    cmdsend.send(['Stop', ''])
    pass

Barr_Stop = Button(description="Stop")
Barr_Stop.button_style = "danger"
Barr_Stop.on_click(on_click_Stop)
