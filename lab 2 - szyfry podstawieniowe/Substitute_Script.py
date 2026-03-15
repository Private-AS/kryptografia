import string

KEY = "shrek"
FILE = "plain.txt"

def vigenere(key, text_file):
    alphabet = string.ascii_letters[:26]

    with open (text_file) as f:
        text = f.read().lower().strip()

    formated_text = ""
    for i in text:
        if ord(i) in range(ord('a'), ord('z')+1):
            formated_text += i
    #print (formated_text)

    long_key = ""
    while len(long_key) < len(formated_text):
        long_key += key
    diff = len(long_key) - len(formated_text)
    if diff > 0:
        long_key = long_key[:-diff]
    #print (long_key)

    cypher = ""
    for i in range(len(formated_text)):
        character = alphabet[( alphabet.find(formated_text[i]) + alphabet.find(long_key[i]) ) % 26]
        cypher += character
    #print(cypher)

    return cypher

output = vigenere(KEY, FILE)
print(output)