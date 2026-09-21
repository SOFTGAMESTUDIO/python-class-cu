# Class & object code 

class StudentInfo:
    def __init__(self, St_UID, St_Name,St_Class):
        self.St_UID = St_UID
        self.St_Name = St_Name
        self.St_Class = St_Class
    def display(self):
        print("\n\nStudnet Information\n")
        print("Student ID : ", self.St_UID)
        print("Student Name : ", self.St_Name)
        print("Student Class : ", self.St_Class)

print("Studnet Details\n")
UID = int(input("Enter The Uid of Studnet: "))
Name = input("Enter The Name of Student: ")
Class = input("Enter The Class of Studnet: ")

st1 = StudentInfo(UID, Name, Class)

st1.display()


# constructor code


class EmployeeInfo:

    def __init__(self, Emp_UID, Emp_Name, Emp_Designation):
        self.Emp_UID = Emp_UID
        self.Emp_Name = Emp_Name
        self.Emp_Designation = Emp_Designation
        print("Constructor is called automatically when object is created")
        print("Employee ID : ", self.Emp_UID)
        print("Employee Name : ", self.Emp_Name)
        print("Employee Designation : ", self.Emp_Designation)
        

print("Employee Details\n")
UID = int(input("Enter The Uid of Employee: "))
Name = input("Enter The Name of Employee: ")
Designation = input("Enter The Designation of Employee: ")

EmployeeInfo(UID, Name, Designation)


# Enclupsulation code

class BankAccount:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance: {self.__balance}")
        else:
            print("Insufficient funds or invalid withdrawal amount.")

    def get_balance(self):
        return self.__balance


print("Bank Account Details\n")
account_number = input("Enter the account number: ")
account_holder = input("Enter the account holder's name: ")
initial_balance = float(input("Enter the initial balance: "))
account = BankAccount(account_number, account_holder, initial_balance)
deposit_amount = float(input("Enter the amount to deposit: "))
account.deposit(deposit_amount)
withdraw_amount = float(input("Enter the amount to withdraw: "))
account.withdraw(withdraw_amount)
print(f"Final balance: {account.get_balance()}")




# inheritance code 

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def display_info(self):
        super().display_info()
        print(f"Student ID: {self.student_id}")

print("Student Details\n")
name = input("Enter the name of the student: ")
age = int(input("Enter the age of the student: "))
student_id = input("Enter the student ID: ")
student = Student(name, age, student_id)
student.display_info()
    




# polymorphism code 
import math

class Shape:
    def area(self):
        pass
    def perimeter(self):
        pass
    def display(self):
        print("Area: ", self.area())
        print("Perimeter: ", self.perimeter())


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius
    
    def display(self):
        print(f"\n--- Circle (radius={self.radius}) ---")
        super().display()


class Triangle(Shape):
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
    
    def area(self):
        # Using Heron's formula
        s = (self.side1 + self.side2 + self.side3) / 2
        return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
    
    def perimeter(self):
        return self.side1 + self.side2 + self.side3
    
    def display(self):
        print(f"\n--- Triangle (sides={self.side1}, {self.side2}, {self.side3}) ---")
        super().display()


class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2
    
    def perimeter(self):
        return 4 * self.side
    
    def display(self):
        print(f"\n--- Square (side={self.side}) ---")
        super().display()





Circle(5).display()
Triangle(3, 4, 5).display() 
Square(4).display() 





