import numpy as np

def def_integrate(func,a,b):
    ans=0
    ep=0.000001
    while(a<b):
        ans=ans+ep*((func(a)+func(a+ep))/2)
        a=a+ep
    return ans


def diff(func,x):
    ep=0.00001
    return (func(x+ep)-func(x))/ep