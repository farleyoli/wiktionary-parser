import re

def get_head(raw):
    # TODO
    return ""

def count_sharp(line):
    """Returns the number of initial sharps in the string."""
    result = 0
    for c in line:
        if c != "#":
            return result
        result += 1
    return result

def is_example(line):
    """Receives line string (possibly with initial sharps), and 
    returns true iff it is an example sentence.
    """
    line = line.strip()
    line = line.strip("#")
    if "ux" not in line:
        return False
    if line[0] == ":":
        return True
    return False

def is_quote(line):
    """Receives line string (possibly with initial sharps), and 
    returns true iff it is a quote sentence.
    """
    line = line.strip()
    line = line.strip("#")
    if line[0] == "*":
        return True
    return False

def is_definition(line):
    """Returns true iff line string (eventually without #s) represents a definition."""
    if is_example(line) or is_quote(line):
        return False
    if count_sharp(line) == 0:
        return False
    line = line.strip()
    line = line.strip("#")
    if line[0] == "*" or line[0] == ":":
        return False
    return True


def sub_bracket_content(line, fn):
    """The method fn receives a list of strings and returns a string.
    This method works by passing the elements of each {{x1|x2|...}} as a list
    to fn and substituting {{x1|x2|...}} with the output of fn in 
    line (and returning it).
    """
    def is_in_interval(i, lst):
        for (x,y) in lst:
            if i >= x and i < y:
                return True
        return False

    def get_interval(i, lst):
        for (x,y) in lst:
            if i>= x and i < y:
                return (x,y)
        return -1

    retv = "" # return value
    pattern = re.compile('{{[^{}]*}}')
    iterator = pattern.finditer(line)
    match_positions = []
    initial_positions = []

    for match in iterator:
        match_positions.append(match.span())
        initial_positions.append(match.span()[0])

    for i, c in enumerate(line):
        if i in initial_positions:
            x,y = get_interval(i, match_positions)
            retv +=  fn( line[x+2:y-2].split("|") ) 
        if is_in_interval(i, match_positions):
            continue
        retv += c

    return retv
    
def clean_html(line):
    """Appropriately cleans up html present in line, according to the tags.
    This is a provisory and rudimentary method and it is probably breaking
    something."""

    todebug = ""
    
    # html comments
    line = re.sub(r"<!--[^<>]*-->", todebug, line)

    # we delete inner content here
    tags = [r"ref"]
    for tag in tags:
        line = re.sub(r"<" + tag + r"[^<>]*>[^<>]*</" + tag + r">", todebug, line)
        line = re.sub(r"<" + tag + r"[^<>]*/>", todebug, line)
   
    # we only delete the tag here
    # self-closing tag
    tags = [r"sup", r"sub", r"i"]
    for tag in tags:
        line = re.sub(r"<[^<>]*" + tag + r"[^<>]*>", todebug, line)

    return line


def clean_common(line):
    """Common pre-processing to clean definition and example lines."""
    line = line.strip()
    line = line.strip("#")

    if len(line) == 0:
        return line

    line = clean_html(line)

    # eliminate patterns not needed
    patterns = ["[[","]]", "'''", "''"]
    for pattern in patterns:
        line = line.replace(pattern, "")

    return line

    # strip html

def clean_dfn_line(line):
    # TODO
    line = clean_common(line)
    return line

def clean_exm_line(line):
    # TODO
    line = clean_common(line)
    return line

def get_idx_of_elems_of_lst(i, no_shs, category):
    """Returns a list with the (ordered) indexes of the contents parallel to no_shs[i].
    (ie, elements which will be in the same dfn list and not nested deeper in other dfns)
    """
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
    """Returns the raw string (assumed to be a unique line),
    but without lines that do not start with a #.
    """
    result = ""
    for line in raw.splitlines():
        if len(line) == 0 or line[0] != "#":
            continue
        result += line.strip() + "\n"
    return result

def get_examples(i, no_shs, category, lines):
    """ Returns a list with examples relative to no_shs[i]. Returns the empty
    list if no_shs[i] is not a definition.
    """
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

def get_dfn (lines, no_shs, category):
    """Returns the root dfn obtained from lines."""
    def fill_dfn (i, lines, no_shs, dfn):
        idx_of_elems = get_idx_of_elems_of_lst(i, no_shs, category)
        #print (idx_of_elems)
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
                fill_dfn(j+1, lines, no_shs, new_dfn)

    dfn = []
    fill_dfn (0, lines, no_shs, dfn) 
    return dfn

def get_category(line):
    """Returns "dfn" if line is a definition,
               "exm" if line is an example, and
               "quo" is line is a quote.
    """
    if is_example(line):
        return "exm"
    elif is_quote(line):
        return "quo"
    elif is_definition(line):
        return "dfn"
    return ""  # unkown category

def clean_dfn(raw):
    """Returns {head, dfn}, where
               dfn = (list of {content, dfn}) or []
           content = {explanation, examples, quotes}
          examples = list of examples (str)
    and     quotes = list of quotes (str) (to do later)
    see definition of head. (ex: head(tested) = test)
    """

    head = get_head(raw)

    nohead = delete_nosharp(raw)
    #print(nohead)

    lines = nohead.splitlines()

    # I really should put the below in a function...
    no_shs = list(map(count_sharp, lines))
    category = list(map(get_category, lines))
    #category = list(filter(None.__ne__, category)) 


    # write recursive function
    dfn = get_dfn(lines, no_shs, category)
    print(dfn)

    return "hue"

