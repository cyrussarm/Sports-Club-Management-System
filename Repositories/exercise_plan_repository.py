from core.models import ExercisePlan 
from Repositories.base_repository import base_repository

class exercise_plan_repository(base_repository):
    file_name = "exercise_plan.json"
    model = ExercisePlan

    @classmethod
    def find_by_username(cls, username):
        return [obj_ for obj_ in cls.all() if obj_.member_username == username]
