str1 = "listen"
str2 = "silent"

if sorted(str1) == sorted(str2):
  print("Anagram")
else:
  print("Not Anagram")


  arr = [10,20,20,30,40,10,50,60,10,20,30,20]
arr2 = [90,30,10,20,50,60,40,50,60,70,50,30]

uneek = []

for i in arr:
  if i in arr2:
    if i not in uneek:
      uneek.append(i)
print(uneek)


# comman = list(set(list1) & set(list2))


arr = [10,20,20,30,40,10,50,60,10,20,30,20]
uneek = {}

for i in arr:
  if i not in uneek:
    uneek[i] = 1
  else:
    uneek[i] += 1
print(uneek)

# for n i number:
#    fequency[n] = fequency.get(n,0) +1



arr = [10,20,20,30,40,10,50,60,10,20,30,20]
uneek = []

for i in arr:
  if i not in uneek:
    uneek.append(i)
print(uneek)