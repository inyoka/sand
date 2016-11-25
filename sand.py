#!/usr/bin/env python3 -tt
import tkinter as tk
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
        self.buttons = []
        self.incomplete = set()
        self.name = tk.StringVar()
        self.dob = tk.StringVar() 
        self.answers = []
        self.finalScore = {}

    def resetConfirm(self):
        result = askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            print ("Deleted")
            self.resetFields()
        else:
            print ("I'm Not Deleted Yet")

    def resetFields(self):
        self.name.set(value = '')
        self.dob.set(value = '')
        #self.answers = []
        #for _count in self.answers:
        #    self.answers.append(tk.IntVar(value = -1))
        for count, button in enumerate(self.buttons):
            self.buttons[count] = tk.IntVar(value = -1)

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
        dobLabel = tk.Label(clientDetails, text='Date(MM/DD/YYYY)').grid(row=1, column=0)
        self.dobEntry = tk.Entry(clientDetails, textvariable=self.info.dob).grid(row=1, column=1)
        dobButton = tk.Button(clientDetails, text='Format DoB', command=self.formatDateWidget).grid(row=1, column=2)
        clientDetails.pack(fill='both', expand=True, side=tk.TOP)

        header = tk.Frame(self)
        headings = [' '*self.info.width*2,'?', 'N', 'M', 'Y']
        for col, heading in enumerate(headings):
            labelheading = tk.Label(header, text=heading, justify=tk.RIGHT)
            labelheading.grid(row=1, column=col, sticky=tk.E)
        header.pack(fill='both', expand=True, side=tk.TOP)

    def formatDateWidget(self):
        entrylist = [c for c in self.info.dob.get() if c !='/']
        for pos in [2, 5]:
            if len(entrylist) > pos:
                entrylist.insert(pos, '/')
        self.info.dob.set(''.join(entrylist))

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
            self.var = tk.IntVar(value = -1)
            width = 5
            line = '{:5}'.format(number, fill=' ') + ' : ' + question.strip()
            label = tk.Label(self, text=line)
            if number % 5 == 0:
                label.configure(background='#d0d0d0')
            label.grid(row=number, column = 0, sticky=tk.W)
            options = ['?', 'No', 'Maybe', 'Yes']
            for answer in range(-1,3):
                button = tk.Radiobutton(self, borderwidth=10, variable = self.var, text=options[answer+1], width = 5, value = answer, indicatoron=0)
                if number % 5 == 0:
                    button.configure(background='#d0d0d0')
                button.grid(row = number, column = answer+2)
                self.info.buttons.append(button)

            self.info.answers.append(self.var)

class Footer(tk.Frame):
    def __init__(self, parent, information):
        super(Footer, self).__init__()
        self.parent = parent
        self.info = information
        footer = tk.Frame(self)
        reset_button = tk.Button(footer, text="Reset All", command=self.info.resetConfirm).grid(row=0, column=0, sticky='w')
        footer.grid_columnconfigure(1, weight=1)
        output_button = tk.Button(footer, text="Output", command=self.outputResults).grid(row=0, column=2)
        done_button = tk.Button(footer, text="Done", command=self.createReport).grid(row=0, column=3)
        exit_button = tk.Button(footer, text="Quit", command=self.exit).grid(row=0, column=4)
        footer.pack(fill='both', expand=True, side=tk.TOP, pady=5)

    def convertToInts(self):
        self.info.answers = [ int(x.get()) for x in self.info.answers ]

    def reverseAnswers(self):
        results = []
        reverse = [7, 11, 14, 21, 25]
        for no, answer in enumerate(self.info.answers, 1):
            # Seems like slices would be better suited to this
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

    def outputResults(self):
        top = tk.Tk()
        #Toplevel()
        top.title("Sample output ...")

        messageScrolled = scrolledtext.ScrolledText(top, wrap=tk.WORD, width=20, height=10)
        messageScrolled.pack(side='top', fill='x', expand=True)

        messageScrolled.insert(tk.INSERT, self.info.name.get())
        messageScrolled.insert(tk.INSERT, self.info.dob.get())
        messageScrolled.insert(tk.INSERT, self.info.incomplete)


        button = tk.Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        '''
        print(self.info.incomplete)
        print(time.strftime("%a %d-%m-%Y %H:%M:%S", time.gmtime()))
        print('Client name :', self.info.name.get())
        print('Birth date  :', self.info.dob.get())
        print('Survey date :', time.strftime("%a %d-%m-%Y %H:%M:%S", time.gmtime()))
        print('Incomplete  :', self.info.incomplete)
        dicttools.dump(self.info.finalScore)
        '''
    def fileSave(self):
        name = asksaveasfile(mode='w', defaultextension=".csv") 
        if name is None:
            return
        with name as f:
            w = csv.writer(f)
            w.writerow(['Client name :']+[self.info.name.get()])
            w.writerow(['Birth date  :']+[self.info.dob.get()])
            w.writerow(['Survey date :']+[time.strftime("%a %d-%m-%Y %H:%M:%S", time.gmtime())])
            w.writerow(['Incomplete  :']+[self.info.incomplete])
            w.writerows(self.info.finalScore.items())
            f.close()

    def displayReport(self):
        # Will eventual display the report results in a window. 
        self.convertToInts()
        self.reverseAnswers()
        self.sumTraits()
        self.printResults()

    def createReport(self):
        # Allows the user to save the results to a .csv file.
        self.convertToInts()
        self.reverseAnswers()
        self.sumTraits()
        self.fileSave()

    def exit(self):
        # Stub awaiting an seperate quit button.
        print('Exiting application')
        root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
