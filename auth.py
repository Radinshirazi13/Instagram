import json
import os

DB_FILE = "users.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    else:
        users = {}

    for data in users.values():
        data.setdefault("email", "")
        data.setdefault("password", "")
        data.setdefault("bio", "")
        data.setdefault("private", False)
        data.setdefault("followers", [])
        data.setdefault("following", [])
        data.setdefault("follow_requests", [])
        data.setdefault("blocked_users", [])
        data.setdefault("posts", [])
        data.setdefault("stories", [])
        data.setdefault("saved_posts", [])
        data.setdefault("inbox", [])

        for p in data["posts"]:
            p.setdefault("liked_by", [])

        for s in data["stories"]:
            s.setdefault("liked_by", [])
            s.setdefault("viewed_by", [])

    return users

def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def register():
    users = load_users()
    print("\n--- REGISTER ---")
    username = input("Username: ").strip()
    email    = input("Email: ").strip()
    password = input("Password: ").strip()

    if not username or not email or not password:
        print("❌ All fields are required.")
        return
    if "@" not in email or "." not in email:
        print("❌ Invalid email format.")
        return
    if username in users:
        print("❌ Username already exists.")
        return
    if any(u["email"] == email for u in users.values()):
        print("❌ Email already in use.")
        return

    users[username] = {
        "email": email,
        "password": password,
        "bio": "",
        "private": False,
        "followers": [],
        "following": [],
        "follow_requests": [],
        "blocked_users": [],
        "posts": [],
        "stories": [],
        "saved_posts": [],
        "inbox": []
    }
    save_users(users)
    print("✅ Registration successful!")

def login():
    users = load_users()
    print("\n--- LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username not in users:
        print("❌ Username not found.")
        return None
    if users[username]["password"] != password:
        print("❌ Incorrect password.")
        return None

    print(f"✅ Logged in as {username}!")
    return username
