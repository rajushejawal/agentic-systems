# name='Raju Shejawal'

# for i in range(len(name)):
#     print(name[i])

# print(name)

# long_name = """Raju Shejawal is a 
# student of Agentic Systems Design"""

# long_name = long_name * 2

# print(long_name)

# name = "alice"
# print(name.upper())

# class Dog:
#     def bark(self):
#         print("Woof!")

# d = Dog()
# d.bark()


#Create a string " python programming " and print the string after applying strip() and title() methods.
s = " python programming "
print("Original string:", repr(s))
print("After strip():", repr(s.strip()))
print("After title():", repr(s.title()))

#Write a program to check whether a given email (string) starts with "user" and contains "@".
email = input("Enter an email: ")
if email.startswith("user") and "@" in email:
    print("Valid email")
else:    print("Invalid email")



#Create a dictionary student = {'name': 'Alice', 'age': 22} and:
# Print all keys, values, and items separately.
student = {'name': 'Alice', 'age': 22}
print("Keys:", student.keys())
print("Values:", student.values()) 
print("Items:", student.items())



# Given a dictionary config = {'theme': 'dark'}, safely access the key 'font_size' using get() and print a default value if it does not exist.
config = {'theme': 'dark'}
font_size = config.get('font_size', 'Default font size: 12')
print(font_size)


# Create a nested dictionary for a user with name and city, and safely access the city using chained get() methods.
user = {'name': 'Alice', 'details': {'city': 'New York'}}
city = user.get('details', {}).get('city', 'City not found')
print("City:", city)
    