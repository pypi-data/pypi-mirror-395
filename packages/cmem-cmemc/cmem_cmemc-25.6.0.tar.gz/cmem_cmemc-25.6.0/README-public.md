# cmemc

cmemc is the official command line client for [eccenca Corporate Memory](https://documentation.eccenca.com/).

[![version][version-shield]][changelog] [![Python Versions][python-shield]][pypi] [![eccenca Corporate Memory][cmem-shield]][cmem]

[![teaser][teaser-image]][cmemc-docu]

## Installation

In order to install the cmemc, run:

    pipx install cmem-cmemc

Of course you can install cmemc also with pip, but we recommend [pipx](https://pypa.github.io/pipx/) for normal desktop usage.

## Configuration and Usage

cmemc is intended for System Administrators and Linked Data Expert, who wants to automate and remote control activities on eccenca Corporate Memory.

The cmemc manual including basic usage pattern, configuration as well as a command reference is available at:

[https://eccenca.com/go/cmemc](https://eccenca.com/go/cmemc)

cmemc only works with Python 3 and refuses to work with Python 2.x.
In addition to that, cmemc will warn you in case an untested Python environment is used.


[version-shield]: https://badge.fury.io/py/cmem-cmemc.svg
[changelog]: https://pypi.org/project/cmem-cmemc/#history
[python-shield]: https://img.shields.io/pypi/pyversions/cmem-cmemc.svg
[pypi]: https://pypi.org/project/cmem-cmemc/
[cmem]: https://documentation.eccenca.com
[cmem-shield]: https://img.shields.io/badge/made%20for-eccenca%20Corporate%20Memory-blue?logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgaWQ9IkxheWVyXzEiCiAgIGRhdGEtbmFtZT0iTGF5ZXIgMSIKICAgdmlld0JveD0iMCAwIDgxLjI5MDAwMSA4Mi4yODk4NiIKICAgdmVyc2lvbj0iMS4xIgogICB3aWR0aD0iODEuMjkwMDAxIgogICBoZWlnaHQ9IjgyLjI4OTg2NCIKICAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogICB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8ZGVmcwogICAgIGlkPSJkZWZzODI2Ij4KICAgIDxzdHlsZQogICAgICAgaWQ9InN0eWxlODI0Ij4KICAgICAgLmNscy0xIHsKICAgICAgICBmaWxsOiAjZjM5MjAwOwogICAgICB9CgogICAgICAuY2xzLTIgewogICAgICAgIGZpbGw6IG5vbmU7CiAgICAgICAgc3Ryb2tlOiAjZjM5MjAwOwogICAgICAgIHN0cm9rZS13aWR0aDogMS41cHg7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxnCiAgICAgaWQ9Imc4NDAiCiAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTMwLjc2LC0zMS4xNDAxMzkpIj4KICAgIDxwYXRoCiAgICAgICBjbGFzcz0iY2xzLTEiCiAgICAgICBkPSJNIDU1LjksODUuMTkgQSAyMC4xNCwyMC4xNCAwIDEgMCAzNS43Niw2NS4wNSAyMC4xNCwyMC4xNCAwIDAgMCA1NS45LDg1LjE5IFoiCiAgICAgICBpZD0icGF0aDgyOCIgLz4KICAgIDxwYXRoCiAgICAgICBjbGFzcz0iY2xzLTEiCiAgICAgICBkPSJtIDk4LDU0LjE0IGEgOSw5IDAgMSAwIC04Ljk1LC05IDguOTUsOC45NSAwIDAgMCA4Ljk1LDkgeiIKICAgICAgIGlkPSJwYXRoODMwIiAvPgogICAgPHBhdGgKICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgIGQ9Ik0gODguMzUsMTA4LjQzIEEgMTIuMzEsMTIuMzEgMCAxIDAgNzYsOTYuMTIgMTIuMzEsMTIuMzEgMCAwIDAgODguMzEsMTA4LjQzIFoiCiAgICAgICBpZD0icGF0aDgzMiIgLz4KICAgIDxsaW5lCiAgICAgICBjbGFzcz0iY2xzLTIiCiAgICAgICB4MT0iODYuOTcwMDAxIgogICAgICAgeTE9IjkyLjA1OTk5OCIKICAgICAgIHgyPSI1OC43Nzk5OTkiCiAgICAgICB5Mj0iNjcuMzYwMDAxIgogICAgICAgaWQ9ImxpbmU4MzQiIC8+CiAgICA8bGluZQogICAgICAgY2xhc3M9ImNscy0yIgogICAgICAgeDE9Ijk5LjE4IgogICAgICAgeTE9IjQ1Ljg0IgogICAgICAgeDI9IjU1LjQ4IgogICAgICAgeTI9IjY2LjEyMDAwMyIKICAgICAgIGlkPSJsaW5lODM2IiAvPgogICAgPGxpbmUKICAgICAgIGNsYXNzPSJjbHMtMiIKICAgICAgIHgxPSI5Ny45ODk5OTgiCiAgICAgICB5MT0iNDQuNjUwMDAyIgogICAgICAgeDI9Ijg4LjM0OTk5OCIKICAgICAgIHkyPSI5Mi44Mzk5OTYiCiAgICAgICBpZD0ibGluZTgzOCIgLz4KICA8L2c+Cjwvc3ZnPgo=
[teaser-image]: https://documentation.eccenca.com/24.1/automate/cmemc-command-line-interface/configuration/completion-setup/22.1-cmemc-create-dataset.gif
[cmemc-docu]: https://eccenca.com/go/cmemc
