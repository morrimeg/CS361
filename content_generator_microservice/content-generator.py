## Name: Megan Morrison
## Date: Febuary 4, 2021
## Class: CS 361
## Project: Content Generator Microservice
## Description:

import csv
import re
import requests
import sys
import tkinter as tk

from bs4 import BeautifulSoup


# Learned about Wikipedia API here: https://towardsdatascience.com/wikipedia-api-for-python-241cfae09f1c
# References:
# https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b


# I used the following site to get my code for the GUI:
# https://www.python-course.eu/tkinter_entry_widgets.php
class ContentGeneratorApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_labels()
        self.primary = self.create_primary_keyword_entry_box()
        self.secondary = self.create_secondary_keyword_entry_box()
        self.output_text = self.create_text_output_box()
        self.generate_paragraph_button()

    def create_labels(self):
        """

        :return:
        """
        tk.Label(self.master, text="Primary Word").grid(row=1)
        tk.Label(self.master, text="Secondary Word").grid(row=2)

    def create_primary_keyword_entry_box(self):
        """

        :return:
        """
        primary_entry = tk.Entry(self.master)
        primary_entry.grid(row=1, column=1)
        return primary_entry

    def create_secondary_keyword_entry_box(self):
        """

        :return:
        """
        secondary_entry = tk.Entry(self.master)
        secondary_entry.grid(row=2, column=1)
        return secondary_entry

    def create_text_output_box(self):
        """
        The function create_text_output_box creates the box the paragraph
        output will go into.
        :return:
        """
        output_box = tk.Text(self.master, height=50, width=50, wrap=tk.WORD)
        output_box.grid(row=1, column=4)
        return output_box

    def generate_paragraph_button(self):
        """

        :return:
        """
        tk.Button(self.master, text='Generate Paragraph',
                  command=self.run_content_generator_backend).grid(row=3,
                                                                   column=1,
                                                                   sticky=tk.W,
                                                                   pady=4)

    def run_content_generator_backend(self):
        """
        The run_content_generator_backend function runs the backend
        parts for the content generator. This includes grabbing the user's
        input and placing it into the FindText class which returns a
        paragraph if found.
        :return:
        """

        # This SO page helped me figure out how to get text out of the entry
        # boxes when using classes:
        # https://stackoverflow.com/questions/10727131/why-is-tkinter-entrys-get-function-returning-nothing

        # 1st delete any content left over in output box
        self.output_text.delete('1.0', tk.END)

        print("Primary Word: %s\nSecondary Word: %s" % (self.primary.get(),
                                                        self.secondary.get()))

        primary_keyword = self.primary.get()
        secondary_keyword = self.secondary.get()

        # Instantiate a findText object
        f = FindText()

        # Run all of the code in FindText in order to find a paragraph if one
        # exists
        paragraph_found = f.run_paragraph_finder(primary_keyword, secondary_keyword)

        # Insert into text box
        self.output_text.insert('1.0', paragraph_found)

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
        self.primary.delete(0, tk.END)
        self.secondary.delete(0, tk.END)


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

            # If both the primary and secondary keyword are in the list mark
            # the paragraph as found (aka keep it)
            if secondary_keyword.lower() in words_list and \
                    primary_keyword.lower() in words_list:
                # see if one of the words in the sentence is the word we want
                found_paragraph = list_of_lines[i]
                break

        return found_paragraph

    def run_paragraph_finder(self, primary_keyword, secondary_keyword):
        """

        :param primary_keyword:
        :param secondary_keyword:
        :return:
        """
        # Send http request to Wikipedia
        wiki_page = self.send_http_request(primary_keyword)

        # Parse Wiki text
        text_grab = self.parse_wikipedia_page_text(wiki_page)

        # Clean text
        clean_text = self.clean_text(text_grab)

        # Find the paragraph with both primary and secondary keywords!
        paragraph_found = self.find_paragraph(clean_text, primary_keyword,
                                           secondary_keyword)

        return paragraph_found

class CsvManipulation:
    def __init__(self):
        """

        """

    def import_csv(self, filename):
        """

        :param filename:
        :return:
        """
        # First we will read in the csv
        # Found this SO helpful: https://stackoverflow.com/questions/24662571/python-import-csv-to-list
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        return data

    def export_csv(self, filename, first_word, second_word, paragraph):
        """

        :param filename:
        :param first_word:
        :param second_word:
        :param paragraph:
        :return:
        """
        # Write output to a csv
        # https://realpython.com/python-csv/
        with open(filename, mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',',
                                       quotechar='"',
                                       quoting=csv.QUOTE_MINIMAL)
            # Write header row
            output_writer.writerow(['input_keywords', 'output_content'])

            # Write content row
            output_writer.writerow(
                [first_word + ';' + second_word, paragraph])




if __name__ == "__main__":
    # If there is only one argument in the command prompt (e.g. no input.csv
    # file, then run the GUI.

    if len(sys.argv) < 1:
        print("Insufficient Arguments Provided. Quitting.")
        exit()

    if len(sys.argv) == 1:

        # Start up the desktop app.
        # Again, I got this code from the following site:
        # https://www.python-course.eu/tkinter_entry_widgets.php
        root = tk.Tk()
        root.title("Content Generator")
        root.geometry('1000x500')
        tk.Label(root, text="Welcome to the Content Generator! Please "
                            "place your search terms in the boxes "
                            "below.").grid(row=0, column=3)

        # Call the ContentGeneratorApp class to actually run the app
        app = ContentGeneratorApp(master=root)
        app.mainloop()

    # Else, read in the input file and make the appropriate calls to Wikipedia.
    elif sys.argv[1] == "input.csv":

        # Instantiate an object for the CsvManipulation class
        c = CsvManipulation()

        # Import the file given
        file_data = c.import_csv(sys.argv[1])

        # Now that we have our words, we need to parse them
        primary_keyword = file_data[1][0]
        secondary_keyword = file_data[2][0]

        # clean up primary_keyword since there is a semicolon
        primary_keyword = re.sub(r';', '', primary_keyword)

        # Instantiate a findText object
        f = FindText()

        # Find the paragraph with both primary and secondary keywords!
        paragraph_found = f.run_paragraph_finder(primary_keyword,
                                                 secondary_keyword)

        # Export to csv. This will export the csv to your current directory
        c.export_csv('output.csv', primary_keyword, secondary_keyword, paragraph_found)

    else:
        print("Incorrect Argument(s) Provided. Quitting.")
        exit()
