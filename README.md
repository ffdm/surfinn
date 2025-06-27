# Surfinn

A simple web browser written in Python.

Usage: `python3 surfinn.py example.org`

Or, with Makefile:

`make example.org`

Currently supports HTTP and HTTPS and prints webpage text to terminal without
formatting. 

---

## Setup

Surfinn uses as the graphical toolkit. This forces me to implement
various features manually and learn more in the process.

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

