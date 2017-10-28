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
from subprocess import call, check_output, PIPE, run

class IndicatorBackup:
    def __init__(self):
            # param1: identifier of this indicator
            # param2: name of icon. this will be searched for in the standard them
            # dirs
            # finally, the category. We're monitoring, so SYSTEM_SERVICES
            self.indic = appindicator.Indicator.new(
                           'Backup Notification indicator app',
                           os.path.abspath('./icon-backup-notification/icon-pitit-chien-violet-p.png'),
                           appindicator.IndicatorCategory.SYSTEM_SERVICES)

            # some more information about the AppIndicator:
            # http://developer.ubuntu.com/api/ubuntu-12.04/python/AppIndicator3-0.1.html
            # http://developer.ubuntu.com/resources/technologies/application-indicators/

            # need to set this for indicator to be shown
            self.indic.set_status(appindicator.IndicatorStatus.ACTIVE)

            # give indicator a menu
            self.menu = gtk.Menu()

            # menu status
            self.status_item = gtk.MenuItem()
            #status.set_label('Status : nothing yet')
            self.status_item.set_label('init ...')
            self.status_item.set_sensitive(False)
            self.status_item.show()
            self.menu.append(self.status_item)

            # menu Backup
            self.backup_item = gtk.MenuItem()
            self.backup_item.set_label("Backup")
            self.backup_item.set_sensitive(False)
            self.backup_item.connect("activate", self.backup)
            self.backup_item.show()
            self.menu.append(self.backup_item)
            
            # menu quit
            out = gtk.MenuItem()
            out.set_label("Quit")
            out.connect("activate", self.handler_menu_exit)
            out.show()
            self.menu.append(out)

            self.menu.show()
            self.indic.set_menu(self.menu)

            # initialize initial status
            #self.check_status()
            # then start updating every 2 seconds
            #
            GLib.timeout_add_seconds(2, self.check_status)

    # def get_cpu_speeds(self):
    #     """Use regular expression to parse speeds of all CPU cores from
    #     /proc/cpuinfo on Linux.
    #     """

    #     f = open('/proc/cpuinfo')
    #     # this gives us e.g. ['2300', '2300']
    #     s = re.findall('cpu MHz\s*:\s*(\d+)\.', f.read())
    #     # this will give us ['2.3', '2.3']
    #     f = ['%.1f' % (float(i) / 1000,) for i in s]
    #     return f

    def check_status(self):

        self.indic.set_icon('/local/VersionControl/GitHub/nomad-fr/scripts-systems/icon-backup-notification/icon-pitit-chien-violet-pb.png')

        # fonctionne quand l'acce VPN ne fonctionne pas
        
        command=['/home/nomad/bin/backup-laptop-neuronfarm.sh', 'last']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)

        print(result.returncode, result.stdout, result.stderr)

        if result.returncode == 0:
            newlabel = 'last backup : '+str(result.stdout)
            self.backup_item.set_sensitive(True)
        if result.returncode != 0:
            newlabel = 'Backup server : '+str(result.stdout)
            self.backup_item.set_sensitive(False)
        self.status_item.set_label(newlabel)
        return True

    # https://developer.gnome.org/gnome-devel-demos/stable/gmenu.py.html.en
        
    def handler_menu_exit(self, evt):
        gtk.main_quit()
            
    def backup(self):
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
