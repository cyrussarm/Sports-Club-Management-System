from services.adminServices import (
    add_user, view_users, change_activity_user, edit_user,
    add_hall, view_hall, change_activity_hall, edit_hall,
    view_class, add_class, edit_class, change_activity_class, 
    register_subscription_for_member,  view_all_payments,                     
    view_subscriptions_status
)

from services.member_services import(wallet_menu, view_profile_and_subscription,
    view_available_classes, view_my_exercise_plan, sabtenam_class,  
    cancel_sabtenam_class, view_my_enrollments)
from services.coach_services import view_coach_class, manage_exercise_plans
from services.reports import show_reports, export_people_txt
from services.member_services import wallet_menu, view_profile_and_subscription,view_available_classes, view_my_exercise_plan
from Repositories.users_repository import UserRepository
from core.exceptions import ClubError

# بررسی لاگین 
def login(role_):    
    if role_ not in ("admin", "coach", "member"):
        print(f"Unknown role: {role_}")
        return None
    try: # اگر در خواندن اطلاعات کاربران از دیتابیس (همان فایل) خطایی رخ ندهد
        all_users = UserRepository.all()
    except ClubError as e:
        print(f"Error: {e}")
        return None    
    while True:
        # آیا بین کاربرها ادمین با این مشخصات هست یا نه؟
        # فرض : ادمین قبل از اجرای کد رجیستر کرده و اطلاعاتش در فایل یوزرز هست
        username = input(f"Enter {role_} username: ").strip()
        password = input(f"Enter {role_} password: ").strip()
        for user in all_users:  
            if (user.username == username and
                user.password == password and
                user.role == role_):
                if not user.is_active:
                    print("This account is inactive.")
                    return None
                return user
        # اگر ورود موفق نبود امکان تکرار مجدد وجود داشته باشد        
        choice = input(f"Invalid {role_} login. Try again? (y/n): ").strip().lower()
        if choice != "y":
            return None 
    
def admin_panel(username):
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
            "14-register subscription\n"         
            "15-view all payments\n"             
            "16-view subscriptions status\n" 
            "17-edit hall\n"    
            "18-log out\n"                       
        ).strip()
        
        if choice == "1":   # add user
            new_user = add_user("admin")
            if new_user is not None:
                print(f"new user created: id: {new_user.id}, name: {new_user.name}")
            else:
                print("new user registration failed")
            
        elif choice == "2": # view user
            view_users("admin")                      
            
        elif choice == "3": # activate/deactivate user
            change_activity_user("admin") 
            
        elif choice == "4": # edit user
            edit_user("admin")
            
        elif choice =="5": # add hall
            add_hall("admin")                            

        elif choice == "6": # view hall
            view_hall("admin")
            
        elif choice =="7": # activate/deactivate hall
            change_activity_hall("admin")
            
        elif choice == "8": # view classes
            view_class("admin")
          
        elif choice == "9": # add class
            add_class("admin")
            
        elif choice == "10": # edit class
            edit_class("admin")
            
        elif choice == "11": # activate/deactivate class
            change_activity_class("admin")
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
            try:
                register_subscription_for_member("admin")
            except ClubError as e:
                print("Error:", e)

        elif choice == "15":
            try:
                view_all_payments("admin")
            except ClubError as e:
                print("Error:", e)
        elif choice == "16":
            try:
                view_subscriptions_status("admin")
            except ClubError as e:
                print("Error:", e)

        elif choice == "17":
            try:
                edit_hall("admin")
            except ClubError as e:
                print("Error:", e)

        elif choice == "18":
            return
        else:
            print("invalid choice")    

def coach_panel(username):
    while True:
        choice = input(
            "1-show my classes\n"
            "2-manage exercise plans\n"
            "3-log out\n"
        ).strip()

        if choice == "1":  
            view_coach_class(username)
        elif choice == "2":
            manage_exercise_plans(username)
        elif choice == "3":
            return
        else:
            print("invalid choice")  

def member_panel(member_username):
    while True:
        choice = input(
        "1-profile & subscription\n"   
        "2-wallet\n"                  
        "3-classes\n"                  
        "4-enroll in class\n"           
        "5-my enrollments\n"             
        "6-cancel enrollment\n"           
        "7-exercise plan\n"            
        "8-log out\n"
            ).strip()

        if choice == "1":
            view_profile_and_subscription(member_username)
        elif choice == "2":
            wallet_menu(member_username)
        elif choice == "3":
            view_available_classes(member_username)
        elif choice == "4":
            sabtenam_class(member_username)
        elif choice == "5":
            view_my_enrollments(member_username)
        elif choice == "6":
            cancel_sabtenam_class(member_username)
        elif choice == "7":
            view_my_exercise_plan(member_username)
        elif choice == "8":
            return
        else:
            print("Invalid choice.")

          

