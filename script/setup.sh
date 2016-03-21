#!/usr/bin/env bash


set -e
cd "$(dirname "$0")/.."

script/install-symlinks.py
script/install-vim-plugins.sh
