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

    class_of_words = ["Noun", "Proper noun", "Verb", "Adjective", "Adverb", "Pronoun", 
            "Preposition", "Conjuction", "Article", "Interjection"]
    # Add "Particle" class? Perhaps later

    for cl in class_of_words:
        # when there are multiple etymologies, they may use four =,
        is_four_e = False

        substr = "====" + cl + "===="
        start_pos = raw.find(substr)
        if start_pos != -1:
            start_pos += len(substr)
            is_four_e = True

        if(not is_four_e):
            substr = "===" + cl + "==="
            start_pos = raw.find(substr)
            if start_pos == -1:
                continue
            start_pos += len(substr)

        is_there_e = bool(re.search("==", raw[start_pos:]))   # E: equal
        if(is_there_e):
            end_pos = re.search("==", raw[start_pos:]).start()
            end_pos += start_pos
            result.append((cl, raw[start_pos:end_pos]))
        else:
            result.append((cl , raw[start_pos:]))

    return result
