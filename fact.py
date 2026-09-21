import math;

def per(n,r):
    return math.factorial(n) // math.factorial(n-r)

def com(n,r):
    return math.factorial(n) // math.factorial(r) * math.factorial(n-r)

n = int(input("Enter Your Value of n : "))
r = int(input("Enter Your Value of r : "))

print("Permuntaction : ", per(n,r))
print("Combination : ", com(n,r))