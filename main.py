import json 
admin = {"username": "admin", "password": "admin123"}
def save_users():
    with open("user_data.json", "w", encoding="utf-8") as file:
        json.dump(user, file, ensure_ascii=False, indent=2)
def load_users():
    try:
        with open("user_data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
user = load_users()
def admin_panel():
    while True:
        choice = input(
            "1-add user\n"
            "2-view user\n"
            "3-log out\n"
        )
        if choice == "1":
            role = input("Enter user type (coach/member): ").strip().lower()
            if role in ["coach", "member"]:
                name = input("Enter name: ").strip()
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                email = input("Enter email: ").strip() 
                user.append({"name": name, "type": role, "username": username, "password": password, "email": email, "is_active": True})
                save_users()
                print(f"{role.capitalize()} added successfully!")
            else:
                print("Invalid user type. Please enter 'coach' or 'member'.")
        elif choice == "2":
            if not user:
                print("No users found.")
            else:
                for u in user:
                    print(f"Name: {u['name']}, Type: {u['type']}, Username: {u['username']}, Email: {u['email']}")
        elif choice == "3":
            return 
        else:
            print("Invalid choice.")
def admin_login():
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    if username == admin["username"] and password == admin["password"]:
        return True
    else:
        choice = input("Invalid admin credentials. if you want to try again press (y)  ").strip()
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
            admin_panel()
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
