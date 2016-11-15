#!/usr/bin/env python3.5 -tt
import tkinter as tk 

file = open('questions.txt')
questions = file.readlines()

class Form(tk.Frame):
    def __init__(self, parent, questions):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        title = tk.Label(self, text="Strengths & Difficulties")
        title.pack()

        self.questions = Questions(self, questions)
        self.questions.pack()

        done_button = tk.Button(self, text="Done.", command=self.done)
        done_button.pack()

    def done(self):
        for answer in self.questions.answers:
            print(answer.get(), end=" ")
            #if answer.get()  is -1 
        print('')    
        root.quit()

class Questions(tk.Frame):
    def __init__(self, master, questions):
        tk.Frame.__init__(self, master)
        self.askQuestions()

    def askQuestions(self):
        self.answers = []
        for count, question in enumerate(questions):
            var = tk.IntVar(value = -1)
            number = count+1
            width = 5
            line = '{:5}'.format(count+1, fill=' ') + ' : ' + question.strip()
            label = tk.Label(self, text=line)
            label.grid(row=count, column = 0, sticky=tk.W)
            for answer in range(0,4):
                button = tk.Radiobutton(self, variable = var, value = answer)
                button.grid(row = count, column = answer+1)
            self.answers.append((var))

if __name__ == '__main__':
    root = tk.Tk()
    window = Form(root, questions)
    window.pack()
    root.mainloop()
