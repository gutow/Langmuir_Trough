import time
import piplates.DAQC2plate as DAQC2

def barrier_at_limit_check():
    """
    Checks if barrier is at or beyond limit and stops barrier if it is headed moving
    in a direction that would make it worse.
    
    Returns
    =======
    True or False. If True also shuts down power to barrier
    """
    direction = 0 # -1 closing, 0 stopped, 1 openning.
    if (DAQC2.getDAC(0,0)>=2.5):
        direction = -1
    else:
        direction = 1
    position = DAQC2.getADC(0,0)-DAQC2.getADC(0,1)
    if (position >= 7.78) and (direction == -1):
        DAQC2.clrDOUTbit(0,0) # switch off power/stop barriers
        return True
    if (position <= 0.005) and (direction == 1):
        DAQC2.clrDOUTbit(0,0) # switch off power/stop barriers
        return True
    return False

while True:
    barrier_at_limit_check()
    time.sleep(0.300)