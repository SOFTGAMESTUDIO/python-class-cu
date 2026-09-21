class StudentInfo:
    
    def display(self, St_UID, St_Name, St_Class ):
        print("\n\nStudnet Information\n")
        print("Student ID : ", St_UID)
        print("Student Name : ", St_Name)
        print("Student Class : ", St_Class)

print("Studnet Details\n")
UID = int(input("Enter The Uid of Studnet: "))
Name = input("Enter The Name of Student: ")
Class = input("Enter The Class of Studnet: ")

st1 = StudentInfo()

st1.display(UID, Name, Class)