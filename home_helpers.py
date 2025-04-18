from rich.console import Console
from rich.table   import Table
import json, os

console = Console()

def show_own_profile(current, users):
    """نمایش و ویرایش پروفایل خود کاربر"""
    u = users[current]
    while True:
        console.rule(f"[bold cyan]Your Profile: {current}")
        console.print(f"Bio: {u['bio']}")
        console.print(f"Followers: {len(u['followers'])}")
        console.print(f"Following: {len(u['following'])}")
        console.print(f"Posts: {len(u['posts'])}")
        console.print("1. Edit username")
        console.print("2. Edit bio")
        console.print("3. View my posts")
        console.print("4. Back")
        cmd = console.input("[green]> ").strip()
        if cmd == "1":
            new = console.input("New username: ").strip()
            if not new or new in users:
                console.print("❌ Invalid or taken username.")
            else:
                users[new] = users.pop(current)
                console.print("✅ Username changed.")
                return new
        elif cmd == "2":
            u["bio"] = console.input("New bio: ")
            console.print("✅ Bio updated.")
        elif cmd == "3":
            for i, p in enumerate(u["posts"], 1):
                console.print(f"{i}. {p['content']} ❤️ {p['likes']} 💬 {len(p['comments'])}")
        elif cmd == "4":
            return None
        else:
            console.print("❌ Invalid choice.")

def show_settings(current, users):
    """تغییر حریم خصوصی و مشاهده بلاک‌شده‌ها"""
    while True:
        priv = users[current]["private"]
        console.rule("[bold yellow]Settings")
        console.print(f"Account is {'Private 🔒' if priv else 'Public 🌍'}")
        console.print("1. Toggle private/public")
        console.print("2. View blocked users")
        console.print("3. Back")
        cmd = console.input("[green]> ").strip()
        if cmd == "1":
            users[current]["private"] = not priv
            console.print("✅ Privacy toggled.")
        elif cmd == "2":
            bl = users[current]["blocked_users"]
            console.print("Blocked:", ", ".join(bl) if bl else "No blocked users.")
        elif cmd == "3":
            break
        else:
            console.print("❌ Invalid choice.")

def handle_requests(current, users):
    """مدیریت درخواست‌های دنبال کردن"""
    reqs = users[current]["follow_requests"]
    if not reqs:
        console.print("📭 No follow requests.")
        return
    console.rule("[bold blue]Follow Requests")
    for r in reqs[:]:
        if console.input(f"{r} wants to follow you. Accept? (y/n): ").lower() == "y":
            users[current]["followers"].append(r)
            users[r]["following"].append(current)
            console.print(f"✅ {r} is now a follower.")
        else:
            console.print(f"❌ Request from {r} rejected.")
        reqs.remove(r)

def show_messages(current, users):
    """مشاهده پیام‌های دریافتی"""
    inbox = users[current]["inbox"]
    if not inbox:
        console.print("📭 No messages.")
        return
    console.rule("[bold cyan]Inbox")
    for m in inbox:
        console.print(f"From {m['from']}: {m['content']}")
    users[current]["inbox"].clear()

def send_message(current, users):
    """ارسال پیام دایرکت"""
    to = console.input("Send message to: ").strip()
    if to not in users:
        console.print("❌ User not found.")
        return
    txt = console.input("Your message: ").strip()
    users[to]["inbox"].append({"from": current, "content": txt})
    console.print("✉️ Message sent!")

def handle_group_chat(current, users):
    """چت گروهی"""
    GROUP_FILE = "groups.json"
    if os.path.exists(GROUP_FILE):
        with open(GROUP_FILE, "r") as f:
            groups = json.load(f)
    else:
        groups = {}

    while True:
        console.rule("[bold green]Group Chats")
        console.print("1. Create group")
        console.print("2. Add member")
        console.print("3. Send group message")
        console.print("4. View group messages")
        console.print("5. Back to Home")
        cmd = console.input("[green]> ").strip()
        if cmd == "1":
            name = console.input("Group name: ").strip()
            if name in groups:
                console.print("❌ Group exists.")
            else:
                groups[name] = {"members":[current], "messages":[]}
                console.print(f"✅ Group '{name}' created.")
        elif cmd == "2":
            name = console.input("Group name: ").strip()
            if name not in groups:
                console.print("❌ No such group.")
            else:
                mem = console.input("Add user: ").strip()
                if mem in users and mem not in groups[name]["members"]:
                    groups[name]["members"].append(mem)
                    console.print(f"✅ {mem} added.")
                else:
                    console.print("❌ Invalid or already a member.")
        elif cmd == "3":
            name = console.input("Group name: ").strip()
            if name not in groups or current not in groups[name]["members"]:
                console.print("❌ Access denied.")
            else:
                msg = console.input("Message: ").strip()
                groups[name]["messages"].append({"from":current, "text":msg})
                console.print("✉️ Sent.")
        elif cmd == "4":
            name = console.input("Group name: ").strip()
            if name not in groups or current not in groups[name]["members"]:
                console.print("❌ Access denied.")
            else:
                tbl = Table(show_header=True, header_style="bold cyan")
                tbl.add_column("From"); tbl.add_column("Message")
                for m in groups[name]["messages"]:
                    tbl.add_row(m["from"], m["text"])
                console.print(tbl)
        elif cmd == "5":
            break
        else:
            console.print("❌ Invalid choice.")

    with open(GROUP_FILE, "w") as f:
        json.dump(groups, f, indent=4)
