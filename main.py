class User:
    def __init__(self, name, role , username, password, email , is_active=True):
        self.name = name
        self.role = role
        self.username = username
        self.password = password
        self.email = email
        self.is_active = is_active
    def show_info(self):
        return f"Name: {self.name}, Role: {self.role}, Username: {self.username}, Email: {self.email}, Active: {self.is_active}"
    def activate(self):
        self.is_active = True
    def deactivate(self):
        self.is_active = False
    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "is_active": self.is_active
        }
import json 
admin = {"username": "admin", "password": "admin123"}
def save_users():
    with open("user_data.json", "w", encoding="utf-8") as file:
        json.dump([u.to_dict() for u in user], file, ensure_ascii=False, indent=2)
def load_users():
    try:
        with open("user_data.json", "r", encoding="utf-8") as file:
            return [User(**u) for u in json.load(file)]
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
                new_user = User(name, role, username, password, email)
                user.append(new_user)
                save_users()
                print(f"{role.capitalize()} added successfully!")
            else:
                print("Invalid user type. Please enter 'coach' or 'member'.")
        elif choice == "2":
            if not user:
                print("No users found.")
            else:
                for u in user:
                    print(u.show_info())
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
