#!/usr/bin/env python

# Kindle to Anki
# Puts Kindle vocabulary words into Anki with their definitions.

# TODO:
# - Allow user to set number of definitions obtained
# - Ensure user enters a valid path
# - Allow user to import cards to multiple decks (no duplicates is global)
# - Fix "no module" errors that occur when not using virtualenv


import csv
import sys, os.path
import re
import json
import urllib2
from bs4 import BeautifulSoup
from anki.importing import TextImporter
from anki import Collection


def set_path(path_type):

    path_extensions = {'clippings':'txt', 'collection':'anki2'}
    ext = path_extensions[path_type]
    path = ''

    while path.split('.')[-1] != ext:
        path = raw_input("Enter the path to your "
                         "{0} file: ".format(path_type))

    return path


def get_path(path_type):

    data = 'data/{0}_path.txt'.format(path_type)

    try:
        with open(data):
            file = open(data, 'r')
            path = unicode(os.path.expanduser(file.readline()))
            #path = os.path.expanduser(path)

            file.close()
            # Also need to ensure user enters a valid path (to a .txt)
            pass

    except:
        path = unicode(os.path.expanduser(set_path(path_type)))
        #path = os.path.expanduser(path)

        file = open(data, 'w')
        file.write(path)
        file.close()

    return path


def set_deck_name():

    if len(sys.argv) < 2:
        deck_name = raw_input("Name of deck to which your cards will "
                              "be imported: ")
    else:
        deck_name = sys.argv[1]

    return deck_name


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

    print("Found Kindle clippings file.")

    for line in file:

        matched = re.match(r'(^|\r\n)([\w-]+)[.]?($|\r\n)',
                           line, re.MULTILINE)

        if matched:
            word = matched.group(2).lower()
            definition = get_definition(word)

            if definition:
                word_definition_pairs[word] = definition

    file.close()

    print("Got word definitions from web.")

    return word_definition_pairs


def get_definition(word):

    url = 'http://dictionary.reference.com/browse/{0}?s=t'.format(word)
    # Does it matter whether we use request?
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    definition = soup.find_all('div', attrs={'class':'dndata'}, text = True)

    if definition:
        for d in definition:
            print(d.string)

        return definition[0].string

    else:
        return False


def add_dictionary_to_anki(collection_path, deck_name = 'Import'):
    # See:
    # http://ankisrs.net/docs/addons.html#the-collection

    dictionary = unicode(os.path.abspath('data/dictionary.txt'))
    col = Collection(collection_path)

    # Change to the basic note type
    m = col.models.byName('Basic')
    col.models.setCurrent(m)

    # Set 'Import' as the target deck
    m['did'] = col.decks.id(deck_name)
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
    deck_name = set_deck_name()

    dictionary = get_dictionary(clippings_path)
    save_dictionary(dictionary)
#    add_dictionary_to_anki(collection_path, deck_name)


if __name__ == "__main__":
    main()
