from rich.console import Console
from rich.table   import Table
import auth
import search
from home_helpers import (
    show_own_profile, show_settings,
    handle_requests, show_messages,
    send_message, handle_group_chat
)

console = Console()

def load_posts(users, current):
    posts = []
    for u, data in users.items():
        for p in data.get("posts", []):
            visible = (
                u == current
                or not data.get("private", False)
                or current in data.get("followers", [])
                or any(f"@{current}" in c.get("text", "") for c in p.get("comments", []))
            )
            if visible:
                copy = p.copy()
                copy["username"] = u
                posts.append(copy)
    return posts

def show_home(current):
    users = auth.load_users()
    posts = load_posts(users, current)

    while True:
        console.rule(f"[bold red]HOME - {current}")

        if not posts:
            console.print("📭 No posts.")
        else:
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#", style="dim", width=3)
            table.add_column("User")
            table.add_column("Content", overflow="fold")
            table.add_column("❤", justify="right")
            table.add_column("💬", justify="right")
            for idx, p in enumerate(posts, 1):
                table.add_row(
                    str(idx), p["username"], p["content"],
                    str(p.get("likes", 0)), str(len(p.get("comments", [])))
                )
            console.print(table)

        console.print("Menu:")
        console.print("1. Like a post")
        console.print("2. Comment on a post")
        console.print("3. New post")
        console.print("4. Save/Unsave a post")
        console.print("5. Share a post")
        console.print("6. View stories")
        console.print("7. Add story")
        console.print("8. Search users")
        console.print("9. My profile")
        console.print("10. Settings")
        console.print("11. Follow requests")
        console.print("12. Messages")
        console.print("13. Group chats")
        console.print("14. Delete a post")
        console.print("15. View post comments")
        console.print("16. Logout to main menu")

        choice = console.input("[green]> ").strip()

        if choice == "1":
            try:
                idx = int(console.input("Post # to like: ")) - 1
                if 0 <= idx < len(posts):
                    owner = posts[idx]["username"]
                    for orig in users[owner]["posts"]:
                        if orig["content"] == posts[idx]["content"]:
                            orig.setdefault("liked_by", [])
                            if current in orig["liked_by"]:
                                console.print("⚠️ You already liked this post.")
                            else:
                                orig["liked_by"].append(current)
                                orig["likes"] = orig.get("likes", 0) + 1
                                auth.save_users(users)
                                posts = load_posts(users, current)
                                console.print("❤️ Liked!")
                            break
                else:
                    console.print("❌ Invalid post number.")
            except ValueError:
                console.print("❌ Enter a valid number.")

        elif choice == "2":
            try:
                idx = int(console.input("Post # to comment: ")) - 1
                if 0 <= idx < len(posts):
                    text = console.input("Your comment: ").strip()
                    owner = posts[idx]["username"]
                    for orig in users[owner]["posts"]:
                        if orig["content"] == posts[idx]["content"]:
                            orig.setdefault("comments", []).append({"user": current, "text": text})
                            break
                    auth.save_users(users)
                    posts = load_posts(users, current)
                    console.print("💬 Comment added!")
                else:
                    console.print("❌ Invalid post number.")
            except ValueError:
                console.print("❌ Enter a valid number.")

        elif choice == "3":
            content = console.input("Enter new post content: ").strip()
            users[current].setdefault("posts", []).append({
                "content": content,
                "likes": 0,
                "comments": [],
                "liked_by": []
            })
            auth.save_users(users)
            posts = load_posts(users, current)
            console.print("📝 New post created!")

        elif choice == "4":
            try:
                idx = int(console.input("Post # to (un)save: ")) - 1
                if 0 <= idx < len(posts):
                    saved = users[current].setdefault("saved_posts", [])
                    content = posts[idx]["content"]
                    if content in saved:
                        saved.remove(content)
                        console.print("❌ Unsaved.")
                    else:
                        saved.append(content)
                        console.print("✅ Saved.")
                    auth.save_users(users)
                else:
                    console.print("❌ Invalid post number.")
            except ValueError:
                console.print("❌ Enter a valid number.")

        elif choice == "5":
            try:
                idx = int(console.input("Post # to share: ")) - 1
                if 0 <= idx < len(posts):
                    to = console.input("Send to username: ").strip()
                    if to in users:
                        users[to].setdefault("inbox", []).append({
                            "from": current,
                            "content": posts[idx]["content"]
                        })
                        auth.save_users(users)
                        console.print("✉️ Post shared!")
                    else:
                        console.print("❌ User not found.")
                else:
                    console.print("❌ Invalid post number.")
            except ValueError:
                console.print("❌ Enter a valid number.")

        elif choice == "6":
            seen = False
            for u in users[current].get("following", []):
                for story in users[u].get("stories", []):
                    story.setdefault("viewed_by", [])
                    story.setdefault("liked_by", [])
                    if current in story["viewed_by"]:
                        continue
                    console.print(f"{u} ▶ {story['content']} ❤ {story['likes']}")
                    story["viewed_by"].append(current)
                    if console.input("Like story? (y/n): ").strip().lower() == 'y':
                        if current not in story["liked_by"]:
                            story["liked_by"].append(current)
                            story["likes"] = story.get("likes", 0) + 1
                    auth.save_users(users)
                    seen = True
            if not seen:
                console.print("📭 No new stories to view.")

        elif choice == "7":
            text = console.input("Enter story content: ").strip()
            users[current].setdefault("stories", []).append({
                "content": text,
                "likes": 0,
                "liked_by": [],
                "viewed_by": []
            })
            auth.save_users(users)
            console.print("📸 Story added!")

        elif choice == "8":
            search.search_user(current, users)
            auth.save_users(users)
            posts = load_posts(users, current)

        elif choice == "9":
            new_user = show_own_profile(current, users)
            if new_user:
                current = new_user
                posts = load_posts(users, current)
            auth.save_users(users)

        elif choice == "10":
            show_settings(current, users)
            auth.save_users(users)

        elif choice == "11":
            handle_requests(current, users)
            auth.save_users(users)
            posts = load_posts(users, current)

        elif choice == "12":
            show_messages(current, users)
            send_message(current, users)
            auth.save_users(users)

        elif choice == "13":
            handle_group_chat(current, users)
            auth.save_users(users)

        elif choice == "14":
            try:
                idx = int(console.input("Post # to delete: ")) - 1
                if 0 <= idx < len(posts) and posts[idx]["username"] == current:
                    content = posts[idx]["content"]
                    users[current]["posts"] = [
                        p for p in users[current]["posts"]
                        if p["content"] != content
                    ]
                    auth.save_users(users)
                    posts = load_posts(users, current)
                    console.print("🗑️ Post deleted.")
                else:
                    console.print("❌ Cannot delete this post.")
            except ValueError:
                console.print("❌ Enter a valid number.")

        elif choice == "15":
            try:
                idx = int(console.input("Post # to view comments: ")) - 1
                if 0 <= idx < len(posts):
                    cmts = posts[idx].get("comments", [])
                    if not cmts:
                        console.print("📭 No comments.")
                    else:
                        console.rule("Comments")
                        for c in cmts:
                            console.print(f"{c.get('user', '')}: {c.get('text', '')}")
                else:
                    console.print("❌ Invalid post number.")
            except ValueError:
                console.print("❌ Enter a valid number.")

        elif choice == "16":
            console.print("🔙 Returning to main menu.")
            break

        else:
            console.print("❌ Invalid choice.")
