## Name: Megan Morrison
## Date: Febuary 4, 2021
## Class: CS 361
## Project: Content Generator Microservice
## Description:

import tkinter as tk
from tkinter import ttk
import csv
from bs4 import BeautifulSoup
import requests
import re


# Learned about Wikipedia API here: https://towardsdatascience.com/wikipedia-api-for-python-241cfae09f1c
# References:
# https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b

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


class FindText():
    def __init__(self):
        """

        """
        self.primary_keyword = ""
        self.secondary_keyword = ""

    def send_http_request(self, primary_keyword):
        """

        :return:
        """
        # Send request to Wikipedia page using the primary keyword
        res = requests.get("https://en.wikipedia.org/wiki/" + primary_keyword)

        # Parse request page
        soup = BeautifulSoup(res.text, 'html.parser')

        return soup

    def parse_wikipedia_page_text(self, soup):
        """

        :param soup:
        :return:
        """

        # bypasses synomyms that are included as a paragraph tag on Wiki
        # this page helped me figure the above out:
        # https://stackoverflow.com/questions/43133632/web-scraping-a-wikipedia-page

        text = ''
        for paragraph in soup.find_all('p')[3:]:
            text += paragraph.text

        return text

    def clean_text(self, text):
        """

        :param text:
        :return:
        """
        # Clean up text to get rid of footnote markers
        text = re.sub(r'\[.*?\]+', '', text)
        # lower case everything
        text = text.lower()

        return text

    def find_paragraph(self, text, primary_keyword, secondary_keyword):
        """

        :param text:
        :param primary_keyword
        :param secondary_keyword
        :return:
        """
        # Now we can find the secondary keyword
        # Each paragraph ends with \n. So we need to split each line by \n
        # I found out how to do this from the following SO article:
        # https://stackoverflow.com/questions/14801057/python-splitting-to-the-newline-character
        list_of_lines = text.splitlines()
        found_paragraph = []  # empty list to hold the found paragraph

        # Now we will iterate through each line, and break up each line word
        # for word to see if the secondary keyword is in a paragraph.
        for i in range(len(list_of_lines)):
            # split the sentence into individual words
            # Found this SO helpful:
            # https://stackoverflow.com/questions/3897942/how-do-i-check-if-a-sentence-contains-a-certain-word-in-python-and-then-perform
            words = list_of_lines[i]
            words_list = words.split()

            if secondary_keyword.lower() in words_list and \
                    primary_keyword.lower() in words_list:

                # see if one of the words in the sentence is the word we want
                found_paragraph = list_of_lines[i]
                break
                # do we want this to print just the 1st paragraph found? or all?

        return found_paragraph




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

    primary_keyword = "Dog"
    secondary_keyword = "familiaris"

    f = FindText()
    s = f.send_http_request(primary_keyword)
    t = f.parse_wikipedia_page_text(s)
    t = f.clean_text(t)
    final = f.find_paragraph(t, primary_keyword, secondary_keyword)
    print(final)


main()
