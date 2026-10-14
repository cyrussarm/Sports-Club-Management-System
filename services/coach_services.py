from Repositories.classes_repository import KelasRepository
from core.exceptions import ClubError

# مشاهده کلاس
def view_coach_class(coach_username): 
    try:
        classes = KelasRepository.list_active_classes_by_coach(coach_username)
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
              f" remaind capacity: {c.remaining_capacity()}/ | state: {status}\n")
    except ClubError as e: # فایل خالی یا خطا
        print (f"Error: {e}")
        return 
    return classes

# تنظیم برنامه تمرین
def manage_exercise_plans(coach_username):
    # انتخاب کلاس    
    class_ids = view_coach_class(coach_username)
    class_ids = [obj_.id for obj_ in class_ids]

    while True:
        target_class_id = int(input("Enter the target class id").strip())
        if target_class_id and not target_class_id in class_ids:
            inp_=input("Invalid id, enter again? (Y/N)").strip().lower()
            if inp_=="n":
                return None
        else:
            break
    try:
        target_class = KelasRepository.find_by_id(target_class_id)
        class_members = target_class.enrolled
        for m in class_members:
            print(f"class id: {m.id} | class name: {m.title} | \n")
            print(f"class members:")
            print(f"{m.enrolled}")
    except:
        print("hichi")
    while True:
        target_member_id = int(input("Enter the target class id").strip())
        if target_class_id and not target_class_id in class_ids:
            inp_=input("Invalid id, enter again? (Y/N)").strip().lower()
            if inp_=="n":
                return None
        else:
            break

            
        



        