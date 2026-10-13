
from panels.adminLogin import admin_login, admin_panel


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
                admin_panel()
            else:
                print("Invalid admin credentials.")
        elif choice == "2":
            pass
            # coach_username = input("Enter coach username: ").strip()
            # coach_password = input("Enter coach password: ").strip()
            # print("Coach login functionality is not implemented yet.")
        elif choice == "3":
            pass
            # member_username = input("Enter member username: ").strip()
            # member_password = input("Enter member password: ").strip()
            # print("Member login functionality is not implemented yet.")
        elif choice == "4" :
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__=="__main__":
    main()
