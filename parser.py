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

def getEnglish(raw):
    # if no English part in text, returns empty string
    # otherwise, returns string with raw english

    substr = "==English=="
    startPos = raw.find(substr)
    if startPos == -1:
        return ""
    startPos = startPos + 11

    # FM: four minus
    isThereFM = bool(re.search("[^-]----[^-]", raw[startPos:]))  
    if(isThereFM):
        endPos = re.search("[^-]----[^-]", raw[startPos:]).start()+1
        endPos += startPos
        #print("(there is at least another lang)")
        return raw[startPos:endPos]


    # add redundancy
    # (DE: double equal)
    isThereDE = bool(re.search("[^=]==[^=]", raw[startPos:]))
    if(isThereDE):
        endPos = re.search("[^=]==[^=]", raw[startPos:]).start()+1
        endPos += startPos
        #print("(there is at least another lang)")
        return raw[startPos:endPos]
    # english goes until end of string
    return raw[startPos:]

def getPron(raw):
    # receives the raw english string and returns the raw
    # pronunciation string
    # returns the empty string if there is no pronunciation (or
    # the formatting of the pronunciation is unorthodox)

    substr = "===Pronunciation==="
    startPos = raw.find(substr)
    if startPos == -1:
        return ""
    startPos = startPos + 19

    # it stands to reason that the pronunciation is not going to be
    # the last = * = type of structure in file
    isThereFM = bool(re.search("===", raw[startPos:]))  
    if(isThereFM):
        endPos = re.search("===", raw[startPos:]).start()
        endPos += startPos
        return raw[startPos:endPos]
    return ""

def getDfn(raw):
    # receives the raw english string and returns a list with 
    # couples of the form (class, defition string)
    # returns the empty list if there is no definition (or
    # the formatting of the definition is unorthodox)

    result = []

    classOfWords = ["Noun", "Verb", "Adjective", "Adverb", "Pronoun", 
            "Preposition", "Conjuction", "Article", "Interjection"]
    # Add "Particle" class? Perhaps later

    for cl in classOfWords:
        # when there are multiple etymologies, they may use four =,
        isFourE = False

        substr = "====" + cl + "===="
        startPos = raw.find(substr)
        if startPos != -1:
            startPos += len(substr)
            isFourE = True

        if(not isFourE):
            substr = "===" + cl + "==="
            startPos = raw.find(substr)
            if startPos == -1:
                continue
            startPos += len(substr)

        isThereE = bool(re.search("==", raw[startPos:]))   # E: equal
        if(isThereE):
            endPos = re.search("==", raw[startPos:]).start()
            endPos += startPos
            result.append((cl, raw[startPos:endPos]))
        else:
            result.append((cl , raw[startPos:]))

    return result
        

def processText(textRaw, title):

    # get english string
    englishRaw = getEnglish(textRaw)
    #print (englishRaw)

    # get pronunciation raw string
    pronRaw = getPron(englishRaw)
    #print(pronRaw)

    # get definition raw strings
    # list of couples (class, def), where class in {noun, verb, etc}
    dfnRaw = getDfn(englishRaw)
    for tpl in dfnRaw:
        if (len(tpl) != 0):
            (cl, df) = tpl
            print(title)
            print(cl)
            print("---hmm---")
            print(df)


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

