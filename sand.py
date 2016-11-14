import tkinter as tk 
from tkinter import ttk

file = open('questions.txt')
questionlist = file.readlines()


class GUI(ttk.Frame):
    def __init__(self, master, questionlist):
        ttk.Frame.__init__(self, master)

        title = ttk.Label(self, text="SURVEY")
        title.pack()

        self.questions = Questions(self, questionlist)
        self.questions.pack()

        done_button = ttk.Button(self, text="Done.", command=self.done)
        done_button.pack()

    def done(self):
        for q, a in self.questions.q_and_a:
            print("{}: {}".format(q,a.get()))
        quit()

class Questions(ttk.Frame):
    '''I put all the questions into a single class so they would line up better'''
    def __init__(self, master, questionlist):
        ttk.Frame.__init__(self, master)
        '''
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        #self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
        #self.frame.bind("<Configure>", self.onFrameConfigure)
        '''
        self.populate()


    def populate(self):
        self.q_and_a = []
        for row, question in enumerate(questionlist):
            var = tk.IntVar(value = -1) #-1 is sorta standard for "not answered", so it's a good default value
            q_label = ttk.Label(self, text=question)
            q_label.grid(row=row, column = 0)
            for i in range(0,3):
                button = tk.Radiobutton(self, variable = var, value = i+1)
                button.grid(row = row, column = i+1)
            self.q_and_a.append((question, var))


root = tk.Tk()
window = GUI(root, questionlist)
window.pack()
root.mainloop()
