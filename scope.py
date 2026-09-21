# scope of lifetime of globel and veriable 
print("Scope of lifetime of globel and veriable")
print("x declared out globley ")
x = 5;

def myfunc():
    print("inner function running")
    print("value of x will chaneg ")
    x = 10
    print("declared y inside of function")
    y = 15
    print("value of x inside function: ", x)
    print("value of y inside function: ", y)
    print("function will closed")
    
myfunc()
print("value of x outside function: ", x)



