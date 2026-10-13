########################################################
#### مدیریت کاربران توسط ادمین
########################################################

from Repositories.users_repository import UserRepository
from Repositories.KelasRepository import KelasRepository
from Repositories.HallsRepository import SalonsRepository
from Repositories.SubscriptionsRepository import SubsRepository
from Repositories.TransactionRepository import TransactionRepository
from core.exceptions import ClubError
from services.validation import validate_user_registration
from core.models import Users, SportClass, Salon

ALLOWED_ROLES = ("admin",)

def generate_user_id():
    user_id = 1
    try:
        users = UserRepository.all()
        return max(user.id for user in users)+1
    except ClubError: # فایل خالی یا خطا
        return user_id

# مدیریت کاربران : افزودن مربی یا عضو
def add_user(current_role):    
    if not current_role.lower() in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return None
    while True:
        user_role = input("Enter user type (coach/member): ").strip().lower()
        if user_role in ["coach", "member"]:
            break
        else:
            print("Invalid user type. Please enter 'coach' or 'member'.")

        # برای نام در سند محدودیت ذکر نشده ولی چک میکنم که خالی نباشه
        name = input("Enter name: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        email = input("Enter email: ").strip() 
        if email=="":
            email = None
        # وارد کردن ایمیل اختیاری است ولی اگر وارد شد باید درست بودنش چک شود
        user_is_valid, msg = validate_user_registration(name, username, password, email)
        if user_is_valid:
            user_id = generate_user_id()
            user = Users.from_dict({"id":user_id, "name":name, "username":username, 
                    "password":password,"email":email,"role":user_role,"is_active":True})
            try:
                Reg = UserRepository.add(user)
                if Reg:
                    print("User added successfully")
                    return user
                else:
                    print("Registration faild: username already exists")
                    return None
            except ClubError as e:
                print (f"Error:{e}")
                return None
        else:
            print(msg)
            return None

# نمایش همه کاربران
def view_users(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    try:
        users = UserRepository.all()
        if not users:
            print("No users found.")
            return
        for u in users:
            if u.is_active:
                status = "active"
            else:
                status = "inactive"
            print(f"{u.name} | {u.username} | {u.role} | {u.email} | {status}")        
    except ClubError as e: # فایل خالی یا خطا
        print (f"Error:{e}")
        return

# فعال/غیرفعال کردن کاربر
def change_activity_user(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    username = input("Enter username of the user to activate/deactivate: ").strip()
    try:
        user = UserRepository.find_by_username(username)
        if user is None:
            print(f"no user found with username: {username}")
            return 
        else:
            if user.is_active:
                do_ = input("user is active. Deactivate?(Y/N)").strip()
                if do_.lower()=="y":
                    UserRepository.deactivate(user.id)
                    print(f"User '{username}' deactivated.")
                    return
            else:
                do_ = input("user is not active. Activate?(Y/N)").strip()
                if do_.lower()=="y":
                    UserRepository.activate(user.id)
                    print(f"User '{username}' activated.")
                    return
    except ClubError as e:
        print("Error:", e)
        return

# ویرایش کاربر
def edit_user(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    username = input("Enter username of the user to edit: ").strip()
    try:
        user = UserRepository.find_by_username(username)
        if user is None:
            print(f"no user found with username: {username}")
            return 
        new_name = input(f"New name ({user.name}): ").strip()
        new_email = input(f"New email ({user.email}): ").strip()
        new_pass = input(f"New password ({user.password}): ").strip()
        activity = "active" if user.is_active else "inactive"
        print(f"current activity is: {activity} ")
        new_activity = input("Change activity? (Y/N)").strip().lower()
        
        name_=user.name
        if new_name :
            name_ = new_name 
        email_=user.email 
        if new_email:
            email_ = new_email
        password_=user.password
        if new_pass:
            password_ = new_pass
        is_valid, msg = validate_user_registration(name_,username,password_,email_)
        if not is_valid:
            print(msg)
            return
        new_user = Users.from_dict({"id":user.id, "name":name_, "username":username, 
                    "password":password_,"email":email_,"role":user.role,"is_active":user.is_active})         
        if new_activity=="y":
            new_user.is_active = not new_user.is_active
        if UserRepository.update(new_user):
            print("user updated successfully.")  
        else:
            print("Failed to update user.") 
    except ClubError as e:
        print("Error:", e)
        return

# افزودن سالن
# تولید id سالن
def generate_hall_id():
    halls = SalonsRepository.all()
    if halls:
        id_ = max(h.id for h in halls) + 1
    else:
        id_ = 1
    return id_
    
def add_hall(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    while True:
        hall_name = input("Hall name: ").strip()
        if hall_name:
            break
        print("Hall name cannot be empty.")
    try:
        found = SalonsRepository.find_hall_by_name(hall_name)
    except ClubError as e:
        print(f"Error: {e}")
        return
    if found is not None:          
        print("hall already exist")
        return

    # مشخصات سالن جدید را بگیر 
    while True:
        try:
            capacity=int(input("enter capacity : ").strip())
            if capacity<=0:
                print("capacity must be a positive number")
                continue
            else:
                break 
        except ValueError:
            print("Capacity must be a number.")
    text = input("Equipments (comma separated): ")
    equipments = [e.strip() for e in text.split(",") if e.strip()] if text else []  
    try:    
        dict_ = {"id": generate_hall_id(),"name": hall_name, "capacity": capacity,"equipments": equipments, "is_active": True}    
        new_hall=Salon.from_dict(dict_)
        
        if SalonsRepository.add(new_hall):
            print("Hall added successfully.")
        else:
            print("Failed to add hall.")
    except ClubError as e:
        print(f"Error: {e}")   

# مشاهده سالن
def view_hall(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    try:
        halls = SalonsRepository.all()
        if not halls:
            print("No halls found.")
            return
        for h in halls:
            equipments = ", ".join(h.equipments) if h.equipments else "—"
            if h.is_active:
                status = "active"
            else:
                status = "inactive"
            print(f"{h.name} | capacity: {h.capacity} | {equipments} | {status}")
    except ClubError as e: # فایل خالی یا خطا
        print (f"Error: {e}")
        return 

# فعال/غیرفعال کردن سالن
def change_activity_hall(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    hallname = input("Enter name of the hall to activate/deactivate: ").strip()
    try:
        hall = SalonsRepository.find_hall_by_name(hallname)
        if hall is None:
            print(f"no hall found with name: {hallname}")
            return 
        else:
            if hall.is_active:
                do_ = input("hall is active. Deactivate?(Y/N)").strip()
                if do_.lower()=="y":
                    SalonsRepository.deactivate(hall.id)
                    print(f"hall '{hallname}' deactivated.")
                    return
            else:
                do_ = input("hall is not active. Activate?(Y/N)").strip()
                if do_.lower()=="y":
                    SalonsRepository.activate(hall.id)
                    print(f"Hall '{hall.name}' activated.")
                    return
    except ClubError as e:
        print(f"Error:, {e}")
        return

# مشاهده کلاس
def view_class(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    try:
        classes = KelasRepository.all()
        if not classes:
            print("No classes found.")
            return
        for c in classes:
            if c.is_active:
                status = "active"
            else:
                status = "inactive"
            
            print(f"class id: {c.id} | class name: {c.title} | sport type: {c.sport_type} | coach: {c.coach_name} | "
              f" coach_username: {c.coach_username} | hall: {c.hall_name} | "
              f"day:{c.day} | time: {c.time} | capacity: {c.capacity} | "
              f" remaind capacity: {c.remaining_capacity()}/ | state: {status}")
    except ClubError as e: # فایل خالی یا خطا
        print (f"Error: {e}")
        return 

# افزودن کلاس
def generate_class_id():
    classes = KelasRepository.all()
    if classes:
        id_ = max(c.id for c in classes) + 1
    else:
        id_ = 1
    return id_
def add_class(current_role):
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return

    #پیش از ایجاد کلاس بررسی شود که سالن وجود داشته باشد و فعال باشد
    while True:
        hall_name = input("Hall name: ").strip()
        if hall_name:
            break
        print("Hall name cannot be empty.")
    try:
        found = SalonsRepository.find_hall_by_name(hall_name)
    except ClubError as e:
        print(f"Error: {e}")
        return
    if found is None:          
        print("Hall not found ")
        return
    elif not found.is_active:
        print("Hall is not active.")
        return
    #پیش از ایجاد کلاس بررسی شود که مربی وجود داشته باشد و فعال باشد
    while True:
        coach_username = input("Coach username: ").strip()
        if coach_username:
            break
        print("coach username cannot be empty.")    
    try:
        print(coach_username)
        coach = UserRepository.find_active_with_username_and_role("coach",coach_username)         
    except ClubError as e:
        print(f"Error: {e}")
        return
    if coach is None:
        print("Coach not found")
        return 
    if not coach.is_active:
        print("Coach is not active")
        return 
    
    #     
    
    while True:       
        title = input("Class title: ").strip()        
        if not title:
            print("Class title cannot be empty.")
            continue
        else:
            break
    try:
        found = KelasRepository.find_by_title(title)
    except ClubError as e:
        print(f"Error: {e}")
        return
    if found:
        print("Class already exists.")
        return

    while True:   
        try:
            capacity=int(input("enter capacity : ").strip())
            if capacity<=0:
                print("capacity must be a positive number")
                continue
            else:
                break 
        except ValueError:
            print("Capacity must be a number.")  

    while True:
        sport_type = input("Sport type: ").strip()
        if not sport_type:
            print("sport type cannot be empty.")            
        else:
            break
    while True:
        day = input("Day: ").strip()
        if not day:
            print("day cannot be empty.")            
        else:
            break
    while True:
        class_time = input("Time: ").strip()
        if not class_time:
            print("time cannot be empty.")
        else:
            break
        
    new_class = SportClass.from_dict({"id":generate_class_id(),
                "title": title, "sport_type": sport_type, "coach_name": coach.name, 
                "coach_username": coach_username, "hall_name": hall_name,
                "day": str(day), "time": str(class_time), "capacity": capacity,
                "enrolled": [], "is_active": True})
    try:
        if KelasRepository.add(new_class):
            print("Class added.")
        else:
            print("class adding failed")
    except ClubError as e:
        print(f"Error: {e}")

# ویرایش کلاس
def edit_class(current_role):
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return

    while True:
        title = input("Class title to edit: ").strip()
        if title:
            break
        print("Title cannot be empty.")

    try:
        target_class = KelasRepository.find_by_title(title)
    except ClubError as e:
        print(f"Error: {e}")
        return

    if target_class is None:
        print("Class not found.")
        return

    # عنوان
    new_title = input(f"New title ({target_class.title}, Enter to keep): ").strip()
    if not new_title:
        new_title = target_class.title

    # نوع ورزش
    new_sport = input(f"New sport type ({target_class.sport_type}, Enter to keep): ").strip()
    if not new_sport:
        new_sport = target_class.sport_type

    # سالن
    new_hall_name = input(f"New hall name ({target_class.hall_name}, Enter to keep): ").strip()
    if new_hall_name:
        try:
            hall = SalonsRepository.find_active_hall(new_hall_name)
        except ClubError as e:
            print(f"Error: {e}")
            return
        if hall is None:
            print("Hall not found or inactive.")
            return
    else:
        try:
            hall = SalonsRepository.find_active_hall(target_class.hall_name)
        except ClubError as e:
            print(f"Error: {e}")
            return
        if hall is None:
            print("Current hall is inactive. Choose a new hall.")
            return
        new_hall_name = target_class.hall_name

    # مربی
    new_coach_name = target_class.coach_name
    new_coach_username = target_class.coach_username

    new_coach = input(f"New coach ({target_class.coach_username}, Enter to keep): ").strip()
    if new_coach:
        try:
            coach = UserRepository.find_active_with_username_and_role("coach", new_coach)
        except ClubError as e:
            print(f"Error: {e}")
            return
        if coach is None:
            print("Coach not found or inactive.")
            return
        new_coach_name = coach.name
        new_coach_username = coach.username

    # روز و ساعت
    new_day = target_class.day
    day_input = input(f"New day ({target_class.day}, Enter to keep): ").strip()
    if day_input:
        new_day = day_input

    new_time = target_class.time
    time_input = input(f"New time ({target_class.time}, Enter to keep): ").strip()
    if time_input:
        new_time = time_input

    # ظرفیت
    new_capacity = target_class.capacity
    text = input(f"New capacity ({target_class.capacity}, Enter to keep): ").strip()
    if text:
        try:
            new_capacity = int(text)
        except ValueError:
            print("Capacity must be a number.")
            return

    if new_capacity <= 0:
        print("Capacity must be greater than zero.")
        return
    if new_capacity > hall.capacity:
        print(f"Capacity cannot exceed hall capacity ({hall.capacity}).")
        return
    if new_capacity < len(target_class.enrolled):
        print(f"Capacity cannot be less than enrolled members ({len(target_class.enrolled)}).")
        return

    # ساخت شیء جدید
    new_class = SportClass.from_dict({
        "id": target_class.id,
        "title": new_title,
        "sport_type": new_sport,
        "coach_name": new_coach_name,
        "coach_username": new_coach_username,
        "hall_name": new_hall_name,
        "day": new_day,
        "time": new_time,
        "capacity": new_capacity,
        "enrolled": target_class.enrolled,
        "is_active": target_class.is_active,
    })

    try:
        if KelasRepository.update(new_class):
            print("Class updated successfully.")
        else:
            print("Failed to update class.")
    except ClubError as e:
        print(f"Error: {e}")

# فعال/غیرفعال کردن کلاس
def change_activity_class(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    classid = int(input("Enter id of the class to activate/deactivate: ").strip())
    try:
        class_ = KelasRepository.find_by_id(classid)
        if class_ is None:
            print(f"no class found with id: {classid}")
            return 
        else:
            if class_.is_active:
                do_ = input("class is active. Deactivate?(Y/N)").strip()
                if do_.lower()=="y":
                    KelasRepository.deactivate(class_.id)
                    print(f"class '{class_.name}' deactivated.")
                    return
            else:
                do_ = input("class is not active. Activate?(Y/N)").strip()
                if do_.lower()=="y":
                    KelasRepository.activate(class_.id)
                    print(f"class '{class_.name}' activated.")
                    return
    except ClubError as e:
        print(f"Error:, {e}")
        return
def get_all_members_subscriptions():
    #مشاهده وضعیت اشتراک همه اعضا
    return SubscriptionsRepository.get_all()

def get_all_transactions():
    #دریافت کل تراکنش ها و پرداخت ها
    return TransactionRepository.get_all()

def purchase_subscription_with_wallet(username, subscription_type, amount):
    # کنترل موجودی کیف پول و اگر اوکی بود خرید اشتراک
    wallet_balance = WalletServices.get_balance(username)
    
    if wallet_balance < amount:
        raise ValueError("The money in your wallet isn't enough, please top up")
    
    # ثبت تراکنش
    WalletServices.withdraw(username, amount)
    # ثبت اشتراک
    return True



def view_members_subscriptions(current_role):
    #برای گزارش وضعیت اشتراک اعضا برای مدیر
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is allowd to do this")
        return
    
    try:
        subscriptions = SubsRepository.get_all()
        if not subscriptions:
            print("No subscriptions found")
            return
            
        print("Member's subscriptions status:")
        for sub in subscriptions:
            print(f"username: {sub.member_username} | subscription's type: {sub.subscription_type} | End date :{sub.end_date} | Subscription's state: {sub.subscription_state}" )
        print("------------------------------")
    except ClubError as e:
        print(f"Error: {e}")

def view_all_financial_transactions(current_role):
    # مشاهده پرداخت ها و لیست مالی 
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is allowed to do this")
        return
        
    try:
        transactions = TransactionRepository.all_transactions() 
        if not transactions:
            print("There is no transaction")
            return
            
        print("All transactions : ")
        for t in transactions:
            print(f"id : {t.transaction_id} | user's id : {t.user_id} | amount :: {t.amount} | subscription's name : {t.subscription_name} | duration mounths : {t.duration_mounths} | status: {t.status}")
        print("------------------------------------------")
    except ClubError as e:
        print(f"Error: {e}")