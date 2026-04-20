# print 1 to 10 using while loop
a = 1

while a <= 10:
    print(a)
    a+=1


#print pasword until it is more than 8 character using while loop
pwd = input("Enter password more than 8 Character:")

while len(pwd) < 8:
    print("Password is short. Try again.")
    pwd = input("Enter password more than 8 Character:")

print("password:",pwd)

#print square of numbers in list using for loop
list = [1,2,3,4,5]
for i in list:
    print("Square of", i, "is", i**2)


#print even numbers from 1 to 20 using for loop
for i in range(1,21):
    if i % 2 == 0:
        print("even number:", i)

#break program when number 7 is reached
list = [1,2,3,4,5,7,6,8,9,10]
for i in list:
    if i == 7:
        print("Number 7 is encountered. Breaking the loop.")
        break
    print("i:", i)

#print only odd numbers from 1 to 10 using continue statement
for i in range(1,11):
    if i % 2 == 0:
        continue
    print("odd number:", i)

#nested loops to print a 3x3 matrix of *
for i in range(3):
    for j in range(3):
        print("*", end=" ")
    print()

#nested loops to print a 8x8 diamond shape of *
for i in range(8):
    for j in range(4 - i):
        print("*", end=" ")
    print()

size = int(input("Enter diamond size: "))
if size < 1:
    print("Size must be at least 1.")
else:
    i = 1
    while i <= size:
        print(" " * (size - i) + "*" * (2 * i - 1))
        i += 1

    i = size - 1
    while i > 0:
        print(" " * (size - i) + "*" * (2 * i - 1))
        i -= 1