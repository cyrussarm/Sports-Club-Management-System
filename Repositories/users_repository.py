# ایجاد یک لایه بین داده های جیسن و کاربر داده ها طوری که کاربر داده تقریبا مثل یک لیست با داده ها کار کند
# UserRepository.all() : لیست همه کاربران
# UserRepository.find_by_id(1) : پیدا کردن کاربر با یک آیدی
# UserRepository.add(user) : اضافه کردن کاربر به لیست کاربران
# UserRepository.update(user): آپدیت مشخصات یک کاربر
# این لایه کاری میکنه که بقیه تیم کار نداشته باشند که داده ها در جیسن هستند در دیتابیس هستند یا لیست هستند.
# میگه تو چی کار داری کاربرهای کجا ذخیره میشن فقط یک اینترفیس داشته باش برای کار کردن با داده ها
# اینطوری بعدا اگر مثلا داده ها انتقال داده شدند به دیتابیس لازم نیست همه کد را دست بزنیم
# از این کلاس نمونه ای نخواهیم ساخت و به صورت کلاس ازش استفاده خواهیم کرد
# 

from core.models import Users
from Repositories.BaseRepository import BaseRepository

class UserRepository(BaseRepository):
    file_name = "users.json"
    model = Users
    
    # پیدا کردن یک کاربر با استفاده از یوزر نیم
    @classmethod
    def find_by_username(cls, username_):
        users = cls.all()          
        for user in users:
            if str(user.username) == str(username_):
                return user
        return None

    #دریافت لیست کاربران با نقش مشخص 
    @classmethod
    def list_of_given_role(cls, role_):
        list_=[]
        users = cls.all() 
        for user in users:
            if user.role == role_:
                list_.append(user)
        return list_

    # اور رایت متد add با بررسی یکتایی یوزرنیم
    @classmethod
    def add(cls,user):        
        if cls.find_by_username(user.username) is not None:
            return False 
        return super().add(user)         

    # یافتن شی های فعال
    @classmethod
    def list_active(cls):
        objects = cls.all()
        return [obj_ for obj_ in objects if obj_.is_active]

    @classmethod
    def list_active_with_username_and_role (cls, role_, username):
        return[obj_ for obj_ in cls.list_active() if obj_.role == role_ and obj_.username==username]

    # اولین مطابقت یافته شده را برگردان یا None
    @classmethod
    def find_active_with_username_and_role (cls, role_, username):        
        return next((obj_ for obj_ in cls.list_active() 
                     if obj_.role == role_ and obj_.username==username),None)
        
        
         

        
        


