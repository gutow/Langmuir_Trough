"""This file contains widgets that display updating trough information and
can be used in multiple ipywidget panels within the same notebook."""

from ipywidgets import Layout, Box, HBox, VBox, GridBox, Tab, Accordion, \
    Dropdown, Label, Text, Button, Checkbox, FloatText, RadioButtons, \
    BoundedIntText
from ipywidgets import HTML as richLabel
from ipywidgets import HTMLMath as texLabel

# Boilerplate style for long descriptions on ipywidget
longdesc = {'description_width': 'initial'}

# Used for surface pressure. Balance zero set during calibration.
tare_pi = 72.00
mg = Text(description="mg",
          disabled=True,
          style=longdesc)
surf_press = Text(description="$\pi$ (mN/m)",
                  disabled=True,
                  style=longdesc)
plate_circumference = FloatText(description="Plate circumference (mm)",
                                value=21.5,
                                style=longdesc)
zero_press = Button(description="Zero Pressure")

degC = Text(description="$^o C$",
            disabled=True,
            style=longdesc)

Bar_Frac = Text(description="% open", disabled=True, style=longdesc)
Bar_Sep = Text(description="Separation (cm)", disabled=True,
               style=longdesc)
Bar_Area = Text(description="Area", disabled=True, style=longdesc)
Bar_Area_per_Molec = Text(description="$\mathring{A^2}$/molecule",
                          disabled=True, style=longdesc)
moles_molec = FloatText(description="moles of molecules",
                        value=3.00e-8, style=longdesc)

Status = richLabel(layout=Layout(border="solid"), value=
'<p>Status messages will appear here.</p>')

def update_status(raw_data:dict, calib_func:dict):
    """
    Call this routine to update the contents of all the status widgets.

    Parameters
    ----------
    raw_data: dict
        dictionary of latest raw data values (volts) for each
        sensor (e.g. {'bal_raw':3.20,'barr_raw':4.55,'temp_raw':2.24})
    It might be better to use an object which initializes itself for below:
    calib_func: dict
        dictionary pointing to globally accessible objects/functions that
        return the calibration in base units of mg for the balance, % open for
        the barriers and degC for the temperature.
    """
    mg.value = calib_func['bal_cal'](raw_data['bal_raw'])
    surf_press.value = tare_pi-mg.value*9.80665/plate_circumference.value
    degC.value = calib_func['temp_cal'](raw_data['temp_raw'])
    Bar_Frac.value = raw_data['barr_raw']
    Bar_Sep.value = calib_func['barr_cal'](raw_data['barr_raw'])
    # TODO rest of them
    pass