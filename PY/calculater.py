A = int(input("Enter Your value: "))
B = int(input("Enter Your value: "))
C = input("Select Yoru Operate \n1. + For Addition \n2. - For Subtraction \n3. * For Multiplaction \n4. / For Devision \n5. % for Modules \nEnter your Selected Opeate No: ")

match C:
    case '+':
        print("The Addition of A & B : ",A+B)
    case '-':
        print("The Subtraction of A & B : ",A-B)
    case '*':
        print("The Multiplaction of A & B : ",A*B)
    case '/':
        print("The Division of A & B : ",A/B)
    case '%':
        print("The Moduless of A & B : ",A%B)
    case _:
        print("Invalid Error")