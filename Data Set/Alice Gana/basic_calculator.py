###############################################################################
#
#   PART 1: Creating functions
#
###############################################################################

history =[]

# Function to add two numbers
def addition():
    a = float(input("Type a number: "))
    b = float(input ("Type another number: "))
    print("addition: " , a +b)
    operation_addition =a + b

    global history
    history.append(operation_addition)

# Function to subtract two numbers
def subtraction():
    a = float(input("Type a number: "))
    b = float(input("Type another number: "))
    print("Subtraction: ", a - b)
    operation_addition = a - b

    global history
    history.append(operation_addition)

# Function to divide two numbers
def division():
    a = float(input("Type a number: "))
    b = float(input("Type another number: "))
    while b == 0:
        print("Erro! Try again")
        b = float(input("Type another number: "))
    print("division: ", a / b)
    operation_division = a / b

    global history
    history.append(operation_division)

# Function to multiply two numbers
def multiplication():
    a = float(input("Type a number: "))
    b = float(input("Type another number: "))
    print("multiplication: ", a * b)
    operation_multiplication = a * b

    global history
    history.append(operation_multiplication)

# Storing results to see previous calculations
def showing_previous_calculations():
    print(history)


###############################################################################
#
#   PART 2: Interacting with user
#
###############################################################################

# Infinite loop which will end with the break statement
while True:
    print("My Calculator - 2021")
    print("----------MENU----------")
    print("""Select an option:
    1 - Addition
    2 - Subtraction
    3 - Multiplication
    4 - Division
    5 - History
    6 - Terminate
    """)

    # Take input from user
    click = float(input("Enter an option: "))

    if click == 1:
        addition()
    elif click == 2:
        subtraction()
    elif click == 3:
        multiplication()
    elif click == 4:
        division()
    elif click == 5:
        showing_previous_calculations()
    elif click == 6:
        break  # break statement to stop a while loop
    else:
        print("Invalid option")
