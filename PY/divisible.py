A = int(input("Enter your value:  "))

b = 0
c = 0

if A%5 ==0:
    b = 1

if A%7 ==0:
    c = 1

if (b and c == 1):
    print("value are disvisibel by 5 & 7")
elif (b == 1 or c == 1):
    print("value are disvisible by 5 or 7 ")
else:
    print("the vale will not divisibel ")


