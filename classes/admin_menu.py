from Repositories.users_repository import UserRepository
from core.exceptions import ClubError
from services.add_user import add_user
def admin_panel(admin):
    while True:
        choice = input(
            "1-add user\n"
            "2-view user\n"
            "3-activate/deactivate user\n"
            "4-log out\n"
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
            try:
                all_users = UserRepository.allusers()
            except ClubError as e:
                print("Error:", e)
                continue
            if not all_users:
                print("No users found.")
            for u in all_users:
                if u.is_active:
                    status = "active"
                else:
                    status = "inactive"
                print(f"{u.name} | {u.username} | {u.role} | {u.email} | {status}")
        elif choice == "3":
            username = input("Enter username of the user to activate/deactivate: ").strip()
            try:
                all_users = UserRepository.allusers()
                found = False
                for u in all_users:
                    if u.username == username:
                        found = True
                        if u.role == "admin":
                            print("You cannot deactivate an admin user.")
                            break
                        u.is_active = not u.is_active
                        UserRepository.save_all(all_users)
                        print(f"User {u.name} is now {'active' if u.is_active else 'inactive'}.")
                        break
                if not found:
                    print("User not found.")
            except ClubError as e:
                print("Error:", e)
        elif choice == "4":
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
