def show_profile(target, current, users):
    u = users.get(target)
    if not u:
        print("❌ User not found.")
        return
    if current in u["blocked_users"] or target in users[current]["blocked_users"]:
        print("🚫 Access denied.")
        return
    if u["private"] and current not in u["followers"]:
        print("🔒 Account is private.")
        if current not in u["follow_requests"]:
            if input("Send follow request? (y/n): ").lower() == "y":
                u["follow_requests"].append(current)
                print("✅ Request sent.")
        else:
            print("⏳ Request pending.")
        return
    print(f"\n— PROFILE of {target} —")
    print(f"Bio: {u['bio']}")
    print(f"Followers: {len(u['followers'])}")
    print(f"Following: {len(u['following'])}")
    print(f"Posts: {len(u['posts'])}")
    if target in users[current]["following"]:
        if input("Unfollow? (y/n): ").lower() == "y":
            users[current]["following"].remove(target)
            users[target]["followers"].remove(current)
            print("❎ Unfollowed.")
    else:
        if input("Follow? (y/n): ").lower() == "y":
            users[current]["following"].append(target)
            users[target]["followers"].append(current)
            print("✅ Followed.")
    if target in users[current]["blocked_users"]:
        if input("Unblock user? (y/n): ").lower() == "y":
            users[current]["blocked_users"].remove(target)
            print("✅ Unblocked.")
    else:
        if input("Block user? (y/n): ").lower() == "y":
            users[current]["blocked_users"].append(target)
            print("🚫 Blocked.")

def search_user(current, users):
    name = input("Enter username to search: ").strip()
    if name == current:
        print("⚠ You cannot search yourself.")
        return
    show_profile(name, current, users)
