import tkinter as tk
from tkinter import ttk 
        
from client import info
from tkinter.messagebox import askquestion


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self)
        information = info()
        self.parent = parent

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        # create the file object)
        file = tk.Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is self.exit
        file.add_command(label="Exit", command=root.quit())
        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        # create the file object)
        edit = tk.Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is self.exit
        edit.add_command(label="Undo")
        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)



        #self.toolbar = Toolbar(self, information)
        self.header = Header(self, information)
        self.questionnaire = Questionnaire(self, information)
        self.footer = Footer(self, information)

        #self.toolbar.pack(side="top", fill="x")
        self.header.pack(side='top', fill='x', expand=True)
        self.questionnaire.pack(side='top', fill='x', expand=True)
        self.footer.pack(side='bottom', fill='x', expand=True)


'''
class Toolbar(tk.Frame):
    def __init__(self, parent, information):
        menubar = tk.Menu(root)
        information = info()
        filemenu = tk.Menu(menubar, tearoff=0 ) # File menu
        root.config(menu=menubar) # this line actually displays menu

        fileMenu= tk.Menu(menuBar, tearoff=0)  
        fileMenu.add_command(label="New")  
        fileMenu.add_separator()  
        fileMenu.add_command(label="Exit", command=_quit)  
        menuBar.add_cascade(label="File", menu=fileMenu)  
'''



class Header(tk.Frame):
    def __init__(self, parent, information):
        super(Header, self).__init__()
        self.parent = parent
        self.info = information

        clientDetails = tk.Frame(self)

        nameLabel = tk.Label(clientDetails, text='Name / Ref : ')
        nameEntry = tk.Entry(clientDetails, textvariable=self.info.name)
        dobLabel = tk.Label(clientDetails, text='Date(dd/mm/yyyy)')
        dobEntry = tk.Entry(clientDetails, textvariable=self.info.dob)
        dobButton = tk.Button(clientDetails, text='Format',
                              command=self.formatDateWidget)

        nameLabel.grid(row=0, column=0)
        nameEntry.grid(row=0, column=1)
        dobLabel.grid(row=0, column=2)
        dobEntry.grid(row=0, column=3)
        dobButton.grid(row=0, column=4)

        clientDetails.pack(fill='both', expand=True, side=tk.TOP)

        header = tk.Frame(self)
        headings = ['       Questions'+' '*90, 'Unknown', 'No   ', 'Maybe', '   Yes']
        for col, heading in enumerate(headings):
            labelheading = tk.Label(header, text=heading, justify=tk.RIGHT)
            labelheading.grid(row=1, column=col, sticky=tk.E)
        header.pack(fill='both', expand=True, side=tk.TOP)

    def formatDateWidget(self):
        entrylist = [c for c in self.info.dob.get() if c != '/']
        for pos in [2, 5]:
            if len(entrylist) > pos:
                entrylist.insert(pos, '/')
        self.info.dob.set(''.join(entrylist))


class Questionnaire(tk.Frame):
    def __init__(self, master, information):
        super(Questionnaire, self).__init__()
        self.info = information
        self.master = master
        self.questions = tk.Frame(self)
        self.radioFrame = tk.Frame(self.questions)
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
            label = tk.Label(self.radioFrame, text=line)
            if number % 5 == 0:
                label.configure(background='#d0d0d0')
            label.grid(row=number, column=0, sticky=tk.W)
            options = ['?', 'N', 'M', 'Y']
            for answer in range(-1, 3):
                button = tk.Radiobutton(self.radioFrame, borderwidth=10,
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

class Footer(tk.Frame):
    def __init__(self, parent, information):
        super(Footer, self).__init__()
        self.parent = parent
        self.info = information
        footer = tk.Frame(self)

        rstButton = ttk.Button(footer, text="Reset All", command=self.rstConfirm)
        winButton = tk.Button(footer, text="View", command=self.info.toWin)
        csvButton = tk.Button(footer, text="Save .csv", command=self.info.toCSV)
        txtButton = tk.Button(footer, text="Save .txt", command=self.info.toTxt)
        extButton = tk.Button(footer, text="Quit", command=self.exit)

        rstButton.grid(row=0, column=0, sticky='w')
        winButton.grid(row=0, column=2)
        csvButton.grid(row=0, column=3)
        txtButton.grid(row=0, column=4)
        extButton.grid(row=0, column=5)

        footer.grid_columnconfigure(1, weight=1)
        footer.pack(fill='both', expand=True, side=tk.TOP, pady=5)

    def rstConfirm(self):
        result = askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.info.resetFields()

    def exit(self):
        print('Exiting application')
        root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title('Strengths & Difficulties - SAND')
    MainApplication(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
