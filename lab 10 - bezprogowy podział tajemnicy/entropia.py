import math
from collections import Counter


with open("tajemnica.txt", "rb") as file:
    content_bin = file.read()
with open(r"shadows\shadow1.txt", "rb") as file:
    shadow1 = bytes.fromhex(file.read().decode('utf-8'))
with open(r"shadows\shadow2.txt", "rb") as file:
    shadow2 = bytes.fromhex(file.read().decode('utf-8'))
with open(r"shadows\shadow3.txt", "rb") as file:
    shadow3 = bytes.fromhex(file.read().decode('utf-8'))

def entropy_polish(text: str) -> float:
    alphabet = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż "
    if not text:
        return 0.0
    text = text.lower()
    text = ''.join(ch for ch in text if ch in alphabet)
    counts = Counter(text)
    N = sum(counts.values())
    H = 0.0
    for ch, c in counts.items():
        p = c / N
        H -= p * math.log2(p)
    return H

def entropy_binary(data_bytes):
    bits = ''.join(f'{b:08b}' for b in data_bytes)
    counts = Counter(bits)  # '0' i '1'
    #print(counts)
    N = len(bits)
    H = 0.0
    for bit, c in counts.items():
        p = c / N
        H -= p * math.log2(p)
    return H

print("Entropia tajemnicy = ", entropy_polish(content_bin.decode("utf-8")), "bits/char")
print("Entropia tajemnicy binarnie = ", entropy_binary(content_bin), "bits/bit")
print("Entropia cienia 1 = ", entropy_binary(shadow1), "bits/bit")
print("Entropia cienia 2 = ", entropy_binary(shadow2), "bits/bit")
print("Entropia cienia 3 = ", entropy_binary(shadow3), "bits/bit")