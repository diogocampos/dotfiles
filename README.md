Diogo's dotfiles
================


Installation
------------

### Quick start

    $ git clone git://github.com/diogocampos/dotfiles.git
    $ dotfiles/script/setup.sh

### Details

The `install-symlinks.py` script asks for confirmation before creating symlinks
in a directory of your choice, defaulting to `$HOME`.  **Conflicting symlinks
will be overwritten**, but existing files and directories are not affected.

You can preview all the changes without applying them by using the
`-d`/`--dry-run` flag:

    $ script/install-symlinks.py [target_dir] --dry-run

To see all the options supported by the script, run:

    $ script/install-symlinks.py --help


Thanks
------

* [Drew Neil][nelstrom] and his excellent [Vimcasts][vimcasts]
* [Tim Pope][tpope]'s awesome [Vim plugins][tpope-repos]
* [dotfiles.github.io](https://dotfiles.github.io/)


[nelstrom]: https://github.com/nelstrom/
[tpope]: https://github.com/tpope/
[tpope-repos]: https://github.com/tpope?tab=repositories
[vimcasts]: http://vimcasts.org/
