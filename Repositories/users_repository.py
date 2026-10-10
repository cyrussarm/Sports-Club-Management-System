# ایجاد یک لایه بین داده های جیسن و کاربر داده ها طوری که کاربر داده تقریبا مثل یک لیست با داده ها کار کند
# UserRepository.all() : لیست همه کاربران
# UserRepository.find_by_id(1) : پیدا کردن کاربر با یک آیدی
# UserRepository.add(user) : اضافه کردن کاربر به لیست کاربران
# UserRepository.update(user): آپدیت مشخصات یک کاربر
# UserRepository.delete(id): حذف یک کاربر 
# این لایه کاری میکنه که بقیه تیم کار نداشته باشند که داده ها در جیسن هستند در دیتابیس هستند یا لیست هستند.
# میگه تو چی کار داری کاربرهای کجا ذخیره میشن فقط یک اینترفیس داشته باش برای کار کردن با داده ها
# اینطوری بعدا اگر مثلا داده ها انتقال داده شدند به دیتابیس لازم نیست همه کد را دست بزنیم
# از این کلاس نمونه ای نخواهیم ساخت و به صورت کلاس ازش استفاده خواهیم کرد
# 

from core.storage import load_data, save_data
from core.models import Users

class UserRepository:
    file_name = "users.json"
    
    # برگرداندن لیست همه کاربران به صورت لیستی از شی ها
    @classmethod
    def allusers(cls):
        raw_data_as_dict = load_data(cls.file_name)
        users = []
        for dict_ in raw_data_as_dict:
            users.append(Users.from_dict(dict_))
        return users

    @classmethod
    def save_all(cls, objs):
        list_ = []
        # تبدیل لیست شی ها به لیست دیکشنری
        # اینجا نیازی نیست بگیم obj از چه نوعیه
        # پایتون خودش تایپ شی را بررسی میکنه و میره متد همان کلاس را اجرا میکنه
        for obj in objs:
            list_.append(obj.to_dict())
        # ذخیره کردن لیست دیکشنری در فایل json        
        save_data(cls.file_name, list_)
        


        

    # پیدا کردن یک کاربر با استفاده از آی دی
    @classmethod
    def find_user_by_id(cls, user_id):
        raw_data_as_dict = load_data(cls.file_name)
        for dict_ in raw_data_as_dict:
            pass

    # افزودن کاربر جدید
    @classmethod
    def add_new_user(cls, user):

        pass

