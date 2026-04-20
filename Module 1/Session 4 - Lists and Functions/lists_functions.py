# 1. list of 5 numbers and print the first and last element using indexing
numbers = [10, 20, 30, 40, 50]
print("numbers:", numbers)
print("First element:", numbers[0])
print("Last element:", numbers[-1])


# 2. list using range() from 1 to 10 and print only even numbers using slicing
numbers = list(range(1, 11))
print("numbers:", numbers)
print("Even numbers:", numbers[1::2])

# 3. Given a list ['apple', 'banana', 'cherry', 'date'], print the last two elements using negative slicing
fruits = ['apple', 'banana', 'cherry', 'date']
print("fruits:", fruits)
print("Last two fruits:", fruits[-2:])


# 4. Use a for loop to iterate through a list of numbers and calculate their sum.
numbers = [1, 2, 3, 4, 5]
total = 0
for n in numbers:
    total += n
print("Sum:", total)

# 5. Use a while loop to iterate through a list and print all elements.
numbers = [1, 2, 3, 4, 5]
index = 0
while index < len(numbers):
    print("Element:", numbers[index])
    index += 1

# 6. Write a function greet(name) that takes a name as a parameter and prints a greeting message.
def greet(name):
    print(f"Hello, {name}!")

name=input("Enter your name: ")
greet(name)


# 7. Write a function add(a, b) that returns the sum of two numbers and print the result.
def add(a, b):
    return a + b

X = int(input("Enter first number: "))
Y = int(input("Enter second number: "))

result = add(X, Y)
print("Sum:", result)

# 8. Write a function with a default parameter power(base, exponent=2) to calculate exponentiation.
def power(base, exponent=2):
    return base ** exponent

base= int(input("Enter base number: "))
exponent= int(input("Enter exponent (press Enter for default 2): ") or 2)

result = power(base, exponent)
print("Power:", result)