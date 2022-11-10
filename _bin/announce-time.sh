#!/bin/sh

dir="$(dirname "$0")"
log_file="${HOME}/.announce-time_history"
max_volume='38'


# don't announce if a file exists at ~/.no-announce-time
[ -f ~/.no-announce-time ] && exit

# don't announce when using external displays
displays="$(osascript -e 'tell application "Image Events" to count displays')"
[ "$displays" -gt 1 ] && exit

# don't announce during calls in MS Teams
( pmset -g | grep 'display sleep prevented' | grep -q 'Teams' ) && exit


# lower the volume if it's over the threshold
prev_volume="$(osascript -e 'output volume of (get volume settings)')"
if [ "$prev_volume" -gt "$max_volume" ] ; then
  osascript -e "set volume output volume ${max_volume}"
fi


announce () {
  echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$@" >> "$log_file"
  say "$@"
}

# Français
#announce -v 'Thomas (Enhanced)' "Il est $(date +'%H:%M')."

# 日本語
announce -v 'Otoya (Enhanced)' "$("$dir"/nanji.py)"


# restore the volume if it was lowered
if [ "$prev_volume" -gt "$max_volume" ] ; then
  osascript -e "set volume output volume ${prev_volume}"
fi
