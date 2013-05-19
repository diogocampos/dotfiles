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

    # TODO highlight the first word of each message in a different color
    skipping_file = 'Skipping existing file or directory: %s'
    skipping_link = 'Skipping up-to-date symlink: %s'
    updating_link = 'Updating symlink: %s -> %s'
    creating_link = 'Creating symlink: %s -> %s'

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
