import string
from Substitute_Script import vigenere

KEY = "shrek"
FILE = "substitute_proprietary.txt"

def de_vigenere(key, cypher_file):
    alphabet = string.ascii_letters[:26]

    with open (cypher_file) as f:
        cypher = f.read().lower().strip()
    #print(cypher)

    formated_cypher = ""
    for i in cypher:
        if ord(i) in range(ord('a'), ord('z')+1):
            formated_cypher += i
    #print (formated_cypher)

    long_key = ""
    while len(long_key) < len(formated_cypher):
        long_key += key
    diff = len(long_key) - len(formated_cypher)
    if diff > 0:
        long_key = long_key[:-diff]
    #print (long_key)

    plain_text = ""
    for i in range(len(formated_cypher)):
        character = alphabet[( alphabet.find(formated_cypher[i]) - alphabet.find(long_key[i]) ) % 26]
        plain_text += character
    #print(plain_text)

    return plain_text

output = de_vigenere(KEY, FILE)
print(output)

def de_vigenere2(key, cypher_file):
    key = key.lower()
    anti_key = ""
    for i in key:
        j = (26 - (ord(i) - 97)) % 26
        anti_key += chr(j + 97)

    #print(anti_key)

    return vigenere(anti_key, cypher_file)

print (de_vigenere2(KEY, FILE))