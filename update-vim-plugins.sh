#!/usr/bin/env sh

cd $(dirname $0)
git submodule foreach 'git pull && git submodule update --init --recursive'
vim +Helptags +q
