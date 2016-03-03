#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Johnathan "Shaggytwodope" Jenkins <twodopeshaggy@gmail.com>
#
# Distributed under terms of the GPL2 license.

import sys
from gi.repository import GLib
from aptdaemon.client import AptClient
from aptdaemon.enums import *


loop = GLib.MainLoop()
aptclient = AptClient()


def on_finished_update(trans, exit):
    if exit == "exit-success":
        print("success")
        loop.quit()
        sys.exit(0)
    else:
        print("error")
        do_bad_exit()
    return True


def do_update():
    trans_update = aptclient.update_cache()
    trans_update.connect("finished", on_finished_update)
    trans_update.run()
    return False


def do_bad_exit():
    print("error9000")
    sys.exit(1)


if __name__ == "__main__":
    try:
        GLib.timeout_add(50, do_update)
        loop.run()
    except:
        print("shaggy")
        sys.exit(1)
