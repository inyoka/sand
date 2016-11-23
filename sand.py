#!/usr/bin/env python3 -tt

import tkinter as tk
import collections
import pprint



def printDict(dictionary):
    for key, item in dictionary.items():
        print(key)
        for attribute, value in dictionary.items():
            print('{} : {}'.format(attribute, value))
    '''
    for x in dictionary:
        print (x)
        for y in dictionary[x]:
            print (y,':',dictionary[x][y])
    '''

class Form(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        file = open('questions.txt')
        questionlist = file.readlines()
        file.seek(0)
        width = len(max(file, key=len))

        title = tk.Label(self, text="Strengths & Difficulties")
        title.pack()
        header = tk.Frame(self)
        header.pack(fill='both', expand=True, side=tk.TOP)
        headings = [' '*width*2,'?', 'N', 'M', 'Y']
        for col, heading in enumerate(headings):
            labelheading = tk.Label(header, text=heading, justify=tk.RIGHT)
            labelheading.grid(row=1, column=col, sticky=tk.E)
        self.questions = Questions(self, questionlist)
        self.questions.pack()
        done_button = tk.Button(self, text="Done", command=self.done)
        done_button.pack()

    def convertToInts(self):
        self.questions.answers = [ int(x.get()) for x in self.questions.answers ]

    def reverseAnswers(self):
        results = []
        reverse = [7, 11, 14, 21, 25]
        for no, answer in enumerate(self.questions.answers):
            if no in reverse:
                if answer == 0:
                    answer = 2
                elif answer == 2:
                    answer = 0
            results.append(answer)
        self.questions.answers = [x  for x in results]

    def done(self):
        # For Dicts .keys prints keys, Dict[key] prints content, .items prints both 
        self.convertToInts()
        self.reverseAnswers()
        traits = {}
        traits['emotional'] = [3, 8, 13, 16, 24]
        traits['conduct'] = [5,7, 12, 18, 22]
        traits['hyperactivity'] = [2, 10, 15, 21, 25]
        traits['peer'] = [6, 11, 14, 19, 23]
        traits['prosocial'] = [1, 4, 9, 17, 20]
        # Create dict by numbering the myresults    
        answerDict = dict(zip(range(1,26), self.questions.answers))
        resultsDict = dict()
        for trait in traits.keys():
            print(trait)
            for number in traits[trait]:
                if answerDict[number] >= 0:
                    
                    print('Printed %s by traits:' % trait, answerDict[number])
                    if trait in resultsDict:
                        resultsDict[trait] = answerDict[number]
                    else:
                        resultsDict[trait] = answerDict[number]
        print({k:sum(v) for k,v in resultsDict.items()})
        for k,v in resultsDict.items():
            print(k:sum(v)) 
        root.quit()

class Questions(tk.Frame):
    def __init__(self, master, questionlist):
        tk.Frame.__init__(self, master)
        self.questionlist = questionlist
        self.askQuestions()

    def askQuestions(self):
        self.answers = []
        for number, question in enumerate(self.questionlist, 1):
            var = tk.IntVar(value = 2)
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
            self.answers.append(var)

if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side='top', fill='both', expand=True)
    #Form(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
