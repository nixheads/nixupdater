#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Johnathan "Shaggytwodope" Jenkins <twodopeshaggy@gmail.com>
#
# Distributed under terms of the GPL2 license.

import shlex
import fcntl
from subprocess import Popen, PIPE
import pygtk
import gtk
from gtk import gdk
import glib
import apt
import time
import sys
import os
import gc
import pyinotify
import notify2
from threading import Thread
pygtk.require('2.0')
gtk.gdk.threads_init()


fl = 0


def run_check():
    global fl
    fl = open(os.path.realpath(__file__), 'r')
    try:
        fcntl.flock(fl, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        sys.exit(0)


iconpath = '/usr/share/lite-updater/icons/'
inactive_icon = iconpath + 'updates-idle.png'
working_icon = iconpath + 'aptdaemon-working.png'
cache_icon = iconpath + 'cache-icon.png'
upgrade_icon = iconpath + 'updates-available.png'
essential_icon = iconpath + 'updates-available.png'
logo = iconpath + 'lite_logo.png'


def get_global_config():
    global config
    config = []
    try:
        for line in open(os.path.expanduser("~") + '/.config' +
                         '/lite-updater.conf'):
            line = line.rstrip()
            config.append(line)
    except:
        config = ["1800", "3600", "3000", "True"]
    return config


class Autostart(object):

    def user_autostart_path(self):
        config_autostart_path = os.getenv("HOME") + "/.config/autostart/"
        if not os.path.exists(config_autostart_path):
            os.makedirs(config_autostart_path)
        return config_autostart_path + "lite-updater.desktop"

    def is_installed(self):
        return os.path.exists(self.user_autostart_path())

    def install(self):
        with open(self.user_autostart_path(), "w") as desktop_file:
            desktop_file.write("""[Desktop Entry]
Type=Application
Version=0.1
Name=Lite-Updater
GenericName=Lite-Updater
Comment=Linux Lite Update Checker
Exec=/usr/bin/lite-updater
Terminal=false
Categories=GTK;Utility;
StartupNotify=true""")

        return True

    def uninstall(self):
        os.remove(self.user_autostart_path())


def checkcount():
    global upgrades
    cache = apt.Cache()
    cache.close()
    cache.open()
    upgrades = 0
    cache.upgrade(dist_upgrade=False)
    changes = cache.get_changes()
    if changes:
        counter = [change.name for change in changes]
        upgrades = (len(counter))
    return upgrades
    cache.close()
    gc.collect()


class Liteupdater:

    def __init__(self):
        self.config = get_global_config()
        self.icon = gtk.status_icon_new_from_file(inactive_icon)
        self.icon.set_tooltip("Idle")
        notify2.init("Lite-updater")
        self.icon.set_visible(True)
        self.update_running = False
        self.notifier = None
        self.watchdir = '/var/lib/apt'
        self.upgrades = 0
        self.icon.connect('activate', self.on_left_click)
        self.icon.connect('popup-menu', self.on_right_click)

    def update_cache(self, foo=None):
        self.set_state('cache')
        cmd = "/usr/share/lite-updater/lite-cache-check.py"
        process = Popen(shlex.split(cmd), stdout=PIPE)
        process.communicate()
        self.update()
        gc.collect()

    def on_left_click(self, foo):
        cmd = "/usr/bin/gksu /usr/scripts/updates-gui"
        process = Popen(shlex.split(cmd), stdout=PIPE)
        process.communicate()
        self.update()

    def checksources(self, foo):
        glib.spawn_async(["/usr/bin/gksu", "/usr/bin/software-properties-gtk"])

    def theconfig(self, foo):
        get_global_config()
        self.doconfig()
        
    def doconfig(self):
        cwindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        cwindow.set_position(gtk.WIN_POS_CENTER)
        cwindow.set_title("Updater Config")
        cwindow.set_icon_from_file(upgrade_icon)
        main_vbox = gtk.VBox(False, 5)
        main_vbox.set_border_width(10)
        cwindow.add(main_vbox)

        def default(self):
            config = ["1800", "3600", "3000",  "True"]
            configfile = open(os.path.expanduser("~") + '/.config' +
                              '/lite-updater.conf', "w")
            for item in config:
                configfile.write("%s\n" % item)
            spinner1.set_value(1)
            spinner2.set_value(30)
            spinner3.set_value(3)
            check.set_active(True)
            apply

        def apply(self):
            mins = spinner2.get_value_as_int()
            config[0] = mins * 60
            hours = spinner1.get_value_as_int()
            config[1] = hours * 60 * 60
            dseconds = spinner3.get_value_as_int()
            config[2] = dseconds * 1000
            config[3] = check.get_active()
            configfile = open(os.path.expanduser("~") + '/.config' +
                              '/lite-updater.conf', "w")
            for item in config:
                configfile.write("%s\n" % item)
            get_global_config()
            cwindow.destroy()

        def checksig(self):
            if check.get_active() is True:
                spinner3.set_sensitive(True)
                check.set_label('Notifications Enabled')
            elif check.get_active() is False:
                spinner3.set_sensitive(False)
                check.set_label('Notifications Disabled')

        def doauto_start(self):
            if Autostart().is_installed():
                pass
            else:
                Autostart().install()

        def doauto_remove(self):
            if Autostart().is_installed():
                Autostart().uninstall()
            else:
                pass

        def autostart(self):
            if Autostart().is_installed():
                doauto_remove(button)
                button.set_label("Enable Autostart")
            else:
                doauto_start(button)
                button.set_label("Disable Autostart")

        frame = gtk.Frame("Update Check Period")
        main_vbox.pack_start(frame, True, True, 0)
        vbox = gtk.VBox(False, 0)
        vbox.set_border_width(5)
        frame.add(vbox)
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, True, True, 5)
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)
        label = gtk.Label("Hours :")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)
        adj = gtk.Adjustment(0, 0, 23, 1, 10, 0)
        spinner1 = gtk.SpinButton(adj, 0, 0)
        policy = gtk.UPDATE_IF_VALID
        spinner1.set_update_policy(policy)
        spinner1.set_value(int(config[1]) / 60 / 60)
        spinner1.set_wrap(True)
        vbox2.pack_start(spinner1, False, True, 0)
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)
        label = gtk.Label("Minutes :")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)
        adj = gtk.Adjustment(0, 5, 59, 1, 10, 0)
        policy = gtk.UPDATE_IF_VALID
        spinner2 = gtk.SpinButton(adj, 0, 0)
        spinner2.set_update_policy(policy)
        spinner2.set_value(int(config[0]) / 60)
        spinner2.set_wrap(True)
        vbox2.pack_start(spinner2, False, True, 0)
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)
        frame = gtk.Frame("Notification Duration")
        main_vbox.pack_start(frame, True, True, 0)
        vbox = gtk.VBox(False, 0)
        vbox.set_border_width(5)
        frame.add(vbox)
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, False, True, 5)
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)
        label = gtk.Label("Seconds :")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)
        adj = gtk.Adjustment(0, 1, 60, 1, 10, 0)
        policy = gtk.UPDATE_IF_VALID
        spinner3 = gtk.SpinButton(adj, 0, 0)
        spinner3.set_update_policy(policy)
        spinner3.set_value(int(config[2]) / 1000)
        spinner3.set_wrap(True)
        spinner3.set_size_request(100, -1)
        vbox2.pack_start(spinner3, False, True, 0)
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)
        check = gtk.CheckButton("Notifcations Enabled")
        if config[3] == "True":
            check.set_active(True)
            spinner3.set_sensitive(True)
        elif config[3] == "False":
            check.set_active(False)
            spinner3.set_sensitive(False)
            check.set_label('Notifications Disabled')
        check.connect("toggled", checksig)
        vbox.pack_start(check, True, True, 0)
        frame = gtk.Frame("Miscellaneous Settings")
        main_vbox.pack_start(frame, True, True, 0)
        vbox = gtk.VBox(False, 0)
        vbox.set_border_width(5)
        frame.add(vbox)
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, False, True, 5)
        button = gtk.Button("Reset")
        button.connect("clicked", default)
        hbox.pack_start(button, True, True, 5)
        if Autostart().is_installed():
            button = gtk.Button("Disable Autostart")
        else:
            button = gtk.Button("Enable Autostart")
        button.connect("clicked", autostart)
        hbox.pack_start(button, True, True, 5)
        hbox = gtk.HBox(False, 0)
        main_vbox.pack_start(hbox, False, True, 0)
        buttonc = gtk.Button(stock=gtk.STOCK_CLOSE)
        buttonc.connect("clicked", lambda w: cwindow.destroy())
        hbox.pack_start(buttonc, True, True, 5)
        buttona = gtk.Button(stock=gtk.STOCK_APPLY)
        buttona.connect("clicked", apply)
        hbox.pack_start(buttona, True, True, 5)
        cwindow.show_all()

    def on_right_click(self, icon, button, time):
        menu = gtk.Menu()

        img1 = gtk.Image()
        img2 = gtk.Image()
        img3 = gtk.Image()
        img4 = gtk.Image()

        about = gtk.ImageMenuItem('gtk-about', None)
        updatechk = gtk.ImageMenuItem('Update Cache')
        img1.set_from_file(cache_icon)
        updatechk.set_image(img1)
        chsources = gtk.ImageMenuItem('Change Sources')
        img2.set_from_file(working_icon)
        chsources.set_image(img2)
        installupdate = gtk.ImageMenuItem('Install Updates')
        img3.set_from_file(essential_icon)
        installupdate.set_image(img3)
        refresh = gtk.ImageMenuItem('gtk-refresh', None)
        quit = gtk.ImageMenuItem('gtk-quit', None)

        about.connect('activate', self.show_about_dialog)
        updatechk.connect('activate', self.update_cache)
        chsources.connect('activate', self.checksources)
        installupdate.connect('activate', self.on_left_click)
        refresh.connect('activate', self.update)
        quit.connect('activate', self.quit)

        menu.append(about)
        enableauto = gtk.ImageMenuItem('Configuration')
        img4.set_from_file(working_icon)
        enableauto.set_image(img4)
        enableauto.connect('activate', self.theconfig)
        menu.append(enableauto)
        sep2 = gtk.SeparatorMenuItem()
        menu.append(sep2)
        menu.append(updatechk)
        menu.append(chsources)
        menu.append(installupdate)
        sep3 = gtk.SeparatorMenuItem()
        menu.append(sep3)
        menu.append(refresh)
        menu.append(quit)

        menu.show_all()
        menu.popup(None, None, gtk.status_icon_position_menu, button, time,
                   icon)

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name('Lite Updater')
        about_dialog.set_comments('A simple, lite update checker'
                                  ' for your tray.')
        about_dialog.set_website('https://github.com/linuxlite/lite-updater')
        about_dialog.set_website_label('Homepage')
        about_dialog.set_icon(gdk.pixbuf_new_from_file(upgrade_icon))
        about_dialog.set_logo(gdk.pixbuf_new_from_file(logo))
        about_dialog.set_copyright('Copyright 2016')
        about_dialog.set_version('1.0-0050')
        about_dialog.set_authors(['Johnathan "ShaggyTwoDope" Jenkins'])
        about_dialog.set_license('''This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA. ''')

        about_dialog.run()
        about_dialog.destroy()

    def quit(self, widget):
        self.notifier.stop()
        sys.exit(0)

    def set_state(self, state):
        self.tooltip_state = {
            'upgrade': 'Updates Available' + " " + str(self.upgrades),
            'inactive': 'No Updates Available',
            'working': 'Operations In Progress\nPlease wait...',
            'cache': 'Updating Package Cache\nPlease wait...'
        }

        self.upgrades = checkcount()
        icon = eval('{0}_icon'.format(state))
        self.icon.set_from_file(icon)
        self.icon.set_tooltip(self.tooltip_state[state])
        if config[3] == "True":
            n = notify2.Notification("Lite-Updater",
                                     (self.tooltip_state[state]))
            nicon = gdk.pixbuf_new_from_file(icon)
            n.set_icon_from_pixbuf(nicon)
            n.set_timeout(int(config[2]))
            n.show()
        elif config[3] == "False":
            pass
        gc.collect()

    def update(self, ev=None):
        if self.update_running is False:
            self.update_running = True
            self.set_state('working')
            if self.upgrades:
                state = 'upgrade'
            else:
                state = 'inactive'

            self.set_state(state)
        self.update_running = False
        gc.collect()

    def timer_update(self):
        while True:
            self.update_cache()
            gc.collect()
            time.sleep(int(config[0] + config[1]))

    def main(self):
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        self.notifier = pyinotify.ThreadedNotifier(wm, self.update)
        wm.add_watch(self.watchdir, mask)
        self.notifier.start()

        t = Thread(target=self.timer_update)
        t.daemon = True
        t.start()
        gc.collect()
        gtk.main()

if __name__ == "__main__":
    app = Liteupdater()
    try:
        run_check()
        app.main()
    except KeyboardInterrupt:
        app.quit()
