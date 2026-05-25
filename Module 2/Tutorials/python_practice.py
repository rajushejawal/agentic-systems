# def make_invoice_line(item_name,tax_rate):
#     def format_line(amount):
#         if amount <= 0:
#             return f"Invalid amount: {amount}"
#         else:
#             tax_amount = amount * tax_rate
#             total_amount = amount + tax_amount
#             return f"Item: {item_name}:| Amount: {amount:.2f} | Tax: {tax_amount:.2f} | Total: {total_amount:.2f}"
#     return format_line

# invoice_line = make_invoice_line('Notebook', 0.18)
# print(invoice_line(250))
# print(invoice_line(-10))


# students = [
#     {'name': 'asha', 'scores': [72, 85, 90], 'active': True},
#     {'name': 'ravi', 'scores': [55, 60, 58], 'active': True},
#     {'name': 'meera', 'scores': [88, 92, 95], 'active': False},
#     {'name': 'kabir', 'scores': [63, 70, 75], 'active': True}
# ]

# def calculate_average(scores):
#     if not scores:
#         return 0
#     return sum(scores) / len(scores)

# def get_status(average):
#     if average >= 80:
#         return "Strong"
#     elif average >= 60:
#         return "Steady"
#     else:
#         return "Needs Practice"
    
# summary = {"Strong": 0, "Steady": 0, "Needs Practice": 0}
# for student in students:
#     if student['active']:
#         average_score = calculate_average(student['scores'])
#         status = get_status(average_score)
#         print(f"Name: {student['name'].title()}, Average Score: {average_score:.2f}, Status: {status}")
#         summary[status] += 1
# print("\nSummary:")
# for status, count in summary.items():
#     print(f"{status}: {count} active students")

# Start with an empty dictionary named borrow_counts.
# Loop through borrow_log and update borrow_counts so each title maps to how many times it appears.
# Define a function most_borrowed(counts) that returns the title with the highest count. If two titles tie, return either one.
# Define a function titles_above(counts, minimum) that returns a list of titles borrowed at least minimum times.
# Print the full dictionary, the most borrowed title, and the list returned by titles_above(borrow_counts, 2).

# borrow_log = ['python basics', 'data structures', 'python basics', 'algorithms', 'data structures', 'python basics']

# borrow_count = {}
# for book in borrow_log:
#     if book in borrow_count:
#         borrow_count[book] +=1
#     else:
#         borrow_count[book] = 1
# print("Borrow Count:")

# def most_borrowed(borrow_count):
#     most_borrowed_book = max(borrow_count, key=borrow_count.get)
#     return most_borrowed_book, borrow_count[most_borrowed_book]

# def titles_above(counts, minimum):
#     return [title for title, count in counts.items() if count >= minimum]

# print("Borrow Count:", borrow_count)
# most_borrowed_title, max_borrows = most_borrowed(borrow_count)
# print("Most Borrowed Title:", most_borrowed_title)
# print("Max Borrows:", max_borrows)
# print("Titles Borrowed 2+ Times:", titles_above(borrow_count, 2))  