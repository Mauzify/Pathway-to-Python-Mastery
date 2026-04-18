import secrets
# secrets is a built in python library used for generating cyrptographically strong random numbers, its specifically designed for managing
# sensitive data like passwords, account authentication tokens, and security keys.
import string
# string is a built in python library that provides a collection of string constants, such as ascii letters, digits and punctuation,
# which can be used to create complex passwords.

def generate_the_damn_password(length, use_digits, use_special): # the function that tells the program how to actually generate the password .
    chars = string.ascii_lowercase # starts with lower case letters as base.

    if use_digits: # if using digits is true, add digits to the characters pool.
        chars += string.digits
    if use_special: # if using special characters is true, add punctuation and uppercase letters to the characters pool, case sensitive. 
        chars += string.punctuation
    chars += string.ascii_uppercase # adds the actual uppercase letters to the characters pool. 

    password = ''.join(secrets.choice(chars) for _ in range(length)) # generates a password by randomly inputting numbers from the characters pool, hense the for _ in range
    return password # stop the function and return what has been generated.

def program(): # program function that runs the actual UI.
    print("--- PASSWORD GENERATOR ---")
    
    try: 
        length = int(input("Enter password length of your choice (min 8): ")) # converts string to an interger (number).
        if length < 8: # if length less than 8, print error and set length to 8.
            print("Error: Password length must be at least eight characters long.")
            length = 8
        
        digits = input("Would you like to include digits? (y/n): ").lower() == 'y' # converts user input to lowercase and checks if returned Y.
        special = input("Would you like to include special characters? (y/n): ").lower() == 'y' # converts user input to special and checks if returned Y.

        if not digits and not special:
            print("Warning: Your password is set to Ultra-Basic mode. No digits nor symbols.") # if both digits and special are false, print this warning.
        elif not digits and special:
            print("Warning: your password is set to Basic Mode. No digits, but symbols are included.") # if digits is false and special is true, print this warning.
        elif digits and not special:
            print("Warning: Your password is set to Moderate Mode. Digits are included, but no symbols.") # if digits is true and special is false, print this warning.
        elif digits and special:
            print("NOTICE: Your password is set to HARDENED MODE. Digits and symbols are included. This is the most secure form of password you can generate with this program.") # if both digits and special are true, print this notice.

        new_password = generate_the_damn_password(length, digits, special) # calls password function and stores the result in new_password variable.

        print("\n" + "="*30) # prints a line of 30 equal signs for visual separation.
        print(f"Generated Password: {new_password}")
        print("="*30) # prints a line of 30 equal signs for visual separation.
        print("Note: Never share this password in plain text.")

    except ValueError: # Heres the error handling if the user inputs something that cannot be converted to an interger.
        print("Error: please enter a valid number.")
    
if __name__ == "__main__": # python idiom for running the program only if this file is executed directly, not imported as a module in another file. 
    program() # calls program to run when file is executed.