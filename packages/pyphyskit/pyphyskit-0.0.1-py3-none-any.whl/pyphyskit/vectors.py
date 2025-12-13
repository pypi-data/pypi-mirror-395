import math

def magnitude(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

def dot(v1, v2):
    return sum(a*b for a,b in zip(v1, v2))

def cross(v1, v2):
    return (
        v1[1]*v2[2]-v1[2]*v2[1],
        v1[2]*v2[0]-v1[0]*v2[2],
        v1[0]*v2[1]-v1[1]*v2[0]
    )
