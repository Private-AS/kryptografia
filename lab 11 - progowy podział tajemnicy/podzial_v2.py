import os

#secret = int(str(a) + str(b) + str(c))
#3 out of 5 shadows needed to reconstruct the secret

# M607 Mersenne Prime
PRIME = 2 ** 607 - 1

with open("tajemnica.txt", "rb") as file:
    content_bin = file.read()
#print(content_bin)
seclen= len(content_bin)
number = int.from_bytes(content_bin, byteorder='big')

with open("params.txt", "wb") as file:
    file.write(f"{seclen},{PRIME}\n".encode('utf-8'))

if PRIME > number:
    print("PRIME is greater than number. All is well.")
else:
    print("PRIME is NOT greater than number. Problem!")
    exit(-1)

#print("number =", number)
number_str = str(number)
param_len = len(number_str) // 3
#print("number_len =", len(number_str))
#print("param_len =", param_len)

a = int(number_str[0:param_len])
b = int(number_str[param_len:2*param_len])
c = int(number_str[2*param_len:])

#print(number)
#print(str(a) + str(b) + str(c))
if not os.path.exists("shadows"):
    os.mkdir(r"shadows")
shadows = []
for i in range (1, 6):
    shadow = (i, (a*i*i  + b*i + c) % PRIME)
    shadows.append(shadow)
    with open(rf"shadows\shadow{i}.txt", "wb") as file:
        file.write(f"{shadow[0]},{shadow[1]}".encode('utf-8'))

print(shadows)