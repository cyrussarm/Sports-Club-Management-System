########################################################
#### مدیریت کاربران توسط ادمین
########################################################

from Repositories.users_repository import UserRepository
from Repositories.classes_repository import KelasRepository
from Repositories.halls_repository import SalonsRepository
from Repositories.wallet_repository import WalletRepository
from Repositories.subscriptions_repository import Subs_repository
from Repositories.transactions_repository import TransactionRepository
from Repositories.subscriptions_repository import Subs_repository
from Repositories.transactions_repository import TransactionRepository
from core.models import Subscription, Transaction
from datetime import datetime
from core.models import Wallet
from core.exceptions import ClubError
from services.validation import validate_user_registration
from core.models import Users, SportClass, Salon
from core.back import ask

ALLOWED_ROLES = ["admin"]

def generate_user_id(): 
    users = UserRepository.all()
    ids = []
    for u in users:
        if u.id is not None:
            ids.append(u.id)
    if ids:
        return max(ids) + 1
    return 1

def generate_wallet_id():    
    wallets = WalletRepository.all()
    ids = []
    for w in wallets:
        if w.id is not None:
            ids.append(w.id)
    if ids:
        return max(ids) + 1
    return 1
     
# مدیریت کاربران : افزودن مربی یا عضو
def add_user(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return None
    while True:
        user_role = ask("Enter user type (coach/member): ")
        if user_role in ["coach", "member"]:
            break
        else:
            print("Invalid user type. Please enter 'coach' or 'member'.")

    # برای نام در سند محدودیت ذکر نشده ولی چک میکنم که خالی نباشه
    name = ask("Enter name: ")
    username = ask("Enter username: ")
    password = ask("Enter password: ")
    email = ask("Enter email: ")
    if email=="":
        email = None
    # وارد کردن ایمیل اختیاری است ولی اگر وارد شد باید درست بودنش چک شود
    user_is_valid, msg = validate_user_registration(name, username, password, email)
    if not user_is_valid:
        print(msg)
        return None
    
    # تولید یک id برای کاربر
    user_id = generate_user_id()
    # ساخت یک شی
    user = Users.from_dict({"id":user_id, "name":name, "username":username, 
            "password":password,"email":email,"role":user_role,"is_active":True})
    try:
        # اضافه کردن شی جدید به مخزن کاربرها
        Reg = UserRepository.add(user)      
    except ClubError as e:
        print(f"Error: {e}")
        return None
    if not Reg:               
        print("Registration faild: username already exists")
        return None
    # اگر کاربر از نوع ممبر است (مربی نیست) براش یک کیف با موجودی صفر پول بساز
    # برای کیف پول یک آیدی هم تولید کن
    # برای ایجاد شی اول باید یک دیکشنری بسازیم
    if user.role == "member":
        wallet = Wallet.from_dict({
            "id": generate_wallet_id(),
            "member_username": user.username,
            "balance": 0.0
         })
        # بعد، دیکشنری را با متد اد والت ریپازیتوری به شی تبدیل کنیم
        WalletRepository.add(wallet)  

    print("User added successfully")     
    return user    
    
    
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
    username = ask("Enter username of the user to activate/deactivate: ")
    try:
        user = UserRepository.find_by_username(username)
        if user is None:
            print(f"no user found with username: {username}")
            return 
        else:
            if user.is_active:
                answer = ask("user is active. Deactivate?(Y/N)")
                if answer.lower()=="y":
                    UserRepository.deactivate(user.id)
                    print(f"User '{username}' deactivated.")
                    return
            else:
                answer = ask("user is not active. Activate?(Y/N)")
                if answer.lower()=="y":
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
    username = ask("Enter username of the user to edit: ")
    try:
        user = UserRepository.find_by_username(username)
        if user is None:
            print(f"no user found with username: {username}")
            return 
        new_name = ask(f"New name ({user.name}): ")
        new_email = ask(f"New email ({user.email}): ")
        new_pass = ask(f"New password : ")
        activity = "active" if user.is_active else "inactive"
        print(f"current activity is: {activity} ")
        new_activity = ask("Change activity? (Y/N)")
        
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
        id_ = max(int(h.id) for h in halls) + 1
    else:
        id_ = 1
    return id_
    
def add_hall(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return 
    while True:
        hall_name = ask("Hall name: ")
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
            capacity=int(ask("enter capacity : "))
            if capacity<=0:
                print("capacity must be a positive number")
                continue
            else:
                break 
        except ValueError:
            print("Capacity must be a number.")
    text = ask("Equipments (comma separated): ")
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
    hallname = ask("Enter name of the hall to activate/deactivate: ")
    try:
        hall = SalonsRepository.find_hall_by_name(hallname)
        if hall is None:
            print(f"no hall found with name: {hallname}")
            return 
        else:
            if hall.is_active:
                answer = ask("hall is active. Deactivate?(Y/N)")
                if answer.lower()=="y":
                    SalonsRepository.deactivate(hall.id)
                    print(f"hall '{hallname}' deactivated.")
                    return
            else:
                answer = ask("hall is not active. Activate?(Y/N)")
                if answer.lower()=="y":
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
        id_ = max(int(c.id) for c in classes) + 1
    else:
        id_ = 1
    return id_

def add_class(current_role):
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return

    #پیش از ایجاد کلاس بررسی شود که سالن وجود داشته باشد و فعال باشد
    while True:
        hall_name = ask("Hall name: ")
        if hall_name:
            break
        print("Hall name cannot be empty.")
    try:
        found_hall = SalonsRepository.find_hall_by_name(hall_name)
    except ClubError as e:
        print(f"Error: {e}")
        return
    if found_hall is None:          
        print("Hall not found ")
        return
    elif not found_hall.is_active:
        print("Hall is not active.")
        return
    #پیش از ایجاد کلاس بررسی شود که مربی وجود داشته باشد و فعال باشد
    while True:
        coach_username = ask("Coach username: ")
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
        title = ask("Class title: ")      
        if not title:
            print("Class title cannot be empty.")
            continue
        else:
            break
    try:
        found_class = KelasRepository.find_by_title(title)
    except ClubError as e:
        print(f"Error: {e}")
        return
    if found_class:
        print("Class already exists.")
        return

    while True:   
        try:            
            capacity = int(ask("enter capacity : "))
            if capacity <= 0:
                print("capacity must be a positive number")
                continue           
            break 
        except ValueError:
            print("Capacity must be a number.")  

    while True:
        sport_type = ask("Sport type: ")
        if not sport_type:
            print("sport type cannot be empty.")            
        else:
            break
    while True:
        day = ask("Day: ")
        if not day:
            print("day cannot be empty.")            
        else:
            break
    while True:
        class_time = ask("Time: ")
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
        title = ask("Class title to edit: ")
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
    new_title = ask(f"New title ({target_class.title}, Enter to keep): ")
    if not new_title:
        new_title = target_class.title

    # نوع ورزش
    new_sport = ask(f"New sport type ({target_class.sport_type}, Enter to keep): ")
    if not new_sport:
        new_sport = target_class.sport_type

    # سالن
    new_hall_name = ask(f"New hall name ({target_class.hall_name}, Enter to keep): ")
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

    new_coach = ask(f"New coach ({target_class.coach_username}, Enter to keep): ")
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
    day_input = ask(f"New day ({target_class.day}, Enter to keep): ")
    if day_input:
        new_day = day_input

    new_time = target_class.time
    time_input = ask(f"New time ({target_class.time}, Enter to keep): ")
    if time_input:
        new_time = time_input

    # ظرفیت
    new_capacity = target_class.capacity
    text = ask(f"New capacity ({target_class.capacity}, Enter to keep): ")
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

    classid = ask("Enter id of the class to activate/deactivate: ")
       
    try:
        class_ = KelasRepository.find_by_id(classid)
        if class_ is None:
            print(f"no class found with id: {classid}")
            return 
        else:
            if class_.is_active:
                answer = ask("class is active. Deactivate?(Y/N)")
                if answer.lower()=="y":
                    KelasRepository.deactivate(class_.id)
                    print(f"class '{class_.title}' deactivated.")
                    return
            else:
                answer = ask("class is not active. Activate?(Y/N)")
                if answer.lower()=="y":
                    KelasRepository.activate(class_.id)
                    print(f"class '{class_.title}' activated.")
                    return
    except ClubError as e:
        print(f"Error:, {e}")
        return

# ویرایش سالن
def edit_hall(current_role):
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return

    hall_name = ask("Enter hall name to edit: ")
    try:
        hall = SalonsRepository.find_hall_by_name(hall_name)
    except ClubError as e:
        print(f"Error: {e}")
        return

    if hall is None:
        print(f"No hall found with name: {hall_name}")
        return

    print(f"Editing hall: {hall.name}")
    print("Press Enter to keep current value.")

    new_name = ask(f"New name ({hall.name}): ")
    if not new_name:
        new_name = hall.name
    else:       
        try:
            existing = SalonsRepository.find_hall_by_name(new_name)
        except ClubError as e:
            print(f"Error: {e}")
            return
        if existing is not None and existing.id != hall.id:
            print(f"Error: another hall with name '{new_name}' already exists.")
            return
    
    new_capacity = hall.capacity
    cap_input = ask(f"New capacity ({hall.capacity}): ")
    if cap_input:
        try:
            new_capacity = int(cap_input)
        except ValueError:
            print("Capacity must be a number.")
            return
        if new_capacity <= 0:
            print("Capacity must be greater than zero.")
            return
    
    current_equip = ", ".join(hall.equipments) if hall.equipments else "(none)"
    print(f"Current equipments: {current_equip}")
    equip_input = ask("New equipments (comma separated, Enter to keep): ")
    if equip_input:
        new_equipments = [e.strip() for e in equip_input.split(",") if e.strip()]
    else:
        new_equipments = hall.equipments

    new_hall = Salon.from_dict({
        "id": hall.id,
        "name": new_name,
        "capacity": new_capacity,
        "equipments": new_equipments,
        "is_active": hall.is_active,
    })

    try:
        if SalonsRepository.update(new_hall):
            print(f"  Hall '{hall.name}' updated successfully.")
            print(f" Name: {new_hall.name}")
            print(f" apacity: {new_hall.capacity}")
            if new_hall.equipments:
                print(f" Equipments: {', '.join(new_hall.equipments)}")
        else:
            print("Failed to update hall.")
    except ClubError as e:
        print(f"Error: {e}")


# ---------------------------------------------------------------
# مدیریت اشتراک‌ها
# ---------------------------------------------------------------

# لیست پلن های اشتراک
# سه پلن اشتراک 1 ماه، 3 ماه و 6 ماه در فایل ذخیره شده اند
def load_subscription_plans():    
    from core.storage import load_data
    return load_data("subscription_plans.json")

# تولید آی دی یکتا برای هر اشتراک
def generate_subscription_id():    
    eshtarak_id = 1
    eshtarakha = Subs_repository.all()
    if eshtarakha:
        eshtarak_id =   max(int(eshtarak.id) for eshtarak in eshtarakha) + 1
    return eshtarak_id

# ایجاد اشتراک جدید
def register_subscription_for_member(current_role):   
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return
    
    username = ask("Enter member username (case-sensitive ast): ")
    member = UserRepository.find_by_username(username)
    if member is None:
        print(f"No user found with username: {username}")
        return
    if member.role != "member":
        print(f"{username} is not a member (role: {member.role}).")
        return
    if not member.is_active:
        print(f"{username} is inactive.")
        return
   
    plans = load_subscription_plans()
    if not plans:
        print("No subscription plans available.")
        return

    print("\n===== Subscription Plans =====")
    for p in plans:
        print(f"  {p['id']}. {p['name']} | "
              f"{p['duration_months']} months | "
              f"price: {p['price']}")

    #  انتخاب پلن
    while True:
        try:
            plan_id = int(ask("Select plan id (or 0 to back): "))
            if plan_id == 0:
                return
            selected_plan = None
            for plan in plans:
                if plan["id"]==plan_id:
                    selected_plan = plan
                    break              

            if selected_plan is None:
                print("Invalid plan id.")
                continue
            break
        except ValueError:
            print("Plan id must be a number.")
    
    today_date = datetime.now() 
    duration = selected_plan["duration_months"]  
    new_month = today_date.month + duration
    new_year = today_date.year + (new_month - 1) // 12
    new_month = (new_month - 1) % 12 + 1
    end_date = today_date.replace(year=new_year, month=new_month)

    # تولید کد اشتراک  
    # ممکنه احتمال تکراری شدنش باشه 
    # البته id کاربر همیشه یونیکه  
    subscription_code= f"SUB-{member.id}-{member.username}"
    dict_ = {"id": generate_subscription_id(),"member_username": member.username,
        "subscription_type": selected_plan["name"], "amount": selected_plan["price"],
        "payment_date": today_date.strftime("%Y-%m-%d"), "start_date": today_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"), "subscription_code": subscription_code,
        "subscription_state": "active"}
    
    subscription = Subscription.from_dict(dict_)
    
    try:
        Subs_repository.add(subscription)
        print(f"\n Eshterak Sabt Shod for {member.username}")
        print(f"   Type: {subscription.subscription_type}")
        print(f"   Amount: {subscription.amount}")
        print(f"   Start: {subscription.start_date}")
        print(f"   End: {subscription.end_date}")
        print(f"   subscription_code: {subscription.subscription_code}")
    except ClubError as e:
        print(f"Error: {e}")
        return
    
    try:
        transaction_ID = f"TRA-{member.id}-{member.username}"
        transaction = Transaction.from_dict({
            "id":transaction_ID,
            "user_id": member.username,
            "amount": selected_plan["price"],
            "subscription_name": selected_plan["name"],
            "duration_months": selected_plan["duration_months"],
            "start_date": today_date.isoformat(),
            "end_date": end_date.isoformat(),
            "status": "success"
        })
        TransactionRepository.add(transaction)
    except ClubError as e:
        print(f"Warning: transaction log failed: {e}")


def view_all_payments(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return

    try:
        transactions = TransactionRepository.all()
        if not transactions:
            print("No transactions found.")
            return

        print("\n===== All Payments =====")
        for trans in transactions:
           
            user = UserRepository.find_by_username(trans.user_id)
            if user:
                print(f"id = {trans.id}  |")
                print(f"name = {user.name}  |") 
                print(f"amount = {trans.amount} \n") 
                print(f"date = {trans.start_date.strftime('%Y-%m-%d')}  |") 
                print(f"status = {trans.status}  |")                    
    except ClubError as e:
        print(f"Error: {e}")


def view_subscriptions_status(current_role):    
    if current_role.lower() not in ALLOWED_ROLES:
        print("Only the admin is authorized to do this.")
        return

    try:
        members = UserRepository.list_of_given_role("member")
        if not members:
            print("No members found.")
            return

        all_subs = Subs_repository.all()
        now = datetime.now()

        print("\n===== Subscriptions Status =====")
        for member in members:
            member_subs = [s for s in all_subs
                           if s.member_username == member.username
                           and s.subscription_state == "active"]

            if not member_subs:
                print(f"{member.name} ({member.username}): no-subscription")
                continue

            latest = member_subs[-1]
            # بررسی انقضا
            try:
                end_date = datetime.strptime(latest.end_date, "%Y-%m-%d")
                if end_date < now:
                    state = "expired"
                else:
                    state = "active"
            except ValueError:
                state = latest.subscription_state

            print(f"{member.name} ({member.username}): "
                  f"{latest.subscription_type} | "
                  f"until {latest.end_date} | "
                  f"{state}")
    except ClubError as e:
        print(f"Error: {e}")