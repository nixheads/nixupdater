##Lite-Updater

Designed for Linux Lite.

Current depends required to run are:
- python-gtk2
- python-apt
- python-pyinotify
- python-notify2

The file
``/etc/apt/apt.conf.d/02periodic``
Is to be installed in the exact path provided. This allows ``apt`` to run "update" once a day on it's own.

