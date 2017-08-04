import math

def similarity(vec1, vec2):
    def pitagoras(vec):
        total = 0 
        for d in vec:
            total = total + (d*d)
        return math.sqrt(total)
    vector_norm = 0 
    for i in range(len(vec1)):
        vector_norm = vector_norm + (vec1[i]*vec2[i])
    vector_prod = pitagoras(vec1) * pitagoras(vec2)
    return vector_norm / vector_prod


print(similarity([1], [17.42]))
