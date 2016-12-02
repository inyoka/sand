#!/usr/bin/env python3 -tt
import tkinter as tk
from client import Info
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import askquestion
from tkinter import scrolledtext
import dicttools
import csv
import sys

import datetime
import time


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self)
        information = Info()
        self.parent = parent

        self.toolbar = Toolbar(self)
        self.header = Header(self, information)
        self.questionnaire = Questionnaire(self, information)
        self.footer = Footer(self, information)

        self.toolbar.pack(side="top", fill="x")
        self.header.pack(side='top', fill='x', expand=True)
        self.questionnaire.pack(side='top', fill='x', expand=True)
        self.footer.pack(side='bottom', fill='x', expand=True)


class Toolbar(tk.Frame):
    pass


class Header(tk.Frame):
    def __init__(self, parent, information):
        super(Header, self).__init__()
        self.parent = parent
        self.info = information

        clientDetails = tk.Frame(self)
        nameLabel = tk.Label(clientDetails, text='Name or Reference (optional) : ').grid(row=0, column=0)
        nameEntry = tk.Entry(clientDetails, textvariable=self.info.name).grid(row=0, column=1)
        dobLabel = tk.Label(clientDetails, text='Date(MM/DD/YYYY)').grid(row=1, column=0)
        self.dobEntry = tk.Entry(clientDetails, textvariable=self.info.dob).grid(row=1, column=1)
        dobButton = tk.Button(clientDetails, text='Format DoB', command=self.formatDateWidget).grid(row=1, column=2)
        clientDetails.pack(fill='both', expand=True, side=tk.TOP)

        header = tk.Frame(self)
        headings = [' '*self.info.width*2, '?', 'N', 'M', 'Y']
        for col, heading in enumerate(headings):
            labelheading = tk.Label(header, text=heading, justify=tk.RIGHT)
            labelheading.grid(row=1, column=col, sticky=tk.E)
        header.pack(fill='both', expand=True, side=tk.TOP)

    def formatDateWidget(self):
        entrylist = [c for c in self.info.dob.get() if c != '/']
        for pos in [2, 5]:
            if len(entrylist) > pos:
                entrylist.insert(pos, '/')
        self.info.dob.set(''.join(entrylist))


class Questionnaire(tk.Frame):
    def __init__(self, master, information):
        super(Questionnaire, self).__init__()
        self.info = information
        self.master = master
        self.questions = tk.Frame(self)
        self.radioFrame = tk.Frame(self.questions)
        self.askQuestions()
        self.radioFrame.pack(fill='both', expand=True, side=tk.TOP)
        # scrollbar = tk.Scrollbar(self.questions).pack(side='right', fill='y')
        self.questions.pack(fill='both', expand=True, side=tk.TOP)

    def askQuestions(self):
        file = open('questions.txt')
        questionlist = file.readlines()
        for number, question in enumerate(questionlist, 1):
            self.var = tk.IntVar(value=-1)
            width = 5
            line = '{:5}'.format(number, fill=' ')+' : '+question.strip()
            label = tk.Label(self.radioFrame, text=line)
            if number % 5 == 0:
                label.configure(background='#d0d0d0')
            label.grid(row=number, column = 0, sticky=tk.W)
            options = ['?', 'No', 'Maybe', 'Yes']
            for answer in range(-1,3):
                button = tk.Radiobutton(self.radioFrame, borderwidth=10, variable=self.var,
                            text=options[answer+1], width=5, value=answer, indicatoron=0)
                if number % 5 == 0:
                    button.configure(background='#d0d0d0')
                button.grid(row=number, column=answer+2)
            self.info.buttons.append(button)
            self.info.answers.append(self.var)


class Footer(tk.Frame):
    def __init__(self, parent, information):
        super(Footer, self).__init__()
        self.parent = parent
        self.info = information
        footer = tk.Frame(self)
        # reset_button = tk.Button(footer, text="Reset All", command=self.resetConfirm).grid(row=0, column=0, sticky='w')
        footer.grid_columnconfigure(1, weight=1)
        # output_button = tk.Button(footer, text="Output", command=self.info.outputResults).grid(row=0, column=2)
        done_button = tk.Button(footer, text="Export .csv", command=self.info.createReport).grid(row=0, column=3)
        exit_button = tk.Button(footer, text="Quit", command=self.exit).grid(row=0, column=4)
        footer.pack(fill='both', expand=True, side=tk.TOP, pady=5)

    def resetConfirm(self):
        result = askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.info.resetFields()

    def exit(self):
        # Stub awaiting an seperate quit button.
        print('Exiting application')
        root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title('Strengths & Difficulties - SAND')
    MainApplication(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
