def troughctl():
    """
    Will run as separate process taking in commands through a pipe and returning data
    on demand through a second pipe.
    Iteration 1, collects data into a fifo and watches barrier position.
    """
    import time
    import numpy as np
    from collections import deque
    from piplates import DAQC2plate as DAQC2

    def barrier_at_limit_check(openlimit, closelimit):
        """
        Checks if barrier is at or beyond limit and stops barrier if it is moving
        in a direction that would make it worse.
        :param float openlimit: lowest voltage allowed for opening
        :param float closelimit: highest voltage allowed for closing

        Returns
        =======
        True or False. If True also shuts down power to barrier
        """

        direction = 0  # -1 closing, 0 stopped, 1 openning.
        if (DAQC2.getDAC(0, 0) >= 2.5):
            direction = -1
        else:
            direction = 1
        position = DAQC2.getADC(0, 0) - DAQC2.getADC(0, 1)
        if (position >= closelimit) and (direction == -1):
            DAQC2.clrDOUTbit(0, 0)  # switch off power/stop barriers
            return True
        if (position <= openlimit) and (direction == 1):
            DAQC2.clrDOUTbit(0, 0)  # switch off power/stop barriers
            return True
        return False

    poshigh = []
    poslow = []
    balhigh = []
    ballow = []
    thermhigh = []
    thermlow = []

    pos_V = deque(maxlen=5)
    pos_std = deque(maxlen=5)
    bal_V = deque(maxlen=5)
    bal_std = deque(maxlen=5)
    therm_V = deque(maxlen=5)
    therm_std = deque(maxlen=5)
    time_stamp = deque(maxlen=5)
    cmd_deque = deque()

    timedelta = 0.500  # seconds
    openmin = 0.005 # minimum voltage allowed when opening.
    openlimit = openmin
    closemax = 7.78 # maximum voltage allowed when closing.
    closelimit = closemax
    run = True
    while run:
        starttime = time.time()
        stopat = starttime + timedelta - 0.200  # leave 200 ms for communications and control
        while (time.time() < stopat):
            poslow.append(DAQC2.getADC(0, 1))
            poshigh.append(DAQC2.getADC(0, 0))
            ballow.append(DAQC2.getADC(0, 3))
            balhigh.append(DAQC2.getADC(0, 2))
            thermlow.append(DAQC2.getADC(0, 4))
            thermhigh.append(DAQC2.getADC(0, 5))
        time_stamp.append((starttime + stopat) / 2)
        # position
        ndata = len(poshigh)
        high = np.array(poshigh, dtype=np.float64)
        low = np.array(poslow, dtype=np.float64)
        vals = high - low
        avg = (np.sum(vals)) / ndata
        stdev = np.std(vals, ddof=1, dtype=np.float64)
        stdev_avg = stdev / np.sqrt(float(ndata))
        pos_V.append(avg)
        pos_std.append(stdev_avg)
        # balance
        ndata = len(balhigh)
        high = np.array(balhigh, dtype=np.float64)
        low = np.array(ballow, dtype=np.float64)
        vals = high - low
        avg = (np.sum(vals)) / ndata
        stdev = np.std(vals, ddof=1, dtype=np.float64)
        stdev_avg = stdev / np.sqrt(float(ndata))
        bal_V.append(avg)
        bal_std.append(stdev_avg)
        # thermistor
        ndata = len(thermhigh)
        high = np.array(thermhigh, dtype=np.float64)
        low = np.array(thermlow, dtype=np.float64)
        vals = high - low
        avg = (np.sum(vals)) / ndata
        stdev = np.std(vals, ddof=1, dtype=np.float64)
        stdev_avg = stdev / np.sqrt(float(ndata))
        therm_V.append(avg)
        therm_std.append(stdev_avg)

        # Check barrier positions
        if openlimit < openmin:
            openlimit = openmin
        if closelimit > closemax:
            closelimit = closemax
        barrier_at_limit = barrier_at_limit_check(openlimit,closelimit)
        # Send warnings and error messages
        # Check command pipe and update command queue
        # Each command is a python list.
        #    element 1: cmd name (string)
        #    element 2: single command parameter (number or string)
        # Execute commands in queue
        while len(cmd_deque) > 0:
            cmd = cmd_deque.popleft()
            # execute the command
            if cmd[0] == 'Stop':
                DAQC2.clrDOUTbit(0, 0)  # switch off power/stop barriers
            elif cmd[0] == 'Send':
                # send current contents of the data deques
            elif cmd[0] == 'Start':
                # start barriers moving using current direction and speed
            elif cmd[0] == 'Direction':
                # set the direction
            elif cmd[0] == 'Speed':
                # set the speed
            elif cmd[0] == 'MoveTo':
                # adjust direction if necessary
                # set the stop position
                # start the barriers
            elif cmd[0] == 'MotorCal':
                # calibrate the voltages for starting motor and speeds
            elif cmd[0] == 'ConstPi':
        # maintain a constant pressure
        # not yet implemented
        # Delay if have not used up all 200 ms
        used = time.time() - starttime
        if used < 0.495:
            time.sleep(0.495 - used)
