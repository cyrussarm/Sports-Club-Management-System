from core.models import Users, SportClass

def test_model():   
    # ساخت نمونه از کلاس یوزرز با دیکشنری ورودی
    # چون داده ها در جیسون به صورت دیکشنری ذخیره میشوند این روش بهتره
    u = Users.from_dict({
    "id": 1, "name": "سیروس", "username": "sirus56@",
    "password": "x", "email": "y@x.com",
    "role": "admin", "is_active": True,
    })
    # نمایش نمونه ساخته شده به صورت یک دیکشنری
    print(u.to_dict())

    # --- Class ---
    c = SportClass.from_dict({
        "title": "بدنسازی", "sport_type": "fitness",
        "coach_username": "coach1", "hall_name": "سالن ۱",
        "day": "شنبه", "time": "10:00", "capacity": 20,
        "enrolled": ["ali", "reza"]
    })
    print(c.remaining_capacity())   
