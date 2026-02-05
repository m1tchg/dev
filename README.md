Contains projects, snippets, dependencies. Slices of the dotfiles and libs you need to run projects.

## Makefile

I store nifty commands in a Makefile. Somewhere I'm hunched over my HHKB, checking links with my Makefile target and my custom Pandoc Lua filter.
``` bash
make checklinks SRC=README.md
```

Convert Markdown to docx, and more.

``` bash
make README.docx
```

Convert Markdown to HTML in Neovim.

``` vim
%!make _tohtml
```

Check the current buffer's links in Neovim. See the report in the quickfix list.

``` vim
%AsyncRun make _checklinks
```
