#!/usr/bin/env python3 -tt
import tkinter as tk 
import sys, os, platform, datetime

from date import DateEntry
from tkinter import ttk, font
from client import info
from tkinter.messagebox import askquestion, askokcancel, showinfo
from resources import questions


class MainApplication(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        ttk.Frame.__init__(self, root)
        information = info()

        self.menu = Menu(self, information)
        self.header = Header(self, information)
        self.questionnaire = Questionnaire(self, information)
        self.buttons = Buttons(self, information)

        self.menu.pack(side='top', fill='x')
        self.header.pack(side='top', fill='x', expand=True)
        self.f = ttk.Separator(root).pack(side='top', fill='x', expand=True)
        self.questionnaire.pack(side='top', fill='x', expand=True)
        self.buttons.pack(side='top', fill='x')



class Menu(ttk.Frame):
    def __init__(self, parent, information):
        super(Menu, self).__init__()
        self.info = information

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0 ) # File menu
        editmenu = tk.Menu(menubar, tearoff=0 ) # Edit menu
        viewmenu = tk.Menu(menubar, tearoff=0 ) # Edit menu
        helpmenu = tk.Menu(menubar, tearoff=0 ) # Help menu
        root.config(menu=menubar) # this line actually displays menu

        fileMenu= tk.Menu(menubar, tearoff=0)  
        fileMenu.add_command(label="Save to .txt", command=self.info.toTxt)  
        fileMenu.add_command(label="Save to .csv", command=self.info.toCSV)  
        fileMenu.add_command(label="Save to New Spreadsheet", command=self.info.toSpreadsheet)  
        fileMenu.add_command(label="Append to Spreadsheet", underline=0, command=self.info.appendSpreadsheet, accelerator="Ctrl+A")  
        fileMenu.add_separator()  
        fileMenu.add_command(label="Exit", underline=1, command=exit, accelerator="Ctrl+Q")  

        editMenu= tk.Menu(menubar, tearoff=0)  
        editMenu.add_command(label="Reset Radio-Buttons", command=self.info.rstRadio)  
        editMenu.add_command(label="Reset All", command=self.info.rstAll)  

        viewMenu= tk.Menu(menubar, tearoff=0)  
        viewMenu.add_command(label="Copy Text", command=self.info.toWin)  

        helpMenu= tk.Menu(menubar, tearoff=0)  
        helpMenu.add_command(label="Help", command=help)  
        helpMenu.add_command(label="Upgrade", command=upgrade)
        menubar.add_cascade(label="File", menu=fileMenu)  
        menubar.add_cascade(label="Edit", menu=editMenu)  
        menubar.add_cascade(label="View", menu=viewMenu)  
        menubar.add_cascade(label="Help", menu=helpMenu)  


class Buttons(ttk.Frame):
    def __init__(self, parent, information):
        super(Buttons, self).__init__()
        self.parent = parent
        self.info = information
        buttons = ttk.Frame(self)

        resetButton = ttk.Button(buttons, text="Reset All", command=self.info.rstAll)
        appendButton = ttk.Button(buttons, text="Append Spreadsheet", command=self.info.appendSpreadsheet)

        resetButton.pack(side='left', padx=5, fill='x', expand=True)
        appendButton.pack(side='right', padx=5, fill='x', expand=True)

        buttons.pack(fill='both', expand=True, side=tk.TOP, pady=5)


class Header(ttk.Frame):
    def __init__(self, parent, information):
        super(Header, self).__init__()
        self.parent = parent
        self.info = information

        clientDetails = ttk.Frame(self)

        # Command Buttons

        nameLabel = ttk.Label(clientDetails, text='ID : ')
        nameEntry = ttk.Entry(clientDetails, textvariable=self.info.name, width=55)
        evalLabel = ttk.Label(clientDetails, text='Evaluator : ')
        evalEntry = ttk.Entry(clientDetails, textvariable=self.info.eval, width=55)
        dobLabel = ttk.Label(clientDetails, text='   DoB : ')
        dobEntry = ttk.Entry(clientDetails, textvariable=self.info.dob, width=10)
        dobButton = ttk.Button(clientDetails, text='Format')
        dateLabel = ttk.Label(clientDetails, text='   Test date : ')
        dateEntry = ttk.Entry(clientDetails, textvariable=self.info.date, width=10)
        dateButton = ttk.Button(clientDetails, text='Format', command=self.formatDateWidget)

        nameLabel.grid(row=0, column=0, sticky='E')
        nameEntry.grid(row=0, column=1, columnspan=5, sticky='W')
        evalLabel.grid(row=1, column=0, sticky='E')
        evalEntry.grid(row=1, column=1, columnspan=5, sticky='W')
        dobLabel.grid(row=0, column=7, sticky='E')
        dobEntry.grid(row=0, column=8, sticky='W')
        dateLabel.grid(row=1, column=7, sticky='E')
        dateEntry.grid(row=1, column=8, sticky='W')

        clientDetails.pack(fill='both', expand=True, side=tk.TOP)

        header = ttk.Frame(self)

        labelheading = ttk.Label(header, text='       Questions', justify=tk.RIGHT)
        labelheading.pack(side='left', fill='x')
        labelheading = ttk.Label(header, text='No   Maybe   Yes  ', justify=tk.RIGHT)
        labelheading.pack(side='right')

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
        reverse = [7, 11, 14, 21, 25]
        for number, question in enumerate(questions, 1):
            self.var = tk.IntVar(value=-1)
            # width = 5
            line = '{:5}'.format(number, fill=' ')+' : '+question.strip()
            label = tk.Label(self.radioFrame, font=('Consolas', sizeOfFont), text='{: <75.75}'.format(line), pady=3)
            if number % 5 == 0:
                label.configure(background='#d0d0d0')
            label.grid(row=number, column=0, sticky=tk.W)
            options = ['?', 'N', 'M', 'Y']
            for answer in range(-1, 3):
                button = tk.Radiobutton(self.radioFrame, borderwidth=1, variable=self.var, text=options[answer+1], width=5, indicatoron=0)
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

def on_closing():
    if askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def help():
    file = open('README.md', 'r')
    showinfo("Help", file.read())

def upgrade():
    if platform.system() == 'Windows':
        showinfo("ERROR", "Windows client cannot update yet. Download new versions here : https://github.com/inyoka/sand.git")
        return
    else: 
        result = askquestion("Upgrade Mac / Linux", "Are you sure you want to run an application upgrade? Program might become unstable.", icon='warning')
        if result == 'yes':
            try:
                print("Performing 'git pull' ...")
                os.system('git pull')
                print("Appears to have been succesful.")
                showinfo('UPGRADE', 'Done!!!')
            except Exception as e:
                print("Failed error: " + str(e))
                showinfo('Upgrade Failed', str(e))

def fontSize():
    if platform.system() == 'Windows':
        return 10
    else :
        return 12

if __name__ == '__main__':
    sizeOfFont = fontSize()
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family='Verdana',size=sizeOfFont, weight='normal')
    root.wm_title('Strengths & Difficulties - SAND')
    root.resizable(width=False, height=False)
    MainApplication(root).pack(side='top', fill='both')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
