# Student Name: Ali Asad
# MISIS NUMBER: 01091335

import bcrypt
import os

# Step 6: Define the User Data File
USER_DATA_FILE = "users.txt"


# Step 4: Password Hashing Function
def hash_password(plain_text_password):
    # Encode the password to bytes, required by bcrypt
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    return hashed


# Step 5: Verify Password Function
def verify_password(plain_text_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')

    hashed_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_bytes)


# Step 8: Check for Duplicate Usernames
def user_exists(username):
    # Check if user data file exists
    if not os.path.exists(USER_DATA_FILE):
        return False
    # Reads the file and checks each line for the username
    with open(USER_DATA_FILE, "r") as h:
        for line in h:
            existing_username, _ = line.strip().split(",", 1)
            if existing_username == username:
                return True
    return False



# Step 7: Registration of New Users
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    hashed_password = hash_password(password)
    
    hashed_str = hashed_password.decode('utf-8')
    # Append the new user credentials to the file
    with open(USER_DATA_FILE, "a") as i:
        i.write(f"{username},{hashed_str}\n")
    print(f"Success: User '{username}' registered successfully!")
    return True


# Step 9. User Login Function
def login_user(username, password):
    # Check if user data file exists
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No Users are Registered.")
        with open(USER_DATA_FILE, "w"):  # Create the file if it doesn't exist
            pass
        return False
    # Reads the file and checks for matching username and password
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            existing_username, stored_hash = line.strip().split(",", 1)
            if existing_username == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False
    print("Error: Username not found.")
    return False


# Step 10: Username Validation
def validate_username(username):
    
    if len(username) < 3 or len(username) > 20: # Requirement for Username Length
        return False, "Username must be between 3 and 20 characters."
    if not username.isalnum(): # Requirement for Alphanumeric Usernames
        return False, "Username must contain numbers and letters only."
    return True, ""


# Step 10: Password Validation
def validate_password(password):
    if len(password) < 6 or len(password) > 50: # Requirement for Password Length
        return False, "Password must be between 6 and 50 characters."
    return True, ""


# Step 11: Display Menu
def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)



def main():
    """Displays the main menu options."""
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration Flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            # Validate username
            is_valid, msg = validate_username(username)
            if not is_valid:
                print("Error:", msg)
                continue

            password = input("Enter a password: ").strip()
            # Validate password
            is_valid, msg = validate_password(password)
            if not is_valid:
                print("Error:", msg)
                continue
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Optional: check early if username exists
            if user_exists(username):
                print(f'Error: Username \'{username}\' already exists.')
                continue


            register_user(username, password)
        



        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            success = login_user(username, password)
            if success:
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard)")
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
