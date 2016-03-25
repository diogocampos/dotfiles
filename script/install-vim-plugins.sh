#!/usr/bin/env bash

PLUGINS=(
  altercation/vim-colors-solarized
  derekwyatt/vim-scala
  ervandew/supertab
  kchmck/vim-coffee-script
  michaeljsmith/vim-indent-object
  morhetz/gruvbox
  Raimondi/delimitMate
  tpope/vim-commentary
  tpope/vim-pathogen
  tpope/vim-repeat
  tpope/vim-surround
  tpope/vim-unimpaired
  vim-airline/vim-airline
)


set -e
cd "$(dirname "$0")/.."

for repo in "${PLUGINS[@]}" ; do
  plugin_dir="_vim/bundle/${repo#*/}"
  if [ ! -e "$plugin_dir" ] ; then
    printf "\e[33m${repo}\e[0m\n"
    git clone "https://github.com/${repo}.git" "$plugin_dir"
    ( cd "$plugin_dir" && git submodule update --init --recursive )
  fi
done

vim +Helptags +q
