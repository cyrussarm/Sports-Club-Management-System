from services.coach_sevices import view_coach_class
from services.coach_sevices import manage_exercise_plans
def adminpanel():
    while True:
        a = input('Choose an option:\n' \
                '1. View Classes\n' \
                '2. Manage Excercise Plans\n' \
                '3. Exit')
        if a == 1:
            view_coach_class(user.username)
            back = input("Type Anything To Go Back.")
            continue
        elif a == 2:
            pass
            

        elif a == 3:
            pass
        
        else:
            print('Invalid input')
            continue