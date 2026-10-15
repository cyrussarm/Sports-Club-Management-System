from core.models import ExercisePlan 
from Repositories.base_repository import base_repository

class exercise_plan_repository(base_repository):
    file_name = "exercise_plan_repository.json"
    model = ExercisePlan

    @classmethod
    def find_by_memeber_coach_classtitle(cls, member_username, coach_username, classtitle):
        userplan = None
        plans = cls.all()
        for plan in plans:
            if str(plan.member_username) == str(member_username) and str(plan.classtitle) == classtitle and str(plan.coach_username) == coach_username:
                userplan = plan
        return userplan    

    @classmethod
    def find_by_member(cls, member_username):
        userplans = []
        plans = cls.all()
        for plan in plans:
            if str(plan.member_username) == str(member_username):
                userplans.append(plan)
        return userplans

    @classmethod
    def find_by_id(cls, planid):
        plans = cls.all()
        for plan in plans:
            if plan.id == planid:
                return plan
        return None

    @classmethod
    def add(cls, plan):        
        if cls.find_by_id(plan.id) is not None:
            return False 
        return super().add(id)     