#!/usr/bin/env python

import glob
import os
import os.path as path
import sys

def abort(message):
    print(message)
    sys.exit(1)

def get_confirmation(message):
    reply = raw_input('%s [y/N]: ' % message)
    return reply.strip().lower().startswith('y')

def colored(color, text):
    escape = '\033[%sm'
    colors = {
      'k' : escape % 30,
      'r' : escape % 31,
      'g' : escape % 32,
      'y' : escape % 33,
      'b' : escape % 34,
      'm' : escape % 35,
      'c' : escape % 36,
      'w' : escape % 37}
    reset = escape % 0
    return colors[color] + text + reset

def install_symlinks(dotfiles_dir, target_dir, dry_run=False):
    """
    Finds the files in `dotfiles_dir` whose names start with an underscore and
    creates symlinks in `target_dir` pointing to those files, replacing the
    underscore with a dot.

    Pre-existing symlinks with the same names in `target_dir` are updated if
    necessary, but existing files and directories are not affected.
    """
    dotfiles_absolute = path.abspath(dotfiles_dir)
    target_absolute   = path.abspath(target_dir)

    dotfiles = glob.glob(path.join(dotfiles_absolute, '_*'))
    if not dotfiles:
        abort('Nothing to install.')

    if dry_run:
        print('Dry run:')
    elif not get_confirmation('Install symlinks into %r?' % target_absolute):
        abort('Installation cancelled.')

    skipping_file = colored('r', 'Skipping') + ' existing file or directory: %s'
    skipping_link = colored('g', 'Skipping') + ' up-to-date symlink: %s'
    updating_link = colored('y', 'Updating') + ' symlink: %s -> %s'
    creating_link = colored('y', 'Creating') + ' symlink: %s -> %s'

    for abspath in dotfiles:
        relpath = path.relpath(abspath, target_absolute)
        dotname = '.' + path.basename(abspath)[1:]
        linkpath = path.join(target_absolute, dotname)

        if path.exists(linkpath) and not path.islink(linkpath):
            print(skipping_file % linkpath)
            continue

        if path.islink(linkpath):
            if path.samefile(abspath, path.realpath(linkpath)):
                print(skipping_link % linkpath)
                continue

            print(updating_link % (linkpath, relpath))
            if not dry_run: os.remove(linkpath)
        else:
            print(creating_link % (linkpath, relpath))

        # Do it!
        if not dry_run: os.symlink(relpath, linkpath)

    print('Done.')

def main(argv):
    try:
        target_dir = argv[1]
    except IndexError:
        target_dir = os.environ['HOME']

    if not path.exists(target_dir):
        abort('Path %r does not exist.' % target_dir)
    if not path.isdir(target_dir):
        abort('%r is not a directory.' % target_dir)

    # TODO support dry-run mode with -d|--dry-run

    dotfiles_dir = path.dirname(argv[0])
    install_symlinks(dotfiles_dir, target_dir)

if __name__ == '__main__':
    main(sys.argv)
