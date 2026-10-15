from core.models import SportClass
from Repositories.base_repository import base_repository

class KelasRepository(base_repository):
    file_name = "sport_classes.json"
    model = SportClass

    # افزودن شی جدید
    @classmethod
    def add(cls, obj):
        existing_objects = cls.all()
        for obj_ in existing_objects:
            if str(obj_.title) == str(obj.title):
                return False
        existing_objects.append(obj)
        cls.save_all(existing_objects)
        return True

    @classmethod
    def find_by_title(cls, name):
        return next((obj_ for obj_ in cls.all() if obj_.title == name),None) 

    @classmethod
    def list_active_classes_by_coach(cls, username):
        return [obj_ for obj_ in cls.all() if obj_.coach_username == username and obj_.is_active]

    @classmethod
    def available_classes(cls):
        list_ = []
        classes = cls.all()
        for i in classes:
            zarfiat = i.remaining_capacity()
            if zarfiat != 0 and i.is_active:
                list_.append(i)
        return list_

    @classmethod
    def find_by_user(cls, member_username):
        list_ = []
        classes = cls.all()
        for i in classes:
            if member_username in i['enrolled']:
                list_.append(i)
        return list_