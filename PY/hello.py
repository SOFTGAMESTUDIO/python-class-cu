# Function to Prime No.
def prime(n):
    # Check No. is grater then 2
    if n < 2:
        return False
    # Check no. Will be divisible by 2 to sqrt(n) or not
    for i in range(2, int(n ** 0.5) + 1):
        # Check the no. is divisible by i or not
        if n % i == 0:
            return False
    return True

# print the twin primes less than 1000
print(f"Twin primes less than 1000 are:")

# loop to iterate the numbers from 3 to 998 with a step of 2
for number in range(3, 998, 2):
    # check if the number and its twin (number + 2) are both prime
    if prime(number) and prime(number + 2):
        # print the twin primes
        print(f"({number}, {number + 2})")

