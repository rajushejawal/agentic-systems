# Take a number as input from the user and check whether it is positive, negative, or zero using if / elif / else.
a = int(input("enter the number:"))

if a == 0:
    print("a is Zero")
elif a > 0:
    print("a is Positive")
else: print("a is Negative")


# a = int(input("enter the number:"))

# Take a number and check whether it is even or odd.
if a % 2 == 0:
    print("a is Even")
else: print("a is Odd")

# Write a program to check if a person is eligible to vote (age ≥ 18).
age = int(input("enter the age:"))

if age >= 18:
    print("Eligible to Vote")
else: print("Not eligible to Vote")


# Write a program using nested if to check:

# If a number is greater than 10
# If yes, check whether it is even or odd
if a > 10:
    if a % 2 == 0:
        print("a is Even")
    else: print("a is Odd")
else: print("a is under 10")


# Take two boolean inputs and print the result using logical operators (and, or).

a = input("enter the number 1:").strip().lower() == "true"
b = input("enter the number 2:").strip().lower() == "true"

print(type(a))
print(type(b))

print ( a and b)
print ( a or b)

# Write a program to take marks as input and print grade:

# ≥ 90 → A
# ≥ 75 → B
# ≥ 50 → C
# Otherwise → Fail

marks = int(input("enter the marks:"))

if marks >= 90:
    print("Grade: A")
elif marks >= 75:
    print("Grade: B")    
elif marks >= 50:
    print("Grade: C")        
else: print("Grade: Fail")        
