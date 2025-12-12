# metarace-tagreg

Read transponder ids from a connected decoder.

![tagreg screenshot](screenshot.png "tagreg")

## Requirements

   - Python >= 3.11
   - Gtk >= 3.0
   - metarace >= 2.1.14


## Installation

Use shared installer from metarace to collect requirements
and install with roadmeet and trackmeet:

	$ wget https://github.com/ndf-zz/metarace/raw/refs/heads/main/metarace-install.sh
	$ sh metarace-install.sh

Alternatively, install system requirements and use pip:

	$ sudo apt-get install python3-venv python3-pip python3-cairo \
	python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-rsvg-2.0 \
	gir1.2-pango-1.0
	$ mkdir -p ~/Documents/metarace
	$ python3 -m venv --system-site-packages ~/Documents/metarace/venv
	$ ~/Documents/metarace/venv/bin/pip install metarace-tagreg
	$ ~/Documents/metarace/venv/bin/tagreg
