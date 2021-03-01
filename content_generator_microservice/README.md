# Content Generator Microservice

The Content Generator microservice is a Wikipedia wescrapper. 
The user is asked to input two words they want to search for. The first
word will pull that Wikipedia page and all of it's contents. The second word
is used for searching the text of the Wikipedia page. 

If a paragraph is found from the searched Wikipedia page that contains
both words, it is returned to the user.

The user has the option to use a desktop GUI in order to make the search
or to include a csv. The csv must have the following form and be called 
input.csv:
```
input_keywords  
dog;breed
```

---
Running the Program
---
First, make sure the following files are in the same directory:  
```
requirements.txt
content-generator.py
server.py
client.py
input.csv (optionally provided)
```

**To run the program use these steps below:**

1. Open the terminal (Mac/Linux) or cmd.exe (Windows)   
   

2. In the command line, create this virtual environment:
```
virtualenv content-generator --python=python3
```
3. Activate the virtual environment: 
```
source content-generator/bin/activate
```

4. Install requirements.txt by running this command in the command line:
```
pip3 install -r requirements.txt
```
   
5. Run the following command to run the Content Generator GUI:
```
python3 content-generator.py
```
6. If you would like to use the Content Generator with a CSV, run the 
   following command:
   
```
python3 content-generator.py input.csv
```