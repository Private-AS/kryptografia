key = [1, 1, 0, 1, 0, 0]
register = key
length = len(key)
polynomial = (6, 3, 2, 0)  # Represents x^6 + x^5 + 1
stream = ""

def lfsr_step(state, poly):
    indexes = [length - p for p in poly[:-1]]  # Calculate indexes for feedback
    feedback = 0
    for i in indexes:
        feedback ^= state[i]  # XOR the bits at the specified indexes

    return feedback


for i in range((2**6 - 1)*3):
    feedback_bit = lfsr_step(register, polynomial)
    stream += str(register[0])  # Append the output bit (first bit of the register)
    register = register[1:] + [feedback_bit]  # Shift the register and insert feedback bit at the end

print ("Stream1:", stream)


stream = stream[:35]
ones = "1" * len(stream)
print("Stream:   ", stream)
print ("Message:  ", ones)
#print(stream[:(2**6 - 1)])
#print(stream[(2**6 - 1):(2**6 - 1)*2])
#print(stream[(2**6 - 1)*2:(2**6 - 1)*3])

cypher = ""
for i in range(len(stream)):
    if stream[i] == ones[i]:
        cypher += "0"
    else:
        cypher += "1"
#because same bits give 0 and different bits give 1 in xor operation
#and we have all 1s in one variable

print("Cypher:   ", cypher)
cypher2 = cypher[:8] + str(int(not bool(cypher[8]))) + cypher[9:]  # swap the 8th bit
#print("Cypher 2: ", cypher2)

cypher3  = cypher[-1] + cypher[:-1]
print("Cypher 3: ", cypher3)

decypher = ""
for i in range(len(cypher)):
    decypher += str(int(cypher3[i]) ^ int(stream[i]))

print("Decypher3:", decypher)