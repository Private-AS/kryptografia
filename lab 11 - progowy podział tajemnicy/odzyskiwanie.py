import os
import random

with open("params.txt", "rb") as file:
    params = tuple(map(int, file.read().decode('utf-8').split(',')))
seclen = params[0]
PRIME = params[1]

if not os.path.exists("shadows"):
    exit("Folder 'shadows' does not exist.")

shadow_n = []
for i in range(3):
    random_index = random.randint(1, 5)
    while random_index in shadow_n:
        random_index = random.randint(1, 5)
    shadow_n.append(random_index)
print("Using shadows:", shadow_n)

shadows = []
for i in shadow_n:
    with open(rf"shadows\shadow{i}.txt", "rb") as file:
        shadow = tuple(map(int, file.read().decode('utf-8').split(',')))
        shadows.append(shadow)

print(shadows)

def det_3x3(matrix, prime):
    """Oblicza wyznacznik macierzy 3×3 modulo prime"""
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]

    det = (a * (e * i - f * h) -
           b * (d * i - f * g) +
           c * (d * h - e * g)) % prime
    return det

# Macierz A i wektor b
A_matrix = []
b_vector = []
for x, y in shadows:
    A_matrix.append([pow(x, 2, PRIME), x % PRIME, 1])
    b_vector.append(y % PRIME)

# Wyznacznik główny
det_A = det_3x3(A_matrix, PRIME)
if det_A == 0:
    raise ValueError("Wyznacznik = 0, układ nierozwiązywalny")

det_A_inv = pow(det_A, -1, PRIME)

# Wzory Cramera
results = []
for i in range(3):
    # Kopia macierzy z i-tą kolumną zamienioną na b
    A_i = [row[:] for row in A_matrix]
    for j in range(3):
        A_i[j][i] = b_vector[j]

    det_A_i = det_3x3(A_i, PRIME)
    x_i = (det_A_i * det_A_inv) % PRIME
    results.append(x_i)

a, b, c = results
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")

# Odtwórz wiadomość
number_str = str(a) + str(b) + str(c)
number = int(number_str)
recovered_bytes = number.to_bytes(seclen, byteorder='big')

with open("odzyskana_tajemnica.txt", "wb") as file:
    file.write(recovered_bytes)

print("\nRecovered message:")
print(recovered_bytes.decode('utf-8', errors='ignore'))