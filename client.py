#!/usr/bin/env python3 -tt
import tkinter as tk
import datetime
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askquestion
from resources import questions
import csv
import time
import os


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
        self.date = tk.StringVar(value=datetime.datetime.today().strftime('%d/%m/%Y'))
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
            self.date.set(value=datetime.datetime.today().strftime('%d/%m/%Y'))
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
            if self.answers[item-1].get() < 0:
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

        txtScroll.insert(tk.INSERT, 'Client name  :'+self.name.get()+'\n')
        txtScroll.insert(tk.INSERT, 'Birth date   :'+self.dob.get()+'\n')
        txtScroll.insert(tk.INSERT, 'Survey date  :'+self.date.get()+'\n')
        txtScroll.insert(tk.INSERT, 'Incomplete   :'+', '.join(a for a in self.incomplete)+'\n')
        txtScroll.insert(tk.INSERT, 'PRO-SOCIAL   :'+str(self.fnlScore['prosocial'])+'\n')
        txtScroll.insert(tk.INSERT, 'Hyperactivity:'+str(self.fnlScore['hyperactivity'])+'\n')
        txtScroll.insert(tk.INSERT, 'Emotional    :'+str(self.fnlScore['emotional'])+'\n')
        txtScroll.insert(tk.INSERT, 'Conduct      :'+str(self.fnlScore['conduct'])+'\n')
        txtScroll.insert(tk.INSERT, 'Peer         :'+str(self.fnlScore['peer'])+'\n')
        txtScroll.insert(tk.INSERT, 'Total score  :'+str(self.stressScore))

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
            f.write('Client name :' + self.name.get() + '\n')
            f.write('Birth date  :' + self.dob.get() + '\n')
            f.write('Survey date :' + time.strftime("%a %d-%m-%Y %H:%M:%S", time.gmtime()) + '\n')
            f.write('Incomplete  :' + str(list(self.incomplete)) + '\n')
            f.write('Stress score:' + str(self.stressScore) + '\n')
            f.write('Emotional distress :' + str(self.fnlScore.get('emotional')) + '\n')
            f.write('Behavioural difficulties :' + str(self.fnlScore.get('conduct')) + '\n')
            f.write('Hyperactivity and concentration difficulties :' + str(self.fnlScore.get('hyperactivity')) + '\n')
            f.write('Difficulties socialising with children :' + str(self.fnlScore.get('peer')) + '\n')
            f.write('Kind and helpful behaviour :' + str(self.fnlScore.get('prosocial')) + '\n')

    def toCSV(self):
        self.setup()

        name = asksaveasfile(mode='w', initialfile = self.name.get(), defaultextension=".csv")
        if name is None:
            return
        with name as f:
            w = csv.writer(f)
            dt = time.strftime("%a %d-%m-%Y %H:%M:%S", time.localtime())
            w.writerow(['Client name  :']+[self.name.get()])
            w.writerow(['Birth date   :']+[self.dob.get()])
            w.writerow(['Survey date  :']+[dt])
            w.writerow(['Incomplete   :']+[a for a in list(self.incomplete)])
            w.writerow(['PRO-SOCIAL   :']+[str(self.fnlScore['prosocial'])])
            w.writerow(['Hyperactivity:']+[str(self.fnlScore['hyperactivity'])])
            w.writerow(['Emotional    :']+[str(self.fnlScore['emotional'])])
            w.writerow(['Conduct      :']+[str(self.fnlScore['conduct'])])
            w.writerow(['Peer         :']+[str(self.fnlScore['peer'])])
            w.writerow(['Total score  :']+[self.stressScore])
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
            w.writerow(['No.']+['ID']+['Evaluator']+['Date']+['DoB']+['Pro-Social']+['Hyperactivity']+['Emotional']
                    +['Conduct']+['Peer']+['Total']+['Incomplete'])
            w.writerow(['']+[self.name.get()]+[self.eval.get()]+[self.date.get()]+[self.dob.get()]
                    +[str(self.fnlScore['prosocial'])]
                    +[str(self.fnlScore['hyperactivity'])]
                    +[str(self.fnlScore['emotional'])]
                    +[str(self.fnlScore['conduct'])]
                    +[str(self.fnlScore['peer'])]
                    +[str(self.stressScore)]
                    +[a for a in list(self.incomplete)])
            f.close()
        f.close()

    def appendSpreadsheet(self):
        self.setup()

        with open(os.path.expanduser('~/Desktop')+'/sand.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow(['']+[self.name.get()]+[self.eval.get()]+[self.date.get()]+[self.dob.get()]
                    +[str(self.fnlScore['prosocial'])]
                    +[str(self.fnlScore['hyperactivity'])]
                    +[str(self.fnlScore['emotional'])]
                    +[str(self.fnlScore['conduct'])]
                    +[str(self.fnlScore['peer'])]
                    +[str(self.stressScore)]
                    +[a for a in list(self.incomplete)])
            f.close()
