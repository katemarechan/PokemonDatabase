from pathlib import Path
from tkinter import Tk, Frame, Canvas, Button, PhotoImage
import mysql.connector

def fetch_user_data(username, password):
    """Pobiera dane użytkownika z bazy danych."""
    try:
        # Połącz się z bazą danych
        connection = mysql.connector.connect(
            host="localhost",
            user= username,  # Zmień na swoją nazwę użytkownika
            password= password,  # Zmień na swoje hasło
            database="bazy_danych_projekt_mysql"  # Zmień na swoją nazwę bazy danych
        )
        cursor = connection.cursor(dictionary=True)

        # Wykonaj zapytanie SQL
        query = "SELECT Role_ID, Join_Date, User_XP_Count, Region_ID, Pokemon_Count FROM Users WHERE username = %s"
        cursor.execute(query, (username,))  # Dodano przecinek dla krotki
        result = cursor.fetchone()

        # Zamknij połączenie
        cursor.close()
        connection.close()

        # Zwróć dane użytkownika (lub pusty słownik, jeśli nie znaleziono użytkownika)
        return result if result else {}

    except mysql.connector.Error as err:
        print(f"Błąd połączenia z bazą danych: {err}")
        return {}

class MainGUI(Frame):
    def __init__(self, master=None, switch_callback=None, username = None, password = None):
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
        self.assets_path = self.output_path / Path(r"assets\frame4")

        self.create_widgets()


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

        # Create welcome text (centered)
        self.canvas.create_text(
            1280 / 2,
            32.0,
            anchor="center",
            text="Great to see you!",
            fill="#FFFFFF",
            font=("Mohave Regular", 48 * -1)
        )

        # Create main rectangles
        self.create_rectangles()

        # Create buttons
        self.setup_buttons()

        # Create images
        self.setup_images()

        # Create text elements
        self.create_text_elements()

        self.master.resizable(False, False)

    def create_rectangles(self):
        # Left rectangle
        self.canvas.create_rectangle(
            39.0,
            103.0,
            355.0,
            683.0,
            fill="#D9D9D9",
            outline=""
        )

        # Right rectangle (stats)
        self.canvas.create_rectangle(
            896.0,
            103.0,
            1267.0,
            370.0,
            fill="#D9D9D9",
            outline=""
        )

        # Stats title rectangle
        self.canvas.create_rectangle(
            955.0,
            33.0,
            1208.0,
            74.0,
            fill="#386ABB",
            outline=""
        )

        # Black rectangle for stars
        self.canvas.create_rectangle(
            908.0,
            121.0,
            1119.0,
            146.0,
            fill="#000000",
            outline=""
        )

    def setup_buttons(self):
        # Add/Delete Pokémon button
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.master,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat",
            text="Add/Delete Pokémon",
            font=("Mohave Regular", 17),
            fg="#000000",
            compound="center"
        )
        self.button_2.place(x=39.0, y=103.0, width=316.0, height=63.0)

        # Look at your Pokémons button
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.master,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat",
            text="Look at your Pokémons",
            font=("Mohave Regular", 17),  # Smaller font for longer text
            fg="#000000",
            compound="center"
        )
        self.button_3.place(x=39.0, y=171.0, width=316.0, height=65.0)

        # Find Pokémon button
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            self.master,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat",
            text="Find Pokémon",
            font=("Mohave Regular", 17),  # Medium font for medium-length text
            fg="#000000",
            compound="center"
        )
        self.button_4.place(x=39.0, y=241.0, width=316.0, height=65.0)

        # Find Trainers button
        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_5 = Button(
            self.master,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat",
            text="Find Trainers",
            font=("Mohave Regular", 17),  # Medium font for medium-length text
            fg="#000000",
            compound="center"
        )
        self.button_5.place(x=39.0, y=311.0, width=316.0, height=65.0)

        # Start a Game button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat",
            text="Start a Game",
            font=("Mohave Regular", 22),  # Slightly larger font for short text on large button
            fg="#FFFFFF",
            compound="center"
        )
        self.button_1.place(x=39.0, y=580.0, width=316.0, height=107.0)

    def setup_images(self):
        # Stars images
        self.image_1_photo = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(932.0, 133.0, image=self.image_1_photo)

        self.image_2_photo = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(957.0, 133.0, image=self.image_2_photo)

        self.image_3_photo = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(982.0, 133.0, image=self.image_3_photo)

        # Bottom images
        self.image_4_photo = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(195.0, 579.0, image=self.image_4_photo)

        self.image_5_photo = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(1084.0, 640.0, image=self.image_5_photo)

        # Center image
        self.image_6_photo = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.image_6 = self.canvas.create_image(
            1280 / 2,  # Center horizontally
            720 / 2,  # Center vertically
            image=self.image_6_photo
        )

    def create_text_elements(self):
        # Stats section text
        self.canvas.create_text(
            1009.0, 37.0,
            anchor="nw",
            text="Your statistics",
            fill="#FAF193",
            font=("Mohave Regular", 24 * -1)
        )

          # Zastąp odpowiednim identyfikatorem użytkownika
        user_database_parameters = fetch_user_data(self.username, self.password)

        # Pobieranie danych użytkownika
        role = user_database_parameters.get("Role_ID")
        join_date = user_database_parameters.get("Join_Date")
        xp_count = user_database_parameters.get("User_XP_Count")
        region = user_database_parameters.get("Region_ID")
        pok_count = user_database_parameters.get("Pokemon_Count")

        # Stats labels
        stats_labels = [
            ("Your Role:", "#FAF193", 918.0, 166.0, role),
            ("Join Date:", "#386ABB", 919.0, 204.0, join_date),
            ("XP Count:", "#9B2828", 920.0, 242.0, xp_count),
            ("Region:", "#512886", 918.0, 280.0, region),
            ("Pok. Count:", "#FF8923", 920.0, 318.0, pok_count),
        ]

        for text, color, x, y, value in stats_labels:
            self.canvas.create_text(
                x, y,
                anchor="nw",
                text=f"{text} {value}",
                fill=color,
                font=("Mohave Regular", 24 * -1)
            )



    def destroy(self):
        """Properly destroy all widgets"""
        self.canvas.destroy()
        for button in [self.button_1, self.button_2, self.button_3, self.button_4, self.button_5]:
            button.destroy()
        super().destroy()


# Example usage
if __name__ == "__main__":
    root = Tk()
    app = MainGUI(root)
    root.mainloop()


# Poberanie danych ze zmiennej user_data działa co oznacz ze dobrze przekazywany jest ten parametr miedzy klasami; trzeba zrobic to samo z pozostałymi i ta da