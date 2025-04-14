import json
import os

DB_FILE = "users.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email

def register():
    users = load_users()
    print("\n📝 ثبت‌نام کاربر جدید")
    username = input("نام کاربری: ").strip()
    email = input("ایمیل: ").strip()
    password = input("رمز عبور: ").strip()

    if not username or not email or not password:
        print("❌ همه فیلدها باید پر شوند.")
        return

    if not is_valid_email(email):
        print("❌ ایمیل وارد شده معتبر نیست.")
        return

    if username in users:
        print("❌ این نام کاربری قبلاً ثبت شده.")
        return

    for user in users.values():
        if user["email"] == email:
            print("❌ این ایمیل قبلاً استفاده شده.")
            return

    users[username] = {
        "email": email,
        "password": password
    }
    save_users(users)
    print("✅ ثبت‌نام با موفقیت انجام شد!")

def login() -> str | None:
    users = load_users()
    print("\n🔐 ورود به حساب")
    username = input("نام کاربری: ").strip()
    password = input("رمز عبور: ").strip()

    if username not in users:
        print("❌ نام کاربری وجود ندارد.")
        return None
    if users[username]["password"] != password:
        print("❌ رمز عبور اشتباه است.")
        return None

    print(f"✅ ورود موفقیت‌آمیز بود! خوش آمدی {username} 👋")
    return username
