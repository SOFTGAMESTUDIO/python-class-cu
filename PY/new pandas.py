import pandas as pd

# Read CSV file
df = pd.read_csv("student_mock_data.csv")

# Display all data
print("All Student Data:")
print(df)

# --------------------------------
# 1. Filter by Program
# --------------------------------

mca_students = df[df["Program"] == "MCA"]

print("\nMCA Students:")
print(mca_students)


# --------------------------------
# 2. Filter by Section
# --------------------------------

section_a = df[df["Section"] == "A"]

print("\nSection A Students:")
print(section_a)


# --------------------------------
# 3. Filter by Class
# --------------------------------

ma_students = df[df["Class"] == "MA"]

print("\nMA Students:")
print(ma_students)


# --------------------------------
# 4. Multiple Conditions
# --------------------------------

mca_section_a = df[
    (df["Program"] == "MCA") &
    (df["Section"] == "A")
]

print("\nMCA Students in Section A:")
print(mca_section_a)


# --------------------------------
# 5. Filter by Name
# --------------------------------

student = df[df["Name"] == "Livesh Garg"]

print("\nLivesh Garg:")
print(student)


# --------------------------------
# 6. Filter using contains()
# --------------------------------

sharma_students = df[
    df["Name"].str.contains("Sharma", case=False, na=False)
]

print("\nStudents with Sharma in their name:")
print(sharma_students)


# --------------------------------
# 7. Get only selected columns
# --------------------------------

result = df.loc[
    df["Program"] == "MCA",
    ["Roll No", "Name", "Section", "Program"]
]

print("\nSelected MCA Data:")
print(result)