import os, errno, time
import piplates.DAQC2plate as DAQC2

def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only. From this stackoverflow suggestion:
    https://stackoverflow.com/a/6940314
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True

pidpath = '/tmp/troughctl.pid'
while true:
    if os.path.exists(pidpath):
        file=open(pidpath,'r')
        pid = int(file.readline())
        if not(pid_exists(pid)):
            DAQC2.clrDOUTbit(0, 0)  # switch off power/stop barriers
    else:
        DAQC2.clrDOUTbit(0, 0)  # switch off power/stop barriers
    time.sleep(1.0)