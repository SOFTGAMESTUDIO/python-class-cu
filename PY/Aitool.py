# Student Marks Analysis Program

print("=" * 70)
print("              STUDENT MARKS ANALYSIS SYSTEM")
print("=" * 70)

# Taking student details
name = input("Enter Student Name: ")
roll_no = input("Enter Roll Number: ")
student_class = input("Enter Class: ")
course = input("Enter Course: ")

print("\nEnter marks out of 100:")

# Taking subject marks
subjects = {}

for i in range(1, 6):
    subject_name = input(f"Enter Subject {i} Name: ")

    while True:
        try:
            marks = float(input(f"Enter marks for {subject_name}: "))

            if 0 <= marks <= 100:
                subjects[subject_name] = marks
                break
            else:
                print("Please enter marks between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")

# Function to calculate grade
def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B+"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"


# Function to calculate status
def calculate_status(marks):
    if marks >= 40:
        return "PASS"
    else:
        return "FAIL"


# Calculate total and percentage
total_marks = sum(subjects.values())
maximum_marks = len(subjects) * 100
percentage = (total_marks / maximum_marks) * 100

# Overall grade
overall_grade = calculate_grade(percentage)

# Overall status
overall_status = "PASS"

for marks in subjects.values():
    if marks < 40:
        overall_status = "FAIL"
        break


# Display Student Details
print("\n")
print("=" * 70)
print("                    STUDENT DETAILS")
print("=" * 70)

print(f"Student Name : {name}")
print(f"Roll Number  : {roll_no}")
print(f"Class        : {student_class}")
print(f"Course       : {course}")

# Subject-wise result
print("\n")
print("=" * 70)
print("                    SUBJECT-WISE RESULT")
print("=" * 70)

print(f"{'Subject':<25}{'Marks':<12}{'Percentage':<15}{'Grade':<10}{'Status'}")
print("-" * 70)

for subject, marks in subjects.items():
    grade = calculate_grade(marks)
    status = calculate_status(marks)

    print(
        f"{subject:<25}"
        f"{marks:<12.2f}"
        f"{marks:<15.2f}"
        f"{grade:<10}"
        f"{status}"
    )

# Grand Total
print("\n")
print("=" * 70)
print("                     GRAND RESULT")
print("=" * 70)

print(f"{'Total Marks':<25}: {total_marks:.2f} / {maximum_marks}")
print(f"{'Percentage':<25}: {percentage:.2f}%")
print(f"{'Overall Grade':<25}: {overall_grade}")
print(f"{'Overall Status':<25}: {overall_status}")

print("=" * 70)

if overall_status == "PASS":
    print("Congratulations! The student has passed.")
else:
    print("The student has failed in one or more subjects.")

print("=" * 70)