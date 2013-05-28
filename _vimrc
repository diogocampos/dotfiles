set nocompatible
set noexrc

runtime bundle/vim-pathogen/autoload/pathogen.vim
execute pathogen#infect()
syntax on
filetype plugin indent on

runtime macros/matchit.vim   " enable `%` to jump between if/else/endif, etc

set number    " show line numbers
set ruler     " show cursor position
set showcmd   " show partial normal-mode commands

colorscheme solarized

if has("gui_running")
  set guifont=Menlo:h12
  set guioptions-=T               " no toolbar
  set fuoptions=maxvert,maxhorz   " actually fill the screen in full screen mode
  set visualbell                  " don't beep
endif

set display+=lastline   " show the window's last line even when it's too long
set linebreak           " break lines at sensible places
set scrolloff=3         " always show a few lines above/below the current one

set formatoptions+=or   " auto-insert comment leaders
set formatprg=par       " external formatter for the `gq` command
set virtualedit+=block  " let the cursor go anywhere in visual block mode

set autoread            " auto-reload externally modified files
set hidden              " allow background buffers

set wildmode=list:longest,list:full   " sensible command line completion

if has("autocmd")
  au FileType markdown setlocal formatoptions+=a   " auto-format paragraphs
endif

"" Whitespace

set autoindent      " new lines copy the current line's indentation
set tabstop=8       " tab characters snap the cursor to multiples of this value
set softtabstop=4   " mixes tabs and spaces when `et` is off and `ts` != `sts`
set shiftwidth=4    " distance used by `>` and `<`
set shiftround      " snap indents to multiples of `shiftwidth`
set expandtab       " indent with spaces, not tabs

set listchars=tab:▸\ ,trail:·   " highlight tabs and trailing spaces
set list

if has("autocmd")
  au FileType coffee     setlocal ts=2 sts=2 sw=2   et
  au FileType *css       setlocal ts=2 sts=2 sw=2   et
  au FileType git*       setlocal ts=8 sts=8 sw=8 noet nolist
  au FileType javascript setlocal ts=2 sts=2 sw=2   et
  au FileType make       setlocal ts=8 sts=8 sw=8 noet
  au FileType markdown   setlocal ts=2 sts=2 sw=2   et
  au FileType python     setlocal ts=4 sts=4 sw=4   et
  au FileType ruby,eruby setlocal ts=2 sts=2 sw=2   et
  au FileType *sh        setlocal ts=8 sts=2 sw=2   et
  au FileType vim        setlocal ts=2 sts=2 sw=2   et
  au FileType *ml        setlocal ts=2 sts=2 sw=2   et
endif

"" Searching

set ignorecase  " case-insensitive search
set smartcase   " don't ignore case when the pattern has uppercase characters
set incsearch   " search as I type

"" Folding

set foldmethod=syntax nofoldenable
nnoremap <Space> za

"" Keyword lookup

if has("autocmd")
  au FileType python setlocal keywordprg=pydoc
  au FileType vim    setlocal keywordprg=:help
endif

"" SuperTab

let g:SuperTabDefaultCompletionType = "context"

"" Netrw

let g:netrw_liststyle = 3     " tree-style listing
let g:netrw_browse_split = 4  " open file in previous window
let g:netrw_preview = 1       " show preview in a vertical split

"" Key mappings

noremap  j gj
noremap  k gk
noremap  Q gw
nnoremap Y y$

if has("gui_macvim")
  " indent and unindent on Cmd-] and Cmd-[
  nnoremap <D-[> <<
  nnoremap <D-]> >>
  vnoremap <D-[> <gv
  vnoremap <D-]> >gv

  " quick access to .vimrc on Cmd-Shift-,
  noremap  <D-<> :split $MYVIMRC<CR>
endif

noremap \ ,
let mapleader = ','

nnoremap <leader>/ :set hlsearch!<CR>
nnoremap <leader>l :set list!<CR>
nnoremap <leader>4 :call <SID>StripTrailingWhitespace()<CR>

nmap <leader>ee :edit <C-R>=expand('%:h').'/'<CR>
nmap <leader>es :split <C-R>=expand('%:h').'/'<CR>
nmap <leader>ev :vsplit <C-R>=expand('%:h').'/'<CR>
nmap <leader>et :tabedit <C-R>=expand('%:h').'/'<CR>

function! <SID>StripTrailingWhitespace()
  " save most recent search pattern and current cursor position
  let _s = @/
  let l = line(".")
  let c = col(".")
  " do it
  %s/\s\+$//e
  " restore search pattern and cursor position
  let @/ = _s
  call cursor(l, c)
endfunction
