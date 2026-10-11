from Repositories.users_repository import UserRepository
from core.exceptions import ClubError
from services.add_user import add_user
from services.add_user import add_user
import json 
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
class Coach(User):
    def show_info(self):
        return "[Coach] " + super().show_info()

class Member(User):
    def show_info(self):
        return "[Member] " + super().show_info()

def save_users():
    with open("user_data.json", "w", encoding="utf-8") as file:
        json.dump([u.to_dict() for u in user], file, ensure_ascii=False, indent=2)
def load_users():
    try:
        with open("user_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            users = []
            for u in data:
                if u["role"] == "coach":
                    users.append(Coach(**u))
                else:
                    users.append(Member(**u))
            return users
    except FileNotFoundError:   
        return []
    except json.JSONDecodeError:
        return []
user = load_users()
def admin_panel(admin):
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
                try:
                    add_user(admin.to_dict(), name, username, password, email, role)
                except ClubError as e:
                    print("Error:", e)
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
    try:
        all_users = UserRepository.allusers()
    except ClubError as e:
        print(f"Error: {e}")
        return None
    for user in all_users:
        if user.username == username and user.password == password and user.role == "admin":
            if not user.is_active:
                print("This account is inactive.")
                return None
            return user
    choice = input("Invalid admin credentials. Try again? (y/n): ").strip().lower()
    if choice == "y":
        return admin_login()
    return None
while True:
    choice = input(
        "1-admin login\n"
        "2-coach login\n"
        "3-member login\n"
        "4-exit\n"
        "Select: "
    )
    if choice == "1":
        admin = admin_login()
        if admin:
            admin_panel(admin)
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
