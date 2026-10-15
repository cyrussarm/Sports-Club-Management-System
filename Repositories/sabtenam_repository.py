from core.models import Enrollment
from Repositories.base_repository import base_repository

class SabtenamRepository(base_repository):
    file_name = "sabtenam.json"
    model = Enrollment

    # همه ثبت نام های یک عضو
    @classmethod
    def find_by_member(cls, member_username):       
        return [e for e in cls.all() if e.member_username == member_username]

    # ثبت نام های فعال یک عضو
    @classmethod
    def find_active_by_member(cls, member_username):        
        return [e for e in cls.all()
                if e.member_username == member_username and e.is_active]

    # ثبت نام فعل یک عضو در یک کلاس مورنظر
    @classmethod
    def find_active_by_member_and_class(cls, member_username, class_id):  
        for e in cls.all():
            if e.member_username == member_username and str(e.class_id) == str(class_id) and e.is_active:
                return e
        return None

    
   
        