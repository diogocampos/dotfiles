#!/bin/sh

[ -f ~/.no-announce-time ] && exit

speech_volume='31'
current_volume="`osascript -e 'output volume of (get volume settings)'`"

osascript -e "set volume output volume ${speech_volume}"
say -v Thomas "Il est `date +'%H:%M'`."
osascript -e "set volume output volume ${current_volume}"
