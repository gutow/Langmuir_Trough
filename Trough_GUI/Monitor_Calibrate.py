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
    from ipywidgets import layout, Box, HBox, VBox, GridBox, Tab, Accordian, \
        Dropdown, Label, Text, Button, Checkbox, FloatText, RadioButtons, \
        BoundedIntText
    from ipywidgets import HTML as richLabel
    from ipywidgets import HTMLMath as texLabel
    from IPython.display import display, HTML
    from IPython.display import Javascript as JS