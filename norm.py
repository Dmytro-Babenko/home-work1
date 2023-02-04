import re
def normalize(TRANS: dict, word: str) -> str:
    '''
    Сhecks if the string contains non-Latin letters or non-digits.
    Replace each character in the string using the given translitaration table.
    Then replace all characters in the string by _, exept latin and didgits. 
    '''
    if re.match(r'\b\w\b', word) is not None:
        return word

    name_translitarate = word.translate(TRANS)
    normalized_word = re.sub(r'\W', '_', name_translitarate) 
    return normalized_word