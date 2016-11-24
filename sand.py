#!/usr/bin/env python3 -tt
import tkinter as tk
from tkinter.filedialog import asksaveasfile
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
        self.header = Header(self, information)
        self.questionnaire = Questionnaire(self, information)
        self.footer = Footer(self, information)
        self.header.pack(side='top', fill='x', expand=True)
        self.questionnaire.pack(side='top', fill='x', expand=True)
        self.footer.pack(side='bottom', fill='x', expand=True) 

class Info():
    def __init__(self):
        file = open('questions.txt')
        self.width = len(max(file, key=len))
        self.traits = {'emotional' : [3, 8, 13, 16, 24], 
                        'conduct' : [5,7, 12, 18, 22], 
                        'hyperactivity' : [2, 10, 15, 21, 25], 
                        'peer' : [6, 11, 14, 19, 23], 
                        'prosocial' : [1, 4, 9, 17, 20]}
        self.answers = []
        self.incomplete = set()
        self.name = tk.StringVar()
        self.finalScore = {}


class Header(tk.Frame):
    def __init__(self, parent, information):
        super(Header, self).__init__()
        self.parent = parent
        self.info = information

        title = tk.Label(self, text="Strengths & Difficulties")
        title.pack()

        clientDetails = tk.Frame(self)
        nameLabel = tk.Label(clientDetails, text='Name or Reference (optional) : ').grid(row=0, column=0)
        nameEntry = tk.Entry(clientDetails, textvariable=self.info.name).grid(row=0, column=1)
        clientDetails.pack(fill='both', expand=True, side=tk.TOP)


        header = tk.Frame(self)
        headings = [' '*self.info.width*2,'?', 'N', 'M', 'Y']
        for col, heading in enumerate(headings):
            labelheading = tk.Label(header, text=heading, justify=tk.RIGHT)
            labelheading.grid(row=1, column=col, sticky=tk.E)
        header.pack(fill='both', expand=True, side=tk.TOP)

class Questionnaire(tk.Frame):
    def __init__(self, master, information):
        super(Questionnaire, self).__init__()
        self.info = information
        self.master = master
        self.askQuestions()

    def askQuestions(self):
        file = open('questions.txt')
        questionlist = file.readlines()
        for number, question in enumerate(questionlist, 1):
            var = tk.IntVar(value = -1)
            width = 5
            line = '{:5}'.format(number, fill=' ') + ' : ' + question.strip()
            label = tk.Label(self, text=line)
            if number % 5 == 0:
                label.configure(background='#d0d0d0')
            label.grid(row=number, column = 0, sticky=tk.W)
            options = ['?', 'No', 'Maybe', 'Yes']
            for answer in range(-1,3):
                button = tk.Radiobutton(self, borderwidth=10, variable = var, text=options[answer+1], width = 5, value = answer, indicatoron=0)
                if number % 5 == 0:
                    button.configure(background='#d0d0d0')
                button.grid(row = number, column = answer+2)
            self.info.answers.append(var)

class Footer(tk.Frame):
    def __init__(self, parent, information):
        super(Footer, self).__init__()
        self.info = information
        done_button = tk.Button(self, text="Done", command=self.createReport)
        done_button.pack()

    def convertToInts(self):
        self.info.answers = [ int(x.get()) for x in self.info.answers ]

    def reverseAnswers(self):
        results = []
        reverse = [7, 11, 14, 21, 25]
        for no, answer in enumerate(self.info.answers, 1):
            if no in reverse:
                if answer == 0:
                    answer = 2
                elif answer == 2:
                    answer = 0
            results.append(answer)
        self.info.answers = [x  for x in results]

    def addScore(self, trait):
        self.lineNumbers = self.info.traits[trait]
        score = 0
        for item in self.lineNumbers:
            if self.info.answers[item-1] > -1:
                score = score + self.info.answers[item-1]
            if self.info.answers[item-1] < 0:
                self.info.incomplete.add(trait)
        return(score)

    def sumTraits(self):
        for trait in self.info.traits.keys():
            self.info.finalScore[trait] = self.addScore(trait)
    
    def printResults(self):
        print('Name : ', self.info.name.get())
        dicttools.dump(self.info.finalScore)
        print(self.info.incomplete)
        print(time.strftime("%a %d-%m-%Y %H:%M:%S", time.gmtime()))

    def file_save(self):
        name = asksaveasfile(mode='w', defaultextension=".csv") 
        if name is None:
            return
        with name as f:
            w = csv.writer(f) #switch to file later
            w.writerow(['Client name :']+[self.info.name.get()])
            #w.writerow(self.info.age.get())
            w.writerow(['Survey date :']+[time.strftime("%a %d-%m-%Y %H:%M:%S", time.gmtime())])
            w.writerow(['Incomplete  :']+[self.info.incomplete])
            w.writerows(self.info.finalScore.items())
            f.close()
        # filename.write(text2save)
        #f.close() # `()` was missing.

    def outputCSV(self):
        filename = self.info.name.get() + time.strftime("-%d%m%Y-%H%M")+'.csv'
        print('Filename : ', filename)
        with open(filename,'wb') as f:
            w = csv.writer(sys.stderr) #switch to file later
            w.writerow(['Client name :']+[self.info.name.get()])
            #w.writerow(self.info.age.get())
            w.writerow(['Survey date :']+[time.strftime("%a %d-%m-%Y %H:%M:%S", time.gmtime())])
            w.writerow(['Incomplete  :']+[self.info.incomplete])
            w.writerows(self.info.finalScore.items())

    def createReport(self):
        # For Dicts .keys prints keys, Dict[key] prints content, .items prints both 
        self.convertToInts()
        self.reverseAnswers()
        self.sumTraits()
        #self.printResults()
        #self.outputCSV()
        self.file_save()
        root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
