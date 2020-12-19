#!/bin/sh

[ -f ~/.no-announce-time ] && exit

speech_volume='31'
current_volume="`osascript -e 'output volume of (get volume settings)'`"

osascript -e "set volume output volume ${speech_volume}"

# Français
#say -v Thomas "Il est `date +'%H:%M'`."

# 日本語
say -v Otoya "今は`date +'%H:%M'`です。"

osascript -e "set volume output volume ${current_volume}"
