class Student:
    def __init__(self, Name, Rollno):
        self.Name = Name
        self.Rollno = Rollno

    def Student_Display(self):
        print("Name : ", self.Name, "\nRollNo : ", self.Rollno)


s1 = Student("Livesh", 20079)
s1.Student_Display()


