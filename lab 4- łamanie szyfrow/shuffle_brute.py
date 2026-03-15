from itertools import permutations
from pprint import pprint

SIZES = [(12, 15), (10, 18), (9, 20), (6, 30), (5, 36), (4, 45), (3, 60), (2, 90)]
print (SIZES[::-1])
CYPHER = "ssyl ipiewiepst yplucts hvdt oseg  enc eeoncdsdraof wentk rry ipr ehsyhedeeamowekoaoltfoeeetrfoy ca  r uamaraely l rsynssoch pnisoeyemle c hbrhbepuri tn ytuccin  caybmtos i tia isr"

print (len(CYPHER))

def brute_force_shuffle(cypher, width, height):
    matrix = [["" for x in range(width)] for y in range(height)]
    #pprint(matrix)
    #print("\n\n")

    #Creating column list
    columns = []
    for i in range(width):
        col = ""
        for j in range(height):
            col += cypher[i*height + j]
        columns.append(col)
    print(columns, "\n", len(columns), "\n")

    output = []
    n = 0
    for perm in permutations(columns):
        if n % 1000000 == 0:
            print(f"Checked {n} permutations...")
        n += 1

        # Filling the matrix down columns
        for j in range(width):
            for i in range(height):
                matrix[i][j] = perm[j][i]
        #pprint(matrix)

        # Reading the matrix in rows
        read_rows = ""
        for i in range(height):
            for j in range(width):
                read_rows += matrix[i][j]

        if "cryptography" in read_rows:
            output.append(read_rows)
            #print("Found possible de-shuffle:\n", read_rows)

    return output

#print(brute_force_shuffle(CYPHER, 10, 18))



for size in SIZES:
    print(f"Trying size: {size}")
    result = brute_force_shuffle(CYPHER, size[0], size[1])
    print("Result: ", result)
