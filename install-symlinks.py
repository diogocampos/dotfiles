#!/usr/bin/env python

from contextlib import contextmanager
import glob
import os
import os.path as path


def get_confirmation(message):
    reply = raw_input('%s [y/N]: ' % message)
    return reply.strip().lower().startswith('y')


@contextmanager
def chdir(target):
    origin = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(origin)


def install_symlinks(dotfiles_dir, target_dir, dry_run=False):
    """
    Finds the files in `dotfiles_dir` whose names start with an underscore and
    creates symlinks in `target_dir` pointing to those files, replacing the
    underscore with a dot.

    Pre-existing symlinks with the same names in `target_dir` are removed and
    recreated, but files and directories are not affected.
    """
    dotfiles_absolute = path.abspath(dotfiles_dir)
    dotfiles_relative = path.relpath(dotfiles_absolute, target_dir)

    with chdir(target_dir):
        relative_paths = glob.glob(path.join(dotfiles_relative, '_*'))
        if not relative_paths:
            print('Nothing to install.')
            return

        if not get_confirmation('Install symlinks into %r?' % target_dir):
            print('Installation cancelled.')
            return

        message_for_skip   = 'Skipping existing file or directory: %s'
        message_for_update = 'Updating symlink: %s -> %s'
        message_for_create = 'Creating symlink: %s -> %s'

        for relpath in relative_paths:
            dotname = '.' + path.basename(relpath)[1:]
            dotpath = path.join(target_dir, dotname)

            if path.exists(dotname) and not path.islink(dotname):
                print(message_for_skip % dotpath)
                continue

            if path.islink(dotname):
                print(message_for_update % (dotpath, relpath))
                if not dry_run: os.remove(dotname)
            else:
                print(message_for_create % (dotpath, relpath))

            # do it!
            if not dry_run: os.symlink(relpath, dotname)

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
