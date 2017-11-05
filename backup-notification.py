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
import time, datetime
import locale, sys

icon_path = os.path.dirname(os.path.dirname(__file__) + '/icon-backup-notification/') + '/'

print(icon_path)

class IndicatorBackup:
    def __init__(self):

        if len(sys.argv) == 2:
            self.script=sys.argv[1]
        else:
            exit
            
        self.lock = threading.Lock()
        
        # param1: identifier of this indicator
        # param2: name of icon. this will be searched for in the standard them
        # dirs
        # finally, the category. We're monitoring, so SYSTEM_SERVICES
        self.indic = appindicator.Indicator.new(
                           'Backup Notification indicator app',
                           os.path.abspath(icon_path+'icon-pitit-chien-violet-p.png'),
                           appindicator.IndicatorCategory.SYSTEM_SERVICES)

        # some more information about the AppIndicator:
        # http://developer.ubuntu.com/api/ubuntu-12.04/python/AppIndicator3-0.1.html
        # http://developer.ubuntu.com/resources/technologies/application-indicators/
        # https://developer.gnome.org/gnome-devel-demos/stable/gmenu.py.html.en
            
        # need to set this for indicator to be shown
        self.indic.set_status(appindicator.IndicatorStatus.ACTIVE)

        # give indicator a menu
        self.menu = gtk.Menu()

        command=['bash', self.script, 'host']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
            
        # menu header
        self.header_item = gtk.MenuItem('backup server : '+str(result.stdout)[2:][:-3])
        self.header_item.set_sensitive(False)
        self.header_item.show()
        self.menu.append(self.header_item)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        self.menu.append(sep)            
            
        # menu status
        self.status_item = gtk.MenuItem()
        #status.set_label('Status : nothing yet')
        self.status_item.set_label('init ...')
        self.status_item.set_sensitive(False)
        self.status_item.show()
        self.menu.append(self.status_item)

        # next
        self.next_item = gtk.MenuItem()
        #status.set_label('Status : nothing yet')
        self.next_item.set_label('next backup in : ...')
        self.next_item.set_sensitive(False)
        self.next_item.show()
        self.menu.append(self.next_item)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        self.menu.append(sep)            

        # go to backup            
        self.gotobackup_item = gtk.MenuItem('Open remote backup folder')
        self.gotobackup_item.connect('activate', self.gotobackup)
        self.gotobackup_item.show()
        self.menu.append(self.gotobackup_item)
            
        # menu Backup
        self.backup_item = gtk.MenuItem()
        self.backup_item.set_label("Backup now")
        self.backup_item.set_sensitive(False)
        self.backup_item.connect("activate", self.backup_t)
        self.backup_item.show()
        self.menu.append(self.backup_item)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        self.menu.append(sep)            
            
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
        newlabel = 'last backup : unknow'
        self.status_item.set_label(newlabel)
        self.set_icon('violet')
        self.backup_item.set_sensitive(False)
        self.hide_gotobackup()
        return True

    def set_ok_status(self, evt):
        newlabel = 'last backup : '+str(self.result.stdout)[2:][:-3]
        self.backup_item.set_label("Backup now")
        self.status_item.set_label(newlabel)        
        self.backup_item.set_sensitive(True)
        self.set_icon('vert')
        self.show_gotobackup()
        return True

    def next_time(self, evt):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
        dt_str = str(self.result.stdout)[2:][:-3]
        last_date = datetime.datetime.strptime(dt_str, '%a %b %d %H:%M %Y')
        hope_date = last_date + datetime.timedelta(hours=1)

        print('last_date : ', last_date)                
        print('hope_date : ', hope_date)        
        now = datetime.datetime.now()
        print('now       : ', str(now))
        if now > hope_date:
            print('backup needed')
            newlabel = 'auto backup now' 
            self.next_item.set_label(newlabel)
            self.backup_t(evt)
        else:
            print('no backup needed')
            next = hope_date - now
            newlabel = 'next auto backup in about '+str(next)[:-10][2:]+' min'
            print(newlabel)
            self.next_item.set_label(newlabel)
        return True

    def hide_gotobackup(self):
        self.gotobackup_item.set_sensitive(False)
        return True

    def show_gotobackup(self):
        self.gotobackup_item.set_sensitive(True)
        return True
    
    def check_status(self):
        print('----')
        with self.lock:
            command=[self.script, 'last']
            self.result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
            if str(self.result.returncode) == '0':
                self.set_ok_status(self)
                self.next_time(self)
                command=['bash', self.script, 'backup_folder']
                result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
                self.folder=str(result.stdout)[2:][:-3]
                if len(self.folder) == 0:
                   self.hide_gotobackup()
            if str(self.result.returncode) == '1':
                self.set_notok_status(self)            
            return True
        
    def handler_menu_exit(self, evt):
        #self.thread_backup.exit()
        gtk.main_quit()

    def gotobackup(self, evt):
        os.system('xdg-open "%s"' % self.folder)

    def backup_t(self, evt):
        self.backup_item.set_sensitive(False)
        self.set_icon('bleu')
        self.backup_item.set_label('backup in progress ...')
        self.thread_backup = threading.Thread(target=self.backup, args=(evt,))        
        self.thread_backup.daemon = False       # Daemonize thread
        self.thread_backup.start()              # Start the execution
        return True
        
    def backup(self,evt):
        with self.lock:
            self.backup_item.set_sensitive(False)
            command=['bash', self.script]
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=False)
            print(result.stdout)
            self.set_icon('vert')
            return True
        
    def set_icon(self, color):
        if color == 'violet':
            self.indic.set_icon(icon_path+'icon-pitit-chien-violet-p.png')
        if color == 'vert':
            self.indic.set_icon(icon_path+'icon-pitit-chien-vert-p.png')
        if color == 'bleu':
            self.indic.set_icon(icon_path+'icon-pitit-chien-bleu-p.png')
        if color == 'rouge':
            self.indic.set_icon(icon_path+'icon-pitit-chien-rouge-p.png')
        return True
        
    def main(self):
        gtk.main()
            
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    indic = IndicatorBackup()
    indic.main()
