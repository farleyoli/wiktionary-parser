#!/usr/bin/env python3

import xml.sax
import string
import re
import os
import json
import argparse # use this!!
from en_pron import clean_pron
from en_dfn import clean_dfn
from en_pre import get_english, get_pron, get_dfn

# TODO: External sorting (current program took up one third of
# my 4 GB ram)
# TODO: Avoid regex when possible: its use is probably what's
# making the program take so long to finish

class WiktionaryXMLHandler(xml.sax.ContentHandler):
    def __init__(self, output_path):
        self.isText = False
        self.counter = 0
        self.textContent = ""
        self.title = ""
        self.dict = []
        self.output_path = output_path

    def startElement(self, name, attrs):
        if name == "text":
            self.isText = True
        else:
            self.isText = False

        if name == "title":
            # new title
            self.isTitle = True
            self.title = ""
        else:
            # preserves old title (until new one is processed)
            self.isTitle = False

    def endElement(self, name):
        if name == "text":
            term = process_text(self.textContent, self.title.strip())
            self.textContent = ""
            if term != -1:
                #print(term)
                self.counter += 1
                print(self.counter)
                self.dict.append(term)


    def characters(self, content):
        if self.isText:
            self.textContent += content
        if self.isTitle:
            self.title += content
            print(self.title)

    def endDocument(self):
        self.dict = sorted(self.dict, key=lambda k: k['t'])
        #fileAddress = os.path.abspath('../..') + "/test.txt"
        #with open(self.output_path, 'w') as outfile:  
        with self.output_path as outfile:
            #json.dump({"dict" : self.dict}, outfile)
            json.dump(self.dict, outfile)

        #print(self.dict)


def process_text(text_raw, title):
    """This method processses one wiktionary page each time it is called.""" 
    english_raw = get_english(text_raw)

    if (len(english_raw) == 0):
        # no need to add words that do not exist
        return -1


    pron_raw = get_pron(english_raw)
    dfn_raw = get_dfn(english_raw)
    pron = clean_pron(pron_raw)

    dfn = []
    for raw in dfn_raw:
        dfn.append(clean_dfn(raw[1]))

    pair = { 't' : title, 'd': dfn }

    return pair

    #print(dfn)

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist." % arg)
    else:
        return open(arg, 'r')  # return an open file handle

def can_we_write_in_path(parser, arg):
    if os.path.exists(arg):
        #the file is there
        return open(arg, 'w')
    elif os.access(os.path.dirname(arg), os.W_OK):
        #the file does not exists but write privileges are given
        return open(arg, 'w')
    return parser.error("We cannot write a new file in path %s." % arg)



def process_args(parser):
    parser.add_argument("-i", dest="filename", required=True, 
            help="Path to wiktionary dump file.", metavar="FILE",
            type=(lambda x: is_valid_file(parser, x)))
    parser.add_argument("-o", dest="output", required=True, 
            help="Path to output json file.", metavar="FILE",
            type=lambda x: can_we_write_in_path(parser, x))
    args = parser.parse_args()
    return args

def main():
    parser = argparse.ArgumentParser()
    args = process_args(parser)

    #fileAddress = os.path.abspath('../..') + "/enwiktionary-20190301-pages-articles.xml"
    fileAddress = args.filename
    output_path = args.output

    # handle XML so we can parse <text>s manually
    parser = xml.sax.make_parser()
    parser.setContentHandler(WiktionaryXMLHandler(output_path))
    parser.parse(fileAddress)

if ( __name__ == "__main__"):
    main()
