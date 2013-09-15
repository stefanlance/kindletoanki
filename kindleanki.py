#!/usr/bin/env python3

# Kindle to Anki
# Puts Kindle vocabulary words into Anki with their definitions.

import csv
import sys
import re
import json
import urllib.request
from bs4 import BeautifulSoup


def set_clippings_path():
    return input("Enter the path to your Calibre Kindle clippings file: ")


def get_words(clippings_path=''):
    # Expects Calibre format

    file = open(clippings_path, 'r')
    word_definition_pairs = dict()

    for line in file:
        matched = re.match(r"^([\w-]+)[.]?$", line)

        if matched:
            word = matched.group(1).lower()
            definition = get_definition(word)

            if definition:
                word_definition_pairs[word] = definition
                print(word, "\t", definition)


    file.close()

    return word_definition_pairs


def get_definition(word):

    url='http://dictionary.reference.com/browse/{0}?s=t'.format(word)
    soup = BeautifulSoup(urllib.request.urlopen(url).read())
    definition = soup.find_all('div', attrs={'class':'dndata'}, text = True)

    if definition:
        return definition[0].string

    else:
        return False


def get_clippings_path():
    try:
        with open('data/clippings_path.txt'):
            file = open('data/clippings_path.txt', 'r')
            path = file.readline()
            file.close()
            # Also need to ensure user enters a valid path (to a .txt)
            pass

    except:
        path = set_clippings_path()
        file = open('data/clippings_path.txt', 'w')
        file.write(path)
        file.close()

    return path


def main():
    path = get_clippings_path()
    get_words(path)


if __name__ == "__main__":
    main()
