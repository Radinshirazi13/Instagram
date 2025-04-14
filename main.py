import auth

def show_menu():
    print("\n✨ خوش آمدید به برنامه Insta-Terminal")
    print("1. ثبت‌نام")
    print("2. ورود")
    print("3. خروج")

def main():
    while True:
        show_menu()
        choice = input("انتخاب شما: ").strip()
        if choice == "1":
            auth.register()
        elif choice == "2":
            user = auth.login()
            if user:
                print(f"\n🎉 {user} عزیز وارد شدید.")
                # در مراحل بعدی وارد صفحه اصلی می‌شود
        elif choice == "3":
            print("👋 خداحافظ!")
            break
        else:
            print("❌ گزینه نامعتبر است.")

if __name__ == "__main__":
    main()
