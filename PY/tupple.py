list = [123, [1, 2, 3], 'abc']
tupple = (list, 456, 'def')
print(tupple)

list[1][0] = 100
print(tupple)

tupple[0][1][1] = 200
print(tupple)

# tupple[2] = 'xyz'  # This will raise an error because tuples are immutable
print(tupple)

set = {1, 2, 3}
set.add(4)
print(set)

set.remove(2)
print(set)

set.discard(3)  # This will not raise an error even if 3 is not in the set
print(set)

#union of sets
set1 = {1, 2, 3}
set2 = {3, 4, 5}
union_set = set1.union(set2)
print(union_set)

# difference between get and []
list_dict = {'a': 1, 'b': 2}
query1 = list_dict.get('c', 'Not Found')  # Returns 'Not Found' if key 'c' is not present
# query2 = list_dict['c']  # Raises KeyError if key 'c' is not present
print(query1)
# print(query2)  # This line will raise an error


# what is item function in pythonIn Python, the `items()` function is a method used with dictionaries. It returns a view object

# can a list be a key in a dictionary? No, a list cannot be used as a key in a dictionary because lists are mutable and not hashable. Dictionary keys must be immutable types, such as strings, numbers, or tuples.


dict = {'a': 1, 'a': 2}
print(dict)  # This will print {'a': 2} because the second assignment overwrites the first one.



