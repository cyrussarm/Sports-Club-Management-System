
from panels.menus import login, admin_panel, coach_panel, member_panel
def main():  
    
    while True:
        choice = input(
            "1-admin login\n"
            "2-coach login\n"
            "3-member login\n"
            "4-exit\n"
            "Select: ").strip()
        if choice == "1":
            admin = login("admin")
            if admin is not None:   
                admin_panel(admin.username)
            else:
                print("Invalid admin credentials.")
        elif choice == "2":
            coach = login("coach")
            if coach:       
                coach_panel(coach.username)
            else:
                print("Invalid coach")
        elif choice == "3":            
            member = login("member")
            if member:
                member_panel(member.username)
            else:
                print("Invalid member")
        elif choice == "4" :
            print("Exiting the program.")
            break            
        else:
            print("Invalid choice. Please try again.")
    

if __name__=="__main__":
    main()
