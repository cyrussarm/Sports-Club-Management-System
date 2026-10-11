from Repositories.users_repository import UserRepository
from core.exceptions import ClubError
from services.add_user import add_user
from core.storage import load_data, save_data
from core.models import Salon,SportClass
def load_class():
    data=load_data("SportClass.json")
    classes = []
    for c in data :
        classes.append(SportClass.from_dict(c))    
    return classes
def save_class(classes):
    class_data=[]
    for c in classes:
        class_data.append(c.to_dict())
    save_data("SportClass.json", class_data)
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
def load_subscriptions():
    return load_data("subscription.json")


def show_reports():
    users = UserRepository.allusers()
    classes = load_class()
    subscriptions = load_subscriptions()

    # --- basic reports ---
    active_members = 0
    active_coaches = 0
    for u in users:
        if u.is_active and u.role == "member":
            active_members += 1
        if u.is_active and u.role == "coach":
            active_coaches += 1

    active_classes = 0
    for c in classes:
        if c.is_active:
            active_classes += 1

    total_revenue = 0
    for s in subscriptions:
        total_revenue += s["amount"]

    print("===== Reports =====")
    print(f"Active members: {active_members}")
    print(f"Active coaches: {active_coaches}")
    print(f"Active classes: {active_classes}")
    print(f"Total revenue: {total_revenue}")

    # --- advanced: revenue per subscription type ---
    revenue_by_type = {}
    for s in subscriptions:
        sub_type = s["subscription_type"]
        if sub_type not in revenue_by_type:
            revenue_by_type[sub_type] = 0
        revenue_by_type[sub_type] += s["amount"]

    print("----- Revenue by subscription -----")
    if not revenue_by_type:
        print("No subscriptions yet.")
    for sub_type, amount in revenue_by_type.items():
        print(f"{sub_type}: {amount}")

    # --- advanced: most popular class ---
    print("----- Most popular class -----")
    best_class = None
    for c in classes:
        if best_class is None or len(c.enrolled) > len(best_class.enrolled):
            best_class = c
    if best_class is None:
        print("No classes yet.")
    else:
        print(f"{best_class.title} ({len(best_class.enrolled)} members)")


def export_people_txt():
    users = UserRepository.allusers()
    with open("people.txt", "w", encoding="utf-8") as file:
        file.write("All people of the club\n")
        file.write("======================\n")
        for u in users:
            if u.is_active:
                status = "active"
            else:
                status = "inactive"
            file.write(f"{u.name} | {u.username} | {u.role} | {u.email} | {status}\n")
        file.write(f"\nTotal people: {len(users)}\n")
    print("people.txt created.")


def find_active_hall(hall_name):
    for h in load_hall():
        if h.name == hall_name:
            if not h.is_active:
                print("Hall is not active.")
                return None
            return h
    print("Hall not found.")
    return None


def find_active_coach(username):
    for u in UserRepository.allusers():
        if u.username == username:
            if u.role != "coach":
                print("This user is not a coach.")
                return None
            if not u.is_active:
                print("Coach is not active.")
                return None
            return u
    print("Coach not found.")
    return None


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
            "8-view classes\n"
            "9-add class\n"
            "10-edit class\n"
            "11-activate/deactivate class\n"
            "12-reports\n"
            "13-export people to txt\n"
            "14-log out\n"
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
            name = input("Hall name: ").strip()
            if not name:
                print("Hall name cannot be empty.")
                continue
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
                    continue
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
            try:
                classes = load_class()
            except ClubError as e:
                print("Error:", e)
                continue
            if not classes:
                print("No classes found.")
            for c in classes:
                if c.is_active:
                    status = "active"
                else:
                    status = "inactive"
                print(f"{c.title} | {c.sport_type} | coach: {c.coach_username} | hall: {c.hall_name} | {c.day} {c.time} | {len(c.enrolled)}/{c.capacity} | {status}")
        elif choice == "9":
            hall_name = input("Hall name: ").strip()
            hall = find_active_hall(hall_name)
            if hall is None:
                continue

            coach_username = input("Coach username: ").strip()
            coach = find_active_coach(coach_username)
            if coach is None:
                continue

            title = input("Class title: ").strip()
            if not title:
                print("Class title cannot be empty.")
                continue
            classes = load_class()
            found = False
            for c in classes:
                if c.title == title:
                    found = True
            if found:
                print("Class already exists.")
                continue
            sport_type = input("Sport type: ").strip()
            day = input("Day: ").strip()
            time = input("Time: ").strip()

            try:
                capacity = int(input("Capacity: "))
            except ValueError:
                print("Capacity must be a number.")
                continue
            if capacity <= 0:
                print("Capacity must be greater than zero.")
                continue
            if capacity > hall.capacity:
                print(f"Capacity cannot be more than hall capacity ({hall.capacity}).")
                continue

            new_class = SportClass.from_dict({
                "title": title, "sport_type": sport_type,
                "coach_username": coach_username, "hall_name": hall_name,
                "day": day, "time": time, "capacity": capacity,
                "enrolled": [], "is_active": True})
            classes.append(new_class)
            save_class(classes)
            print("Class added.")
        elif choice == "10":
            title = input("Class title to edit: ").strip()
            classes = load_class()
            cls = None
            for c in classes:
                if c.title == title:
                    cls = c
            if cls is None:
                print("Class not found.")
                continue
            print("Press Enter to keep the current value.")

            new_hall_name = input(f"New hall ({cls.hall_name}): ").strip()
            if new_hall_name:
                hall = find_active_hall(new_hall_name)
                if hall is None:
                    continue
            else:
                hall = find_active_hall(cls.hall_name)
                if hall is None:
                    print("Current hall is not usable, choose another hall.")
                    continue

            new_coach = input(f"New coach ({cls.coach_username}): ").strip()
            if new_coach:
                if find_active_coach(new_coach) is None:
                    continue

            new_day = input(f"New day ({cls.day}): ").strip()
            new_time = input(f"New time ({cls.time}): ").strip()

            new_capacity = cls.capacity
            text = input(f"New capacity ({cls.capacity}): ").strip()
            if text:
                try:
                    new_capacity = int(text)
                except ValueError:
                    print("Capacity must be a number.")
                    continue
            if new_capacity <= 0:
                print("Capacity must be greater than zero.")
                continue
            if new_capacity > hall.capacity:
                print(f"Capacity cannot be more than hall capacity ({hall.capacity}).")
                continue
            if new_capacity < len(cls.enrolled):
                print(f"Capacity cannot be less than enrolled members ({len(cls.enrolled)}).")
                continue

            # all checks passed, now apply the changes
            cls.hall_name = hall.name
            if new_coach:
                cls.coach_username = new_coach
            if new_day:
                cls.day = new_day
            if new_time:
                cls.time = new_time
            cls.capacity = new_capacity
            save_class(classes)
            print("Class updated.")
        elif choice == "11":
            title = input("Class title: ").strip()
            classes = load_class()
            found = False
            for c in classes:
                if c.title == title:
                    found = True
                    c.is_active = not c.is_active
                    save_class(classes)
                    if c.is_active:
                        print(f"Class {c.title} is now active.")
                    else:
                        print(f"Class {c.title} is now inactive.")
                    break
            if not found:
                print("Class not found.")
        elif choice == "12":
            try:
                show_reports()
            except ClubError as e:
                print("Error:", e)
        elif choice == "13":
            try:
                export_people_txt()
            except ClubError as e:
                print("Error:", e)
        elif choice == "14":
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
def main():
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


if __name__ == "__main__":
    main()
