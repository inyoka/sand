#!/usr/bin/env python3 -tt
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter.scrolledtext import ScrolledText
import csv
import time


class Info():
    def __init__(self):
        file = open('questions.txt')
        self.width = len(max(file, key=len))
        self.traits = {'emotional': [3, 8, 13, 16, 24],
                       'conduct': [5, 7, 12, 18, 22],
                       'hyperactivity': [2, 10, 15, 21, 25],
                       'peer': [6, 11, 14, 19, 23],
                       'prosocial': [1, 4, 9, 17, 20]}
        self.incomplete = set()
        self.name = tk.StringVar()
        self.dob = tk.StringVar()
        self.buttons = []
        self.answers = []
        self.finalScore = {}
        self.stressScore = int()

    def resetFields(self):
        self.name.set(value='')
        self.dob.set(value='')
        for a in self.answers:
            # a.set(value=-1)
            a == -1  # .set(value = -1)

    '''
    def resetFields(self):
        self.name.set(value='')
        self.dob.set(value='')
        # print({a for a in self.answers})
        for a in self.answers:
            # a.set(value = -1)
            a = -1  # .set(value = -1)
        # print({a for a in self.answers})
    '''

    def convertToInts(self):
        self.answers = [int(x.get()) for x in self.answers]

    def reverseAnswers(self):
        results = []
        reverse = [7, 11, 14, 21, 25]
        for no, answer in enumerate(self.answers, 1):
            # Seems like slices would be better suited to this
            if no in reverse:
                if answer == 0:
                    answer = 2
                elif answer == 2:
                    answer = 0
            results.append(answer)
        self.answers = [x for x in results]

    def addScore(self, trait):
        self.lineNumbers = self.traits[trait]
        score = 0
        for item in self.lineNumbers:
            if self.answers[item-1] > -1:
                score = score + self.answers[item-1]
            if self.answers[item-1] < 0:
                self.incomplete.add(trait)
        return(score)

    def sumTraits(self):
        for trait in self.traits.keys():
            self.finalScore[trait] = self.addScore(trait)

    def calcStressScore(self):
        self.stressScore = (
            sum(self.finalScore.values()) - self.finalScore.get('prosocial'))

    def createReport(self):
        # Allows the user to save the results to a .csv file.
        self.convertToInts()
        self.reverseAnswers()
        self.sumTraits()
        self.calcStressScore()
        self.fileSaveCSV()
        self.resetFields()

    def displayReport(self):
        # Will eventual display the report results in a window.
        self.convertToInts()
        self.reverseAnswers()
        self.sumTraits()
        self.printResults()

    def outputResults(self):
        top = tk.Tk()
        top.title("Sample output ...")

        txtScroll = ScrolledText(top, wrap=tk.WORD, width=20, height=10)
        txtScroll.pack(side='top', fill='x', expand=True)
        txtScroll.insert(tk.INSERT, self.name.get())
        txtScroll.insert(tk.INSERT, self.dob.get())
        txtScroll.insert(tk.INSERT, (a.get() for a in self.incomplete))

        button = tk.Button(top, text="Dismiss", command=top.destroy)
        button.pack()

    def fileSaveCSV(self):
        name = asksaveasfile(mode='w', defaultextension=".csv")
        if name is None:
            return
        with name as f:
            w = csv.writer(f)
            dt = time.strftime("%a %d-%m-%Y %H:%M:%S", time.localtime())
            w.writerow(['Client name  :']+[self.name.get()])
            w.writerow(['Birth date   :']+[self.dob.get()])
            w.writerow(['Survey date  :']+[dt])
            w.writerow(['Incomplete   :']+[a for a in list(self.incomplete)])
            w.writerow(['PRO-SOCIAL   :']+[str(self.finalScore['prosocial'])])
            w.writerow(['Hyperactivity:']+[str(self.finalScore['hyperactivity'])])
            w.writerow(['Emotional    :']+[str(self.finalScore['emotional'])])
            w.writerow(['Conduct      :']+[str(self.finalScore['conduct'])])
            w.writerow(['Peer         :']+[str(self.finalScore['peer'])])
            w.writerow(['Total score  :']+[self.stressScore])
            f.close()
