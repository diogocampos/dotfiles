#!/bin/sh

[ -f ~/.no-announce-time ] && exit

dir="$(dirname "$0")"

volume='31'
prev_volume="`osascript -e 'output volume of (get volume settings)'`"
if [ "$prev_volume" -gt "$volume" ] ; then
  osascript -e "set volume output volume ${volume}"
fi

# Français
#say -v Thomas "Il est `date +'%H:%M'`."

# 日本語
"$dir"/jp-time.py | say -v Otoya

if [ "$prev_volume" -gt "$volume" ] ; then
  osascript -e "set volume output volume ${prev_volume}"
fi
