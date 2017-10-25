#!/usr/bin/env python3

# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

# source : https://gist.github.com/jmarroyave/a24bf173092a3b0943402f6554a2094d
# see also : http://www.devdungeon.com/content/desktop-notifications-python-libnotify

# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# http://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html

# https://openclassrooms.com/courses/pygtk/les-widgets-suite-partie-1

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

APPINDICATOR_ID = 'Backup NeuronFarm indicator app'

def backuplaptop_callback_func():
    call(['bash', '/home/nomad/bin/backup-laptop-neuronfarm.sh'])
    
def status(_):
    last = check_output(['bash', '/home/nomad/bin/backup-laptop-neuronfarm.sh', 'last'])
    Notify.init("App Name")
    # Create the notification object
    summary = "Last snapshot"
    body = str(last)
    icon = "/usr/share/icons/gnome/24x24/emotes/face-smile-big.png"
    notification = Notify.Notification.new(
        summary,
        body, # Optional
        icon, 
    )
    notification.show()

def gotobackup(_):
    ### /!\ A CHANGER
    os.system('xdg-open "%s"' % '/media/gobt/Backup-houyo/'  )
    
def backup(_):
    backuplaptop_callback_func()
    
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
    
def quit(_):
    Notify.uninit()
    gtk.main_quit()

# good exemple
# https://askubuntu.com/questions/108035/writing-indicators-with-python-gir-and-gtk3
    
    
def build_menu(menu):
    item_status = gtk.MenuItem('Status')
    #item_status.connect('activate', status)
    menu.append(item_status)
    item_status.set_sensitive(False)

    item_backup = gtk.MenuItem('Backup')
    item_backup.connect('activate', backup)
    menu.append(item_backup)

    item_gotobackup = gtk.MenuItem('Open remote backup folder')
    item_gotobackup.connect('activate', gotobackup)
    menu.append(item_gotobackup)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def timespent(indicator, menu):
    # changement de l'icon du menu
    indicator.set_icon('/usr/share/icons/gnome/24x24/emotes/face-embarrassed.png')
    # ici rajouter un argument pour faire menu 1 ou menu 2
    indicator.set_menu(build_menu(menu))
    print("hello")
    return True


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, \
        os.path.abspath('/usr/share/icons/gnome/24x24/emotes/face-smile-big.png'), \
        appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    menu = gtk.Menu()
    indicator.set_menu(build_menu(menu))
    GObject.timeout_add(1000, timespent, indicator, menu)
    gtk.main()  

main()
