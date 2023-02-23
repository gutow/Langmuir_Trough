"""This file contains unit conversion utility functions for use in the GUI

 * To nest these functions replace the `value, err` part of the call with
   `*func(...)`. For example `sqcm_to_angpermolec(*cm_to_sqcm(9.2, 0.1, cals),
   cals)`
"""

def cm_to_sqcm(value, err, cals):
    """convert barrier separation in cm to trough area in sqcm"""
    from round_using_error import numbers_rndwitherr
    # TODO
    raise NotImplementedError

def sqcm_to_cm(value, err, cals):
    """convert trough area in sqcm to barrier separation in cm"""
    from round_using_error import numbers_rndwitherr
    # TODO
    raise NotImplementedError

def sqcm_to_angpermolec(value, err, moles):
    """convert trough area in sqcm to square angstroms per molecules"""
    from round_using_error import numbers_rndwitherr
    # TODO
    raise NotImplementedError

def mg_to_mNperm(value, err, pi_tare, plate_circ):
    """convert balance measurement in mg to milliNewtons per meter"""
    from round_using_error import numbers_rndwitherr
    surf_press_err = err*9.80665/plate_circ
    surf_press = (pi_tare - value) * 9.80665 / plate_circ
    return numbers_rndwitherr(surf_press,surf_press_err)

def nNperm_to_mg(value, err, pi_tare, plate_circ):
    """convert surface pressure in milliNewtons per meter to mg"""
    from round_using_error import numbers_rndwitherr
    mg_err = err / 9.80665 * plate_circ
    mg = pi_tare - value / 9.80665 * plate_circ
    return numbers_rndwitherr(mg, mg_err)
