Kindle to Anki
==============

Imports single-word highlights from your Kindle clippings file (or any .txt file with one word per line) to a specified Anki deck with their definitions.


Requirements
------------

From requirements.txt:

```
user@machine:kindleanki$ pip freeze
Send2Trash==1.3.0
argparse==1.2.1
beautifulsoup4==4.3.1
httplib2==0.8
wsgiref==0.1.2
```

The program works with Python 2.7 and Anki 2.0.12 on Ubuntu 13.04.

Instructions
------------

To run, type `python kindleanki.py`. If an argument isn't supplied, the program will input the cards to a deck called "Import". If an argument is supplied, the program will import the cards to the specified deck. For example, `python kindleanki.py Vocabulary` will import the cards to a deck called "Vocabulary".