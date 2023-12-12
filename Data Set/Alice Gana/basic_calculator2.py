
###############################################################################
#
#   PART 1: Creating functions
#
###############################################################################

# Function to take input from user
def taking_input_from_user():
    a = float(input("Enter a number: "))
    b = float(input ("Enter another number: "))
    return a,b

# Function to add two numbers
def add (x,y):
    operation_add=x+y
    print("Addition: ",operation_add)
    return operation_add

#Function to subtract two numbers
def subtract(x,y):
    operation_subtract=x-y
    print("Subtraction: ",x-y)
    return operation_subtract

# Function to divide two numbers
def divisao(x,y):
    while y == 0:
        print("WARNING: Invalid Equation! Try again!")
        y = float(input("Enter another number: "))
    operation_division = x / y
    print("Division: ",x/y)
    return operation_division

# Function to multiply two numbers
def multiplication(x,y):
    operation_multiplication=x*y
    print("Multiplication: ", x*y)
    return operation_multiplication

# Storing results to see previous calculations
def history(calculations):
    print(calculations)

previous_calculations = []

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

#Taking input from user
    click = float(input("Type an option: "))
    num_1, num_2=0,0

    if click >=1 and click <=4:
        num_1, num_2 = taking_input_from_user()

    if click == 1:
        operation=add(num_1,num_2)
        previous_calculations.append(operation)

    elif click ==2:
        operation = subtract(num_1, num_2)
        previous_calculations.append(operation)

    elif click == 3:
        operation = multiplication(num_1, num_2)
        previous_calculations.append(operation)

    elif click ==4:
        operation = divisao(num_1, num_2)
        previous_calculations.append(operation)

    elif click == 5:
         history(previous_calculations)

    elif click == 6:
        break
    else:
        print("Invalid option")


