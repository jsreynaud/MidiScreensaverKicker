#!/usr/bin/python3
#
#  Kick the screensaver by sending a SimulateActivity via dbus
# when a midi event occur
#
# To use on ubuntu
# apt install python3-mido python3-dbus
#
# then manualy start (or add on autostart)
#
import dbus
import time
import mido

# Track last time we send the kick
last_send = time.time()


def get_msg(msg):
    # On message receive: SimulateActivity
    global last_send
    print(msg)
    t = time.time()
    if (t - last_send) > 30:
        last_send = t
        print("ping")
        saver_interface.SimulateUserActivity()


# Open dbus interface
bus = dbus.SessionBus()
saver = bus.get_object('org.freedesktop.ScreenSaver', '/ScreenSaver')
saver_interface = dbus.Interface(saver, dbus_interface='org.freedesktop.ScreenSaver')


print("start")
# Add a callback on each midi input port
inports = mido.get_input_names()
for i in inports:
    mido.open_input(i, callback=get_msg)

# Finaly wait forever...
while True:
    time.sleep(3660)
