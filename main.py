from tkinter import Tk, messagebox
from Start import FirstGUI
from Choice import SecondGUI
from SignIn import SignInGUI
from SignUp import SignUpGUI
from MainScreenUnlog import MainGUI
from SearchPokUnLog import MainGUI as PokemonSearchGUI
from SearchTrainUnl import TrainerGUI
from MainScreenLogUr import MainGUI as MainScreenLogUr
from AddDelPok import PokemonGUI
from YourPokem import MainGUI as YourPokemGUI
from SearchPokLog import MainGUI as SearchPokLogGUI
from SearchTrainLog import TrainerGUI as SearchTrainLogGUI
from Game import BattleGUI


class WindowManager:
    def __init__(self):
        self.username = None
        self.password = None
        self.is_logged_in = False
        self.root = Tk()
        self.current_frame = None

    def show_gui1(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = FirstGUI(self.root, self.show_gui2)

    def show_gui2(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SecondGUI(self.root, self.show_gui1)
        # Configure all buttons for the Choice menu
        self.current_frame.button_1.configure(command=self.show_main_unlogged)  # Continue without login
        self.current_frame.button_2.configure(command=self.show_sign_in)  # Sign In
        self.current_frame.button_3.configure(command=self.show_sign_up)  # Sign Up

    def handle_login(self, login_successful, username = None, password = None):
        if login_successful:
            self.is_logged_in = True
            self.username = username  # Przechowujemy dane użytkownika w WindowManager
            self.password = password
            print("Logowanie powiodło się!")
            self.show_main_logged()
        else:
            print("Logowanie nie powiodło się.")
            self.show_sign_in()

    def show_sign_in(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SignInGUI(self.root, self.handle_login)

    def show_sign_up(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SignUpGUI(self.root, self.handle_login)

    def show_main_unlogged(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainGUI(self.root, self.show_gui2)
        # Configure all buttons in MainScreenUnlog
        self.current_frame.button_1.configure(command=self.show_gui2)  # Login button
        self.current_frame.button_2.configure(command=self.show_pokemon_search)  # Find Pokémon
        self.current_frame.button_3.configure(command=self.show_trainer_search)  # Find Trainers

    def show_pokemon_search(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = PokemonSearchGUI(self.root, self.show_main_unlogged)
        # Configure buttons in Pokemon Search screen
        self.current_frame.button_1.configure(command=self.show_gui2)  # Login button

    def show_trainer_search(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TrainerGUI(self.root, self.show_main_unlogged)
        # Configure buttons in Trainer Search screen
        self.current_frame.button_1.configure(command=self.show_gui2)  # Login button

    def show_game(self):
        """Method to show the game screen"""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = BattleGUI(self.root, self.show_main_logged, self.username, self.password)
        # self.current_frame.button_1.configure(command=self.show_gui2)
        # Configure the fight button if needed
        # self.current_frame.button_1.configure(command=lambda: print("Fight clicked"))

    def show_main_logged(self):
        if not self.username or not self.password:
            messagebox.showerror("Error", "You must be logged in to access this screen.")
            self.show_sign_in()
            return

        if self.current_frame:
            self.current_frame.destroy()

        # Przekazujemy dane użytkownika do MainScreenLogUr
        self.current_frame = MainScreenLogUr(
            self.root,
            self.show_gui2,
            username=self.username,
            password=self.password
        )

        # Konfiguracja przycisków
        self.current_frame.button_2.configure(command=self.show_add_del_pokemon)
        self.current_frame.button_3.configure(command=self.show_your_pokemon)
        self.current_frame.button_4.configure(command=self.show_search_pokemon_logged)
        self.current_frame.button_5.configure(command=self.show_search_trainer_logged)
        self.current_frame.button_1.configure(command=self.show_game)  # Przycisk do gry

    def show_add_del_pokemon(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = PokemonGUI(self.root, self.show_main_logged, username=self.username, password=self.password)
        self.current_frame.button_1.configure(command=self.show_game)  # Start game button

    def show_your_pokemon(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = YourPokemGUI(self.root, self.show_main_logged, username=self.username, password=self.password)
        self.current_frame.button_1.configure(command=self.show_game)  # Start game button

    def show_search_pokemon_logged(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SearchPokLogGUI(self.root, self.show_main_logged, username=self.username,
            password=self.password)
        self.current_frame.button_1.configure(command=self.show_game)  # Start game button

    def show_search_trainer_logged(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SearchTrainLogGUI(self.root, self.show_main_logged,  username=self.username,
            password=self.password)
        self.current_frame.button_1.configure(command=self.show_game)  # Start game button

    def run(self):
        self.show_gui1()  # Start with the first GUI
        self.root.mainloop()


def main():
    app = WindowManager()
    app.run()


if __name__ == "__main__":
    main()

