from rich.console import Console
import auth
import home

console = Console()

def main():
    while True:
        console.rule("[bold red]Welcome to Insta")
        console.print("1. Register")
        console.print("2. Login")
        console.print("3. Exit")
        choice = console.input("[green]> ").strip()

        if choice == "1":
            auth.register()
        elif choice == "2":
            user = auth.login()
            if user:
                home.show_home(user)
        elif choice == "3":
            console.print("👋 bye")
            break
        else:
            console.print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
