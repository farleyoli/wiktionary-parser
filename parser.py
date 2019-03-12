import xml.sax
import string
import re
import os

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
            processText(self.textContent, self.title)
            self.textContent = ""


    def characters(self, content):
        if self.isText:
            self.textContent += content
        if self.isTitle:
            self.title += content

def getEnglish(textRaw):
    # if no English part in text, returns empty string
    # otherwise, returns string with raw english

    substr = "==English=="
    startPos = textRaw.find(substr)
    if startPos == -1:
        return ""
    startPos = startPos + 11

    isThereOtherLang = bool(re.search("[^=]==[A-Z]", textRaw[startPos:]))
    if(isThereOtherLang):
        endPos = re.search("[^=]==[^=]", textRaw[startPos:]).start()+1
        endPos += startPos
        #print("(there is at least another lang)")
        return textRaw[startPos:endPos]
    # english goes until end of string
    return textRaw[startPos:]


def processText(textRaw, title):
    #print(title)

    # get english string
    englishRaw = getEnglish(textRaw)
    print (englishRaw)
    print("\n------hmm------\n")

    # get pronunciation raw string

    # get definition raw string

    # pronunciation: raw string -> nice string

    # definition: raw string -> json

    # construct final json

    # add json to json dict file

def main():
    fileAddress = os.path.abspath('..') + "/test.xml"

    # handle XML so we can parse <text>s manually
    parser = xml.sax.make_parser()
    parser.setContentHandler(WiktionaryXMLHandler())
    parser.parse(fileAddress)

if ( __name__ == "__main__"):
    main()

