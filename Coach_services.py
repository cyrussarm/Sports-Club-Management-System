from Repositories.classes_repository import KelasRepository
from core.models import Exercise
from core.models import ExercisePlan 
from Repositories.Exercise_Plan_Repository import exercise_plan_repository
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
            
            print(f"class id: {c.id} | class name: {c.title} | sport type: {c.sport_type} | coach: {c.coach_name}\n" \
              f" coach_username: {c.coach_username} | hall: {c.hall_name}\n" \
              f"day:{c.day} | time: {c.time} | capacity: {c.capacity}\n" \
              f" remaining capacity: {c.remaining_capacity()} | state: {status}\n")
    except ClubError as e: # فایل خالی یا خطا
        print (f"Error: {e}")
        return 
    return classes

# ساخت آیدی برای برنامه
def generate_plan_id():
    plan_id = 1
    try:
        plans = exercise_plan_repository.all()
        plan_id = max(int(plan.id) for plan in plans)+1
    except ClubError: # فایل خالی یا خطا
        return plan_id

# اضافه کردن یک حرکت
def add_exercise(exercises):
    while True:
        d = {}
        d['name'] = input('Enter exercise name: ')

        while True:
            sets = input('Enter the number of sets: ')
            if not sets.isdigit() or sets == '0':
                print('The number of sets should be a positive integer!')
                continue
            else:
                d['sets'] = sets
                break

        while True:
            repetitions = input('Enter the number of repetitions: ')
            if not repetitions.isdigit() or repetitions == '0':
                print('The number of reptitions should be a positive integer!')
                continue
            else:
                d['tekrars'] = repetitions
                break

        while True:
            resttime = input('Enter the rest time in minutes (between 1 and 59):')
            if not resttime.isdigit() or int(resttime) >=60 or int(resttime) == 0:
                print('The number of rest minutes should be an integer!')
                continue
            else:
                d['rest_time']
                break
        d['description'] = input('Enter the description for this exercise: ')
                    
        newexercise = Exercise.from_dict(d)
        exercises.append(newexercise)
        exercise_plan_repository.update(exercises)
        temp = input("New exercise added to the plan.\n " \
        "Enter 'n' to add another exercise to the plan, or enter any other value to finish this task: ")
        if temp == 'n':
            continue
        else:
            return None


# ویرایش حرکت
def edit_exercise(exercises):
    if len(exercises)>0 :
        exists= False
        while not exists:
            target_exercise = input("Enter the name of the exercise you want to edit: ")
            for i in exercises:
                if i['name'] == target_exercise:
                    target_exercise = i
                    exists= True
                    break
            if exists == False:
                print('Invalid exercise name.')
                continue
            else:
                break
        print(f"Target exercise:\n {target_exercise}")
        
        while True:
            temp = input("Choose the option you want to change:\n" \
                         "1- name | 2- sets | 3- tekrars\n" \
                         "4- rest time | 5- description\n")
            
            if temp == '1':
                target_exercise['name'] = input('Enter the new name: ')
                exercise_plan_repository.update(exercises)
                return None
            
            elif temp == '2':
                while True:
                    newval = input('Enter the new number of sets: ')
                    if newval.isdigit() and newval != '0':
                        target_exercise['sets'] = newval
                        exercise_plan_repository.update(exercises)
                        return None
                    else:
                        print('The input must be a positive integer!')
                        continue
            
            elif temp == '3':
                while True:
                    newval = input('Enter the new number of tekrars: ')
                    if newval.isdigit() and newval != '0':
                        target_exercise['tekrars'] = newval
                        exercise_plan_repository.update(exercises)
                        return None
                    else:
                        print('The input must be a positive integer!')
                        continue
            
            elif temp == '4':
                while True:
                    newval = input('Enter the new number of minutes (between 1 and 59): ')
                    if newval.isdigit() and 1<=newval<=59 :
                        target_exercise['rest_time'] = newval
                        exercise_plan_repository.update(exercises)
                        return None
                    else:
                        print('The input must be a number between 1 and 59!')
                        continue
            
            elif temp == '5':
                target_exercise['description'] = input('Enter the new description: ')
                exercise_plan_repository.update(exercises)
                return None
            
            else:
                print('Invalid input')
                continue
        
    else:
        print('No exercises found. Add an exercise first.')
        return None


# حذف یک حرکت
def delete_exercise(exercises):
    if len(exercises) == 0:
        print('There are no exercises in this plan.')
        return None
    else:
        while True:
            temp_ = input("Enter the name of the exercise you want to delete: ")
            exists = False
            for i in exercises:
                if i['name'] == temp_:
                    exists = True
                    break
            if exists:
                exercises.pop()
                print('Exercise deleted.')
                plan = ExercisePlan.from_dict(plan)
                exercise_plan_repository.update(plan)
                return None
            else:
                print('Exercise not found.')
                continue


# اضافه کردن برنامه جدید
def add_exercise_plan(coach_username, SportClass, member_username):
    d = {}
    d['id'] = generate_plan_id()
    d['class_title'] = SportClass.title
    d['member_username'] = member_username
    d['coach_username'] = coach_username
    exercises = []

    while True:
        a = input('Choose an option:\n 1- Add an exercise\n 2- Edit an existing exercise\n 3- Delete an exercise\n 4- Back')

        if a == '1':
            add_exercise(exercises)
            break

        elif a == '2':
            print(f"This plan's exercises:\n {exercises}" )
            edit_exercise(exercises)
            break

        elif a == '3':
            print(f"This plan's exercises:\n {exercises}")
            while True:
                temp = input("Enter the name of the exercise you want to delete: ")
                exists = False
                for i in exercises:
                    if i['name'] == temp:
                        exists = True
                        break
                if exists:
                    exercises.pop()
                    print('Exercise deleted.')
                    break
                else:
                    print('Exercise not found.')
                    continue
        elif a == '4':
            return None
        else:
            print('Invalid input.')
            continue
    
    d['exercises'] = exercises

    d = ExercisePlan.from_dict(d)
    exercise_plan_repository.update(d)
    return None



# ویرایش برنامه ورزشی
def edit_exercise_plan(plan):
    plan = plan.to_dict()
    exercises = plan['exercises']

    print(f"The selected plan:\n" \
          f"Plan ID: {plan['id']} | Class: {plan['class_title']}\n" \
          f"Member Username: {plan['member_username']}\n" \
          f"Exercises: {plan['exercises']}")
    
    while True:
        a = input('Choose an option:\n 1- Edit exercises\n 2- Go back\n')
        if a == '1':
            while True:
                temp = input('Choose an option:\n 1- Add an exercise\n 2- Edit an exercise\n 3- Delete an exercise\n 4- Back\n')
                if temp == '1':
                    add_exercise(exercises)
                elif temp == '2':
                    edit_exercise(exercises)
                elif temp == '3':
                    delete_exercise(exercises)
                elif temp == '4':
                    return None
                else:
                    print('Invalid input.')
                    continue
        
        elif a == '2':
            return None
        else:
            print('Invalid input.')
            continue


# تنظیم برنامه تمرین
def manage_exercise_plans(coach_username):

    # انتخاب کلاس    
    class_ids = view_coach_class(coach_username)
    class_ids = [obj_.id for obj_ in class_ids]

    while True:
        target_class_id = input("Enter the target class ID:").strip()
        while True:
            if not target_class_id.isdigit() or not target_class_id in class_ids:
                while True:
                    inp_=input("Invalid ID, try again or enter 'b' to go back to main menu.").strip().lower()
                    if inp_=="b":
                        return None
                    else:
                        target_class_id = inp_
                        break
            else:
                break

        target_class_id = int(target_class_id)
        
        target_class = KelasRepository.find_by_id(target_class_id)
        print(f"Class ID: {target_class.id} | Class name: {target_class.title} | \n")
        print(f"Class members: \n")
        print(f"{target_class.enrolled}")
        a = input("Enter 'b' to choose another class, enter any other value to continue. ")
        if a == 'b':
            continue
        else:
            break

    # انتخاب یوزر
    enrolled_usernames = [obj_.id for obj_ in target_class.enrolled]
    while True:
        target_member_username = input("Enter the target member username:").strip()
        while True:
            if not target_member_username or not target_member_username in enrolled_usernames:
                inp_=input("Invalid username, try again or enter 'b' to go back to main menu.").strip().lower()
                if inp_=="b":
                    return None
                else:
                    target_member_username = inp_
                    continue
            else:
                break
        target_member_username = str(target_member_username)

        userplan = exercise_plan_repository.find_by_memeber_coach_classtitle(target_member_username, coach_username, target_class.title)

        print(f"Member username: {target_member_username} \n")
        print(f"Member excercise plans:\n")
        print(userplan)

        a = input("Enter 'b' to choose another user, enter any other value to continue. ")
        if a == 'b':
            continue
        else:
            break


    #منو بعد از انتخاب کلاس و ممبر
    while True:
        action = input('Choose an option:\n 1- Add an excercise plan\n 2- Edit an excercise plan\n 3- Return to main menu\n')

        if action == '1':
            if userplan == None:
                add_exercise_plan(coach_username, target_class, target_member_username)
            else:
                print('A plan already exists.')
                continue

        elif action == '2':
            edit_exercise_plan(userplan)

        elif action == '3':
            return None
        else:
            print('Invalid input.')
            continue





