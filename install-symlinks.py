#!/usr/bin/env python

import argparse
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
      'k' : escape % 30,    # black
      'r' : escape % 31,    # red
      'g' : escape % 32,    # green
      'y' : escape % 33,    # yellow
      'b' : escape % 34,    # blue
      'm' : escape % 35,    # magenta
      'c' : escape % 36,    # cyan
      'w' : escape % 37}    # white
    reset = escape % 0
    return colors[color.lower()] + text + reset

def install_symlinks(dotfiles_dir, target_dir, dry_run=False, confirm=True):
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
        print(colored('b', 'Dry run:'))
    elif confirm:
        message = 'Install symlinks into %s?' % colored('b', target_absolute)
        get_confirmation(message) or abort('Installation cancelled.')

    skipping_file = colored('r', 'Skipping') + ' existing file or directory: %s'
    skipping_link = colored('y', 'Skipping') + ' up-to-date symlink: %s'
    updating_link = colored('g', 'Updating') + ' symlink: %s -> %s'
    creating_link = colored('g', 'Creating') + ' symlink: %s -> %s'

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

def argument_parser(prog_name=None):
    parser = argparse.ArgumentParser(prog=prog_name,
            description='Install dotfiles as symbolic links.')

    parser.add_argument('target_dir', nargs='?',
            type=lambda string: (lambda: string),
            default=lambda: os.environ['HOME'],
            help='the directory that will contain the links (default: $HOME)')

    parser.add_argument('-d', '--dry-run', action='store_true',
            help="don't install anything; just show what would happen")

    parser.add_argument('-y', '--no-confirm',
            dest='confirm', action='store_false',
            help="don't ask for confirmation before installing")

    return parser

def main(argv):
    dotfiles_dir, prog_name = path.split(argv[0])
    args = argument_parser(prog_name).parse_args(argv[1:])

    target_dir = args.target_dir()
    if not path.exists(target_dir):
        abort('Path %r does not exist.' % target_dir)
    if not path.isdir(target_dir):
        abort('%r is not a directory.' % target_dir)

    install_symlinks(dotfiles_dir, target_dir, args.dry_run, args.confirm)

if __name__ == '__main__':
    main(sys.argv)
