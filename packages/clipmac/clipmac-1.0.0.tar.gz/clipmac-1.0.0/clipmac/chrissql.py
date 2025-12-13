#!/usr/bin/env python

import sys, os, time, sqlite3

# Replaces g c o n f, so it is less platform dependent

class Pedsql():

    def __init__(self, file):

        #self.take = 0

        try:
            self.conn = sqlite3.connect(file)
        except:
            print("Cannot open/create db:", file, sys.exc_info())
            return
        try:
            self.c = self.conn.cursor()
            # Create table
            self.c.execute("create table if not exists config \
             (pri INTEGER PRIMARY KEY, key text, val text, clip text)")
            self.c.execute("create index if not exists iconfig on config (key)")
            self.c.execute("create index if not exists pconfig on config (pri)")
            self.c.execute("PRAGMA synchronous=OFF")
            # Save (commit) the changes
            self.conn.commit()
        except:
            print("Cannot insert sql data", sys.exc_info())

        finally:
            # We close the cursor, we are done with it
            #c.close()
            pass

    # --------------------------------------------------------------------
    # Return None if no data

    def   get(self, kkk):
        try:
            #c = self.conn.cursor()
            if os.name == "nt":
                self.c.execute("select * from config where key = ?", (kkk,))
            else:
                self.c.execute("select * from config indexed by iconfig where key = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("Cannot get sql data", sys.exc_info())
            rr = None
        finally:
            #c.close
            pass
        if rr:
            return rr[2], rr[3]
        else:
            return None

    # --------------------------------------------------------------------
    # Return zero if no data

    def get_int(self, kkk):
        ret = self.get(kkk)
        if ret:
            return int(float(ret[0]))
        else:
            return int(0)

    # --------------------------------------------------------------------
    # Return empty if no data

    def get_str(self, kkk):
        ret = self.get(kkk)
        if ret:
            return str(ret)
        else:
            return ""

    # --------------------------------------------------------------------
    # Return False if cannot put data

    def   put(self, key, val, clip):

        #got_clock = time.clock()

        ret = True
        try:
            #c = self.conn.cursor()
            if os.name == "nt":
                self.c.execute("select * from config where key == ?", (key,))
            else:
                self.c.execute("select * from config indexed by iconfig where key == ?", (key,))
            rr = self.c.fetchall()
            if rr == []:
                #print "inserting"
                self.c.execute("insert into config (key, val, clip) \
                    values (?, ?, ?)", (key, val, clip))
            else:

                #print "updating"
                if os.name == "nt":
                    self.c.execute("update config set val = ?, clip = ? where key = ?",\
                                     (val, clip, key))
                else:
                    self.c.execute(
                    "update config indexed by iconfig set val = ?, clip = ? where key = ?",\
                                     (val, clip, key))
            self.conn.commit()
        except:
            print("Cannot put sql data", sys.exc_info())
            ret = False
        finally:
            #c.close
            pass

        #self.take += time.clock() - got_clock

        return ret

    # --------------------------------------------------------------------
    # Get All

    def   getall(self):
        try:
            #c = self.conn.cursor()
            self.c.execute("select * from config")
            rr = self.c.fetchall()
        except:
            print("Cannot get sql data", sys.exc_info())
        finally:
            #c.close
            pass
        return rr

    # --------------------------------------------------------------------
    # Return None if no data

    def   rmall(self):
        #print("removing all")
        try:
            #c = self.conn.cursor()
            self.c.execute("delete from config")
            self.conn.commit()
            rr = self.c.fetchone()
        except:
            print("Cannot delete sql data", sys.exc_info())
        finally:
            #c.close
            pass
        if rr:
            return rr[1]
        else:
            return None

# EOF
