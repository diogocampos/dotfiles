#!/usr/bin/env python

import glob
import os
import os.path as path


def get_confirmation(message):
    reply = raw_input('%s [y/N]: ' % message)
    return reply.strip().lower().startswith('y')


def install_symlinks(dotfiles_dir, target_dir, dry_run=False):
    """
    Finds the files in `dotfiles_dir` whose names start with an underscore and
    creates symlinks in `target_dir` pointing to those files, replacing the
    underscore with a dot.

    Pre-existing symlinks with the same names in `target_dir` are removed and
    re-created, but files and directories are not affected.
    """
    dotfiles_absolute = path.abspath(dotfiles_dir)
    target_absolute   = path.abspath(target_dir)

    dotfiles = glob.glob(path.join(dotfiles_absolute, '_*'))
    if not dotfiles:
        print('Nothing to install.')
        return

    if dry_run:
        print('Dry run:')
    elif not get_confirmation('Install symlinks into %r?' % target_absolute):
        print('Installation cancelled.')
        return

    message_for_skip   = 'Skipping existing file or directory: %s'
    message_for_update = 'Updating symlink: %s -> %s'
    message_for_create = 'Creating symlink: %s -> %s'

    for abspath in dotfiles:
        relpath = path.relpath(abspath, target_absolute)
        dotname = '.' + path.basename(abspath)[1:]
        linkpath = path.join(target_absolute, dotname)

        if path.exists(linkpath) and not path.islink(linkpath):
            print(message_for_skip % linkpath)
            continue

        if path.islink(linkpath):
            print(message_for_update % (linkpath, relpath))
            if not dry_run: os.remove(linkpath)
            # TODO don't touch links that already point to the right place
        else:
            print(message_for_create % (linkpath, relpath))

        # Do it!
        if not dry_run: os.symlink(relpath, linkpath)

    print('Done.')


def main(argv):
    try:
        target_dir = argv[1]
    except IndexError:
        target_dir = os.environ['HOME']

    dotfiles_dir = path.dirname(argv[0])
    install_symlinks(dotfiles_dir, target_dir)


if __name__ == '__main__':
    import sys
    main(sys.argv)
