import xml.sax
import string
import re
import os
from enPron import cleanPron
from enDfn import cleanDfn
from enPre import getEnglish, getPron, getDfn

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
            processText(self.textContent, self.title.strip())
            self.textContent = ""


    def characters(self, content):
        if self.isText:
            self.textContent += content
        if self.isTitle:
            self.title += content

        

def processText(textRaw, title):

    englishRaw = getEnglish(textRaw)
    #print (englishRaw)

    if (len(englishRaw) == 0):
        # no need to add words that do not exist
        return ""

    print(title)

    pronRaw = getPron(englishRaw)
    #print(pronRaw)

    dfnRaw = getDfn(englishRaw)

    pron = cleanPron(pronRaw)
    #print(pron)

    # definition: raw string (one for each class) -> 
    #      (ancestor, [dfn, [exs], [quotes]])
    for raw in dfnRaw:
        dfn = cleanDfn(raw)

    # construct final json

    # add json to json dict file


    print()

def main():
    fileAddress = os.path.abspath('../..') + "/test.xml"

    # handle XML so we can parse <text>s manually
    parser = xml.sax.make_parser()
    parser.setContentHandler(WiktionaryXMLHandler())
    parser.parse(fileAddress)

if ( __name__ == "__main__"):
    main()

