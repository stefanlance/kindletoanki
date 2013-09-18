#!/usr/bin/env python

# Kindle to Anki
# Puts Kindle vocabulary words into Anki with their definitions.

# TODO:
# - Allow user to set number of definitions obtained
# - Ensure user enters a valid path
# - Allow user to import cards to multiple decks (no duplicates is global)
# - -Fix "no module" errors that occur when not using virtualenv-
# - After a deck has been set, using a deck of a different name does not
# work (could be for todo #3)


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

    # Do we have a command-line arg? If so, 

    try:
        with open(data):
            file = open(data, 'r')
            path = unicode(os.path.expanduser(file.readline()))

            file.close()
            # Also need to ensure user enters a valid path (to a .txt)
            pass

    except:
        path = unicode(os.path.expanduser(set_path(path_type)))

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
        line = u"{0}\t{1}\n".format(key, dictionary[key])
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
            print("\n\n")
            print(word)
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

    soup_group = soup.find_all('div', attrs={'class':'pbk'})

    dict_entry = ''

    if soup_group:
        for entry in soup_group:
            part_of_speech = entry.find_all('span', attrs={'class':'pg'})
            def_num = 1

            if part_of_speech:
                dict_entry += u'</br><b>{0}'.format(part_of_speech[0].string)
                dict_entry += '</b></br>'

            for definition in entry.find_all('div',
                                             attrs={'class':'dndata'},
                                             text = True):
                dict_entry += u'<li>{0}</li>'.format(definition.string)
            

    if dict_entry:
        print(dict_entry)
        return dict_entry

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
    ti.allowHTML = True
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
    add_dictionary_to_anki(collection_path, deck_name)


if __name__ == "__main__":
    main()
