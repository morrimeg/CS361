## Name: Megan Morrison
## Date: Febuary 4, 2021
## Class: CS 361
## Project: Content Generator Microservice
## Description:

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        #self.create_widgets()
        self.primary_keyword_text_box()
        self.secondary_keyword_text_box()
        self.generate_paragraph_button()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def primary_keyword_text_box(self):

        # Add text before textbox to tell users what to do
        primary_text = tk.Text(self, height=2, width=30)
        # activate
        primary_text.pack()
        # Place text in textbox
        primary_text.insert(tk.END, "Place your primary search term here ("
                                    "e.g. dog)\n")

        # Creates the text entry box for entering the primary keyword
        self.primary_keyword = tk.Entry(self, width=20)
        # Should add text to the entry box -- but doesn't
        self.primary_keyword["text"] = "Primary Keyword"
        # Activates the text entry box
        self.primary_keyword.pack(side="bottom")

    def secondary_keyword_text_box(self):
        """

        :return:
        """

        # Add text before textbox to tell users what to do
        secondary_text = tk.Text(self, height=2, width=30)
        # activate
        secondary_text.pack()
        # Place text in textbox
        secondary_text.insert(tk.END, "Place your secondary search term here ("
                                    "e.g. bites)\n")

        # Creates the text entry box for entering the primary keyword
        self.secondary_keyword = tk.Entry(self, width=20)
        # Should add text to the entry box -- but doesn't
        self.secondary_keyword["text"] = "Secondary Keyword"
        # Activates the text entry box
        self.secondary_keyword.pack(side="bottom")

    def get_keywords(self):
        """"""


    def generate_paragraph_button(self):
        """

        :return:
        """

        self.gen_para = tk.Button(self, text="Generate Paragraph!", fg="red",
                              command=self.get_keywords())
        self.gen_para.pack(side="bottom")


root = tk.Tk()
root.title("Content Generator")
root.geometry('800x400')
app = Application(master=root)
app.mainloop()

