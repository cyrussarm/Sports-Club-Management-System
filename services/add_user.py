from core.storage import load_data, save_data
from core.exceptions import ValidationError, AuthError, BusinessError

import re

def _validate(name, username, password, email, role):
    USERNAME_RE = re.compile(r"^[A-Za-z0-9_@&!.]{3,30}$")
    PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+$")
    EMAIL_RE    = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    VALID_ROLES = ("coach", "member")
    name = name.strip()
    if not name:
        raise ValidationError("name is required")
    if not USERNAME_RE.match(username):
        raise ValidationError("username must be 3-30 chars including (letters, digits, _ @ & ! .)")
    if not PASSWORD_RE.match(password):
        raise ValidationError(f"password must contain a letter, a digit and @ or &: {password}")
    if not EMAIL_RE.match(email):
        raise ValidationError("email is invalid")
    # فرض شده است فقط یک ادمین وجود دارد که قبلا در فایل دیتا وارد شده و ادمین نمیتونه ادمین جدید اضافه کنه
    if role not in VALID_ROLES:
        raise BusinessError("role must be 'coach' or 'member'")
    

def add_user(current_user, name, username, password, email, role):

    # اعتبارسنجی ورودی
    _validate(name, username, password, email, role)

    # چک نقش کاربر
    if not current_user or current_user.get("role") != "admin" :
        raise AuthError("only admin can add users")
    if not current_user.get("is_active"):
        raise AuthError("admin account is not active")

    # لود داده های کاربران
    users = load_data("users.json")
    # بررسی یکتایی یوزرنیم
    for user in users:
        if user["username"]==username:
            raise BusinessError(f"username '{username}' already exists")            
    # تولید id
    new_id = max(user["id"] for user in users)+1

    # ایجاد دیکشنری کاربر جدید
    new_user = {
        "id": new_id,
        "name": name,
        "username": username,
        "password": password,
        "email": email,
        "role": role,
        "is_active": True
    }

    # اپند کاربر جدید به لیست
    users.append(new_user)

    # ذخیره داده ها
    save_data("users.json", users)

    print("User added successfully")
