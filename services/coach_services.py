from Repositories.classes_repository import KelasRepository
from Repositories.users_repository import UserRepository
from Repositories.exercise_plan_repository import exercise_plan_repository
from core.models import Exercise, ExercisePlan
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

# تنظیم برنامه تمرین توسط مربی
def manage_exercise_plans(coach_username):
    # کلاس‌های مربی را نمایش بده   
    classes = view_coach_class(coach_username)
    if not classes:
        print("no class found")
        return

    class_ids = [obj_.id for obj_ in classes]

    
    while True:
        try:
            target_class_id = int(input("\nEnter class id (0 to cancel): ").strip())
        except ValueError:
            print("enter a number.")
            continue
        if target_class_id == 0:
            return
        if target_class_id not in class_ids:
            print("Invalid id. Try again.")
            continue
        break

    target_class = KelasRepository.find_by_id(target_class_id)

    class_members = target_class.enrolled
    if not class_members:
        print("no one enrolled in this class")
        return
    
    
    print(f"\n members of class: {target_class.title}:")
    for username in target_class.enrolled:
        member = UserRepository.find_by_username(username)
        if member:
            print(f"  name: {member.name} | username: ({member.username})")
        
    while True:
        member_username = input("Enter member username (0 to cancel)").strip()        
        if member_username == "0":
            return
        if member_username not in target_class.enrolled:
            print("This member not found in this class. Try again.")
            continue
        member = UserRepository.find_by_username(member_username)
        if not member:
            print("Member not found.")
            continue
        break

    workout_list = []
    while True:
        print(f"Enter workout : {len(workout_list)+1}")
        work_name = input("enter name of workout (0 to finish)").strip()
        if not work_name or work_name == "0":
            break

        while True:  
            try:
                set_numbers = input("enter number of sets:").strip()
                set_numbers = int(set_numbers)
                if set_numbers<=0:
                    print("you must enter a positive number")
                    continue
                break
            except ValueError:
                print("you must enter a number")
        
        while True:
            try:
                rep_numbers = input("enter repetition's number:").strip()
                rep_numbers = int(rep_numbers)
                if rep_numbers<=0:
                    print("you must enter a positive number")
                    continue
                break
            except ValueError:
                print("you must enter a number")
            
                    
        rest_times = input("enter rest times (for ex. (2 min.))").strip()
        if not rest_times:
            rest_times = "-"
        desc = input("any description/comment about this workout (optional)").strip()
        if not desc:
            desc = "-"

        dict_ = {"id":len(workout_list)+1, "name":work_name, "sets":set_numbers, 
                 "tekrars": rep_numbers, "rest_time":rest_times, "description": desc}    
        workout_list.append(Exercise.from_dict(dict_))
        print(f"'{work_name}' added.")

        inp_ = input("Add another exercise? (Y/N): ").strip().lower()
        if inp_ != "y":
            break

    if not workout_list:
        print("No exercises entered.")
        return

    # اضافه کردن تمرین ها به برنامه تمرینی کاربر
    all_plans = exercise_plan_repository.all() # همه تمرین های مخزن (برای تولید آیدی جدید)
    if all_plans:
        new_id = max(int(a.id) for a in all_plans)+1
    else:
        new_id = 1
    dict_={
    "id": new_id,
    "class_title": target_class.title,
    "member_username": member_username,
    "coach_username": coach_username,
    "exercises": [w.to_dict() for w in workout_list]}
    new_plan = ExercisePlan.from_dict(dict_)
    # بررسی اینکه آیا این برنامه تمرینی قبلا در لیست تمرینهای همین کاربر بوده یا نه
    exist = False
    p_ = None
    for p in all_plans:
        if p.member_username == member_username and p.class_title == target_class.title:
            p_=p
            exist = True
    
    if exist:
        inp_ = input(f"do you want to update {p_.class_title } exercise of {p_.member_username}? (Y/N)").strip().lower()
        if inp_=="y":
            new_plan.id = p_.id
            exercise_plan_repository.update(new_plan)
            print(f"\n Exercise plan updated.")
        else:
            print("plan updating cancelled.")
    else:
        exercise_plan_repository.add(new_plan)
        print(f"\n Exercise plan created for {member.name}.")

    
    



        

       
