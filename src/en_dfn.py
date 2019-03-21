def get_head(raw):
    # TODO
    return ""

def count_sharp(line):
    """Receives a string, and returns
    the number of initial sharps in the string,
    """
    result = 0
    for c in line:
        if c != "#":
            return result
        result += 1
    return result

def is_example(line):
    """Receives a string (possibly with initial sharps), and 
    returns true iff it is an example sentence."""
    line = line.strip()
    line = line.strip("#")
    if "ux" not in line:
        return False
    if line[0] == ":":
        return True
    return False

def is_quote(line):
    """Receives a string (possibly with initial sharps), and 
    returns true iff it is an quote sentence."""
    line = line.strip()
    line = line.strip("#")
    if line[0] == "*":
        return True
    return False

def is_definition(line):
    if is_example(line) or is_quote(line):
        return False
    if count_sharp(line) == 0:
        return False
    line = line.strip()
    line = line.strip("#")
    if line[0] == "*" or line[0] == ":":
        return False
    return True

def clean_dfn_line(line):
    # TODO
    return line

def clean_exm_line(line):
    # TODO
    return line

def get_idx_of_elems_of_lst(i, no_shs, category):
    """Receives an index i, a list with the number of sharps of each line and 
    a list with the category (definition, quote, example or other) of each line
    and returns a list with pairs: the (ordered) indexes of the parallel contents 
    (ie, elements which will be in the same dfn list and not nested deeper in
     other dfns); """
    ans = []

    if len(category) == 0 or category[i] != "dfn": # is not definition, so list is empty
        return []

    n = len(no_shs)
    for j in range(i, n):
        if no_shs[j] < no_shs[i]:
            break
        if no_shs[j] == no_shs[i]:
            if category[j] == "dfn":
                ans.append(j)

    return ans
        
def delete_nosharp(raw):
    """Receives string with text and returns the same string,
    but without lines that do not start with a #"""
    result = ""
    for line in raw.splitlines():
        if len(line) == 0 or line[0] != "#":
            continue
        result += line.strip() + "\n"
    return result

def get_examples(i, no_shs, category, lines):
    """Receives index i, no_shs and array with categories, and returns
    a list with index of examples relative to no_shs[1]. Returns the empty
    list if no_shs[i] is not a definition."""
    if category[i] != "dfn":
        return []
    ans = []
    n = len(no_shs)
    for j in range(i+1, n):
        if category[j] == "quo":
            continue
        elif category[j] == "exm":
            ans.append(j)
        else: 
            break
    examples_idx = ans
    examples = []
    if len(examples_idx) > 0:
        examples = [clean_exm_line(lines[k]) for k in examples_idx]
    else:
        examples = []
    return examples

def fill_dfn (lines, no_shs, dfn, category):

    def fill_dfn_aux (i, lines, no_shs, dfn):
        idx_of_elems = get_idx_of_elems_of_lst(i, no_shs, category)
        print (idx_of_elems)
        for j in idx_of_elems: # idx_of_elems can't be zero
            content = clean_dfn_line(lines[j][no_shs[j]:])
            examples = get_examples(j, no_shs, category, lines)
            #if len(examples_idx) > 0:
            #    examples = [clean_exm_line(lines[k]) for k in examples_idx]
            #else:
            #    examples = []
            new_dfn = []
            obj = {"c" : content, "d" : new_dfn, "e" : examples, "q": []}
            dfn.append(obj)
            if j != len(no_shs) - 1 and no_shs[j+1] > no_shs[j]:
                fill_dfn_aux(j+1, lines, no_shs, new_dfn)

    fill_dfn_aux (0, lines, no_shs, dfn) 

def get_category(line):
    """Returns "dfn" if line is a definition,
               "exm" if line is an example, and
               "quo" is line is a quote."""
    if is_example(line):
        return "exm"
    elif is_quote(line):
        return "quo"
    elif is_definition(line):
        return "dfn"
    return ""  # unkown category

def clean_dfn(raw):
    """Returns {head, dfn},
               dfn = (list of {content, dfn}) or []
           content = {explanation, examples}
          examples = list of examples (str)
    and     quotes = list of quotes (str) (to do later)
    see definition of head (ex: head(tested) = test)"""

    head = get_head(raw)

    nohead = delete_nosharp(raw)
    #print(nohead)

    lines = nohead.splitlines()

    # I really should put the below in a function...
    no_shs = list(map(count_sharp, lines))
    category = list(map(get_category, lines))
    #category = list(filter(None.__ne__, category)) 


    print(no_shs)
    print(category)
    
    dfn = []
    # write recursive function
    fill_dfn(lines, no_shs, dfn, category)
    print(dfn)

    return "hue"

