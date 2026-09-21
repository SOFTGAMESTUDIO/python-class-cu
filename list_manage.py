def CreateList():
    my_list = []
    return my_list

def AddElement(my_list, element):
    my_list.append(element)
    print(f"Element {element} added to the list.")

def UpdateList(my_list, index, new_value):
    if 0 <= index < len(my_list):
        my_list[index] = new_value
        print(f"Element at index {index} updated to {new_value}.")
    else:
        print("Invalid index. Please try again.")

    
def DeleteElement(my_list, value):
    my_list.remove(value)
    print("The Elemet will removed")
    


while True:
    print("1. Create a new list")
    print("2. Adding an element to the list")
    print("3. Display the list")
    print("4. Update the list")
    print("5. Delete an element from the list")
    print("6. Sorted list ")
    print("7. Exit")
    
    choice = int(input("Enter your choice (1-7): "))
    
    if choice == 1:
        my_list = CreateList()
        print("New list created.")
        
    elif choice == 2:
        element = int(input("Enter the element to add: "))
        AddElement(my_list, element)
            
    elif choice == 3:
        print("Current list:", my_list)

    elif choice == 4:
        index = int(input("Enter the index: "))
        new_value = int(input("Enter the Value: "))
        UpdateList(my_list, index, new_value)

    elif choice == 5:
         delete = int(input("Enter Value"))
         DeleteElement(my_list, delete)

    elif choice == 6:
        print(my_list)
        my_list.sort()
        print(my_list)
            
    elif choice == 7:
        print("Exiting the program.")
        break
        
    else:
        print("Invalid choice. Please try again.")