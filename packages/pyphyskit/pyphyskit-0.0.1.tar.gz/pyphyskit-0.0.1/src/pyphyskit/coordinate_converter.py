import math 

def spherical(x,y,z):
    r=math.sqrt(x**2+y**2+z**2)
    theta=0.0
    if r!=0:
        theta=math.acos(z/r)
    phi=math.atan2(y,x)
    return r,theta,phi

def cylindrical(x,y,z):
    rho=math.sqrt(x**2+y**2)
    phi = math.atan2(y, x)
    return rho,phi,z

def sph_to_cart(r,theta,phi):
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    return x,y,z
def cly_to_cart(rho,phi,z):
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return x,y,z
