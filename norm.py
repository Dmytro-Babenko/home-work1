import re
def make_translitarate_table() -> dict:
    '''Make translitarate table from cyrillic to latin'''
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", 
        "i", "j", "k", "l", "m", "n", "o", "p", "r", 
        "s", "t", "u","f", "h", "ts", "ch", "sh", "sch", 
        "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
        )
    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    return TRANS

TRANS = make_translitarate_table()

def normalize(word: str, TRANS = TRANS) -> str:
    '''
    Сhecks if the string contains non-Latin letters or non-digits.
    Replace each character in the string using the given translitaration table.
    Then replace all characters in the string by _, exept latin and didgits. 
    '''
    if re.match(r'^\w+$', word) is not None:
        return word

    name_translitarate = word.translate(TRANS)
    normalized_word = re.sub(r'\W', '_', name_translitarate) 
    return normalized_word