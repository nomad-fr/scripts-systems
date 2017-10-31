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

import threading
import time

class IndicatorBackup:
    def __init__(self):

            self.lock = threading.Lock()
            self.value = 0

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
            self.backup_item.connect("activate", self.backup_t)
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
            
            ## # initialize initial status
            self.check_status()        
            ## # then start updating every 2 seconds
            GLib.timeout_add_seconds(2, self.check_status)
            
    def set_notok_status(self, evt):
        newlabel = 'Backup server : '+str(self.result.stdout)[2:][:-3]
        self.status_item.set_label(newlabel)
        self.set_icon('violet')
        self.backup_item.set_sensitive(False)
        return True

    def set_ok_status(self, evt):
        newlabel = 'last backup : '+str(self.result.stdout)[2:][:-3]
        self.status_item.set_label(newlabel)
        self.set_icon('vert')
        self.backup_item.set_sensitive(True)
        return True
        
    def check_status_t(self):

        self.thread = threading.Thread(target=self.check_status, args=())
        self.thread.daemon = False       # Daemonize thread
        self.thread.start()              # Start the execution        
        
    def check_status(self):
        print(self.value)

        command=['/home/nomad/bin/backup-laptop-neuronfarm.sh', 'last']
        self.result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
        print(self.result.returncode, self.result.stdout, self.result.stderr)
            
        if str(self.result.returncode) == '0':
            self.set_ok_status(self)
        if str(self.result.returncode) == '1':
            self.set_notok_status(self)
            
        return True

# https://developer.gnome.org/gnome-devel-demos/stable/gmenu.py.html.en
        
    def handler_menu_exit(self, evt):
        #self.thread_backup.exit()
        gtk.main_quit()
        
    def backup_t(self, evt):
        self.backup_item.set_sensitive(False)
        self.set_icon('bleu')
        self.backup_item.set_label('backup in progress ...')

        self.thread_backup = threading.Thread(target=self.backup, args=(evt))        
        self.thread_backup.daemon = False       # Daemonize thread
        self.thread_backup.start()              # Start the execution        
        return True
        
    def backup(self,evt):
        with self.lock:
            self.value = 1
            command=['bash', '/home/nomad/bin/backup-laptop-neuronfarm.sh']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
            print(result.returncode, result.stdout, result.stderr)
            
            self.backup_item.set_label("Backup")
            self.backup_item.set_sensitive(True)
            self.set_icon('vert')
            self.value = 0
            return True
        
    def set_icon(self, color):
        if color == 'violet':
            self.indic.set_icon('/local/VersionControl/GitHub/nomad-fr/scripts-systems/icon-backup-notification/icon-pitit-chien-violet-p.png')            
        if color == 'vert':
            self.indic.set_icon('/local/VersionControl/GitHub/nomad-fr/scripts-systems/icon-backup-notification/icon-pitit-chien-vert-p.png')            
        if color == 'bleu':
            self.indic.set_icon('/local/VersionControl/GitHub/nomad-fr/scripts-systems/icon-backup-notification/icon-pitit-chien-bleu-p.png')            
        if color == 'rouge':
            self.indic.set_icon('/local/VersionControl/GitHub/nomad-fr/scripts-systems/icon-backup-notification/icon-pitit-chien-rouge-p.png')            
        return True
        
    def main(self):
        gtk.main()
            
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indic = IndicatorBackup()
    indic.main()
