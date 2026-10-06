my_list = [10,20,30,40,50,60,70,80,90,100] # Createing a List

print("Accissing list : ",my_list) # accessing

print("Sclicing list : ", my_list[1:3]) #scliciing teh list 

my_list[2] = 50 # Modifing way 
print("Modifing list : ", my_list)

my_list.append(110) # adding new element 
print("Appending list : ",my_list)

my_list.insert(4, 120) # insert new element 
print("insert  list : ",my_list)

my_list.remove(100) # removing element 
print("Removing list : ",my_list)

my_list.pop() # pop element 
print("pop list : ",my_list)

my_list.sort()  # sort the list 
print("sorting list : ",my_list)

my_list.reverse() # reverce 
print("reverce list : ", my_list)

print("length list : ",len(my_list)) # find length 


for i in range(0, len(my_list)):
    print("looping  list : ",my_list[i])