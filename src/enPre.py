import re
import string
def getEnglish(raw):
    """If no English part in text, returns empty string
    otherwise, returns string with raw english."""

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
    """Receives the raw english string and returns the raw
    pronunciation string.
    Returns the empty string if there is no pronunciation (or
    the formatting of the pronunciation is unorthodox)."""

    # when there are multiple etymologies, they may use four =,
    isFourE = False

    substr = "====Pronunciation===="
    startPos = raw.find(substr)
    if startPos != -1:
        startPos += len(substr)
        isFourE = True

    if (not isFourE):
        substr = "===Pronunciation==="
        startPos = raw.find(substr)
        if startPos == -1:
            return ""
        startPos += len(substr)

    # it stands to reason that the pronunciation is not going to be
    # the last = * = type of structure in file
    isThereFM = bool(re.search("===", raw[startPos:]))  
    if(isThereFM):
        endPos = re.search("===", raw[startPos:]).start()
        endPos += startPos
        return raw[startPos:endPos]
    return ""

def getDfn(raw):
    """Receives the raw english string and returns a list with 
    couples of the form (class, defition string).
    Returns the empty list if there is no definition (or
    the formatting of the definition is unorthodox)."""

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

