from Shuffle_Script import find_min_square

def de_spiral_shuffle(cypher, directions="LTC", width=0, height=0):

    #If matrix size is not input, create the smallest square matrix to fit the text
    if width == 0 and height == 0:
        width = find_min_square((len(cypher)))
        #The online tool only uses odd sized square matrixes for some reason, so i'll do the same to match the output
        if width % 2 == 0:
            width += 1
        height = width
    #print(width, height)

    #Checking if params are correct
    if len(cypher) > width * height:
        raise ValueError(f"Cypher is too long ({len(cypher)}) to fit in a {width}x{height}={width * height} grid")

    dir_err = f"Direction must be in following format: [L|R][T|D][C|A] eg. LTC - left top clockwise. Your direction is {directions}"

    if directions[0] != "L" and directions[0] != "R":
        raise ValueError (dir_err)

    if directions[1] != "T" and directions[1] != "D":
        raise ValueError(dir_err)

    if directions[2] != "C" and directions[2] != "A":
        raise ValueError(dir_err)


    #Setting up helper variables
    if directions[2] == "C":
        dirs = ["R", "D", "L", "U"]
    elif directions[2] == "A":
        dirs = ["D", "R", "U", "L"]

    #print(directions[:2])
    #print(directions[2])

    if directions[:2] == "LT":
        start_dir = 0

    elif directions[:2] == "LD":
        if directions[2] == "C":
            start_dir = 3
        else:
            start_dir = 1

    elif directions[:2] == "RT":
        if directions[2] == "C":
            start_dir = 1
        else:
            start_dir = 3

    elif directions[:2] == "RD":
        start_dir = 2

    dims = [width, height]

    if dirs[start_dir] == "R" or dirs[start_dir] == "L":
        start_dim = 0
    else:
        start_dim = 1


    #print(dirs)
    #print(start_dir)

    #Enlongating text to fill the matrix
    for i in range (width*height - len(cypher)):
        cypher += " " #spacja zamiast x zeby porownac z webowym narzedziem
    #print (text)

    #creating empty matrix
    matrix = [["" for x in range(width)] for y in range(height)]
    #pp.pprint(matrix)

    x=0
    while x < len(cypher):
        for i in range(height):
            for j in range(width):
                matrix[i][j] = cypher[x]
                x += 1


    # Reading the matrix in spiral
    i = 0
    offset = 0
    end = 0
    dim = start_dim
    x= 0
    result = ""
    while x < len(cypher):

        #print(f"Offset: {offset}, End: {end}, i: {i}, Dim: {dim}, Start_dir: {start_dir}")
        #TODO: Only works for LTC for some reason

        if dirs[start_dir] == "R":
            for j in range (offset, dims[dim]-end):
                result += matrix[offset][j]
                x += 1
        elif dirs[start_dir] == "L":
            for j in range (offset, dims[dim]-end):
                result += matrix[dims[1] - offset][dims[0]-1 - j]
                x += 1
        elif dirs[start_dir] == "D":
            for j in range (offset, dims[dim]-end):
                result += matrix[j][dims[0] - offset]
                x += 1
        elif dirs[start_dir] == "U":
            for j in range (offset, dims[dim]-end):
                result += matrix[dims[1]-1 - j][offset-1]
                x += 1

        #pp.pprint(matrix)

        if i % 4 == 0:
            offset += 1
        if (i+2) %4 == 0:
            end += 1
        dim = (dim + 1) % 2
        start_dir = (start_dir + 1) % 4
        i += 1

    #print()
    #pp.pprint(matrix)

    return result

with open("shuffle_proprietary.txt") as f:
    print(de_spiral_shuffle(f.read().strip()))


TEXT = "ssyl ipiewiepst yplucts hvdt oseg  enc eeoncdsdraof wentk rry ipr ehsyhedeeamowekoaoltfoeeetrfoy ca  r uamaraely l rsynssoch pnisoeyemle c hbrhbepuri tn ytuccin  caybmtos i tia isr"

print("\n\n")
print(de_spiral_shuffle(TEXT, directions="LTC", width=14, height=14))