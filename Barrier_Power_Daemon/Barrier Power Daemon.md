## Deamon to prevent barrier crashing
The idea is to have a daemon service that depowers the trough
barriers if a process to monitor them is not running. This may
be overkill.

This Daemon must be set up using super user status.
It checks if a process with the process id
stored in `/tmp/troughctl.pid` is running. If the process is
not running it shuts down power to the barriers. Requires
the daemon python script run within a virtual environment
that has all the modules to access the DAQC2 plate.

## To set up
1. Gain super user status `sudo -i`.
2. Create a virtual environment for the daemon to run in:
   `python3 -m venv /usr/local/shared/trough`.
3. Navigate to this directory and activate this virtual environment:
   `source bin/activate`.
4. Install the piplates software and what it depends on: `python -m
pip install RPi.GPIO pi-plates`. This will not work on a computer
   that does not support Raspberry Pi-like GPIO.
5. Exit the virtual environment: `exit`.
6. Copy `troughdaemon.py` to the directory you virtual environment.
7. Edit the `trough.service` file to point to the relocated
   `troughdaemon.py`.
8. Copy `trough.service` to `/etc/systemd/user`.
9. Activate the daemon: `systemctl enable trough.service`.
10. Start the daemon: `systemctl start trough.service`.
11. Make sure the daemon is running: `systemctl status trough.service`.
   If it is not running troubleshoot using the error messages provided.
12. 