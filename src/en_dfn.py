def get_head(raw):
    # TODO
    return ""

def count_sharp(line):
    """Receives a line, and returns
    the number of initial sharps in the line"""
    result = 0
    for c in line:
        if c != "#":
            return result
        result += 1
    return result

def clean_dfn_line(line):
    # TODO
    return line

def get_idx_of_elems_of_lst(i, no_shs):
    """Receives a index i and list with number of sharps
    and returns a list with the (ordered) indexes of the paralel elements
    (ie, elements which will be in the same dfn list and not nested deeper in
     other dfns)."""
    ans = []
    n = len(no_shs)
    for j in range(i, n):
        if no_shs[j] < no_shs[i]:
            break
        if no_shs[j] == no_shs[i]:
            ans.append(j)

    return ans
        
def delete_nosharp(raw):
    """receives string with text and returns same string,
    but without lines that do not start with a #"""
    result = ""
    for line in raw.splitlines():
        if len(line) == 0 or line[0] != "#":
            continue
        result += line.strip() + "\n"
    return result

def fill_dfn (lines, no_shs, dfn):
    def fill_dfn_aux (i, lines, no_shs, dfn):
        idx_of_elems = get_idx_of_elems_of_lst(i, no_shs)
#        if len(idx_of_elems) == 1:
#           content = clean_dfn_line(lines[i][no_shs[i]:])
#           obj = {"content" : content, "dfn": []}
#           dfn.append(obj)
#           return None
            
        for j in idx_of_elems: # idx_of_elems can't be zero
            content = clean_dfn_line(lines[j][no_shs[j]:])
            new_dfn = []
            obj = {"content" : content, "dfn" : new_dfn}
            dfn.append(obj)
            if j != len(no_shs) - 1 and no_shs[j+1] > no_shs[j]:
                fill_dfn_aux(j+1, lines, no_shs, new_dfn)

    fill_dfn_aux (0, lines, no_shs, dfn) 

def clean_dfn(raw):
    """Returns {head, dfn},
               dfn = (list of {content, dfn}) or []
           content = {explanation, examples}
    and   examples = list of examples (str)
    see definition of head (ex: head(tested) = test)"""

    head = get_head(raw)

    nohead = delete_nosharp(raw)
    #print(nohead)

    lst = []

    lines = nohead.splitlines()
    no_shs = list(map(count_sharp, lines))

    print(no_shs)
    #print(get_idx_of_elems_of_lst(0, no_shs))
    #print("----")
    
    dfn = []
    # write recursive function
    fill_dfn(lines, no_shs, dfn)
    print(dfn)

    return "hue"

