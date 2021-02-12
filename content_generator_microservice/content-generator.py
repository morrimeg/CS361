## Name: Megan Morrison
## Date: Febuary 4, 2021
## Class: CS 361
## Project: Content Generator Microservice
## Description:

import tkinter as tk
from tkinter import ttk
import csv, sys, re, requests
from bs4 import BeautifulSoup


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
        self.get_keywords()
        self.primary_keyword = ""
        self.secondary_keyword = ""

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

    def set_primary_keyword(self, primary_keyword):
        """
        :param primary_keyword:
        :return:
        """
        self.primary_keyword = primary_keyword

    def set_secondary_keyword(self, secondary_keyword):
        """

        :param secondary_keyword:
        :return:
        """
        self.secondary_keyword = secondary_keyword


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
        primary_keyword = tk.Entry(self, width=20)
        # Should add text to the entry box -- but doesn't
        primary_keyword["text"] = "Primary Keyword"
        # Activates the text entry box
        # self.primary_keyword.pack(side="bottom")
        primary_keyword.grid(column=1, row=4)

        self.set_primary_keyword(primary_keyword.get())

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
        secondary_keyword = tk.Entry(self, width=20)
        # Should add text to the entry box -- but doesn't
        secondary_keyword["text"] = "Secondary Keyword"
        # Activates the text entry box
        # self.secondary_keyword.pack(side="bottom")
        secondary_keyword.grid(column=1, row=7)

        self.set_secondary_keyword(secondary_keyword.get())


    def get_keywords(self):
        """
        param: primary_keyword:
        param: secondary_keyword:
        :return:
        """
        print("Primary: %s\nSecondary: %s" % (self.primary_keyword,
                                              self.secondary_keyword))


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


class FindText:
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

        return found_paragraph


if __name__ == "__main__":
    # If there is only one argument in the command prompt (e.g. no input.csv
    # file, then run the GUI.

    if len(sys.argv) < 1:
        print("Insufficient Arguments Provided. Quitting.")
        exit()

    if len(sys.argv) == 1:

        def show_entry_fields():
            # 1st delete any content left over in output box
            e3.delete('1.0', tk.END)

            print("Primary Word: %s\nSecondary Word: %s" % (e1.get(),
                                                            e2.get()))

            primary_keyword = e1.get()
            secondary_keyword = e2.get()

            # Instantiate a findText object
            f = FindText()

            # Send http request to Wikipedia
            wiki_page = f.send_http_request(primary_keyword)

            # Parse Wiki text
            text_grab = f.parse_wikipedia_page_text(wiki_page)

            # Clean text
            clean_text = f.clean_text(text_grab)

            # Find the paragraph with both primary and secondary keywords!
            paragraph_found = f.find_paragraph(clean_text, primary_keyword,
                                               secondary_keyword)

            # Insert into text box
            e3.insert('1.0', paragraph_found)

            # Write output to a csv
            # https://realpython.com/python-csv/
            with open('output2.csv', mode='w') as output_file:
                output_writer = csv.writer(output_file, delimiter=',',
                                           quotechar='"',
                                           quoting=csv.QUOTE_MINIMAL)

                output_writer.writerow(['input_keywords', 'output_content'])
                output_writer.writerow(
                    [primary_keyword + ';' + secondary_keyword,
                     paragraph_found])

            # Clear input
            e1.delete(0, tk.END)
            e2.delete(0, tk.END)

        master = tk.Tk()
        master.title("Content Generator")
        master.geometry('600x800')
        tk.Label(master, text="Welcome to the Content Generator! Please "
                              "place your search terms in the boxes "
                              "below.").grid(row=0, column=3)
        tk.Label(master, text="Primary Word").grid(row=1)
        tk.Label(master, text="Secondary Word").grid(row=2)

        e1 = tk.Entry(master)
        e2 = tk.Entry(master)
        e3 = tk.Text(master, height=50, width=50, wrap=tk.WORD)

        e1.grid(row=1, column=1)
        e2.grid(row=2, column=1)
        e3.grid(row=1, column=5)

        tk.Button(master,
                  text='Generate Paragraph', command=show_entry_fields).grid(
            row=3, column=1, sticky=tk.W, pady=4)


        master.mainloop()

        # root = tk.Tk()
        # root.title("Content Generator")
        # root.geometry('800x400')
        # root = ttk.Frame(root, padding="3 3 12 12")
        # root.grid(column=0, row=0)
        # root.columnconfigure(0, weight=1)
        # root.rowconfigure(0, weight=1)
        # app = Application(master=root)
        # app.mainloop()

    # Else, read in the input file and make the appropriate calls to Wikipedia.
    elif sys.argv[1] == "input.csv":
        # First we will read in the csv
        # Found this SO helpful: https://stackoverflow.com/questions/24662571/python-import-csv-to-list
        with open(sys.argv[1], newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        # Now that we have our words, we need to parse them
        primary_keyword = data[1][0]
        secondary_keyword = data[2][0]

        # clean up primary_keyword since there is a semicolon
        primary_keyword = re.sub(r';', '', primary_keyword)

        # Instantiate a findText object
        f = FindText()

        # Send http request to Wikipedia
        wiki_page = f.send_http_request(primary_keyword)

        # Parse Wiki text
        text_grab = f.parse_wikipedia_page_text(wiki_page)

        # Clean text
        clean_text = f.clean_text(text_grab)

        # Find the paragraph with both primary and secondary keywords!
        paragraph_found = f.find_paragraph(clean_text, primary_keyword,
                                           secondary_keyword)

        # Write output to a csv
        # https://realpython.com/python-csv/
        with open('output.csv', mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',',
                                         quotechar='"',
                                         quoting=csv.QUOTE_MINIMAL)

            output_writer.writerow(['input_keywords', 'output_content'])
            output_writer.writerow([primary_keyword + ';' + secondary_keyword, paragraph_found])

    else:
        print("Incorrect Argument(s) Provided. Quitting.")
        exit()
