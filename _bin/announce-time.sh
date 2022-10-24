#!/bin/sh

log_file="${HOME}/.announce-time_history"


[ -f ~/.no-announce-time ] && exit

# don't announce when using external displays
displays="$(osascript -e 'tell application "Image Events" to count displays')"
[ "$displays" -gt 1 ] && exit

# don't announce during calls in MS Teams
( pmset -g | grep 'display sleep prevented' | grep -q 'Teams' ) && exit


dir="$(dirname "$0")"

volume='38'
prev_volume="$(osascript -e 'output volume of (get volume settings)')"
if [ "$prev_volume" -gt "$volume" ] ; then
  osascript -e "set volume output volume ${volume}"
fi


announce () {
  echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$@" >> "$log_file"
  say "$@"
}

# Français
#announce -v Thomas "Il est $(date +'%H:%M')."

# 日本語
announce -v Otoya "$("$dir"/nanji.py)"


if [ "$prev_volume" -gt "$volume" ] ; then
  osascript -e "set volume output volume ${prev_volume}"
fi
