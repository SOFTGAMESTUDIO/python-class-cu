# 1.  convert list to tupple 

# list = [1,2,3,4,5,6]
# print(list)
# tupple = tuple(list)
# print(tupple)

# 2.  unpack a tupple

# frutes = ('apple', 'banana', 'mango', 'orange')

# 3.  create and access directry 

# dri = {
#     101:{
#         'Name': 'Livesh',
#         'Class': 'MCA',
#         'RollNo': 101,
#         'Marks': 90
#     },
#     102:{
#         'Name': 'Livesh',
#         'Class': 'MCA',
#         'RollNo': 102,
#         'Marks': 80
#     },
#     103:{
#         'Name': 'Livesh',
#         'Class': 'MCA',
#         'RollNo': 103,
#         'Marks': 93
#     },
#     104:{
#         'Name': 'Livesh',
#         'Class': 'MCA',
#         'RollNo': 104,
#         'Marks': 70
#     }
# }

# print(dri)


# 5.  add and update Directry element

# rollno = input("Enter Your Rollno: ")
# name = input("Enter Your name: ")
# classe = input("Enter Your Class: ")
# marks = input("Enter Your Marks: ")

# dri[int(rollno)] = {
#     'Name': name,
#     'Class': classe,
#     'RollNo': int(rollno),
#     'Marks': int(marks)
# }

# print(dri)



# 6.  delete Elemet form directery 

# delete_rollno = int(input("Enter Rollno to delete: "))
# deleted_student = dri.pop(delete_rollno, None)

# if deleted_student is None:
#     print("Rollno not found")
# else:
#     print("Student deleted")
#     print(dri)

# 7.  find the student with highest marks

# high_marks = max(dri.items(), key=lambda x: x[1]['Marks'])
# print(f"Student with highest marks: RollNo: {high_marks[0]}, Name: {high_marks[1]['Name']}, Marks: {high_marks[1]['Marks']}")

# 8.  count frequency of elemets using dictonery 

# numbers = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3]
# frequency = {}

# for num in numbers:
#     frequency[num] = frequency.get(num, 0) + 1

# print("Frequency:", frequency)

# 9.  create a pandas series 

# import pandas as pd
# num = pd.Series([1,2,3,4,5,6,7])
# print(num)


# 10. perfom opration on pandas series

# import pandas as pd
# num = pd.Series([1,2,3,4,5,6,7])

# min = num.min()
# max = num.max()
# median = num.median()


# print(min)
# print(max)
# print(median)

# 11. dispaly basic information data 




# 12. create a data framen
# import pandas as pd
# df = pd.DataFrame({
#     'Name': ['Livesh', 'Rohit', 'Mohit', 'Davi'],
#     'Age': [25, 30, 35, 40],
#     'City': ['Abohar', 'Delhi', 'Chandigarh', 'Mumbai']
# })

# print(df)

# 13 add new column to data framen

# import pandas as pd
# df = pd.DataFrame({
#     'Name': ['Livesh', 'Rohit', 'Mohit', 'Davi'],
#     'Age': [25, 30, 35, 40],
#     'City': ['Abohar', 'Delhi', 'Chandigarh', 'Mumbai']
# })

# salary = [50000, 60000, 70000, 80000]
# df['Salary'] = salary

# print(df)