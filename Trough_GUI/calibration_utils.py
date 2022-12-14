"""Utilities for:
* writing and reading calibration files stored in the local
user directory `.Trough/calibrations`.
* fitting calibration data to generate calibration parameters.
* converting between raw signal and user-friendly values.
"""


class Calibration:
    def __init__(self, name, units, timestamp, param, param_stdev,
                 cal_data_x, cal_data_y, fit_type="polynomial",
                 fit_eqn_str = "y = C0 + C1*x + C2*x*x + C3*x*x*x + ...",
                 fit_ceof_lbls = ["C0", "C1", "C2", "C3", "C4", "C5", "C6",
                                  "C7"]):
        """
        Defines a calibration of type `name`.
        Parameters
        ----------
        name: str
            calibration name.

        units: str
            string representation of the units the calibration yields.

        timestamp: float
            Unix floating point timestamp.

        param:list
            list of the numerical parameters for the fit yielding the
            calibration.

        param_stdev: list
            list of the numerical values for the estimated standard
            deviation of the parameters from the fit.

        cal_data_x: list
            x-data used for the calibration fit.

        cal_data_y: list
            y-data used for the calibration fit.

        fit_type: str
            string name for the fit type. Defaults to "polynomial"
        """
        self.name = name
        self.units = units
        self.timestamp = timestamp
        self.param = param
        self.param_stdev = param_stdev
        self.cal_data_x = cal_data_x
        self.cal_data_y = cal_data_y
        self.fit_type = fit_type
        self.fit_eqn_str = fit_eqn_str
        self.fit_coef_lbls = fit_ceof_lbls
        if self.fit_type == "polynomial" and\
                len(self.param) != len(self.fit_coef_lbls):
            self.fit_coef_lbls = self.fit_coef_lbls[0:len(self.param)]

    @classmethod
    def cal_from_html(cls, html):
        """This takes in an html str, parses it and returns a new
        calibration.

        Parameters
        ----------
        html: str
            The html to be parsed to create the calibration object

        Returns
        -------
        calibration: calibration
            a calibration object.
        """
        from AdvancedHTMLParser import AdvancedHTMLParser as Parser
        from datetime import datetime

        document = Parser()
        document.parseStr(html)
        name = document.getElementById('name').text
        units = document.getElementById('units').text
        fit_type = document.getElementById('fit_type').text
        timestamp = float(document.getElementById('timestamp').text)
        coef_el = document.getElementById('coefficients')
        coef_val = []
        for k in coef_el.children:
            if k.tagName == 'td':
                coef_val.append(float(k.text))
        stdev_el = document.getElementById('stdev')
        coef_stdev = []
        for k in stdev_el:
            if k.tagName == 'td':
                coef_stdev.append(float(k.text))
        cal_el = document.getElementById('calibration_data')
        cal_x  = []
        cal_y = []
        for k in cal_el.getElementById('cal_data_x'):
            if k.tagName == 'td':
                cal_x.append(float(k.text))
        for k in cal_el.getElementById('cal_data_y'):
            if k.tagName == 'td':
                cal_y.append(float(k.text))
        return Calibration(name, units, timestamp, coef_val, coef_stdev,
                 cal_x, cal_y, fit_type=fit_type)

    def cal_to_html(self):
        """This routine creates an html str that would be human-readable in a
        browser detailing the calibration. This can be written to a file to
        store the calibration.

        Returns
        -------
        calib_div: str
            string containing the html detailing the calibration.
        """
        from AdvancedHTMLParser import AdvancedTag as Domel
        from datetime import datetime
        calib_div = Domel('div')
        calib_title = Domel('h3')
        calib_title.appendInnerHTML('Calibration of '+str(self.name))
        calib_div.appendChild(calib_title)

        calib_info = Domel('table')
        calib_info.setAttribute('class', 'calib_info')
        calib_info.setAttribute('id', 'calib_info')
        calib_info.setAttribute('border', '1')
        tr = Domel('tr')
        tr.appendInnerHTML('<th>Calibration of</th><th>Units returned</th>'
                           '<th>Fit function</th><th>Time</th>'
                           '<th>Timestamp</th>')
        calib_info.appendChild(tr)
        tr = Domel('tr')
        isotime = (datetime.fromtimestamp(self.timestamp)).isoformat()
        tr.appendInnerHTML('<td id = "name">'+str(self.name)+'</td>'
                           '<td id = "units">'+str(self.units)+'</td>'
                           '<td id = "fit_type">'+str(self.fit_type)+'</td>'
                           '<td id = "iso_time">'+str(isotime)+'</td>'
                           '<td id = "timestamp">'+str(self.timestamp)+'</td>')
        calib_info.appendChild(tr)
        calib_div.appendChild(calib_info)

        p = Domel('p')
        p.setAttribute('id','fit_eqn_str')
        p.appendInnerHTML('Fit Equation: '+ self.fit_eqn_str)
        calib_div.appendChild(p)

        parameters = Domel('table')
        parameters.setAttribute('class', 'parameters')
        parameters.setAttribute('id', 'parameters')
        parameters.setAttribute('border', '1')
        caption = Domel('caption')
        caption.appendInnerHTML('Parameters')
        parameters.appendChild(caption)
        tr = Domel('tr')
        tr.setAttribute('id', 'coef_labels')
        innerstr = '<th>Labels</th>'
        for k in self.fit_coef_lbls:
            innerstr += '<td>'+str(k) + '</td>'
        tr.appendInnerHTML(innerstr)
        parameters.appendChild(tr)
        tr = Domel('tr')
        tr.setAttribute('id', 'coefficients')
        innerstr = '<th>Coefficients</th>'
        for k in self.param:
            innerstr += '<td>'+str(k)+'</td>'
        tr.appendInnerHTML(innerstr)
        parameters.appendChild(tr)
        tr = Domel('tr')
        tr.setAttribute('id', 'stdev')
        innerstr = '<th>Standard Deviation</th>'
        for k in self.param_stdev:
            innerstr += '<td>'+str(k)+'</td>'
        tr.appendInnerHTML(innerstr)
        parameters.appendChild(tr)
        calib_div.appendChild(parameters)

        fit_data = Domel('table')
        fit_data.setAttribute('class', 'calibration_data')
        fit_data.setAttribute('id', 'calibration_data')
        fit_data.setAttribute('border', '1')
        caption = Domel('caption')
        caption.appendInnerHTML('Calibration Data')
        fit_data.appendChild(caption)
        tr = Domel('tr')
        tr.setAttribute('id', 'cal_data_x')
        innerstr = '<th>X Calibration Data</th>'
        for k in self.cal_data_x:
            innerstr += '<td>'+str(k)+'</td>'
        tr.appendInnerHTML(innerstr)
        fit_data.appendChild(tr)
        tr = Domel('tr')
        tr.setAttribute('id', 'cal_data_y')
        innerstr = '<th>Y Calibration Data</th>'
        for k in self.cal_data_y:
            innerstr += '<td>'+str(k)+'</td>'
        tr.appendInnerHTML(innerstr)
        fit_data.appendChild(tr)
        calib_div.appendChild(fit_data)
        return calib_div.asHTML()

    def cal_apply(self, data, stdev):
        """Apply the calibration to some data.

        Parameters
        ----------
        data: object
            either a float or iterable of floats

        stdev: object
            either a float or iterable of floats containing the uncertainty
            in the data

        Returns
        -------
        object
            the data after applying the calibration: a float or iterable of
            floats depending on what was passed to the operation.

        object
            the standard deviation of the data after applying the
            calibration: a float or iterable of floats depending on what was
            passed to the operation.
        """
        cal_data = None
        cal_stdev = None
        from collections.abc import Iterable
        from round_using_error.round_using_error import numbers_rndwitherr
        if isinstance(data,Iterable):
            cal_data = []
            cal_stdev = []
            import numpy as np
            npdata = np.array(data)
            npstdev = np.array(stdev)
            # calculate the new calibrated values and errors
            npcal_data = np.zeros(len(data))
            npcal_stdev = np.zeros(len(data))
            if self.fit_type == 'polynomial':
                coef_n = 0
                for j, k in zip(self.param,self.param_stdev):
                    npcal_data += j*npdata**coef_n
                    npcal_stdev += (coef_n*j*npdata**(coef_n-1)*npstdev)**2 + \
                                 (npdata**coef_n*k)**2
                    coef_n += 1
                npcal_stdev = npcal_stdev**0.5
                for j, k in zip(npcal_data,npcal_stdev):
                    j, k = numbers_rndwitherr(j,k)
                    cal_data.append(j)
                    cal_stdev.append(k)
            else:
                raise NotImplementedError('Only polynomial calibration '
                                          'implemented.')
        elif isinstance(data,float):
            # calculate the new calibrated value and error.
            # each polynomial term contributes x^2*n*u(x)^2 +
            # n^2*Cn^2*x^(2n-2)*u(Cn)^2 to the square of the uncertainty.
            cal_data = 0
            cal_stdev = 0
            if self.fit_type == 'polynomial':
                coef_n = 0
                for j, k in zip(self.param,self.param_stdev):
                    cal_data += j*data**coef_n
                    cal_stdev += (coef_n*j*data**(coef_n-1)*stdev)**2 + \
                                 (data**coef_n*k)**2
                    coef_n += 1
                cal_stdev = cal_stdev**0.5
                cal_data, cal_stdev = numbers_rndwitherr(cal_data,cal_stdev)
            else:
                raise NotImplementedError('Only polynomial calibration '
                                          'implemented.')
        else:
            raise TypeError('Data must be a float or an iterable of floats.')
        return cal_data, cal_stdev


class Calibrations:
    def __init__(self):
        #self.bal = self.get_bal()
        self.bal_param_default = [0, -0.0192425437271595]
        #self.barr = self.get_barr()
        self.barr_param_default = [-137.10895, 0.012425222, -3.6923632e-07,
                                   4.6662292e-12, -2.1849642e-17]
        #self.temp = self.get_temp()
        self.temp_param_default = [-55.47043609619141, 0.00352556980215013,
                                   -7.295400905604765e-08,
                                   7.455005037772244e-13]

    def read_cal(self, name):
        """This routine reads in a calibration file. If it is the standard
        html file it uses `calibration.cal_from_html()` operation to convert
        it to a calibration.

        Parameters
        ----------
        name: str
            either the basename (current options: 'balance', 'barriers' or
            'temperature') or a string representation of the path to the
            calibration file to be read. If one of the basenames is used
            this code will look for the most recent calibration of that type
            in the directory '~\.Trough\calibrations'.

        Returns
        -------
        Calibration
        """
        from pathlib import Path
        temppath = Path(name)
        path_parent = temppath.parent
        path_suffixes = temppath.suffixes
        fullpath = Path()
        if str(path_parent) == '.' and len(path_suffixes) == 0:
            basepath = Path('~/.Trough/calibrations').expanduser()
            filelist = list(basepath.glob(name+'_*.trh.cal.html'))
            filelist.sort()
            fullpath = filelist[-1:][0]
        else:
            fullpath = temppath
        f = open(fullpath,'r')
        tempdoc = f.read()
        f.close()
        return Calibration.cal_from_html(tempdoc)

    def write_cal(self, dirpath, cal, **kwargs):
        """
        Writes a calibration file with the base filename `cal.name + int(
        cal.timestamp)` into the directory specified. Currently only produces
        an html file that is also human-readable. Other file formats may be
        available in the future through the use of key word arguments.

        Parameters
        ----------
        dirpath:
            pathlike object or string
        cal: Calibration
            a calibration object containing the information about the
            calibration to write to the file.
        kwargs:
            optional key word arguments for future adaptibility
        """
        from pathlib import Path
        fileext = '.trh.cal.html'
        filename = str(cal.name) + '_' + str(int(cal.timestamp))+fileext
        fullpath = Path(dirpath,filename)
        svhtml = '<!DOCTYPE html><html><body>' + cal.cal_to_html() + \
                 '</body></html>'
        f = open(fullpath,'w')
        f.write(svhtml)
        f.close()
        pass

    def poly_fit(self, data_x, data_y, order):
        """Does a polynomial fit of the specified order using the x and y
        values provided.

        Parameters
        ----------
        data_x: list
            of numerical x values.
        data_y: list
            of numerical y values.
        order: int
            the order of the polynomical used for fitting.

        Returns
        -------
        param: list
            of fitted parameters.
        param_stdev: list
            of estimated standard deviation in the parameters.
        """
        import numpy as np
        import lmfit as lmfit
        from round_using_error.round_using_error import numbers_rndwitherr

        # Define the fit model, initial guesses, and constraints
        fitmod = lmfit.models.PolynomialModel(degree=order)
        for k in range(0, order+1):
            fitmod.set_param_hint("c"+str(k), vary=True, value=0.0)

        # Do fit
        fit = fitmod.fit(np.array(data_y), x=np.array(data_x),
                         nan_policy="omit")
        param = (order+1)*[None]
        param_stdev = (order+1)*[None]
        for k in fit.params.keys():
            pwr = int(str(k)[-1:])
            if pwr <= order:
                rounded = numbers_rndwitherr(fit.params[k].value,fit.params[k].stderr)
                param[pwr] = rounded[0]
                param_stdev[pwr] = rounded[1]
        return param, param_stdev
