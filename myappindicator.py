#!/usr/bin/env python3

# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

# source : https://gist.github.com/jmarroyave/a24bf173092a3b0943402f6554a2094d
# see also : http://www.devdungeon.com/content/desktop-notifications-python-libnotify

import os
import signal
import json

from urllib import request
from urllib.error import URLError
from urllib.request import urlopen

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify

APPINDICATOR_ID = 'myappindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/usr/share/icons/gnome/24x24/emotes/face-smile-big.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_joke = gtk.MenuItem('Joke')
    item_joke.connect('activate', joke)
    menu.append(item_joke)

    item_backup = gtk.MenuItem('Backup')
    item_backup.connect('activate', backup)
    menu.append(item_backup)
    
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)

    menu.append(item_quit)
    menu.show_all()
    return menu

def my_callback_func():
    pass

def joke(_):
    Notify.init("App Name")
    # Create the notification object
    summary = "Wake up!"
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
        my_callback_func,
        None # Arguments
    )
    notification.show()

def backup(_):
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
        my_callback_func,
        None # Arguments
    )
    notification.show()
    
def quit(_):
    Notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

main()
