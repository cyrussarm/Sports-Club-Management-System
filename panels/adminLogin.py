from services.adminServices import *
from services.reports import show_reports, export_people_txt

# بررسی لاگین ادمین
def admin_login():        
    # ذخیره همه کاربران موجود در فایل users.json به صورت لیستی از آبجکتها
    try: # اگر در خواندن اطلاعات کاربران از دیتابیس (همان فایل) خطایی رخ ندهد
        all_users = UserRepository.all()
    except ClubError as e:
        print(f"Error: {e}")
        return None
    while True:
        # آیا بین کاربرها ادمین با این مشخصات هست یا نه؟
        # فرض : ادمین قبل از اجرای کد رجیستر کرده و اطلاعاتش در فایل یوزرز هست
        username = input("Enter admin username: ").strip()
        password = input("Enter admin password: ").strip()
        for user in all_users:  
            if (user.username == username and
                user.password == password and
                user.role == "admin"):
                if not user.is_active:
                    print("This account is inactive.")
                    return None
                return user
        # اگر ورود موفق نبود امکان تکرار مجدد وجود داشته باشد        
        choice = input("Invalid admin credentials. Try again? (y/n): ").strip().lower()
        if choice != "y":
            return None 

def admin_panel():
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
            return
        else:
            print("invalid choice")      

