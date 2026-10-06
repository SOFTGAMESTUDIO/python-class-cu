User = {}

number = int(input("Enter the No of Users you Enter: "))

for i in range(0, number):
    uid = int(input("Enter User ID: "))
    name = input("Enter User Name: ")
    age = int(input("Enter User Age: "))

    User[uid] = {
        "Name": name,
        "Age": age
    }


print("Search the User: ")

user_id = int(input("Enter User id: "))

print("Name: ", User[user_id]["Name"])
print("Age: ", User[user_id]["Age"])






