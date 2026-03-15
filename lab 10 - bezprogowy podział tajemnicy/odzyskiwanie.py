import os
import sys

if not os.path.exists("shadows"):
    exit( "Folder 'shadows' does not exist.")

with open(r"shadows\shadow1.txt", "rb") as file:
    shadow1 = bytes.fromhex(file.read().decode('utf-8'))
with open(r"shadows\shadow2.txt", "rb") as file:
    shadow2 = bytes.fromhex(file.read().decode('utf-8'))
with open(r"shadows\shadow3.txt", "rb") as file:
    shadow3 = bytes.fromhex(file.read().decode('utf-8'))



def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

message = xor_bytes(xor_bytes(shadow1, shadow2), shadow3)

print("Recovered message:")
print(message.decode('utf-8'))
