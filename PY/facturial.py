# Function of Facturial
def facturial(num):
    fact = 1
    for i in range(1, num+1):
        fact = fact*i
    return fact
# Function of Combinations
def Combinations(n, r):
    fact_n = facturial(n)
    fact_r = facturial(r)
    fact_n_r = facturial(n-r)
    result = fact_n / (fact_r * fact_n_r)
    return result
# Function of  Permutations
def Permutations(n, r):
    fact_n = facturial(n)
    fact_n_r = facturial(n-r)
    result = fact_n / fact_n_r
    return result

# Value Input 
n = int(input("Enetr Yor Value of n: "))
r = int(input("Enetr Yor Value of r: "))

# check Condiction 
if (n>r):
    print(Permutations(n,r))
    print(Combinations(n,r))
else:
    print("Enter Valid Input")