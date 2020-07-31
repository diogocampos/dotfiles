#!/bin/sh

time_volume='31'
prev_volume="`osascript -e 'output volume of (get volume settings)'`"

osascript -e "set volume output volume ${time_volume}"
say -v Thomas "Il est `date +'%H:%M'`."
osascript -e "set volume output volume ${prev_volume}"
