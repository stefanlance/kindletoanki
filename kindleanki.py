#!/usr/bin/env python3

# Kindle to Anki
# Puts Kindle vocabulary words into Anki with their definitions.

import csv
import sys
import re
import json
import urllib.request, urllib.parse

def set_clippings_path():
    return input("Enter the path to your Calibre Kindle clippings file: ")

def get_words(clippings_path=""):
    # Find Kindle Clippings file (set by Calibre for us)
    # Expects Calibre format

    file = open(clippings_path, "r")
    word_def = dict()

    for line in file:
        m = re.match(r"^([\w-]+)[.]?$", line)
        if m:
            word = m.group(1).lower()
            print(word)
            url='http://dictionary.reference.com/browse/{0}?s=t'.format(word)
            print(urllib.request.urlopen(url))
    

    # Look up their definitions
    get_definition(word)

    return 0

def get_definition(word):
    return 0


def main():
    # if <clippings_path.txt does not exist>
    path = set_clippings_path()
    # add a "change path" option, too...
    get_words(path)


if __name__ == "__main__":
    main()
