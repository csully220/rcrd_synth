#!/bin/bash
export DBUS_SESSION_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
amixer sset 'Speaker' 90
fluidsynth -a alsa -sv /usr/share/sounds/sf2/FluidR3_GM.sf2


