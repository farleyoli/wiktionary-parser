import xml.sax
import string
import re
import os
from en_pron import clean_pron
from en_dfn import clean_dfn
from en_pre import get_english, get_pron, get_dfn

class WiktionaryXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.isText = False
        self.counter = 0
        self.textContent = ""
        self.title = ""

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
            process_text(self.textContent, self.title.strip())
            self.textContent = ""


    def characters(self, content):
        if self.isText:
            self.textContent += content
        if self.isTitle:
            self.title += content

        
def process_text(text_raw, title):
    """This method processses one wiktionary page each time it is called.""" 
    english_raw = get_english(text_raw)

    if (len(english_raw) == 0):
        # no need to add words that do not exist
        return ""

    print(title)

    pron_raw = get_pron(english_raw)
    dfn_raw = get_dfn(english_raw)
    pron = clean_pron(pron_raw)

    dfn = []
    for raw in dfn_raw:
        dfn.append(clean_dfn(raw[1]))

    # process json


def main():
    fileAddress = os.path.abspath('../..') + "/test.xml"

    # handle XML so we can parse <text>s manually
    parser = xml.sax.make_parser()
    parser.setContentHandler(WiktionaryXMLHandler())
    parser.parse(fileAddress)

if ( __name__ == "__main__"):
    main()

