#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import signal, os, time, sys, subprocess, platform
import warnings

import gi
#from six.moves import range
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

import config, chrisdlg, chrissql

sys.path.append('..' + os.sep + "pycommon")

from pyvguicom import pgutils
sys.path.append(os.path.dirname(pgutils.__file__))

from pyvguicom.pgutils import *
from pyvguicom.pggui import *
from pyvguicom.pgsimp import *

keystate = 0
shiftstate = 0
altstate = 0

# These can be arbitrary texts ... fill in sensible defaults

barr = [
                "text here 0_1",
                "text here 0_2",
                "text here 0_3",
                "text here 0_4",
                ]

barr2 = [
                "text here 0_5",
                "text here 0_6",
                "text here 0_7",
                "text here 0_8",
                ]
barr3 = [
                "text here 21",
                "text here 22",
                "text here 23",
                "text here 24",
                ]
barr4 = [
                "text here 31",
                "text here 32",
                "text here 33",
                "text here 34",
                ]
barr5 = [
                "text here 41",
                "text here 42",
                "text here 43",
                "text here 44",
                ]
barr6 = [
                "text here 51",
                "text here 52",
                "text here 53",
                "text here 54",
                ]
barr7 = [
                "text here 61",
                "text here 62",
                "text here 63",
                "text here 64",
                ]
barr8 = [
                "text here 71",
                "text here 72",
                "text here 73",
                "text here 74",
                ]
barr9 = [
                "text here 81",
                "text here 82",
                "text here 83",
                "text here 84",
                ]

barr10 = [
                "text here 91",
                "text here 92",
                "text here 93",
                "text here 94",
                ]

# -----------------------------------------------------------------------
# Create document

class edPane(Gtk.VPaned):

    def __init__(self, bname = "No Name", focus = False):

        pos = config.conf.sql.get_int("vpaned")
        if pos == 0: pos = 120

        Gtk.VPaned.__init__(self)
        self.set_border_width(3)
        self.set_position(pos)
        self.vbox = buttwin(bname);
        self.add2(self.vbox)
        self.bname = bname
        #self.vbox2 = buttwin(buff, True)
        #self.add1(self.vbox2)

        self.set_size_request(100, 100)

        # Shortcuts to access the editor windows
        self.area  = self.vbox.area
        #self.area2 = self.vbox2.area

    def close_button(self, butt):
        print("Close pressed, deactivated function")
        pass

# -----------------------------------------------------------------------
# Create main document widget with scroll bars

class buttwin(Gtk.VBox):

    def __init__(self, bname, readonly = False):

        global notebook, mained, keystate, shiftstate

        Gtk.VBox.__init__(self)
        self.bname = bname

        # Make it acessable:
        #self.area  = peddoc.pedDoc(buff, mained, readonly)
        self.area = Gtk.Window()
        self.area.set_can_focus(True)

        self.set_spacing(10)

        #print "created", self.area, mained

        # Give access to notebook and main editor window
        #self.area.notebook = notebook
        #self.area.mained = mained
        self.area.fname = ""

        vtext = Gtk.Label(" ")
        self.pack_start(vtext, 0 ,0 , 0)

        bgarr = [
                barr, barr2, barr3, barr4,barr5, barr6, barr7,
                barr8, barr9, barr10
                ]

        for bb in bgarr:
            hbox = Gtk.HBox()
            txtb = Gtk.Label("  ")
            hbox.pack_start(txtb, 1 , 0 , 0)
            for aa in bb:
                cc = "    " + self.bname + "  " + aa + "    "
                ccc = config.conf.sql.get(cc);
                if ccc != None:
                    ddd = ccc[0]
                else:
                    ddd = cc

                butt = RCLButt(ddd, self.rcl, self.rcl2,
                                                ttip = "Action Button")
                butt.ord = 1; butt.id = aa;
                butt.org  = cc
                butt.connect("clicked", self.butt_press, cc)
                hbox.pack_start(butt, 0 ,0 , 0)
                txt = Gtk.Label(label="  ")
                hbox.pack_start(txt, 0 ,0 , 0)

            txtc = Gtk.Label(label="  ")
            hbox.pack_start(txtc, 1 ,0 , 0)

            self.pack_start(hbox, 0 ,0 , 0)

    def rcl(self, arg1, arg2, arg3):
        #print("rcl", arg1, arg2)
        #print("rcl", arg1.ord, arg1.id)
        pass

    def rcl2(self, arg1, arg2, arg3):
        #print("rcl2 label:", "'" + arg1.get_label() + "'",
        #                    "'" + arg1.org + "'")
        mylab = arg1.get_label()
        ccc = config.conf.sql.get(arg1.org);
        #print ("ccc from database:", ccc)
        if ccc == None:
            ccc = []
            ccc.append("Not configured"); ccc.append("")
            config.conf.pedwin.update_statusbar3("Not configured yet.")
            config.conf.pedwin.update_statusbar(ccc[0])

        menu = MenuButt(("To Clip", "Configure"), self.submenu_click)
        # Let it travel on the menu object
        menu.mylab = mylab
        menu.ccc = ccc
        menu.butt = arg1
        menu.area_rbutton(arg1, arg3)

    def submenu_click(self, arg1, arg2, arg3):
        print("submenu_click:", "1", arg1, "2", arg2, "3", arg3)
        #pedconfig.conf.sql.put("xx", xx)
        if arg3 == 0:
            print("submenu_click clip")
            self.toclip(arg1.mylab, arg1.ccc)
        if arg3 == 1:
            print("submenu_click config")
            self.config(arg1.butt, arg1.butt.org, arg1.mylab, arg1.ccc[1])
        if arg3 == 2:
            print("submenu_click face")

    def config(self, butt, par, lab, cont):
        bbb, eee = chrisdlg.config_dlg(lab, cont);
        if eee != None:
            butt.set_label(bbb)
            ret = config.conf.sql.put(par, bbb, eee);
            #print("Saved:", ret, par, bbb)
            config.conf.pedwin.update_statusbar("Saved: '%s'" % par)

    def butt_press(self, butt, par):

        global keystate,  shiftstate, altstate

        mylab = butt.get_label()
        #print("Butt pressed, mylab: [", mylab, "] par:", "'" + par + "'",
        #                "shift:", shiftstate )
        ccc = config.conf.sql.get(par);
        #print("ccc from database:", ccc)
        if ccc == None:
            ccc = []
            ccc.append("Not configured"); ccc.append("")
            config.conf.pedwin.update_statusbar3("Not configured yet.")
            config.conf.pedwin.update_statusbar(ccc[0])

        if shiftstate:
            shiftstate = False
            self.config(butt, par, mylab, ccc[1])
        else:
            self.toclip(mylab, ccc)
        pass

    def toclip(self, mylab, ccc):
        disp2 = Gdk.Display()
        disp = disp2.get_default()
        clip = Gtk.Clipboard.get_default(disp)
        clip.set_text(ccc[1], len(ccc[1]))
        config.conf.pedwin.update_statusbar3(\
                            "Last Button: '" + mylab + "'")
        ppp = str.split(str(ccc[1]), "\n")
        if not ppp[0]:
            config.conf.pedwin.update_statusbar(\
                    "This item is not configured")
        else:
            config.conf.pedwin.update_statusbar( \
                    "Copied to clipboard: '%s'" % ppp[0])

# EOF
