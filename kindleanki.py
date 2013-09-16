#!/usr/bin/env python

# Kindle to Anki
# Puts Kindle vocabulary words into Anki with their definitions.

# TODO:
# - Allow user to set number of definitions obtained
# - Ensure duplicates aren't added to the deck
# - Ensure user enters a valid path

import csv
import sys, os.path
import re
import json
import urllib2
from bs4 import BeautifulSoup
from anki.importing import TextImporter
from anki import Collection


def set_path(path_type):
    return raw_input("Enter the path to your {0} file: ".format(path_type))


def get_path(path_type):

    data = 'data/{0}_path.txt'.format(path_type)

    try:
        with open(data):
            file = open(data, 'r')
            path = file.readline()

            if re.compile('^\~').match(path):
                path = re.sub(r'^\~', path, '')
                print(path)

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
        file.write(line)

    file.close()

    print("Saved words and definitions to dictionary file.")


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
    # Does it matter whether we use request?
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    # soup = BeautifulSoup(urllib2.openurl(url).read())
    definition = soup.find_all('div', attrs={'class':'dndata'}, text = True)

    if definition:
        # Add multiple definitions here (maybe by part of speech?)
        return definition[0].string

    else:
        return False


def add_dictionary_to_anki(collection_path):
    # See:
    # http://ankisrs.net/docs/addons.html#the-collection

    dictionary = u'{0}'.format(os.path.abspath('data/dictionary.txt'))
    col = Collection(collection_path)

    # Change to the basic note type
    m = col.models.byName('Basic')
    col.models.setCurrent(m)

    # Set 'Import' as the target deck
    m['did'] = col.decks.id('Import')
    col.models.save(m)

    # Import into the collection
    ti = TextImporter(col, dictionary)
    ti.initMapping()
    ti.run()
    
    col.close()

    print("Imported dictionary into collection.")

    return 0


def main():
    clippings_path = get_path('clippings')
    collection_path = get_path('collection')

    dictionary = get_dictionary(clippings_path)
    save_dictionary(dictionary)
    add_dictionary_to_anki(collection_path)


if __name__ == "__main__":
    main()
