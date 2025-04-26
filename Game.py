from pathlib import Path
from tkinter import Tk, Frame, Canvas, Button, PhotoImage, Entry
import mysql.connector


def play_game_from_gui(username, password, display_callback, pokemon_entry):
    """Pobiera dane z GUI, porównuje Pokemony i wyświetla wynik w GUI."""
    try:
        # Pobranie wartości wpisanej w polu tekstowym dla ID Pokémona
        pokemon_id = pokemon_entry.get()
        if not pokemon_id.isdigit():
            raise ValueError("Wartość ID Pokémona musi być liczbą całkowitą.")

        pokemon_id = int(pokemon_id)  # Konwersja na liczbę całkowitą

        # Połączenie z bazą danych
        mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="bazy_danych_projekt_mysql"
        )
        mycursor = mydb.cursor()

        # Pobranie User_ID dla bieżącego użytkownika
        get_user_id_query = "SELECT User_ID FROM Users WHERE Username = %s"
        mycursor.execute(get_user_id_query, (username,))
        current_user_data = mycursor.fetchone()
        if not current_user_data:
            raise ValueError("Nie znaleziono użytkownika w bazie danych.")
        current_user_id = current_user_data[0]  # Numer User_ID dla bieżącego użytkownika

        # Zapytanie o Pokémona wybranego przez użytkownika
        query_user_pokemon = """
        SELECT p.Pokemon_Name, p.HP, p.Strength, p.Pokemon_ID 
        FROM Pokemon p 
        WHERE p.User_ID = %s AND p.Pokemon_ID = %s
        """
        mycursor.execute(query_user_pokemon, (current_user_id, pokemon_id))
        user_pokemon = mycursor.fetchone()

        if not user_pokemon:
            raise ValueError("Nie znaleziono Pokémona z podanym ID dla tego użytkownika.")

        # Zapytanie o wylosowanego użytkownika i Pokémona
        query_random_user = """
        SELECT u.User_ID, u.Username, p.Pokemon_Name, p.HP, p.Strength, p.Pokemon_ID
        FROM users u
        JOIN Pokemon p ON u.User_ID = p.User_ID
        WHERE u.Pokemon_Count > 0 AND u.Pokemon_Count IS NOT NULL 
        ORDER BY RAND() LIMIT 1
        """
        mycursor.execute(query_random_user)

        # Pobranie wylosowanego użytkownika i jego Pokémona
        random_user_data = mycursor.fetchone()

        if not random_user_data:
            display_callback("Brak wylosowanego użytkownika z Pokémonem.")
            return

        random_user_pokemon = {
            'User_ID': random_user_data[0],
            'Username': random_user_data[1],
            'Pokemon_Name': random_user_data[2],
            'HP': random_user_data[3],
            'Strength': random_user_data[4],
            'Pokemon_ID': random_user_data[5],
        }

        # Formatowanie informacji o Pokémonach i użytkownikach
        user_pokemon_text = f"Twój Pokémon: {user_pokemon[0]}\nHP: {user_pokemon[1]}\nSiła: {user_pokemon[2]}\nPokemon ID: {user_pokemon[3]}"
        random_user_text = f"Wylosowany użytkownik: {random_user_pokemon['Username']}\nPokémon: {random_user_pokemon['Pokemon_Name']}\nHP: {random_user_pokemon['HP']}\nSiła: {random_user_pokemon['Strength']}\nPokemon ID: {random_user_pokemon['Pokemon_ID']}"

        # Porównanie Pokémonów na podstawie HP i Strength
        user_wins = 0
        random_user_wins = 0

        if user_pokemon[1] > random_user_pokemon['HP']:
            user_wins += 1
        elif user_pokemon[1] < random_user_pokemon['HP']:
            random_user_wins += 1

        if user_pokemon[2] > random_user_pokemon['Strength']:
            user_wins += 1
        elif user_pokemon[2] < random_user_pokemon['Strength']:
            random_user_wins += 1

        # Wynik gry
        if user_wins > random_user_wins:
            result_message = "Twój Pokémon wygrał!"
            winner_id = current_user_id
            winner_pokemon_id = user_pokemon[3]
            loser_id = random_user_pokemon['User_ID']
            loser_pokemon_id = random_user_pokemon['Pokemon_ID']
        elif user_wins < random_user_wins:
            result_message = "Wylosowany Pokémon wygrał!"
            winner_id = random_user_pokemon['User_ID']
            winner_pokemon_id = random_user_pokemon['Pokemon_ID']
            loser_id = current_user_id
            loser_pokemon_id = user_pokemon[3]
        else:
            result_message = "Walka zakończyła się remisem!"
            display_callback(user_pokemon_text + "\n\n" + random_user_text + "\n\n" + result_message)
            return  # W przypadku remisu nie przyznajemy XP

        # Wyświetlanie wyników w GUI
        display_callback(user_pokemon_text + "\n\n" + random_user_text + "\n\n" + result_message)

        # Wywołanie procedur Grant_XP
        grant_xp_query = "CALL Grant_XP(%s, %s, %s)"

        # Zapis zwycięzcy
        mycursor.execute(grant_xp_query, (winner_id, winner_pokemon_id, True))
        # Zapis przegranego
        mycursor.execute(grant_xp_query, (loser_id, loser_pokemon_id, False))

        # Zatwierdzenie zmian w bazie danych
        mydb.commit()

    except mysql.connector.Error as err:
        display_callback(f"Błąd bazy danych: {err}")
    except ValueError as ve:
        display_callback(f"Błąd: {ve}")
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def display_user_and_pokemon(username, password, display_user_callback, display_pokemon_callback):
    """Wyświetla dane użytkownika i Pokémona w GUI."""
    try:
        # Połączenie z bazą danych
        mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="bazy_danych_projekt_mysql"
        )
        mycursor = mydb.cursor()

        # Losowanie użytkownika
        query_user = "SELECT u.User_ID, u.Username, r.Region_Name, u.Pokemon_Count, u.User_XP_Count FROM users u JOIN Regions r ON u.Region_ID = r.Region_ID WHERE u.Pokemon_Count > 0 AND u.Pokemon_Count IS NOT NULL ORDER BY RAND() LIMIT 1"
        mycursor.execute(query_user)

        # Pobranie użytkownika
        user = mycursor.fetchone()
        column_names_user = [desc[0] for desc in mycursor.description]

        if user:
            # Formatowanie wyników użytkownika
            user_text = "\n".join(f"{column_names_user[i]}: {user[i]}" for i in range(len(user)))
            display_user_callback(user_text)

            # Pobranie user_ID z losowego użytkownika
            user_id = user[column_names_user.index("User_ID")]

            # Losowanie Pokémona przypisanego do user_ID
            query_pokemon = "SELECT p.Pokemon_Name, p.Evolution_Stage, p.Weight, p.Height, p.HP, e.Energy_Name FROM Pokemon p JOIN Energy e ON p.Energy_ID = e.Energy_ID WHERE p.User_ID = %s ORDER BY RAND() LIMIT 1"
            mycursor.execute(query_pokemon, (user_id,))

            # Pobranie Pokémona
            pokemon = mycursor.fetchone()
            column_names_pokemon = [desc[0] for desc in mycursor.description]

            if pokemon:
                # Formatowanie wyników Pokémona
                pokemon_text = "\n".join(f"{column_names_pokemon[i]}: {pokemon[i]}" for i in range(len(pokemon)))
                display_pokemon_callback(pokemon_text)
            else:
                display_pokemon_callback("Brak Pokémonów przypisanych do tego użytkownika.")
        else:
            display_user_callback("Brak użytkowników w bazie danych.")
            display_pokemon_callback("")

    except mysql.connector.Error as err:
        display_user_callback(f"Błąd bazy danych: {err}")
        display_pokemon_callback("")
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

class BattleGUI(Frame):
    def __init__(self, master=None, switch_callback=None, username=None, password=None):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.username = username
        self.password = password

        # Setup the initial window configuration
        self.master.geometry("1280x720")
        self.master.configure(bg="#2A2522")

        # Setup assets path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"assets\frame12")

        # Create the widgets (this initializes self.canvas)
        self.create_widgets()

        # Load random user and Pokémon after widgets are ready
        self.load_random_user_and_pokemon()

        self.master.resizable(False, False)


    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def create_widgets(self):
        # Create and configure the canvas
        self.canvas = Canvas(
            self.master,
            bg="#2A2522",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create title text
        self.canvas.create_text(
            425.0,
            33.0,
            anchor="nw",
            text="Choose your Pokémon!",
            fill="#FFFFFF",
            font=("Mohave Regular", 48 * -1)
        )

        # Create rectangles
        self.create_rectangles()

        # Create battle text
        self.create_battle_text()

        # Setup buttons
        self.setup_buttons()

        # Add the textbox for Pokemon ID input
        self.create_textbox()

        self.master.resizable(False, False)

    def create_rectangles(self):
        # Left pokemon display area
        self.canvas.create_rectangle(
            144.0,
            101.0,
            537.0,
            609.0,
            fill="#D9D9D9",
            outline=""
        )

        # Right pokemon display area
        self.canvas.create_rectangle(
            744.0,
            101.0,
            1137.0,
            609.0,
            fill="#D9D9D9",
            outline=""
        )

        # Header rectangles (blue and red)
        self.canvas.create_rectangle(
            744.0,
            101.0,
            1137.0,
            165.0,
            fill="#386ABB",  # Blue for opponent
            outline=""
        )

        self.canvas.create_rectangle(
            144.0,
            101.0,
            537.0,
            165.0,
            fill="#9B2828",  # Red for player
            outline=""
        )

        # Pokemon display areas (gray rectangles)
        self.canvas.create_rectangle(
            765.0,
            181.0,
            1123.0,
            450.0,
            fill="#575656",
            outline=""
        )

        # self.canvas.create_rectangle(
        #     765.0,
        #     387.0,
        #     1123.0,
        #     578.0,
        #     fill="#575656",
        #     outline=""
        # )

    def create_battle_text(self):
        # Create the header texts
        # Center text in the rectangles
        # For opponent (right rectangle)
        self.canvas.create_text(
            (744.0 + 1137.0) / 2,  # Center of right rectangle
            133.0,  # Vertically centered in header
            anchor="center",
            text="Battle Result",
            fill="#FFFFFF",
            font=("Mohave Regular", 24)
        )

        # For player (left rectangle)
        self.canvas.create_text(
            (144.0 + 537.0) / 2,  # Center of left rectangle
            133.0,  # Vertically centered in header
            anchor="center",
            text="Your Pokémon",
            fill="#FFFFFF",
            font=("Mohave Regular", 24)
        )

    def setup_buttons(self):
        # Fight button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_battle,  # Przypisanie metody
            relief="flat",
            text="FIGHT!",
            font=("Mohave Regular", 20),
            fg="#000000",
            compound="center"
        )

        self.button_1.place(
            x=558.0,
            y=293.0,
            width=165.0,
            height=52.0
        )

    def create_textbox(self):
        """Creates a textbox inside the left rectangle for Pokémon ID input."""
        # Create an entry widget
        self.pokemon_id_entry = Entry(
            self.master,
            font=("Mohave Regular", 16),
            justify="center"
        )
        # Place the textbox inside the left rectangle
        self.pokemon_id_entry.place(
            x=145.0,  # X coordinate inside the left rectangle
            y=170.0,  # Y coordinate inside the left rectangle
            width=390.0,  # Width of the textbox
            height=50.0  # Height of the textbox
        )
        # Add a placeholder behavior (optional)
        self.pokemon_id_entry.insert(0, "Enter Pokémon ID")
        self.pokemon_id_entry.bind("<FocusIn>", self.clear_placeholder)

    def clear_placeholder(self, event):
        """Clears the placeholder text when the textbox gains focus."""
        if self.pokemon_id_entry.get() == "Enter Pokémon ID":
            self.pokemon_id_entry.delete(0, "end")

    def start_battle(self):
        print("Button clicked!")  # Dodanie prostego wydruku
        username = self.username
        password = self.password
        play_game_from_gui(username, password, self.display_battle_results, self.pokemon_id_entry)

    def display_battle_results(self, result_text):
            """Wyświetla wyniki walki w lewym prostokącie."""
            # Usuń poprzednie wyniki
            self.canvas.delete("battle_results")

            # Podziel tekst na linie
            lines = result_text.split("\n")
            y_position = 200  # Pozycja startowa poniżej textboxa
            line_height = 20

            for line in lines:
                self.canvas.create_text(
                    (765.0 + 1123.0) / 2,  # Środek lewego prostokąta
                    y_position,
                    anchor="center",
                    text=line,
                    fill="#000000",
                    font=("Mohave Regular", 12),
                    tags="battle_results"
                )
                y_position += line_height

    def load_random_user_and_pokemon(self):
        """Automatycznie ładuje losowego użytkownika i jego Pokémona po uruchomieniu."""
        username = "root"  # Zmień na swoją nazwę użytkownika
        password = "password"  # Zmień na swoje hasło

        def display_user_callback(user_result):
            """Wyświetla dane użytkownika w prawym górnym prostokącie."""
            # Usuń istniejący tekst użytkownika
            self.canvas.delete("user_display")

            # Podziel tekst na linie, aby zmieścić go w prostokącie
            lines = user_result.split("\n")
            y_position = 200  # Startowa pozycja tekstu w pionie
            line_height = 20  # Wysokość pojedynczej linii tekstu

            for line in lines:
                self.canvas.create_text(
                    (765.0 + 1123.0) / 2,  # X: Center of the right gray rectangle
                    y_position,
                    anchor="center",
                    text=line,
                    fill="#FFFFFF",
                    font=("Mohave Regular", 12),  # Zmniejszony rozmiar czcionki
                    tags="user_display"  # Tag for clearing text later
                )
                y_position += line_height

        def display_pokemon_callback(pokemon_result):
            """Wyświetla dane Pokémona w prawym dolnym prostokącie."""
            # Usuń istniejący tekst Pokémona
            self.canvas.delete("pokemon_display")

            # Podziel tekst na linie, aby zmieścić go w prostokącie
            lines = pokemon_result.split("\n")
            y_position = 400  # Startowa pozycja tekstu w pionie
            line_height = 20  # Wysokość pojedynczej linii tekstu

            for line in lines:
                self.canvas.create_text(
                    (765.0 + 1123.0) / 2,  # X: Center of the right gray rectangle
                    y_position,
                    anchor="center",
                    text=line,
                    fill="#FFFFFF",
                    font=("Mohave Regular", 12),  # Zmniejszony rozmiar czcionki
                    tags="pokemon_display"  # Tag for clearing text later
                )
                y_position += line_height

        #display_user_and_pokemon(username, password, display_user_callback, display_pokemon_callback)


# Example usage
if __name__ == "__main__":
    root = Tk()
    app = BattleGUI(root)
    root.mainloop()
