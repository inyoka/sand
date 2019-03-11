#!/usr/bin/env python3 -tt
import tkinter as tk 
import datetime
from date import DateEntry
from tkinter import ttk, font
from client import info
from tkinter.messagebox import askquestion
import sys


class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self)
        information = info()
        self.parent = parent

        self.menu = Menu(self, information)
        #self.toolbar = Toolbar(self, information)
        self.header = Header(self, information)
        self.questionnaire = Questionnaire(self, information)
        self.buttons = Buttons(self, information)

        self.menu.pack(side="top", fill="x")
        #self.toolbar.pack(side="top", fill="x")
        self.header.pack(side='top', fill='x', expand=True)
        self.questionnaire.pack(side='top', fill='x', expand=True)
        self.buttons.pack(side='bottom', fill='x', expand=True)

class Toolbar(ttk.Frame):
    def __init__(self, parent, information):
        super(Toolbar, self).__init__()
        self.info = information

        toolbar = ttk.Frame(self) 
        insertButt = ttk.Button(toolbar, text="Test", command=root.quit)
        insertButt.pack(side="left")
        deleteButt = ttk.Button(toolbar, text="Test", command=root.quit)
        deleteButt.pack(side="left")
        toolbar.pack()

class Menu(ttk.Frame):
    def __init__(self, parent, information):
        super(Menu, self).__init__()
        self.info = information

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0 ) # File menu
        editmenu = tk.Menu(menubar, tearoff=0 ) # Edit menu
        root.config(menu=menubar) # this line actually displays menu

        fileMenu= tk.Menu(menubar, tearoff=0)  
        fileMenu.add_command(label="Save to .txt", command=self.info.toTxt)  
        fileMenu.add_command(label="Save to .csv", command=self.info.toCSV)  
        fileMenu.add_command(label="Save to New Spreadsheet", command=self.info.toSpreadsheet)  
        fileMenu.add_command(label="Append to Spreadsheet", command=self.info.appendSpreadsheet, accelerator="Ctrl+A")  
        fileMenu.add_separator()  
        fileMenu.add_command(label="Exit", underline=1, command=exit, accelerator="Ctrl+Q")  

        self.bind_all("<Control-a>", self.info.appendSpreadsheet)
        self.bind_all("<Control-q>", self.quit)

        editMenu= tk.Menu(menubar, tearoff=0)  
        editMenu.add_command(label="Reset Radio-Buttons", command=self.info.rstRadio)  
        editMenu.add_command(label="Reset All", command=self.info.rstAll)  

        menubar.add_cascade(label="File", menu=fileMenu)  
        menubar.add_cascade(label="Edit", menu=editMenu)  


class Buttons(ttk.Frame):
    def __init__(self, parent, information):
        super(Buttons, self).__init__()
        self.parent = parent
        self.info = information
        buttons = ttk.Frame(self)

        rstButton = ttk.Button(buttons, text="Reset All", command=self.info.rstAll)
        winButton = ttk.Button(buttons, text="View", command=self.info.toWin)
        txtButton = ttk.Button(buttons, text="To text", command=self.info.toTxt)
        sprButton = ttk.Button(buttons, text="Append Spreadsheet", command=self.info.appendSpreadsheet)
        extButton = ttk.Button(buttons, text="Quit", command=exit)

        rstButton.grid(row=0, column=0, sticky='w')
        winButton.grid(row=0, column=1, sticky='e')
        sprButton.grid(row=0, column=2)
        txtButton.grid(row=0, column=3)

        buttons.grid_columnconfigure(1, weight=1)
        buttons.pack(fill='both', expand=True, side=tk.TOP, pady=5)


class Header(ttk.Frame):
    def __init__(self, parent, information):
        super(Header, self).__init__()
        self.parent = parent
        self.info = information

        clientDetails = ttk.Frame(self)

        # Command Buttons

        nameLabel = ttk.Label(clientDetails, text='ID : ')
        nameEntry = ttk.Entry(clientDetails, textvariable=self.info.name, width=60)
        evalLabel = ttk.Label(clientDetails, text='Evaluator : ')
        evalEntry = ttk.Entry(clientDetails, textvariable=self.info.eval, width=60)
        dobLabel = ttk.Label(clientDetails, text='DoB : ')
        dobEntry = ttk.Entry(clientDetails, textvariable=self.info.dob, width=10)
        dobButton = ttk.Button(clientDetails, text='Format')
        dateLabel = ttk.Label(clientDetails, text='Test date :')
        dateEntry = ttk.Entry(clientDetails, textvariable=self.info.date, width=10)
        dateButton = ttk.Button(clientDetails, text='Format', command=self.formatDateWidget)

        nameLabel.grid(row=0, column=0, sticky='E')
        nameEntry.grid(row=0, column=1, columnspan=5, sticky='W')
        evalLabel.grid(row=1, column=0, sticky='E')
        evalEntry.grid(row=1, column=1, columnspan=5, sticky='W')
        dobLabel.grid(row=2, column=1, sticky='W')
        dobEntry.grid(row=2, column=2, sticky='W')
        dateLabel.grid(row=2, column=3, sticky='W')
        dateEntry.grid(row=2, column=4, sticky='W')

        clientDetails.pack(fill='both', expand=True, side=tk.TOP)

        header = ttk.Frame(self)
        headings = ['       Questions'+' '*112, 'No   ', 'Maybe', '   Yes']
        for col, heading in enumerate(headings):
            labelheading = ttk.Label(header, text=heading, justify=tk.RIGHT)
            labelheading.grid(row=1, column=col, sticky=tk.E)
        header.pack(fill='both', expand=True, side=tk.TOP)

    def formatDateWidget(self):
        entrylist = [c for c in self.info.dob.get() if c != '/']
        for pos in [2, 5]:
            if len(entrylist) > pos:
                entrylist.insert(pos, '/')
        self.info.dob.set(''.join(entrylist))


class Questionnaire(ttk.Frame):
    def __init__(self, master, information):
        super(Questionnaire, self).__init__()
        self.info = information
        self.master = master
        self.questions = ttk.Frame(self)
        self.radioFrame = ttk.Frame(self.questions)
        self.askQuestions()
        self.radioFrame.pack(fill='both', expand=True, side=tk.TOP)
        self.questions.pack(fill='both', expand=True, side=tk.TOP)

    def askQuestions(self):
        file = open('questions.txt')
        questionlist = file.readlines()
        reverse = [7, 11, 14, 21, 25]
        for number, question in enumerate(questionlist, 1):
            self.var = tk.IntVar(value=-1)
            # width = 5
            line = '{:5}'.format(number, fill=' ')+' : '+question.strip()
            label = tk.Label(self.radioFrame, font=('Consolas', 12), text='{: <75.75}'.format(line), pady=3)
            if number % 5 == 0:
                label.configure(background='#d0d0d0')
            label.grid(row=number, column=0, sticky=tk.W)
            options = ['?', 'N', 'M', 'Y']
            for answer in range(-1, 3):
                                        variable=self.var,
                                        text=options[answer+1], width=5,
                                        indicatoron=0)
                button.configure(value=answer)
                if number in reverse:
                    if answer == 0:
                        button.configure(value=2)
                    elif answer == 2:
                        button.configure(value=0)

                if number % 5 == 0:
                    button.configure(background='#d0d0d0')
                button.grid(row=number, column=answer+2)
            self.info.buttons.append(button)
            self.info.answers.append(self.var)

def exit():
    result = askquestion("Exit", "Are you sure?\n\n have you saved?", icon='warning')
    if result == 'yes':
        print('Exiting application')
        root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap("img/icon.ico")
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family='Verdana',size=12, weight='normal')
    root.wm_title('Strengths & Difficulties - SAND')
    MainApplication(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
