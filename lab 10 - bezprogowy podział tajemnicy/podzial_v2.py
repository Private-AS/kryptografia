import os

with open("tajemnica.txt", "rb") as file:
    content_bin = file.read()

keylen = len(content_bin)

shadow1 = os.urandom(keylen)
shadow2 = os.urandom(keylen)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

shadow3 = xor_bytes(xor_bytes(shadow1, content_bin), shadow2)
if not os.path.exists("shadows"):
    os.mkdir(r"shadows")
with open(r"shadows\shadow1.txt", "wb") as file:
    file.write(shadow1.hex().encode('utf-8'))
with open(r"shadows\shadow2.txt", "wb") as file:
    file.write(shadow2.hex().encode('utf-8'))
with open(r"shadows\shadow3.txt", "wb") as file:
    file.write(shadow3.hex().encode('utf-8'))


print("shadow1 =", shadow1.hex())
print("shadow2 =", shadow2.hex())
print("shadow3 =", shadow3.hex())
