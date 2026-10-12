import re

def validate_user_registration(name, username, password, email=None):
    # نام کاربری : طول از 3 تا 30 کاراکتر. کاراکترهای مجاز: حروف کوچک+حروف بزرگ+عدد+آندرلاین
    # نکته: در سند این مورد نیست و فقط یکتا بودن نام کاربری قید شده است
    USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,30}$")
    # محدودیت های رمز عبور طبق سند: حداقل شامل یک حرف انگلیسی، یک عدد و یکی از کاراکترهای & یا @ باشد
    # سه تا شرط گذاشته ایم که اگر هر سه اکی بودند از کرسر تا انتهای خط مصرف میشوند
    PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+$")
    # سند: در صورت استفاده از ایمیل-> وجود . و @ در دامنه
    # [^@\s] : مجموعه کاراکترها بدون & یا فاصله
    EMAIL_RE    = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")    
    
    if not name:
        msg = ("ValidationError: name is required")
        return False, msg
    if not USERNAME_RE.match(username):
        msg = ("ValidationError: username must be 3-30 chars including letters, digits and underscore")
        return False, msg
    if not PASSWORD_RE.match(password):
        msg = ("ValidationError:password must contain a letter, a digit and @ or &")
        return False, msg
    if email is not None:        
        # ایمیل حتما باید از نوع استرینگ باشد و با الگوی داده شده مطابقت داشته باشد
        if not isinstance(email,str) or not EMAIL_RE.match(email):
            msg = ("ValidationError: email is invalid")
            return False, msg

    return True, None
   
    


