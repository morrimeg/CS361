## Name: Megan Morrison
## Date: Febuary 4, 2021
## Class: CS 361
## Project: Content Generator Microservice
## Description:

import tkinter as tk
from tkinter import ttk
import wikipedia as w
from bs4 import BeautifulSoup
import requests
import re


# Learned about Wikipedia API here: https://towardsdatascience.com/wikipedia-api-for-python-241cfae09f1c

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        # self.pack()
        # self.create_widgets()
        self.primary_keyword_text_box()
        self.secondary_keyword_text_box()
        self.generate_paragraph_button()
        self.empty_results_box()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        # self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def primary_keyword_text_box(self):
        # Add text before textbox to tell users what to do
        primary_text = tk.Text(self, height=2, width=30)
        # activate
        # primary_text.pack()
        primary_text.grid(column=1, row=3)
        # Place text in textbox
        primary_text.insert(tk.END, "Place your primary search term here ("
                                    "e.g. dog)\n")

        # Creates the text entry box for entering the primary keyword
        self.primary_keyword = tk.Entry(self, width=20)
        # Should add text to the entry box -- but doesn't
        self.primary_keyword["text"] = "Primary Keyword"
        # Activates the text entry box
        # self.primary_keyword.pack(side="bottom")
        self.primary_keyword.grid(column=1, row=4)

    def secondary_keyword_text_box(self):
        """

        :return:
        """

        # Add text before textbox to tell users what to do
        secondary_text = tk.Text(self, height=2, width=30)
        # activate
        # secondary_text.pack()
        secondary_text.grid(column=1, row=6)
        # Place text in textbox
        secondary_text.insert(tk.END,
                              "Place your secondary search term here e.g. bites\n")

        # Creates the text entry box for entering the primary keyword
        self.secondary_keyword = tk.Entry(self, width=20)
        # Should add text to the entry box -- but doesn't
        self.secondary_keyword["text"] = "Secondary Keyword"
        # Activates the text entry box
        # self.secondary_keyword.pack(side="bottom")
        self.secondary_keyword.grid(column=1, row=7)

    def get_keywords(self):
        """"""

    # This grid stuff needs to be fixed
    def empty_results_box(self):
        """

        :return:
        """
        # Add blank textbox to be filled out
        secondary_text = tk.Text(self, height=50, width=50)
        secondary_text.grid(column=10, row=9)

    def generate_paragraph_button(self):
        """

        :return:
        """

        self.gen_para = tk.Button(self, text="Generate Paragraph!", fg="black",
                                  command=self.get_keywords())
        # self.gen_para.pack(side="bottom")
        self.gen_para.grid(column=1, row=8)


# root = tk.Tk()
# root.title("Content Generator")
# root.geometry('800x400')
# root = ttk.Frame(root, padding="3 3 12 12")
# root.grid(column=0, row=0)
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# app = Application(master=root)
# app.mainloop()

# Testing out wiki api
def main():
    # dog = w.search("dog")
    # print(dog)
    # print()
    # dog2 = w.page(dog[0], auto_suggest=False, redirect=True)
    # print()
    # print(dog2.summary)
    # word = 'Neutering'
    #
    # #print(dog2.content.find(word))
    # print()
    #
    # word_index = dog2.content.find(word)
    # para = dog2.content.split()
    # print(para)
    # print(len(para)) # true len
    # print(para[7633]) # true last word

    primary_keyword = "Dog"
    secondary_keyword = "familiaris"

    def findWholeWord(w):

        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
    
    res = requests.get("https://en.wikipedia.org/wiki/"+ primary_keyword)
    print(res)
    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    for item in soup.find_all("p"):
        #https://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string
        if findWholeWord(secondary_keyword)(item.text) is True:
            print(item.text)
        
        print(item.text)








main()
