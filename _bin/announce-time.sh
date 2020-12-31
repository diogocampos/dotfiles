#!/bin/sh

[ -f ~/.no-announce-time ] && exit

node () {
  local version=default
  while [ -f ~/.nvm/alias/"$version" ] ; do
    version="$(cat ~/.nvm/alias/"$version")"
  done
  local node=~/.nvm/versions/node/"$version"/bin/node
  "$node" "$@"
}

dir="$(dirname "$0")"

speech_volume='31'
previous_volume="`osascript -e 'output volume of (get volume settings)'`"
osascript -e "set volume output volume ${speech_volume}"

# Français
#say -v Thomas "Il est `date +'%H:%M'`."

# 日本語
#say -v Otoya "今は`date +'%H:%M'`です。"
#NODE_VERSION=default ~/.nvm/nvm-exec node "$dir"/jp-time.js | say -v Otoya
node "$dir"/jp-time.js | say -v Otoya

osascript -e "set volume output volume ${previous_volume}"
