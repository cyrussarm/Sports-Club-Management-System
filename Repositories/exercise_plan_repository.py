from core.models import ExercisePlan 
from Repositories.base_repository import base_repository

class exercise_plan_repository(base_repository):
    file_name = "exercise_plan_repository.json"
    model = ExercisePlan