#!/usr/bin/env bash


set -e
cd "$(dirname "$0")/.."

for plugin_dir in _vim/bundle/* ; do
  printf "\e[33m$(basename "$plugin_dir"):\e[0m "
  ( cd "$plugin_dir" && git pull && git submodule update --init --recursive )
done

vim +Helptags +q
