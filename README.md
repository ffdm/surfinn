# Surfinn

A simple web browser written in Python.

Usage: `python3 surfinn.py example.org`

Or, with Makefile:

`make example.org`

Currently supports HTTP and HTTPS and prints webpage text to terminal without
formatting. 

---

## Setup

Surfinn uses
[PyQt6](https://www.riverbankcomputing.com/static/Docs/PyQt6/index.html) as the graphical toolkit. 
To install on MacOSX with homebrew, use:

`brew install pyqt`

To install on Linux with pip, use:

`pip install PyQt6`

For help, refer to the documentaion
[here](https://www.riverbankcomputing.com/static/Docs/PyQt6/installation.html).

---

## Todo:

- [ ] Initial GUI
- [ ] Add support for file scheme
- [ ] Add support for data scheme
- [ ] Add support for &lt; and &gt; entities
- [ ] Add support for the view-source scheme
- [ ] Keep-alive to speed up repeated requests
- [ ] Add caching
- [ ] Support HTTP compression
- [x] Support redirects

