#!/usr/bin/env python3 -tt
import tkinter as tk
import datetime
from pathlib import Path
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from tkinter.messagebox import askquestion
from resources import questions, textLines, csvLines, windowLines
import csv, time, os


pathname = os.path.expanduser(Path("~/Desktop/sand.csv"))
today = datetime.date.today().strftime('%d/%m/%Y') 

def writeHeadings(self, w):
    w.writerow(['No.']+['ID']+['Evaluator']+['Date']+['DoB']+['Pro-Social']+['Hyperactivity']+['Emotional']
        +['Conduct']+['Peer']+['Total']+['Incomplete'])

def writeDetails(self, w):
    w.writerow(['']+[self.name.get()]+[self.eval.get()]+[self.date.get()]+[self.dob.get()]
        +[str(self.fnlScore['prosocial'])]
        +[str(self.fnlScore['hyperactivity'])]
        +[str(self.fnlScore['emotional'])]
        +[str(self.fnlScore['conduct'])]
        +[str(self.fnlScore['peer'])]
        +[str(self.stressScore)]
        +[a for a in list(self.incomplete)])


class info():
    def __init__(self):
        self.width = max(questions, key=len)
        self.traits = {'emotional': [3, 8, 13, 16, 24],
                       'conduct': [5, 7, 12, 18, 22],
                       'hyperactivity': [2, 10, 15, 21, 25],
                       'peer': [6, 11, 14, 19, 23],
                       'prosocial': [1, 4, 9, 17, 20]}
        self.incomplete = set()
        self.name = tk.StringVar()
        self.eval = tk.StringVar()
        self.dob = tk.StringVar(value='01/12/2000')
        self.date = tk.StringVar(value=today)
        self.time = time.strftime("%a %d-%m-%Y %H:%M:%S", time.localtime())
        self.buttons = []
        self.answers = []
        self.fnlScore = {}
        self.stressScore = int()


    def rstAll(self):
        result = askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.name.set(value='')
            self.eval.set(value='')
            self.dob.set(value='')
            self.date.set(value=today)
            for a in self.answers:
                a.set(value = -1)

    def rstRadio(self):
        result = askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            for a in self.answers:
                a.set(value = -1)

    def addScore(self, trait):
        self.lineNumbers = self.traits[trait]
        score = 0
        for item in self.lineNumbers:
            if self.answers[item-1].get() > -1:
                score = score + self.answers[item-1].get()
            else :
                self.incomplete.add(trait)
        return(score)

    def sumTraits(self):
        for trait in self.traits.keys():
            self.fnlScore[trait] = self.addScore(trait)

    def calcStress(self):
        self.stressScore = (
            sum(self.fnlScore.values()) - self.fnlScore.get('prosocial'))

    def setup(self):
        # self.reverseAnswers()
        self.sumTraits()
        self.calcStress()

    def toWin(self):
        self.setup()
        top = tk.Tk()
        top.title("Copy & Paste Report ...")
        scrollbar = tk.Scrollbar(top)

        txtScroll = tk.Text(top, width=80, height=10, wrap="word",
                            yscrollcommand=scrollbar.set,
                            borderwidth=1, highlightthickness=0)
        for line in windowLines(self):
            txtScroll.insert(tk.INSERT, line)

        scrollbar.config(command=txtScroll.yview)
        scrollbar.pack(side="right", fill="y")
        txtScroll.pack(side='top', fill=tk.BOTH, expand=True)

        button = tk.Button(top, text="Dismiss", command=top.destroy)
        button.pack()

    def toTxt(self):  # exportText(self):
        self.setup()
        name = asksaveasfilename(initialfile = self.name.get(), defaultextension=".txt")
        if name is None:
            return
        else:
            f = open(name, 'w')
            for line in textLines(self):
                f.write(line)

    def toCSV(self):
        self.setup()

        name = asksaveasfile(mode='w', initialfile = self.name.get(), defaultextension=".csv")
        if name is None:
            return
        with name as f:
            w = csv.writer(f)
            for line in csvLines(self):
                w.writerow(line)
            f.close()
        f.close()

    def toSpreadsheet(self):
        self.setup()

        name = asksaveasfile(mode='w', initialfile = 'sand', defaultextension=".csv")
        if name is None:
            return
        with name as f:
            w = csv.writer(f)
            dt = time.strftime("%a %d-%m-%Y %H:%M:%S", time.localtime())
            writeHeadings(self, w)
            writeDetails(self, w)
            f.close()
        f.close()

    def appendSpreadsheet(self):
        result = askquestion("Append", "Append these results to spreadsheet?\n\nFilename : \n{}".format(pathname), icon='warning')
        if result == 'yes':
            self.setup()
            with open(pathname, 'a') as f:
                w = csv.writer(f)
                writeDetails(self, w)
                f.close()