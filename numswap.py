## Write an experiment to swap two columns in numpy array.

import numpy as np

arr = np.array([[1,2,3], [4,5,6],[6,7,8]])

print("Orignal array: ")
print(arr)


# the method in build 
arr[:,[0,2]] = arr[:,[2,0]]

print("swap collem")
print(arr)

arr[[0,2]] = arr[[2,0]]

print("swap row")
print(arr)
arr[[0,2],[0,2]] = arr[[2,0],[2,0]]

# the method with using for loop 
# for i in range(arr.shape[0]):
#     arr[i, 0] = arr[i, 0] + arr[i, 2]
#     arr[i, 2] = arr[i, 0] - arr[i, 2]
#     arr[i, 0] = arr[i, 0] - arr[i, 2]


# the method with 3rd veriable 
# temp = arr[:,[0,2]].copy()
# arr[:,[0,2]] = arr[:,[2,0]]
# arr[:,[2,0]] = temp


# the method in build 



print("swap array")
print(arr)


