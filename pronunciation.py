import re

def cleanPron(raw):
    """Receives raw pronunciation string.
    Returns tuple (str: US IPA, str: UK IPA).
    String is empty in case IPA is not found.
    If no region is stated, returns same IPA for both"""

    strUS = ""
    strUK = "" # strings to be returned
    
    american = ["US", "GenAm", "GA"]
    british = ["UK", "RP"]

    isUS = False
    isUK = False
    res = ""
    for line in raw.splitlines():
        result = re.search(r"/[^/]*/", line)
        if (not result):
            continue
        res = result.group()

        for pat in american:
            if (line.find(pat) != -1):
                isUS = True
                strUS = res
        for pat in british:
            if (line.find(pat) != -1):
                isUK = True
                strUK = res

        if ( (not isUK) and (not isUS) ):
            strUK = res
            strUS = res

    print(strUS) 


