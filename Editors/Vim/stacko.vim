" Vim syntax file
" Language:         Stacko
" Maintainer:       Suirabu <suirabu.dev@gmail.com>
" Latest Revision:  6-04-2022

" Usage:
" Put this file in your `~/.vim/syntax/` directory
" Add the line:
"
"     au BufRead,BufNewFile *.{stko,stacko} set filetype=stacko
"
" into your .vimrc

if exists("b:current_syntax")
    finish
endif

syn keyword stackoConditional if else
syn keyword stackoRepeat while
syn keyword stackoOperator + - * / % = < <= > >=
syn keyword stackoKeyword dup pop not print printLine readLine exit assert assertEqual assertNotEqual toNum toString toBool fnn const file var set

syn region stackoString start='"' end='"'
syn match stackoFloat "\d+(\.\d+)?"
syn keyword stackoBoolean Yes No

syn keyword stackoTodo TODO FIXME XXX
syn match stackoComment "#.*$\n" contains=stackoTodo

hi def link stackoConditional Conditional
hi def link stackoRepeat Repeat
hi def link stackoOperator Operator
hi def link stackoKeyword Keyword

hi def link stackoString String
hi def link stackoFloat Float
hi def link stackoBoolean Boolean

hi def link stackoTodo Todo
hi def link stackoComment Comment

let b:current_syntax = "stacko"
