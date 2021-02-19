#!/bin/sh

[ -f ~/.no-announce-time ] && exit

displays="$(osascript -e 'tell application "Image Events" to count displays')"
[ "$displays" -gt 1 ] && exit

dir="$(dirname "$0")"

volume='38'
prev_volume="$(osascript -e 'output volume of (get volume settings)')"
if [ "$prev_volume" -gt "$volume" ] ; then
  osascript -e "set volume output volume ${volume}"
fi

# Français
#say -v Thomas "Il est $(date +'%H:%M')."

# 日本語
"$dir"/nanji.py | say -v Otoya

if [ "$prev_volume" -gt "$volume" ] ; then
  osascript -e "set volume output volume ${prev_volume}"
fi
