# Name: Megan Morrison
# Date: February 21, 2021
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
import tkinter as tk
import threading
from server import micro_server
from client import micro_client
from bs4 import BeautifulSoup

# References:
# How to get content from Wikipedia:
# https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-
# wikipedia-in-python-9ce07426579b

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
        self.request_data_button()
        self.paragraph_found = ''

    def create_labels(self):
        """
        Creates labels for text entry boxes.
        :return: None
        """
        tk.Label(self.master, text="Primary Word (e.g. Dog)").grid(row=2)
        tk.Label(self.master, text="Secondary Word (e.g Breed)").grid(row=3)

    def create_primary_keyword_entry_box(self):
        """
        Returns a string which is input as the primary keyword
        :return: primary_entry_box:
        """
        primary_entry_box = tk.Entry(self.master)

        primary_entry_box.grid(row=2, column=1, sticky=tk.W, pady=2)

        return primary_entry_box

    def create_secondary_keyword_entry_box(self):
        """
        Returns a string which is input as the secondary keyword
        :return: secondary_entry_box:
        """
        secondary_entry_box = tk.Entry(self.master)

        secondary_entry_box.grid(row=3, column=1, sticky=tk.W)

        return secondary_entry_box

    def create_text_output_box(self):
        """
        Creates a box to hold the output text.
        :return: output_box:
        """
        output_box = tk.Text(self.master, height=40, width=40, wrap=tk.WORD)

        output_box.grid(row=2, column=3, columnspan=4, rowspan=4,
                        sticky=tk.E)

        return output_box

    def generate_paragraph_button(self):
        """
        Sends request to Wikipedia using the primary and secondary keywords.
        :return None:
        """
        tk.Button(self.master, text='Generate Paragraph',
                  command=self.run_content_generator_backend).grid(row=4,
                                                                   column=1,
                                                                   sticky=tk.W,
                                                                   pady=2)
    def request_data_button(self):
        """
        :return:
        """
        tk.Button(self.master, text='Request Life\n Generator Data',
                  command=self.get_life_generator_input).grid(row=5, column=1)

    def start_life_generator_client(self, message):
        """
        :param message:
        :return:
        """
        # Note that Joseph Polaski and I worked together to devleop the
        # socket client/server programs. Our calls to the client and server
        # are similar since we developed the sockets together.
        client = micro_client('LIFE_GEN')  # create a life generator
        response = client.send_message(message)
        print(response)
        return response

    def start_content_generator_server(self):
        """
        :return:
        """
        # Note that Joseph Polaski and I worked together to devleop the
        # socket client/server programs. Our calls to the client and server
        # are similar since we developed the sockets together.
        server = micro_server(self.content_generator_server_callback, "CONT_GEN")
        run_server_thread = threading.Thread(target=server.start_listening)
        run_server_thread.start()

    def content_generator_server_callback(self, request):
        """Returns data to the Life Generator when requested."""
        # Note that Joseph Polaski and I worked together to devleop the
        # socket client/server programs. Our calls to the client and server
        # are similar since we developed the sockets together.
        print(f"The request was: {request}")

        if len(self.get_returned_paragraph()) == 0:
            self.paragraph_found = "I couldn't find a paragraph with " \
                                          "these terms."

        return self.paragraph_found

    def get_life_generator_input(self):
        """
        :return:
        """
        client_data = self.start_life_generator_client('Give me some life!')

        primary_keyword, secondary_keyword = FindText().parse_incoming_data(
            client_data, 'text')

        self.paragraph_found = self.get_wikipedida_text(primary_keyword,
                                                   secondary_keyword)

        self.output_content_generator_results(primary_keyword,
                                              secondary_keyword,
                                              self.paragraph_found)


    def get_returned_paragraph(self):
        """Returns paragraph_found attribute"""
        return self.paragraph_found

    def get_content_generator_input(self):
        """
        Gets input from content generator GUI and returns two string variables
        :return primary_keyword:
        :return secondary_keyword:
        """
        # This SO page helped me figure out how to get text out of the entry
        # boxes when using classes:
        # https://stackoverflow.com/questions/10727131/why-is-tkinter-entrys-get-function-returning-nothing

        self.output_text.delete('1.0', tk.END)

        primary_keyword = self.primary.get()
        secondary_keyword = self.secondary.get()

        return primary_keyword, secondary_keyword

    def get_wikipedida_text(self, primary_keyword, secondary_keyword):
        """
        Takes in two string variables and returns a string variable.
        :param primary_keyword:
        :param secondary_keyword:
        :return:
        """

        find_text_object = FindText()

        self.paragraph_found = find_text_object.run_paragraph_finder(primary_keyword,
                                                  secondary_keyword)

        self.output_text.insert('1.0', self.paragraph_found)

        return self.paragraph_found

    def output_content_generator_results(self, primary_keyword,
                                         secondary_keyword,
                                         paragraph):
        """
        Takes in 3 string variables and exports data.
        :param primary_keyword:
        :param secondary_keyword:
        :param paragraph_found:
        :return:
        """

        csv_object = CsvManipulation()

        csv_object.export_csv('output.csv', primary_keyword, secondary_keyword, self.
                     paragraph_found)

    def clear_content_generator_input(self):
        """
        Clears entry text boxes in GUI.
        :return:
        """
        self.primary.delete(0, tk.END)
        self.secondary.delete(0, tk.END)

    def run_content_generator_backend(self):
        """
        Runs the entire content generator program.
        :return None:
        """

        primary_keyword, secondary_keyword = self.get_content_generator_input()

        self.paragraph_found = self.get_wikipedida_text(primary_keyword,
                                                    secondary_keyword)

        self.output_content_generator_results(primary_keyword,
                                              secondary_keyword,
                                              self.paragraph_found)

        self.clear_content_generator_input()


class FindText:
    def __init__(self):
        self.primary_keyword = ""
        self.secondary_keyword = ""

    def send_http_request(self, primary_keyword):
        """
        Takes in a string which is sent to Wikipedia and returns a string
        of text.
        :param primary_keyword:
        :return parsed_page_content:
        """
        # All of this code is from:
        # https://levelup.gitconnected.com/two-simple-ways-to-scrape-text
        # -from-wikipedia-in-python-9ce07426579b
        # This code sends a request to Wikipedia and parses the returned page.

        res = requests.get("https://en.wikipedia.org/wiki/" + primary_keyword)

        parsed_page_content = BeautifulSoup(res.text, 'html.parser')

        return parsed_page_content

    def parse_wikipedia_page_text(self, parsed_page_content):
        """
        Takes in a string of parsed webpage content and returns it as a
        string of text.
        :param parsed_page_content:
        :return text:
        """
        # All of this code is from:
        # https://levelup.gitconnected.com/two-simple-ways-to-scrape-text
        # -from-wikipedia-in-python-9ce07426579b
        # https://stackoverflow.com/questions/43133632/web-scraping-a-wikipedia-page
        parsed_wiki_text = ''
        for paragraph in parsed_page_content.find_all('p'):
            parsed_wiki_text += paragraph.text

        return parsed_wiki_text

    def clean_text(self, parsed_text):
        """
        Takes in a string of text, cleans it, and returns a string of text.
        :param text:
        :return text:
        """
        # All of this code is from:
        # https://levelup.gitconnected.com/two-simple-ways-to-scrape-text
        # -from-wikipedia-in-python-9ce07426579b

        # Clean up text to get rid of footnote markers
        parsed_text = re.sub(r'\[.*?\]+', '', parsed_text)

        parsed_text_cleaned = parsed_text.lower()

        return parsed_text_cleaned

    def split_paragraph_text_into_lines(self, cleaned_wiki_text):
        """
        Takes in a string variable and returns two lists of strings.
        :param text:
        :return:
        """
        # We need to split each line by \n.
        # I found out how to do this from the following SO article:
        # https://stackoverflow.com/questions/14801057/python-splitting-to-the
        # -newline-character
        list_of_lines = cleaned_wiki_text.splitlines()

        return list_of_lines

    def remove_punctionation_and_split_into_list_of_lines(self,
                                                          cleaned_wiki_text):
        """
        Takes in a string and returns a list of strings
        :param text:
        :return:
        """
        # Make sure punctuation marks don't get attached to words. (e.g.'dog.', 'cat,')
        # I found the below SO helpful in parsing this out:
        # https://stackoverflow.com/questions/59877761/how-to-strip-string-from
        # -punctuation-except-apostrophes-for-nlp?noredirect=1&lq=1
        text_no_punctuation = re.sub(r'[^\w\d\s\']+', '', cleaned_wiki_text)

        list_of_line_no_punctuation = text_no_punctuation.splitlines()

        return list_of_line_no_punctuation

    def split_lines_into_words(self, list_of_lines_no_punctuation, index):
        """
        Takes in a list of strings and returns a list of strings
        :param list_of_lines:
        :return:
        """
        # split the sentence into individual words
        # Found this SO helpful:
        # https://stackoverflow.com/questions/3897942/how-do-i-check-if-a-
        # sentence-contains-a-certain-word-in-python-and-then-perform
        words = list_of_lines_no_punctuation[index]
        words_list = words.split()
        return words_list

    def do_primary_and_secondary_words_exist_in_text(self, primary_keyword,
                                                     secondary_keyword, text):
        """

        :param primary_keyword:
        :param secondary_keyword:
        :param text:
        :return:
        """
        index = 0
        list_of_lines = self.split_paragraph_text_into_lines(text)
        words_list = self.split_lines_into_words(list_of_lines, index)
        if primary_keyword.lower() in words_list and secondary_keyword.lower() in words_list:
            return True

    def find_paragraph(self, text, primary_keyword, secondary_keyword):
        """
        Takes in three string arguements, finds the text in a paragraph,
        and returns a string of text.
        :param text:
        :param primary_keyword
        :param secondary_keyword
        :return found_paragraph:
        """
        # # We need to split each line by \n.
        # # I found out how to do this from the following SO article:
        # # https://stackoverflow.com/questions/14801057/python-splitting-to-the
        # # -newline-character
        # list_of_lines = text.splitlines()
        #
        # # Make sure punctuation marks don't get attached to words. (e.g.
        # # 'dog.', 'cat,')
        # # I found the below SO helpful in parsing this out:
        # # https://stackoverflow.com/questions/59877761/how-to-strip-string-from
        # # -punctuation-except-apostrophes-for-nlp?noredirect=1&lq=1
        # text_no_punctuation = re.sub(r'[^\w\d\s\']+', '', text)
        # list_of_line_no_punctuation = text_no_punctuation.splitlines()

        list_of_lines = self.split_paragraph_text_into_lines(text)
        list_of_lines_no_punctuation = \
            self.remove_punctionation_and_split_into_list_of_lines(text)
        #words = self.split_lines_into_words(index, text)

        found_paragraph = []

        for i in range(len(list_of_lines)):
            # # split the sentence into individual words
            # # Found this SO helpful:
            # # https://stackoverflow.com/questions/3897942/how-do-i-check-if-a-
            # # sentence-contains-a-certain-word-in-python-and-then-perform
            words = list_of_lines_no_punctuation[i]
            words_list = words.split()

            if primary_keyword.lower() in words_list and \
                    secondary_keyword.lower() in words_list:
                found_paragraph = list_of_lines[i]
                break

        return found_paragraph

    def run_paragraph_finder(self, primary_keyword, secondary_keyword):
        """
        Takes in two string variables, finds a paragraph from Wiki,
        and returns as string variable.
        :param primary_keyword:
        :param secondary_keyword:
        :return paragraph_found:
        """
        wiki_page = self.send_http_request(primary_keyword)

        wikipedia_text = self.parse_wikipedia_page_text(wiki_page)

        clean_text = self.clean_text(wikipedia_text)

        paragraph_found = self.find_paragraph(clean_text, primary_keyword,
                                              secondary_keyword)

        return paragraph_found

    def get_incoming_data(self, input_data, filetype):
        """Gets data from csv or sockets. Takes in a string or list as
        input_data and a string for filetype (text or csv) and returns a
        string of data"""
        if filetype == 'csv':
            words_data = input_data[1][0].split(';')

        else:
            words_data = input_data.split(';')

        return words_data

    def parse_incoming_data(self, input_data, filetype):
        """Parses data from csv or sockets. Takes in a string or list as
        input_data and a string for filetype (text or csv) and returns two
        string variables."""

        words_data = self.get_incoming_data(input_data, filetype)
        primary_keyword = words_data[0]
        secondary_keyword = words_data[1].split()[0]

        secondary_keyword = re.sub(r'[^\w\d\s\']+', '', secondary_keyword)

        return primary_keyword, secondary_keyword


class CsvManipulation:
    def __init__(self):
        """
        Constructor
        """

    def import_csv(self, filename):
        """
        Takes in a string variable, imports the csv, and returns a string.
        :param filename:
        :return: data
        """
        # Found this SO helpful: https://stackoverflow.com/questions/24662571/
        # python-import-csv-to-list
        with open(filename, newline='') as file:
            csv_reader = csv.reader(file)
            data_from_csv = list(csv_reader)

        return data_from_csv

    def export_csv(self, filename, first_word, second_word, paragraph):
        """
        Takes in 4 string variables and exports to a csv.
        :param filename:
        :param first_word:
        :param second_word:
        :param paragraph:
        :return: Nothing
        """
        # Source: https://realpython.com/python-csv/
        with open(filename, mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',',
                                       quotechar='"',
                                       quoting=csv.QUOTE_MINIMAL)

            output_writer.writerow(['input_keywords', 'output_content'])

            output_writer.writerow([first_word + ';' + second_word, paragraph])



if __name__ == "__main__":
    # If there is only one argument in the command prompt run the GUI.
    if len(sys.argv) == 1:

        # Start up the desktop app.
        # Again, I got this code from the following site:
        # https://www.python-course.eu/tkinter_entry_widgets.php
        root = tk.Tk()
        root.title("Content Generator")
        root.geometry('1000x650')

        # Used this for learning how to scale widgets:
        # https://stackoverflow.com/questions/18252434/scaling-tkinter-widgets
        tk.Label(root, text="Welcome to the Content Generator! Please "
                            "place your search terms in the boxes "
                            "below \nin order to find a paragraph.").grid(
            row=0,
            column=3,
            columnspan=5,
            sticky=tk.NSEW)

        app = ContentGeneratorApp(master=root)
        app.start_content_generator_server()
        app.mainloop()

    # Else, read in the input file.
    elif sys.argv[1] == "input.csv":

        csv_object = CsvManipulation()

        file_data = csv_object.import_csv(sys.argv[1])

        find_text_object = FindText()

        primary_keyword, secondary_keyword = find_text_object.parse_incoming_data(
            file_data, 'csv')

        paragraph_found = find_text_object.run_paragraph_finder(primary_keyword,
                                                 secondary_keyword)

        csv_object.export_csv('output.csv', primary_keyword, secondary_keyword,
                     paragraph_found)

    # Otherwise, if an incorrect argument was input, quit.
    else:
        print("Incorrect Argument(s) Provided. Quitting.")
        exit()


# This is how the program is gonna work
# 1. Open both programs
# 2. In Content Generator click request button
# 3. Request made & data sent back
# 4. Content gen runs paragraph finder & stores paragraph
# 5. Go into Life Generator & click request button
# 6. Content gen sends back stored paragraph
# 5. Life Gen displays paragraph data.