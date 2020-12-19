set nocompatible
set noexrc
set nomodeline

runtime bundle/vim-pathogen/autoload/pathogen.vim
execute pathogen#infect()
syntax on
filetype plugin indent on

set number    " show line numbers
set ruler     " show cursor position
set showcmd   " show partial normal-mode commands

set background=dark
colorscheme gruvbox

if has('gui_running')
  set guifont=Fantasque\ Sans\ Mono:h14
  "set linespace=2
  set guioptions-=T               " no toolbar
  set guioptions-=r               " no vertical scrollbar
  set fuoptions=maxvert,maxhorz   " actually fill the screen in full screen mode
  set visualbell                  " don't beep
endif

set display+=lastline   " show the window's last line even when it's too long
"set linebreak           " break lines at sensible places
set scrolloff=2         " always show a few lines above/below the current one

set formatoptions+=or   " auto-insert comment leaders
set virtualedit+=block  " let the cursor go anywhere in visual block mode

set autoread            " auto-reload externally modified files
set hidden              " allow background buffers

set splitbelow          " put new splits below the current one
set splitright          " put new vsplits to the right of the current one

set wildmode=list:longest,list:full   " sensible command line completion

set ttimeoutlen=0       " no delay when hitting Esc in a terminal


"" Whitespace

set autoindent      " new lines copy the current line's indentation
set tabstop=8       " tab characters snap the cursor to multiples of this value
set softtabstop=2   " mixes tabs and spaces when `et` is off and `ts` != `sts`
set shiftwidth=2    " distance used by `>` and `<`
set shiftround      " snap indents to multiples of `shiftwidth`
set expandtab       " indent with spaces, not tabs

set listchars=tab:▸\ ,trail:·   " make tabs and trailing whitespace visible
set list

if has('autocmd')
  au FileType coffee     setlocal ts=2 sts=2 sw=2   et
  au FileType css        setlocal ts=2 sts=2 sw=2   et
  au FileType git*       setlocal ts=8 sts=8 sw=8 noet nolist
  au FileType go         setlocal ts=4 sts=4 sw=4 noet
  au FileType html       setlocal ts=2 sts=2 sw=2   et
  au FileType jade       setlocal ts=2 sts=2 sw=2   et
  au FileType javascript setlocal ts=2 sts=2 sw=2   et
  au FileType json       setlocal ts=2 sts=2 sw=2   et
  au FileType make       setlocal ts=4 sts=4 sw=4 noet
  au FileType markdown   setlocal ts=4 sts=4 sw=4   et
  au FileType python     setlocal ts=4 sts=4 sw=4   et
  au FileType ruby,eruby setlocal ts=2 sts=2 sw=2   et
  au FileType sh         setlocal ts=8 sts=2 sw=2   et
  au FileType vim        setlocal ts=2 sts=2 sw=2   et
  au FileType xml        setlocal ts=2 sts=2 sw=2 noet
endif

"" Folding

set foldmethod=syntax nofoldenable

if has('autocmd')
  au FileType coffee   setlocal foldmethod=indent nofoldenable
  au FileType json     setlocal foldmethod=syntax nofoldenable
  au FileType markdown setlocal foldmethod=manual
  au FileType python   setlocal foldmethod=indent nofoldenable
  au FileType text     setlocal foldmethod=marker foldmarker=/#,#/ foldenable
endif

"" Keyword lookup

if has('autocmd')
  au FileType python   setlocal keywordprg=pydoc
  au FileType vim,help setlocal keywordprg=:help
endif

"" Adding and subtracting

if has('autocmd')
  au FileType text setlocal nrformats-=octal
endif

"" Searching

"set hlsearch    " highlight matches
set incsearch   " search as I type
set ignorecase  " case-insensitive search
set smartcase   " don't ignore case when the pattern has uppercase characters

"" Airline

set laststatus=2  " always show a status line
set noshowmode    " don't show mode names in the last line

let g:airline_powerline_fonts = 1

"" CamelCaseMotion

let g:camelcasemotion_key = '<leader>'

"" delimitMate

let delimitMate_expand_cr = 1
let delimitMate_expand_space = 1

"" highlightedyank
"
let g:highlightedyank_highlight_duration = 200

"" Prettier

if has('autocmd')
  au FileType css        setlocal equalprg=prettier\ --stdin-filepath\ _.css
  au FileType javascript setlocal equalprg=prettier\ --stdin-filepath\ _.js
  au FileType json       setlocal equalprg=prettier\ --stdin-filepath\ _.json
  au FileType markdown   setlocal equalprg=prettier\ --stdin-filepath\ _.markdown
endif

"" Key mappings

inoremap jj <Esc>

noremap j gj
noremap k gk
nnoremap Y y$
nnoremap cw caw

nnoremap U /\u<CR>
onoremap U /\u<CR>
vnoremap U /\u<CR>h

vnoremap p "0p

nnoremap <Space> za

cnoremap %% <C-R>=fnameescape(expand('%:h')).'/'<CR>


noremap \ ,
let mapleader = ','

nnoremap <Leader>go :call <SID>Open()<CR>

nnoremap <Leader>jq :%!jq '.'<CR>
vnoremap <Leader>jq :!jq '.'<CR>

nnoremap <Leader>/ :set hlsearch!<CR>
nnoremap <Leader>l :set list!<CR>
nnoremap <Leader>4 :call <SID>StripTrailingWhitespace()<CR>

"nmap <Leader>ee :edit <C-R>=expand('%:h').'/'<CR>
"nmap <Leader>es :split <C-R>=expand('%:h').'/'<CR>
"nmap <Leader>ev :vsplit <C-R>=expand('%:h').'/'<CR>
"nmap <Leader>et :tabedit <C-R>=expand('%:h').'/'<CR>


function! <SID>Open()
  silent execute "!open " . expand("<cWORD>")
endfunction

function! <SID>StripTrailingWhitespace()
  " save most recent search pattern and current cursor position
  let _s = @/
  let l = line('.')
  let c = col('.')
  " do it
  %s/\s\+$//e
  " restore search pattern and cursor position
  let @/ = _s
  call cursor(l, c)
endfunction
