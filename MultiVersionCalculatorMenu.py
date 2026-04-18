# Mauzify's Multi-Version Calculator
# IMPORTS: >>>
import time
#EOL



############################################################################
# INTRODUCTION
name = input("\nGreetings, what is your name, User? ")
if name.strip() == "":
    name = "Guest"
    print("NOTICE: USERNAME NOT DETECTED, SWITCHING TO GUEST NAME...")
if name.isdigit():
    print("NAME CANNOT BE A NUMBER. SWITCHING TO GUEST NAME...")
    name = "Guest"
time.sleep(1.2)
print(f"Welcome, {name}. Welcome to the Multi-Version Calculator. Simple, yet effective.")
time.sleep(1.2)
############################################################################
# STANDARD CALCULATOR
def standard_calculator():
    try:
        num1 = float(input("First Number: "))
        operator = input("Operator (+, -, *, /): ")
        num2 = float(input("Second Number: "))
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                print("Not a number, Try again.")
                return
            result = num1 / num2
        else:
            print("Invalid operator/operation.")
            return
        print(f"Result: {result}")
    except ValueError:
        print("Not a number, Try again.")
############################################################################
def help_menu():
    print("Welcome to the Help-Menu. This Multi-Version Calculator conists of 2 simple calculators that 1. Calculates Taxes depending on how many People, Billing, and Tax %." \
    "This was created by Mauzify, a Developer in GitHub. >> https://github.com/Mauzify 2. A basic mathematical calculator for simple equations, as well as algebra and complex arithmetic. (Coming soon.)")
############################################################################
# TAXES CALCULATOR

# MAJOR KEYPOINT FUNCTIONS
history = []
def calculate_thesplit(tax_percentage, bill_total, people):
    tax_amount = bill_total * (tax_percentage / 100)
    total_bill = bill_total + tax_amount
    total_per_person = total_bill / people
    return {
        "total": total_bill,
        "per_person": total_per_person
    }

def get_input(prompt):
    value = input(prompt)
    if value.lower() == 'exit':
        return None
    return value

def taxes_calculator():
   print("\n--> Welcome to the Tax Calculator! <--")
   Bill_Total = get_input("Enter bill total (or type 'exit' to quit.): ")
   if Bill_Total is None:
       print("\n ---> CALCULATION SUMMARY <----")
       print(f"TOTAL BILLS PROCESSED OVERALL: {len(history)}")
       print(f"TOTAL MONEY CALCULATED: ${sum(history):.2f}")
       print(f"HIGHEST PAYCHECK RAISED: ${max(history):.2f}")

       print(f"Goodbye, {name}. Take care, and Calculate soon.")
       return
   try:
       Bill_Total = float(Bill_Total)
       tax_percentage = float(input("Tax Percentage (%)?: "))
       people = int(input("How many people (x)?: "))
   except ValueError:
       print("Error, Please enter numbers, not letters or symbols (Special Characters).")
       return
   if Bill_Total < 0 or tax_percentage < 0:
       print("Error [MATH]: Values cannot be negative, You don't pay taxes with negative numbers.")
       return
   if people <= 0:
       print("Error [MATH]: Cannot divide by 0, NOR less than 0.")
       return
   result = calculate_thesplit(tax_percentage, Bill_Total, people)
   history.append(result["total"])
   if people == 1:
       print(f"Damn bro. You're paying alone huh?: ${result['per_person']:.2f}")
   elif people >= 10:
       print(f"Wow, you're either broke as hell, or having a group of people. Nothing in between, each pays: ${result['per_person']:.2f}")
############################################################################
while True:
    print("\n===== MAIN MENU =====")
    print("1. Calculate Taxes")
    print("2. Standard Calculator")
    print("3. Help")
    print("4. Exit")
    choice = input("Select option: ")
    if choice == "1":
        taxes_calculator()
    elif choice == "2":
        standard_calculator()
    elif choice == "3":
        help_menu()
    elif choice == "4":
        print("Goodbye.")
        break
    else:
        print("Invalid option. Please select 1 through 4. (1-4)")
############################################################################
