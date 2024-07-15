from unicodedata import normalize

def remove_varios_espacos(txt):
    array = txt.split()
    return " ".join(array).strip()

def remove_acentos(txt):
    if not txt:
        return txt
    text = str((normalize('NFKD', txt).encode("ascii",errors="ignore")).decode("utf-8",errors="ignore"))
    return text.replace("'","").replace('"',"")