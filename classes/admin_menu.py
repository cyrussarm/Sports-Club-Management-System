from Repositories.users_repository import UserRepository
from core.exceptions import ClubError
from services.add_user import add_user
from core.storage import load_data, save_data
from core.models import Salon
def load_hall():
          data = load_data("salon.json")
          halls = []
          for d in data:
            halls.append(Salon.from_dict(d))
          return halls
def save_files(halls):
    halls_data=[]
    for d in halls:
        halls_data.append(d.to_dict())
    save_data("salon.json", halls_data)
def admin_panel(admin):
    while True:
        choice = input(
            "1-add user\n"
            "2-view user\n"
            "3-activate/deactivate user\n"
            "4-edit user\n"
            "5-add hall\n"
            "6-view hall\n"
            "7-activate/deactivate hall\n"
            "8-log out\n"
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
            found=False
            username=input("input your username : ").strip()
            try:
                all_users=UserRepository.allusers()
                for u in all_users:
                    if u.username==username:
                        found=True
                        new_name = input(f"New name ({u.name}): ").strip()
                        new_email = input(f"New email ({u.email}): ").strip()
                        if new_name :
                            u.name = new_name  
                        if new_email:
                            if "@" in new_email and "." in new_email:
                                u.email = new_email
                            else:
                                print("email is in invalid format")
                        UserRepository.save_all(all_users)
                        print("user update")
                        break
                if not found:
                    print("user not found")
            except ClubError as e :
                print("Error:", e)
        elif choice =="5":
            name=input("hall name").strip() 
            try:
                capacity=int(input("enter capacity : "))
                if capacity<=0:
                    print("capacity must more than 0 ")
                    continue
                halls=load_hall()
                found=False
                for h in halls :
                    if h.name==name:
                        found=True
                if found:
                    print("hall already exist")
                    continueلهف
            except ValueError:
                print("capacity must be number")
                continue

            text = input("Equipments (comma separated): ")
            equipments = [e.strip() for e in text.split(",")]
            new_hall=Salon.from_dict({"name": name, "capacity": capacity,"equipments": equipments, "is_active": True})
            halls.append(new_hall)
            save_files(halls)
            print("Hall added.")                         

        elif choice == "6":
            try:
                halls = load_hall()
            except ClubError as e:
                print("Error:", e)
                continue
            if not halls:
                print("No halls found.")
            for h in halls:
                equipments=", ".join(h.equipments)
                if h.is_active:
                    status = "active"
                else:
                    status = "inactive"
                print(f"{h.name} | capacity: {h.capacity} | {equipments} | {status}")
        elif choice =="7":
            name = input("Enter hall name  to activate/deactivate: ").strip()
            try:
                all_halls = load_hall()
                found = False
                for h in all_halls:
                    if h.name == name:
                        found = True
                        h.is_active = not h.is_active
                        save_files(all_halls)
                        print(f"User {h.name} is now {'active' if h.is_active else 'inactive'}.")
                        break
                if not found:
                    print("hall not found.")
            except ClubError as e:
                print("Error:", e)
        elif choice == "8":
            return
        else:
            print("invalid choice")
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
