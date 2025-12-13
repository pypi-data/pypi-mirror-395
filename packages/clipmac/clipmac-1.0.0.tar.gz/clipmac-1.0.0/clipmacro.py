#!/usr/bin/env python

'''
 This is open source macro feeder. Written in python. The motivation for
 this project was to create macro shortcuts for pasting pre made
 text onto the clipboard.

 The clipmac program functions near identical on
    Linux / Windows / Mac / Raspberry PI

 Redirecting stdout to a fork to real stdout and log. This way
 messages can be seen even if clipmac is started without a
 terminal (from the GUI)

'''

import os, sys, getopt, signal

from clipmac import chrissql

basedir = os.path.dirname(chrissql.__file__)
#print(basedir)
sys.path.append(basedir)

from clipmac import config
#config.conf = config.Config()

import config
config.basedir = basedir

from clipmac import chriswin

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

mainwin = None
show_timing = 0
show_config = 0
clear_config = 0
use_stdout = 0

VERSION = "1.0.0"

# ------------------------------------------------------------------------

def main(strarr):

    if(config.conf.verbose):
        print("clipmac running on", "'" + os.name + "'", \
            "GTK", Gtk._version, "PyGtk", \
               "%d.%d.%d" % (Gtk.get_major_version(), \
                    Gtk.get_minor_version(), \
                        Gtk.get_micro_version()))

    signal.signal(signal.SIGTERM, terminate)

    # Initialize sqlite to load / save preferences & other info
    config.conf.sql = chrissql.Pedsql(config.conf.sql_data)

    mainwin =  chriswin.ChrisMainWin(None, None, strarr)
    config.conf.pedwin = mainwin

    Gtk.main()

def help():

    #print()
    #print("clipmacro version: ", config.conf.version)
    print("Usage: " + os.path.basename(sys.argv[0]) + " [options]")
    print("Options:  -d level  - Debug level 1-10. (Limited implementation)")
    print("          -v        - Verbose (to stdout and log)")
    print("          -c        - Dump Config")
    print("          -V        - Show version")
    print("          -x        - Clear (eXtinguish) config (will prompt)")
    print("          -h        - Help. (This screen)")
    #print()

# ------------------------------------------------------------------------

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream

   def write(self, data):
       self.stream.write(data)
       self.stream.flush()

   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()

   def __getattr__(self, attr):
       return getattr(self.stream, attr)

def terminate(arg1, arg2):

    if(config.conf.verbose):
        print("Terminating clipmac.py, saving files to ~/clipmac")

    # Save all
    config.conf.pedwin.activate_quit(None)
    #return signal.SIG_IGN

def mainfunc():

    global clear_config, show_config, use_stdout

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h?fvxctVo")
    except getopt.GetoptError as err:
        print("Invalid option(s) on command line:", err)
        sys.exit(1)

    #print "opts", opts, "args", args

    config.conf.version = VERSION

    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-?": help();  exit(1)
        if aa[0] == "-V": print("Version", config.conf.version); \
            exit(1)
        if aa[0] == "-f": config.conf.full_screen = True
        if aa[0] == "-v": config.conf.verbose = True
        if aa[0] == "-x": clear_config = True
        if aa[0] == "-c": show_config = True
        if aa[0] == "-t": show_timing = True
        if aa[0] == "-o": use_stdout = True

    try:
        if not os.path.isdir(config.conf.config_dir):
            if(config.conf.verbose):
                print("making", con.config_dir)
            os.mkdir(config.conf.config_dir)
    except: pass

    # Let the user know it needs fixin'
    if not os.path.isdir(config.conf.config_dir):
        print("Cannot access config dir:", config.conf.config_dir)
        sys.exit(1)

    if not os.path.isdir(config.conf.data_dir):
        if(config.conf.verbose):
            print("making", con.data_dir)
        os.mkdir(config.conf.data_dir)

    if not os.path.isdir(config.conf.log_dir):
        if(config.conf.verbose):
            print("making", config.conf.log_dir)
        os.mkdir(config.conf.log_dir)

    if not os.path.isdir(config.conf.macro_dir):
        if(config.conf.verbose):
            print("making", config.conf.macro_dir)
        os.mkdir(config.conf.macro_dir)

    if not os.path.isdir(config.conf.sess_data):
        if(config.conf.verbose):
            print("making", config.conf.sess_data)
        os.mkdir(config.conf.sess_data)

    #config.conf.keyh = pyedlib.keyhand.KeyHand()
    config.conf.mydir = os.path.abspath(__file__)

    # To clear all config vars
    if clear_config:
        print("Are you sure you want to clear config ? (y/n)")
        sys.stdout.flush()
        aa = sys.stdin.readline()
        if aa[0] == "y":
            print("Removing configuration ... ", end=' ')
            # Initialize sqlite to load / save preferences & other info
            config.conf.sql = chrissql.Pedsql(config.conf.sql_data)
            config.conf.sql.rmall()
            print("OK")
        else:
            print("Not deleted.")
            pass
        sys.exit(0)

    # To check all config vars
    if show_config:
        print("Dumping configuration:")
        # Initialize sqlite to load / save preferences & other info
        config.conf.sql = chrissql.Pedsql(config.conf.sql_data)
        ss = config.conf.sql.getall();
        for aa in ss:
            print(aa)
        sys.exit(0)

    #Uncomment this for silent stdout
    if use_stdout:
        #print("Using real stdout")
        sys.stdout = Unbuffered(sys.stdout)
        sys.stderr = Unbuffered(sys.stderr)
    else:
        pass
        #sys.stdout = pyedlib.log.fake_stdout()
        #sys.stderr = pyedlib.log.fake_stdout()

    # Uncomment this for buffered output
    if config.conf.verbose:
        #print("Started clipmac")
        #pyedlib.log.print("Started clipmac")
        pass

    main(args[0:])

# Start of program:

if __name__ == '__main__':
    mainfunc()

# EOF
