#!/usr/bin/env python3


import os
import signal

from urllib import request
from urllib.error import URLError
from urllib.request import urlopen

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk, GLib, GObject, AppIndicator3 as appindicator, Notify
from subprocess import call, check_output

class IndicatorBackup:
    def __init__(self):
            # param1: identifier of this indicator
            # param2: name of icon. this will be searched for in the standard them
            # dirs
            # finally, the category. We're monitoring, so SYSTEM_SERVICES
            self.indic = appindicator.Indicator.new(
                           'Backup Notification indicator app',
                           os.path.abspath('/usr/share/icons/gnome/24x24/emotes/face-smile-big.png'),
                           appindicator.IndicatorCategory.SYSTEM_SERVICES)

            # some more information about the AppIndicator:
            # http://developer.ubuntu.com/api/ubuntu-12.04/python/AppIndicator3-0.1.html
            # http://developer.ubuntu.com/resources/technologies/application-indicators/

            # need to set this for indicator to be shown
            self.indic.set_status(appindicator.IndicatorStatus.ACTIVE)

            # give indicator a menu
            self.menu = gtk.Menu()

            # menu status
            item = gtk.MenuItem()
            item.set_label('Status')
            #item.connect("activate", self.handler_menu_test)
            item.set_sensitive(False)
            item.show()
            self.menu.append(item)

            # menu Backup
            item = gtk.MenuItem()
            item.set_label("Backup")
            item.connect("activate", self.backup)
            item.show()
            self.menu.append(item)
            
            # menu quit
            item = gtk.MenuItem()
            item.set_label("Quit")
            item.connect("activate", self.handler_menu_exit)
            item.show()
            self.menu.append(item)

            self.menu.show()
            self.indic.set_menu(self.menu)

            # # initialize cpu speed display
            # self.update_cpu_speeds()
            # # then start updating every 2 seconds
            # # http://developer.gnome.org/pygobject/stable/glib-functions.html#function-glib--timeout-add-seconds
            # GLib.timeout_add_seconds(2, self.handler_timeout)
            
    def handler_menu_exit(self, evt):
        gtk.main_quit()
            
    def backup():
            call(['bash', '/home/nomad/bin/backup-laptop-neuronfarm.sh'])    
            Notify.init("App Name")
            # Create the notification object
            summary = "Backing up!"
            body = "Meeting at 3PM!"
            icon = "/usr/share/icons/gnome/24x24/emotes/face-smile-big.png"
            notification = Notify.Notification.new(
                summary,
                body, # Optional
                icon, 
            )
            notification.add_action(
                "action_click",
                "Reply to Message",
                backuplaptop_callback_func,
                None # Arguments
            )
            notification.show()            

    def main(self):
        gtk.main()
            
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indic = IndicatorBackup()
    indic.main()
