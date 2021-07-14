dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
        'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15,
        'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23,
        'y': 24, 'z': 25, ' ': 26}

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', ' ']

bigraphs = ["th", "er", "on", "an", "re", "he", "in", "ed", "nd", "ha", "at", "en", "es", "of", "or", "nt", "ea", "ti", "to", "it",
            "st", "io", "le", "is", "ou", "ar", "as", "de", "rt", "ve"]

trigraphs = ["the", "and", "tha", "ent", "ion", "tio", "for", "nde", "has", "nce", "edt", "tis", "oft", "sth", "men"]

word1 = [" a "]

word2 = [" of ", " to ", " in ", " it ", " is ", " be ", " as ", " at ", " so ", " we ", " he ", " by ",
        " or ", " on ", " do ", " if ", " me ", " my ", " up ", " an ", " go ", " no ", " us ", " am "]

word3 = [" the ", " and ", " for ", " are ", " but ", " not ", " you ", " all ", " any ", " can ", " had ", " her ",
        " was ", " one ", " our ", " out ", " day ", " get ", " has ", " him ", " his ", " how ", " man ", " new ",
        " now ", " old ", " see ", " two ", " way ", " who ", " boy ", " did ", " its ", " let ", " put ", " say ",
        " she ", " too ", " use "]

word4 = [" that ", " with ", " have ", " this ", " will ", " your ", " from ", " they ", " know ",
        " want ", " been ", " good ", " much ", " some ", " time "]

doubles = ["ss", "ee", "tt", "ff", "ll", "mm", "oo"]

def crypt_mono_shift(string, n):

    """Fa la crittografia di un testo spostando di n posti in avanti nell'alfabeto ogni lettera del testo"""

    l = list(string)
    out = []

    for i in l:
        out.append(alphabet[dict.get(i) - (27-n)])

    return "".join(out)


def decrypt_mono_shift(string, n):

    """Trova il testo originale dato un testo crittografato con crypt_mono_shift(string, n)"""

    l = list(string)
    out = []

    for i in l:
        out.append(alphabet[dict.get(i) - n])

    return "".join(out)



def crypt_mono_permutation(string, key):

    """Fa la crittografia di un testo costruendo una mappa 1 a 1 tra le lettere dell'alfabeto nell'ordine vero
    e le lettere nell'ordine in cui appaiono in key, che è una permutazione dell'alfabeto"""

    l = list(string)
    out = []
    d = {}

    for i in range(len(key)):
        d.update({alphabet[i]: key[i]})

    for i in l:
        out.append(d.get(i))

    return "".join(out)


def decrypt_mono_permutation(string, key):

    """Trova il testo originale dato un testo crittografato con crypt_mono_permutation(string, key)"""

    l = list(string)
    out = []
    d = {}

    for i in range(len(key)):
        d.update({key[i]: alphabet[i]})

    for i in l:
        out.append(d.get(i))

    return "".join(out)


def crypt_poli(string, keyword):

    """Data una parola chiave la ripete per tutta la lunghezza del testo originale, e restituisce un
    testo crittografato in cui ogni lettera è ottenuta sommando le posizioni (nell'alfabeto) delle lettere
    nel testo originale con le posizioni delle corrispondenti lettere nella stringa ottenuta dalla parola chiave"""

    l = list(string)
    out = []
    word = list(keyword)
    for i in range(word.count("-")):
        word.remove("-")
    counter = 0
    key = []

    for i in range(len(l)):
        key.append(word[counter])
        counter += 1
        if counter == len(word):
            counter = 0

    for i in range(len(l)):
        out.append(alphabet[dict.get(l[i]) - (27 - dict.get(key[i]))])

    return "".join(out)


def decrypt_poli(string, keyword):

    """Trova il testo originale dato un testo crittografato con crypt_poli(string, keyword)"""

    l = list(string)
    out = []
    word = list(keyword)
    for i in range(word.count("-")):
        word.remove("-")
    counter = 0
    key = []

    for i in range(len(l)):
        key.append(word[counter])
        counter += 1
        if counter == len(word):
            counter = 0

    for i in range(len(l)):
        out.append(alphabet[dict.get(l[i]) -  dict.get(key[i])])

    return "".join(out)
