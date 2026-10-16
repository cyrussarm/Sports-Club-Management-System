from core.models import SportClass
from Repositories.base_repository import base_repository

class KelasRepository(base_repository):
    file_name = "sport_classes.json"
    model = SportClass

    # افزودن شی جدید
    @classmethod
    def add(cls, new_obj):
        existing_objects = cls.all()
        for obj in existing_objects:
            if str(obj.title) == str(new_obj.title):
                return False
        existing_objects.append(new_obj)
        cls.save_all(existing_objects)
        return True

    @classmethod
    def find_by_title(cls, name):
        return next((obj for obj in cls.all() if obj.title == name),None) 

    @classmethod
    def list_active_classes_by_coach(cls, username):
        return [obj for obj in cls.all() if obj.coach_username == username and obj.is_active]

    @classmethod
    def list_active_classes_a_member(cls, username):
        return [obj for obj in cls.all() if username in obj.enrolled and obj.is_active]
    # @classmethod
    # def list_my_students(cls,username):
    #     my_classes = cls.list_active_classes_by_coach(username)
    #     my_students = set()
    #     for c in my_classes:
    #         my_students._hash()