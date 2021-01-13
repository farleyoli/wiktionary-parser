import xml.sax
import string
import re
import os
import json
import string
import argparse # use this!!
from en_pron import clean_pron
from en_dfn import clean_dfn
from en_pre import get_english, get_pron, get_dfn

class WiktionaryXMLHandler(xml.sax.ContentHandler):
    def add_term_to_dict(self, term):
        """Add term to the appropriate json dictionary file.
        """
        lettert = get_letter(term[0])
        if lettert != self.letter:
            return
        fname = "../../output_dict/" + lettert + ".json"
        #print(fname)
    ##    with open(fname, "r") as f:
    ##        dictf = json.load(f)
    ##    dictf[term[0]] = term[1]
    ##    with open(fname, "w") as f:
    ##        json.dump(dictf, f)
        self.dict[term[0]] = term[1]
        print(term[0])
    def get_first_letter(self):
        """Get initial letter for which to create JSON dictionary from user.
        """
        ret = ""
        while True:
            ret = raw_input("Which initial letter do you wish to create a JSON dictionary for? (Please input a ascii lowercase or 'other')\n")
            if ret in list(string.ascii_lowercase) or ret == "other":
                return ret
    def initialize_dicts(self):
        """Create (new) output json files which correspond to each letter
        of the alphabet. Beware that files will be overwritten if they
        already exist (will probably change this later).
        """
        alphabet = list(string.ascii_lowercase)
        alphabet.append('other')
        d = {}
        for letter in alphabet:
            fname = str('../../output_dict/') + letter + '.json'
            with open(fname, "w") as f:
                json.dump(d, f)

    def __init__(self, output_path):
        self.isText = False
        self.counter = 0
        self.textContent = ""
        self.title = ""
        self.dict = {}
        self.output_path = output_path
        #self.initialize_dicts()
        self.letter = self.get_first_letter()

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
                #print(self.counter)
                #self.dict[term[0]] = term[1]
                self.add_term_to_dict(term)
                if self.counter % 10 == 0:
                    print(self.counter)
                #print(term[0])


    def characters(self, content):
        if self.isText:
            self.textContent += content
        if self.isTitle:
            self.title += content
            #print(self.title)

    def endDocument(self):
        #self.dict = sorted(self.dict, key=lambda k: k['t'])
        #fileAddress = os.path.abspath('../..') + "/test.txt"
        #with open(self.output_path, 'w') as outfile:  
        with self.output_path as outfile:
            json.dump(self.dict, outfile)
            #json.dump({"dict" : self.dict}, outfile)
        #print(self.dict)

def get_letter(word):
    """Return first letter (or other) of word, in order to select the
    dictionary file to which to add the term.
    """
    alphabet = list(string.ascii_lowercase)
    if word[0].lower() in alphabet:
        return word[0].lower()
    return 'other'

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

    pair = ( title, dfn )

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
