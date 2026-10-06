def OddAndEven(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

num = int(input("Enter a number to check if it is Odd or Even: "))
result = OddAndEven(num)
print(f"The number {num} is {result}.")