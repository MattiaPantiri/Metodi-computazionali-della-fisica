import crypto

import random

import argparse

def clean(text): #pulisce il testo da criptare da tutti i caratteri strani
    l = list(text)
    for i in range(l.count(".")):
        l.remove(".")
    for i in range(l.count(":")):
        l.remove(":")
    for i in range(l.count(",")):
        l.remove(",")
    for i in range(l.count(";")):
        l.remove(";")
    for i in range(l.count("-")):
        l.remove("-")
    for i in range(l.count("_")):
        l.remove("_")
    for i in range(l.count("'")):
        l.remove("'")
    for i in range(l.count("?")):
        l.remove("?")
    for i in range(l.count("!")):
        l.remove("!")
    for i in range(l.count('"')):
        l.remove('"')
    for i in range(l.count('(')):
        l.remove('(')
    for i in range(l.count(')')):
        l.remove(')')

    return "".join(l)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "A program which crypts a text with mono-alphabetic method")
    parser.add_argument('filename', help="Input Text (the one that needs to be crypted)", type = str)

    args = parser.parse_args()
    filename = args.filename

    file = open(filename)
    in_text = file.read()
    file.close()

    in_text = clean(in_text)
    in_text = in_text.lower()

    key = []
    alph = crypto.alphabet[:]
    for k in range(len(crypto.alphabet)):
        key.append(alph.pop(random.randint(0, len(alph) - 1)))

    crypted = crypto.crypt_mono_permutation(in_text, key)

    out = open("crypted.txt", "w")

    out.write(crypted)

    out.close()

    print("Crypted text printed in 'crypted.txt' file")
    print("Key:")
    print(key)
