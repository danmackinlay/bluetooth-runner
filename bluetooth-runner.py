#!/usr/bin/env python

import sys
import signal
import logging
import dbus
import dbus.service
import dbus.mainloop.glib
import gi.repository.GLib
import time

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
    # It would be nice if I knew enough dbus to run this only on
    # appropriate dbus events for appropriate dbus devices
    # but I don't.
    time.sleep(3)
    try:
        devcode = subprocess.check_output([
            'xinput', 'list', '--id-only',
            "Bluetooth Mouse M336/M337/M535 Mouse"
        ]).decode('ascii').strip()
        propstring = subprocess.check_output([
            'xinput', 'list-props',
            devcode ]).decode('ascii')
        match = re.search(
            r'Natural Scrolling Enabled \(([\d]*)\)', propstring)
        if match:
            propcode = match.group(1)
            subprocess.call([
                'xinput', 'set-prop', devcode, propcode, '1'])
        else:
            logging.error(
              "Unable to find the right prop code in '{0}'.".format(
                propstring))
    except subprocess.CalledProcessError as ex:
        logging.error("xinput error '{0}'.".format(ex))

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
