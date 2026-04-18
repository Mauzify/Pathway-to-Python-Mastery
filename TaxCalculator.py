# Tax Calculator + 1 hour elasped time of script development

# imports
import time

# define split calulation between math equations
def calculate_split(tax_percentage, bill_total, people):
    tax_amount = bill_total * (tax_percentage / 100)
    total_bill = bill_total + tax_amount
    total_per_person = total_bill / people

    return {
        "total": total_bill,
        "per_person": total_per_person
    }

# Actual Program itself
history = []
name = input("What's your name? ")
print(f"Greetings, {name}. Lets get started with a calculation that you need to do.")
time.sleep(2)
while True:
    print("\n---TAX CALCULATOR---")
    user_input = input("Enter Bill total (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        if history:
            print("\n--- CALCULATIONS SUMMARY ---")
            print(f"Total Bills Processed: {len(history)}")
            print(f"Total Money Handled: ${sum(history):.2f}")
            print(f"Highest Bill raised: ${max(history):.2f}")
        # End Logic

        print(f"Goodbye {name}. Calculate you soon.")
        break

    # memory + ValueError Incident Response | Statements

    try: 
        bill_total = float(user_input)
        tax_percentage = float(input("Tax Percentage (%): "))
        people = int(input("How many people? (X): "))
    except ValueError:
        print("Error: Please enter numbers, not letters or symbols.")
        continue

    if bill_total < 0 or tax_percentage < 0:
       print("Error: Values cannot be negative.")
       continue

    if people <= 0:
       print("Error [MATH]: Cannot divide by 0, nor less than 0.")
       continue


    result = calculate_split(tax_percentage, bill_total, people)

    history.append(result["total"])

    if people == 1:
        print(f"Big balls, paying alone huh?: ${result['per_person']:.2f}")
    elif people >= 10:
        print(f"Wow, you're either broke as hell, or having a party. Each pays: ${result['per_person']:.2f}")
    else:
        print(f"Each person should pay: ${result['per_person']:.2f}")

  # Script fully functions, however, indenting may be a little offset. Bugs may differ. 
