max = 5
top = -1

stack = []

while True:
    print(''' Chouse Your Opration:
    \n1. Adding New Element in Stack : 
    \n2. Removing Elemnet in Stack :
    \n3. See All Element in Stack:
    \n4. Enter The Program
    ''')
    sel = int(input("Select Your Option: "))

    def checkFull():
        if(top >= max-1):
            print("The Stack is Full")
            return False
        return True
    
    def checkEmpty():
            if(top <= -1):
                print("The stack is Empty")
                return False
            return True

    match sel:
        case 1:
            if checkFull():
                value = int(input("Enter your Value :"))
                stack.append(value)
                top=top+1
            
        case 2:
            if checkEmpty():
                stack.pop()
                top = top-1
        case 3:
            if checkEmpty():
                for i in stack:
                    print(i)
        case 4:
            print("Program will End")
            break
        case _:
            print("Invalid input")
