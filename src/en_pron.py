import re

def clean_pron(raw):
    """Receives raw pronunciation string.
    Returns list of tuples (str: Region, str: IPA, str: ogg add).
    String is empty in case IPA is not found.
    If no region is stated, returns same IPA for both"""

    strUS = ""
    strUK = "" # strings to be returned
    
    american = ["US", "GenAm", "GA"]
    british = ["UK", "RP"]

    isUS = False
    isUK = False
    are_both_same = False
    res = ""
    for line in raw.splitlines():
        result = re.search(r"/[^/]*/", line)
        if not result:
            continue
        res = result.group()

        for pat in american:
            if (line.find(pat) != -1 and isUS == False):
                # select only first
                isUS = True
                strUS = res
        for pat in british:
            if (line.find(pat) != -1 and isUK == False):
                # select only first
                isUK = True
                strUK = res

        if ( (not isUK) and (not isUS) ):
            strUK = res
            strUS = res
            are_both_same = True

    strUS = strUS.strip()
    strUK = strUK.strip()
   
    """ # for debugging
    if(len(strUS) != 0):
        print("US: " + strUS) 
    if(len(strUK) != 0):
        print("UK: " + strUK)
    if(len(strUS) != 0 or len(strUK) != 0):
        print()
    """
    res = []
    if(isUS or are_both_same):
        res.append(("US", strUS, ""))
    if(isUK or are_both_same):
        res.append(("UK", strUK, ""))

    return res
