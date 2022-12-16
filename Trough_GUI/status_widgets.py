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

def set_zero_pressure():
    tare_pi = float(surf_press.value)
    update_status()
    pass

zero_press = Button(description="Zero Pressure")

degC = Text(description="$^o C$",
            disabled=True,
            style=longdesc)

Bar_Frac = Text(description="% open", disabled=True, style=longdesc)
Bar_Sep = Text(description="Separation (cm)", disabled=True,
               style=longdesc)
Bar_Area = Text(description="Area ($cm^2$)", disabled=True, style=longdesc)
Bar_Area_per_Molec = Text(description="$\mathring{A^2}$/molecule",
                          disabled=True, style=longdesc)
moles_molec = FloatText(description="moles of molecules",
                        value=3.00e-8, style=longdesc)

Status = richLabel(layout=Layout(border="solid"), value=
'<p>Status messages will appear here.</p>')

def update_status(raw_data:dict, calibrations):
    """
    Call this routine to update the contents of all the status widgets.

    Parameters
    ----------
    raw_data: dict
        dictionary of latest raw data values for each
        sensor (e.g. {'bal_raw':3.20,'barr_raw':0.5,'temp_raw':2.24})

    calibrations: Calibrations
        Object containing the calibrations for the trough (currently
        `.balance`, `.barriers` and `.temperature`). A call to
        `.balance.cal_apply(raw_data)` will return the balance reading in the
        calibration units (`.balance.units`).
    """
    if calibrations.balance.units != 'mg':
        raise ValueError('Expect balance to be calibrated in mg. Instead got '
                         + calibrations.balance.units + '.')
    mg.value = str(calibrations.balance.cal_apply(raw_data['bal_raw'],0)[0])
    surf_press.value = str(tare_pi-float(mg.value)*\
                           9.80665/plate_circumference.value)
    if calibrations.temperature.units != 'C':
        raise ValueError('Expected temperature to be calibrated in C. '
                         'Instead got ' + calibrations.temperature.units + '.')
    degC.value = str(calibrations.temperature.cal_apply(raw_data['temp_raw'],
                                                      0)[0])
    Bar_Frac.value = str(raw_data['barr_raw']*100)
    if calibrations.barriers.units != 'cm':
        raise ValueError('Expected barrier separation to be calibrated in cm. '
                         'Instead got ' + calibrations.barriers.units + '.')
    sep_cm = calibrations.barriers.cal_apply(raw_data['barr_raw'], 0)[0]
    area_cm_sq = sep_cm*calibrations.barriers.\
                         additional_data["trough width (cm)"] - \
                         calibrations.barriers.\
                         additional_data["skimmer correction (cm^2)"]
    area_per_molec_ang_sq = area_cm_sq*1e16/moles_molec.value/6.02214076e23
    Bar_Sep.value = str(sep_cm)
    Bar_Area.value = str(area_cm_sq)
    Bar_Area_per_Molec.value = str(area_per_molec_ang_sq)
    pass