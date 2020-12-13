#!/usr/bin/python3

import sys
import signal
import logging
import dbus
import dbus.service
import dbus.mainloop.glib
import gi.repository.GLib
import time
import subprocess
import re

LOG_LEVEL = logging.INFO
#LOG_LEVEL = logging.DEBUG
LOG_FILE = "/dev/stdout"
#LOG_FILE = "/var/log/syslog"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

def properties_changed(
        interface,
        changed,
        invalidated,
        path,
        *args, **kwargs):
    time.sleep(3)
    try:
        resstring = subprocess.check_output([
            'restore_logitech_scroll'
        ]).decode('ascii')
    except subprocess.CalledProcessError as ex:
        logging.error("subproc error '{0}'.".format(ex))

def shutdown(signum, frame):
    mainloop.quit()

if __name__ == "__main__":
    # shut down on a TERM signal
    signal.signal(signal.SIGTERM, shutdown)

    # start logging
    logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info("Starting to monitor Bluetooth connections")

    # get the system bus
    try:
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
    except Exception as ex:
        logging.error("Unable to get the system dbus: '{0}'. Exiting."
                      " Is dbus running?".format(ex.message))
        sys.exit(1)

    # listen for signals on the Bluez bus
    bus.add_signal_receiver(
        properties_changed,
        dbus_interface = "org.freedesktop.DBus.Properties",
        signal_name = "PropertiesChanged",
        arg0 = "org.bluez.Device1",
        path_keyword = "path")
    try:
        mainloop = gi.repository.GLib.MainLoop()
        mainloop.run()
    except KeyboardInterrupt:
        pass
    except:
        logging.error("Unable to run the gobject main loop")

    logging.info("Shutting down bluetooth-runner")
    sys.exit(0)
