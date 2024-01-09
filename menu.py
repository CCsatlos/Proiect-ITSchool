
class MainMenu:
    def __init__(self) -> None:
        self.menu_entries = {}
    
    def add_option(self, num: str, name, command):
        self.menu_entries[num] = (name, command)

    def show_menu(self):
        print("Main Menu:")
        for number, (name, _) in self.menu_entries.items():
            print(f"{number} : {name}")

    def run(self):
        keep_running = True
        while keep_running:
            self.show_menu()
            print()
            user_input = input("Enter your choice or 0 to exit: ")
            if user_input == "0":
                print("See you soon!")
                keep_running = False
            elif user_input in self.menu_entries:
                _, command = self.menu_entries[user_input]
                command()
                print(input("Press ENTER to return! "))
            else:
                print("Command not found. Please try again!")
            
        
                
                
            

