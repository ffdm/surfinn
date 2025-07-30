# Surfinn

A simple web browser written in Python.

Usage: `python3 surfinn.py example.org`

Or, with Makefile:

`make example.org`

Currently supports HTTP and HTTPS and prints webpage text to terminal without
formatting. 

---

## Setup

Surfinn uses Tkinter as the graphical toolkit. This forces me to implement
various features manually and learn more in the process.

---

## Todo:

- [ ] Add support for file scheme
- [ ] Add support for data scheme
- [ ] Add support for &lt; and &gt; entities
- [ ] Add support for the view-source scheme
- [ ] Keep-alive to speed up repeated requests
- [ ] Add caching
- [ ] Support HTTP compression
- [ ] Line breaks
- [ ] Make browser resizeable
- [ ] Add scrollbar
- [ ] Add support for emojis (openmoji)
- [ ] Add about:blank
- [ ] Alternate text direction
- [ ] Support mouse wheel scroll for other OS
- [ ] Prevent user from scrolling down past page bottom
- [x] Support mouse wheel scroll
- [x] Initial GUI
- [x] Support redirects

