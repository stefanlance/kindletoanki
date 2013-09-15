#!/usr/bin/env python3

# Kindle to Anki
# Puts Kindle vocabulary words into Anki with their definitions.

# TODO:
# - Allow user to set number of definitions obtained
# - Ensure duplicates aren't added to the deck
# - Ensure user enters a valid path

import csv
import sys
import re
import json
import urllib.request
from bs4 import BeautifulSoup
# from anki.importing import TextImporter
# from anki import Collection


def set_path(path_type):
    return input("Enter the path to your {0} file: ".format(path_type))


def get_path(path_type):

    data = 'data/{0}_path.txt'.format(path_type)

    try:
        with open(data):
            file = open(data, 'r')
            path = file.readline()
            file.close()
            # Also need to ensure user enters a valid path (to a .txt)
            pass

    except:
        path = set_path(path_type)
        file = open(data, 'w')
        file.write(path)
        file.close()

    return path


def save_dictionary(dictionary):

    file = open('data/dictionary.txt', 'w')
    for key in dictionary.keys():
        line = "{0}\t{1}\n".format(key, dictionary[key])
        print(line)
        file.write(line)

    file.close()


def get_dictionary(clippings_path=''):

    file = open(clippings_path, 'r')
    word_definition_pairs = dict()

    for line in file:
        matched = re.match(r"^([\w-]+)[.]?$", line)

        if matched:
            word = matched.group(1).lower()
            definition = get_definition(word)

            if definition:
                word_definition_pairs[word] = definition

    file.close()

    return word_definition_pairs


def get_definition(word):

    url = 'http://dictionary.reference.com/browse/{0}?s=t'.format(word)
    soup = BeautifulSoup(urllib.request.urlopen(url).read())
    definition = soup.find_all('div', attrs={'class':'dndata'}, text = True)

    if definition:
        # Add multiple definitions here (maybe by part of speech?)
        return definition[0].string

    else:
        return False


def add_dictionary_to_anki(collection_path):
    # See:
    # http://ankisrs.net/docs/addons.html#the-collection

    # file = u'data/dictionary.txt'
    # col = Collection(collection_path)

    # # Change to the basic note type
    # m = mw.col.models.byName('Basic')
    # mw.col.models.setCurrent(m)

    # # Set 'Import' as the target deck
    # m['did'] = mw.col.decks.id('Import')
    # mw.col.models.save(m)

    # # Import into the collection
    # ti = TextImporter(mw.col, file)
    # ti.initMapping()
    # ti.run()
    
    # col.close()

    return 0


def main():
    clippings_path = get_path('clippings')
    collection_path = get_path('collection')

    dictionary = get_dictionary(clippings_path)
    save_dictionary(dictionary)
    add_dictionary_to_anki(collection_path)


if __name__ == "__main__":
    main()
