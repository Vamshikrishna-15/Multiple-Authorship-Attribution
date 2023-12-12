
import datetime

###############################################################################
#
#   PART 1: Creating four functions
#
###############################################################################

history = []

#Function to add multiple numbers
def add():
    operation_add = 0
    numbers = []
    user_input = input("Enter a number:")

    #This While Loop will happen until the user enters an empty string (by pressing "enter")
    while user_input != "":
        numbers.append(float(user_input))
        user_input = input("Enter another number:")
    #This For Loop repeats the addition operation
    for n in numbers:
        operation_add = operation_add + n
    #Displaying the answer:
    print(f"The sum of {numbers} is equal to {operation_add}")
    #Inserting the answer inside the history list:
    sentence = "The sum of " + str(numbers) + " is equal to: " + str(operation_add) + "\n" + str(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    history.append(sentence)

#Function to subtract multiple numbers
def subtraction():
    operation_subtraction = 0
    numbers = []
    user_input = input("Enter a number:")

    # This While Loop will continue until the user enters an empty string (by pressing "enter")
    while user_input != "":
        numbers.append(float(user_input))
        user_input = input("Enter another number:")
    # This For Loop repeats the subtraction operation
    for n in numbers:
        operation_subtraction = operation_subtraction - n
    # Displaying the answer:
    print(f"The subtraction of {numbers} is equal to {operation_subtraction}")
    # Inserting the answer inside the history list:
    sentence = "A subtraction of " + str(numbers) + " is equal to: " + str(operation_subtraction) + "\n" + str(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    history.append(sentence)


def division():
    operation_division = 1
    numbers = []
    user_input = input("Enter a number:")

    # This While Loop will happen until the user enters an empty string (by pressing "enter")
    while user_input != "" or len(numbers) < 2:
        if user_input != "":
            numbers.append(float(user_input))
        else:
            print("Invalid operation!")
        user_input = input("Enter another number or click enter:")

    # This For Loop repeats the division operation
    for n in numbers:
        operation_division = operation_division * n

    # Displaying the answer
    print(f"The division of {numbers} is equal to {operation_division}")
    # Inserting the answer inside the history list
    sentence = "The division of " + str(numbers) + " is equal to: " + str(
        operation_division) + "\n" + str(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    history.append(sentence)

#Function to multiply multiple numbers
def multiplication():
    operation_multiplication = 1
    numbers = []
    user_input = input("Enter a number:")

    # This While Loop will happen until the user enters an empty string (by pressing "enter")
    while user_input != "" or len(numbers)<2:
        if user_input != "":
            numbers.append(float(user_input))
        else:
            print("Invalid operation")
        user_input = input("Enter another number or click enter:")

    #This For Loop repeats the multiplication operation
    for n in numbers:
        operation_multiplication = operation_multiplication * n

    #Displaying the answer
    print(f"The multiplication of {numbers} is equal to {operation_multiplication}")
    #Inserting the answer inside the history list:
    sentence = "The multiplication of " + str(numbers) + " is equal to: " + str(operation_multiplication) + "\n" + str(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    history.append(sentence)

#Function to show user's previous calculations
def previous_calculations():
    for line in history:
        print("\n", line)

###############################################################################
#
#   PART 2: Interacting with user
#
###############################################################################


while True:
    print("My Calculator - 2021")
    print("----------MENU----------")
    print("""Type an option:
    1 - Addition
    2 - Subtraction
    3 - Multiplication
    4 - Division
    5 - History
    6 - Terminate
    """)
    # User selects the operation
    click = int(input("Select an option: "))

    if click == 1:
        add()
    elif click == 2:
        subtraction()
    elif click == 3:
        multiplication()
    elif click == 4:
        division()
    elif click == 5:
        previous_calculations()
    elif click == 6:
        break
    else:
        print("Invalid option. Please try again :-)")


