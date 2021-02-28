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
