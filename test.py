#!/usr/bin/env python3#!/usr/bin/env python3 -tt -tt

from tkinter import *

# This example program creates a scroling canvas, and demonstrates
# how to tie scrollbars and canvses together. The mechanism
# is analogus for listboxes and other widgets with
# "xscroll" and "yscroll" configuration options.

class Test(Frame):

    def createWidgets(self):
        self.draw = Canvas(self, width="5i", height="5i",
                           background="white",
                           scrollregion=(0, 0, "20i", "20i"))
        self.draw.scrollY = Scrollbar(self, orient=VERTICAL)
        self.draw['yscrollcommand'] = self.draw.scrollY.set
        self.draw.scrollY['command'] = self.draw.yview

        self.draw.scrollY.pack(side=RIGHT, fill=Y)
        self.draw.pack(side=LEFT)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.createWidgets()

test = Test()

test.mainloop()
