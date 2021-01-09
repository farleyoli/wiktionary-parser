import re
import string
def get_english(raw):
    """If there is no English part in the Wiktionary entry,
    returns empty string. Otherwise, returns string with raw english.
    """

    substr = "==English=="
    start_pos = raw.find(substr)
    if start_pos == -1:
        return ""
    start_pos = start_pos + 11

    p = re.search(r"[^=]==[a-zA-Z]+==[^=]", raw[start_pos:])
    if p is None:
        end_pos = -1
    else:
        end_pos = p.start()
    if end_pos != -1:
        end_pos = end_pos + start_pos
    #print("start_pos = " + str(start_pos) + ", end_pos = " + str(end_pos))
    #print(raw[start_pos:end_pos])
    return raw[start_pos:end_pos]

def get_pron(raw):
    """Receives the raw english string and returns the raw pronunciation
    string. Returns the empty string if there is no pronunciation
    (or the formatting of the pronunciation is unorthodox).
    """

    m = re.search(r"=+Pronunciation=+", raw)
    if m is None:
        return ""

    beg = int(m.start())
    end = int(m.end())
    start_pos = end
    #print(raw[beg:end])
    new_raw = raw[end:]
    no_equal = (len(raw[beg:end]) - len("Pronunciation"))/2

    p_bef = p_aft = r'=' * no_equal

    m = re.search(r"[^=]"+ p_bef + r"[a-zA-Z\s0-9]+" + p_aft + r"[^=]", new_raw)
    if m is None:
        end_pos = -1
    else:
        end_pos = m.start()
    if end_pos != -1:
        end_pos = end_pos + start_pos

    #print(raw[start_pos:end_pos])
    return raw[start_pos:end_pos]


def get_dfn(raw):
    """Receives the raw english string and returns a list with
    pairs of the form (class, defition string).
    Returns the empty list if there is no definition (or
    the formatting of the definition is unorthodox).
    """

    result = []

    class_of_words = ["Noun", "Proper noun", "Verb", "Adjective", "Adverb",
                      "Pronoun", "Preposition", "Conjuction", "Article",
                      "Interjection"]

    re_group = "=+(" + "|".join(class_of_words) + ")=+"

    p = re.compile(re_group)

    matches = p.finditer(raw)

    for m in matches:
        word = raw[m.start():m.end()]
        no_equals = 0
        for letter in word:
            if letter == "=":
                no_equals += 1
        idt = no_equals / 2
        sub_p = r"[^=]={1," + str(idt) + r"}[a-zA-Z0-9\s]+={1," + str(idt) + r"}[^=]"
        sub_m = re.search(sub_p, raw[m.end():])
        if sub_m is None:
            end_pos = -1
        else:
            end_pos = m.end() + sub_m.start()
        result.append((word.strip("="), raw[m.end():end_pos]))

    return result
