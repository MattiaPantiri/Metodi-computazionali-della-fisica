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
    parser = argparse.ArgumentParser(description= "A program which crypts a text with poli-alphabetic method")
    parser.add_argument('filename', help="Input Text (the one that needs to be crypted)", type = str)
    parser.add_argument('key_length', help="Key Length (from 4 to 15)", type = int)

    args = parser.parse_args()
    filename = args.filename
    key_length = args.key_length

    file = open(filename)
    in_text = file.read()
    file.close()

    in_text = clean(in_text)
    in_text = in_text.lower()

    keyword = []
    for k in range(key_length):
        keyword.append(crypto.alphabet[random.randint(0, len(crypto.alphabet) - 1)])

    crypted = crypto.crypt_poli(in_text, keyword)

    out = open("crypted.txt", "w")

    out.write(crypted)

    out.close()

    print("Crypted text printed in 'crypted.txt' file")
    print("Key:")
    print(keyword)
