#!/usr/bin/env python

# Global configuration for macros. Also a place we share globals to
# the rest of the project like the main window, statusbar, keyhandler
# etc ... so the functionality is acessable from the key handler
# or the key handler is acessable from the main window ... etc
# The majority of dynamic vars are inited in clipmacro.py

import signal, os, time, sys

#sys.path.append(os.path.dirname(__file__) )

IDLE_TIMEOUT = 15               # Time for a backup save
SYNCIDLE_TIMEOUT = 2            # Time for syncing windows and spelling
UNTITLED = "untitled.txt"       # New (empty) file name
CONFIG_REG = "/apps/clipmac"
BASEX = "~/.clipmac/"

class Config():

    def __init__(self):

        self.full_screen = False
        self.keyh = None
        self.pedwin = None

        # Count down variables
        self.idle = 0;
        self.syncidle = 0;
        self.statuscount = 0

        # Where things are stored (backups, orgs, macros, logs)
        self.config_dir = os.path.expanduser(BASEX)
        self.macro_dir = os.path.expanduser(BASEX + "macros")
        self.data_dir = os.path.expanduser(BASEX + "data")
        self.log_dir = os.path.expanduser(BASEX + "log")
        self.sql_data = os.path.expanduser(BASEX + "sql_data")
        self.sess_data = os.path.expanduser(BASEX + "sess")
        self.sql = None
        self.config_file = "defaults"

        # Where things are stored (UI x/y pane pos.)
        self.config_reg = "/apps/clipmac"
        self.verbose = False

conf = Config()
#print("conf", conf)

# EOF
