class Routine:
    def __init__(self, sportsclass, student, *args):
        self.sportsclass = sportsclass
        self.student = student
        self.moves = args

    def addmoves(self):
        newmove = {}
        move = input("Enter The Move's Name: ")
        sets = input("Enter The Number Of Sets: ")
        repetitions = input("Enter The Number Of Repetitions: ")
        breaktime = input("Enter The Break Duration In Minutes: ")
        description = input("Enter The Move's Description: ")
        newmove['Move'] = move
        newmove['Sets'] = sets
        newmove['Repetitions'] = repetitions
        newmove['Brektime'] = breaktime
        newmove['Description'] = description
        self.args.append(newmove)
    