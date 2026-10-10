admin = {"username": "admin", "password": "admin123"}
def admin_login():
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    if username == admin["username"] and password == admin["password"]:
        return True
    else:
        choice = input("Invalid admin credentials. if you want to try again press (y)  ")
        if choice.lower() == "y":
            return admin_login()
        else :
            return False
while True:
    choice = input(
        "1-admin login\n"
        "2-coach login\n"
        "3-member login\n"
        "4-exit\n"
        "Select: "
    )
    if choice == "1":
        if admin_login():
            print("Admin login successful!")
        else:
            print("Invalid admin credentials.")
    elif choice == "2":
        coach_username = input("Enter coach username: ").strip()
        coach_password = input("Enter coach password: ").strip()
        print("Coach login functionality is not implemented yet.")
    elif choice == "3":
        member_username = input("Enter member username: ").strip()
        member_password = input("Enter member password: ").strip()
        print("Member login functionality is not implemented yet.")
    elif choice == "4" :
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")

