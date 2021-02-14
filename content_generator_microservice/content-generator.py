# Name: Megan Morrison
# Date: Febuary 4, 2021
# Class: CS 361
# Project: Content Generator Microservice
# Description: This file contains the following classes:
# ContentGeneratorApp, FindText, and CsvManipulation. ContentGeneratorApp
# creates a desktop app that allows the user to input a primary and
# secondary search term. The app then searches Wikipedia for the article
# containing the primary search term and returns a paragraph to the user
# that contains both the primary and secondary search terms (if one exists).

import csv
import re
import requests
import sys
import string
import tkinter as tk

from bs4 import BeautifulSoup


# References:
# How to get content from Wikipedia:
# https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b

# Building a Tkinter App:
# https://www.python-course.eu/tkinter_entry_widgets.php
# https://tkdocs.com/tutorial/firstexample.html

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
        The create_labels function creates text labels that are placed next
        to each text entry box
        :return:
        """
        # Create labels for the text entry boxes
        tk.Label(self.master, text="Primary Word (e.g. Dog)").grid(row=2)
        tk.Label(self.master, text="Secondary Word (e.g Breed)").grid(row=3)

    def create_primary_keyword_entry_box(self):
        """
        The create_primary_keyword_entry_box creates the box that the user
        will put their 1st search term in.
        :return: primary_entry:
        """
        # Creates text entry box
        primary_entry = tk.Entry(self.master)

        # Place box on grid layout
        primary_entry.grid(row=2, column=1, sticky=tk.W, pady=2)

        return primary_entry

    def create_secondary_keyword_entry_box(self):
        """
        The create_secondary_keyword_entry_box creates the box that users
        will put their 2nd search term in.
        :return: secondary_entry:
        """
        # Creates text entry box
        secondary_entry = tk.Entry(self.master)

        # Place box on grid
        secondary_entry.grid(row=3, column=1, sticky=tk.W)

        return secondary_entry

    def create_text_output_box(self):
        """
        The function create_text_output_box creates the box the paragraph
        output will go into.
        :return: output_box:
        """
        # Create the output box for the returned paragraph
        output_box = tk.Text(self.master, height=40, width=40, wrap=tk.WORD)

        # Place output box on grid
        output_box.grid(row=2, column=3, columnspan=4, rowspan=4,
                        sticky=tk.E)

        return output_box

    def generate_paragraph_button(self):
        """
        The generate_paragraph_button function creates the button to
        generate a paragraph of text after the search terms have been entered.
        :return:
        """
        # Create a button, and set it to run_content_generator_backend when
        # clicked.
        tk.Button(self.master, text='Generate Paragraph',
                  command=self.run_content_generator_backend).grid(row=4,
                                                                   column=1,
                                                                   sticky=tk.W,
                                                                   pady=2)

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

        # Grab the keywords that were entered into the text entry boxes
        primary_keyword = self.primary.get()
        secondary_keyword = self.secondary.get()

        # Instantiate a findText object
        f = FindText()

        # Run all of the code in FindText in order to find a paragraph if one
        # exists
        paragraph_found = f.run_paragraph_finder(primary_keyword,
                                                 secondary_keyword)

        # Insert into text box
        self.output_text.insert('1.0', paragraph_found)

        c = CsvManipulation()  # Instantiate a CsvManipulation object

        # Write output to a csv
        c.export_csv('output.csv', primary_keyword, secondary_keyword,
                     paragraph_found)

        # Clear input
        self.primary.delete(0, tk.END)
        self.secondary.delete(0, tk.END)


class FindText:
    def __init__(self):
        self.primary_keyword = ""  # variable to hold primary keyword
        self.secondary_keyword = ""  # variable to hold secondary keyword

    def send_http_request(self, primary_keyword):
        """
        The send_http_request function makes a request to Wikipedia using
        the primary keyword and returns the parsed page for that primary
        keyword.
        :param primary_keyword:
        :return parsed_page_content:
        """
        # All of this code is from:
        # https://levelup.gitconnected.com/two-simple-ways-to-scrape-text
        # -from-wikipedia-in-python-9ce07426579b

        # Send request to Wikipedia page using the primary keyword
        res = requests.get("https://en.wikipedia.org/wiki/" + primary_keyword)

        # Parse request page
        parsed_page_content = BeautifulSoup(res.text, 'html.parser')

        # Return the parsed content of the page
        return parsed_page_content

    def parse_wikipedia_page_text(self, parsed_page_content):
        """
        The parse_wikipedia_page_text takes in all the content from the
        Wikipedia page and pulls out sentences with paragraph tags. It then
        returns a block of text which contains only the text on the
        Wikipedia page.
        :param parsed_page_content:
        :return text:
        """
        # All of this code is from:
        # https://levelup.gitconnected.com/two-simple-ways-to-scrape-text
        # -from-wikipedia-in-python-9ce07426579b

        # bypasses synonyms that are included as a paragraph tag on Wiki
        # this page helped me figure the above out:
        # https://stackoverflow.com/questions/43133632/web-scraping-a-wikipedia-page
        text = ''
        for paragraph in parsed_page_content.find_all('p'):  # [3:]:
            text += paragraph.text

        return text

    def clean_text(self, text):
        """
        The clean_text method takes in the paragraph text from the Wikipedia
        page and strips the text of footnote markers, and makes sure that
        all of the text is lower case. It then returns the cleaned text.
        :param text:
        :return text:
        """
        # All of this code is from:
        # https://levelup.gitconnected.com/two-simple-ways-to-scrape-text
        # -from-wikipedia-in-python-9ce07426579b

        # Clean up text to get rid of footnote markers
        text = re.sub(r'\[.*?\]+', '', text)

        # lower case everything
        text = text.lower()

        return text

    def find_paragraph(self, text, primary_keyword, secondary_keyword):
        """
        The find_paragraph method takes in the cleaned text, primary_keyword,
        and secondary_keyword and searches for the primary and secondary
        keywords in the text blob. It then returns the paragraph where both
        of these words are found if one exists.
        :param text:
        :param primary_keyword
        :param secondary_keyword
        :return found_paragraph:
        """
        # Now we can find the secondary keyword
        # Each paragraph ends with \n. So we need to split each line by \n
        # I found out how to do this from the following SO article:
        # https://stackoverflow.com/questions/14801057/python-splitting-to-the
        # -newline-character
        list_of_lines = text.splitlines()

        # When splitting lines, we need to also clean up words that can get
        # split with punctuation marks (e.g. dog., cat,, etc.). This is
        # because when we got to search for the word dog != dog. since the
        # period is attached to the 2nd occurance of dog. I found the below
        # SO helpful in parsing this out:
        # https://stackoverflow.com/questions/59877761/how-to-strip-string-from
        # -punctuation-except-apostrophes-for-nlp?noredirect=1&lq=1
        text_no_punctuation = re.sub(r'[^\w\d\s\']+', '', text)
        list_of_line_no_punctuation = text_no_punctuation.splitlines()

        found_paragraph = []  # empty list to hold the found paragraph


        # Now we will iterate through each line, and break up each line word
        # for word to see if the secondary keyword is in a paragraph.
        for i in range(len(list_of_lines)):
            # split the sentence into individual words
            # Found this SO helpful:
            # https://stackoverflow.com/questions/3897942/how-do-i-check-if-a-sentence-contains-a-certain-word-in-python-and-then-perform
            #words = list_of_lines[i]
            words = list_of_line_no_punctuation[i]
            words_list = words.split()

            # If both the primary and secondary keyword are in the list mark
            # the paragraph as found (aka keep it)
            if primary_keyword.lower() in words_list and \
                    secondary_keyword.lower() in words_list:

                # If both words are found, we return the paragraph.
                found_paragraph = list_of_lines[i]
                break

        return found_paragraph

    def run_paragraph_finder(self, primary_keyword, secondary_keyword):
        """
        The run_paragraph_finder method takes in the primary keyword and
        secondary keyword and runs all of the methods in the FindText class.
        This is to avoid redundancy. The function returns the paragraph if
        one is found.
        :param primary_keyword:
        :param secondary_keyword:
        :return paragraph_found:
        """
        # Send http request to Wikipedia
        wiki_page = self.send_http_request(primary_keyword)

        # Parse Wiki text
        text_grab = self.parse_wikipedia_page_text(wiki_page)

        # Clean text
        clean_text = self.clean_text(text_grab)
        print(clean_text)  # TAKE OUT

        # Find the paragraph with both primary and secondary keywords!
        paragraph_found = self.find_paragraph(clean_text, primary_keyword,
                                              secondary_keyword)

        return paragraph_found


class CsvManipulation:
    def __init__(self):
        """
        Constructor
        """

    def import_csv(self, filename):
        """
        The import_csv function takes in a filename and imports the csv to a
        list. It returns the list of data in the csv.
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
        The export_csv method takes in a filename, the primary keyword,
        secondary keyword and paragraph found and exports all of this
        information to a csv. The output can be found in your current
        directory.
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
    if len(sys.argv) == 1:

        # Start up the desktop app.
        # Again, I got this code from the following site:
        # https://www.python-course.eu/tkinter_entry_widgets.php
        root = tk.Tk()
        root.title("Content Generator")  # name of the application
        root.geometry('1000x650')  # initial size of the desktop app

        # Welcome message
        # Used this for learning how to scale widgets:
        # https://stackoverflow.com/questions/18252434/scaling-tkinter-widgets
        tk.Label(root, text="Welcome to the Content Generator! Please "
                            "place your search terms in the boxes "
                            "below \nin order to find a paragraph.").grid(
            row=0,
            column=3,
            columnspan=5,
            sticky=tk.NSEW)

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
        c.export_csv('output.csv', primary_keyword, secondary_keyword,
                     paragraph_found)

    # Otherwise if an incorrect argument was input, quit.
    else:
        print("Incorrect Argument(s) Provided. Quitting.")
        exit()
