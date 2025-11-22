#!/usr/bin/python3
#
#  Kick the screensaver by sending a SimulateActivity via dbus
# when a midi event occur
#
# To use on ubuntu
# apt install python3-mido python3-dbus python3-rtmidi xdotool
#
# then manualy start (or add on autostart)
#
import time
import mido
import argparse
import subprocess
import os

# Track last time we send the kick
last_send = time.time()


class ScreenSaverKick:

    def __init__(self):
        # Test /usr/bin/xdotool exist
        if not os.path.exists("/usr/bin/xdotool"):
            print("!!!!! Error: xdotool is unavailable. Please install it")

    def Kick(self):
        subprocess.run(["xdotool", "key", "ctrl"])


def get_msg(msg):
    # On message receive: SimulateActivity
    global last_send
    # print(msg)
    t = time.time()
    if (t - last_send) > 5:
        last_send = t
        print("ping")
        saver_interface.Kick()


# Open dbus interface
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="verbose", action="store_true")
parser.add_argument("-s", "--simulate", help="simulate action on screensaver", action="store_true")
args = parser.parse_args()

saver_interface = ScreenSaverKick()


if args.simulate:
    saver_interface.Kick()
else:
    print("Start")
    # Add a callback on each midi input port
    inports = mido.get_input_names()
    for i in inports:
        print("Connect to {}".format(i))
        mido.open_input(i, callback=get_msg)

    # Finaly wait forever...
    while True:
        time.sleep(3660)
