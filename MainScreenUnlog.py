from pathlib import Path
from tkinter import Frame, Canvas, Button, PhotoImage
import mysql.connector

# Funkcja do pobierania danych z bazy
def fetch_pokemons(filters=None):
    try:
        # Połączenie z bazą danych
        mydb = mysql.connector.connect(
            host="localhost",
            user="unloged_User",
            password="password",
            database="bazy_danych_projekt_mysql"
        )
        mycursor = mydb.cursor()

        # Budowanie zapytania SQL
        query = "SELECT * FROM pokemon"
        values = []

        if filters:
            conditions = []
            for column, value in filters.items():
                conditions.append(f"{column} = %s")
                values.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        mycursor.execute(query, values)

        # Pobranie wyników i nazw kolumn
        rows = mycursor.fetchall()
        column_names = [desc[0] for desc in mycursor.description]

        # Formatowanie wyników
        column_widths = [
            max(len(str(row[i])) for row in rows) if rows else 0
            for i in range(len(column_names))
        ]
        column_widths = [
            max(len(column_names[i]), column_widths[i])
            for i in range(len(column_names))
        ]

        formatted_text = " | ".join(f"{column_names[i]:<{column_widths[i]}}" for i in range(len(column_names))) + "\n"
        formatted_text += "-" * (sum(column_widths) + 3 * (len(column_widths) - 1)) + "\n"

        for row in rows:
            formatted_text += " | ".join(f"{str(row[i]):<{column_widths[i]}}" for i in range(len(row))) + "\n"

        return formatted_text
    except mysql.connector.Error as err:
        return f"Błąd bazy danych: {err}"
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()



# Funkcja do wyświetlania wyników w aplikacji
def display_pokemons(text_field=None, username=None, password=None, filters=None):
    results = fetch_pokemons(filters)  # Przekaż filtry do funkcji pobierającej dane
    text_field.config(state="normal")  # Odblokuj pole tekstowe, aby wstawić tekst
    text_field.delete("1.0", "end")  # Wyczyszczenie pola tekstowego
    text_field.insert("1.0", results)  # Wstawienie wyników
    text_field.config(state="disabled")  # Zablokuj pole tekstowe po wstawieniu


class MainGUI(Frame):
    def __init__(self, master=None, switch_callback=None):
        super().__init__(master)
        self.button_4 = None
        self.master = master
        self.switch_callback = switch_callback

        # Setup the initial window configuration
        self.master.geometry("1280x720")
        self.master.configure(bg="#2A2522")

        # Setup assets path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"assets\frame5")

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

        # Create centered welcome text
        self.canvas.create_text(
            1280 / 2,  # Center horizontally (half of window width)
            32.0,  # Vertically positioned near top
            anchor="center",
            text="Great to see you!",
            fill="#FFFFFF",
            font=("Mohave Regular", 48 * -1)
        )

        # Create main rectangle
        self.canvas.create_rectangle(
            39.0,
            103.0,
            355.0,
            683.0,
            fill="#D9D9D9",
            outline=""
        )

        # Create buttons
        self.setup_buttons()

        # Create images
        self.setup_images()

        # Create text elements
        self.create_text_elements()

        self.master.resizable(False, False)

    def setup_buttons(self):
        # Button 1 (Login)
        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat",
            text="Log In/Sign In",
            font=("Mohave Regular", 24),
            fg="#FFFFFF",
            compound="center"  # This ensures text appears on top of the image
        )
        self.button_1.place(
            x=39.0,
            y=580.0,
            width=316.0,
            height=107.0
        )

        # Button 2 (Find Pokémon)
        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.master,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat",
            text="Find Pokémon",
            font=("Mohave Regular", 24),
            fg="#000000",
            compound="center"
        )
        self.button_2.place(
            x=39.0,
            y=103.0,
            width=316.0,
            height=63.0
        )

        # Button 3 (Find Trainers)
        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.master,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat",
            text="Find Trainers",
            font=("Mohave Regular", 24),
            fg="#000000",
            compound="center"
        )
        self.button_3.place(
            x=39.0,
            y=171.0,
            width=316.0,
            height=65.0
        )

    def setup_images(self):
        # Image 1 (bottom left)
        self.image_1_photo = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            195.0,
            579.0,
            image=self.image_1_photo
        )

        # Image 2 (bottom right)
        self.image_2_photo = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            1084.0,
            640.0,
            image=self.image_2_photo
        )

        # Image 3 (center)
        self.image_3_photo = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        # Get the image dimensions
        self.image_3 = self.canvas.create_image(
            1280 / 2,  # Center horizontally (half of window width)
            720 / 2,  # Center vertically (half of window height)
            image=self.image_3_photo
        )

    def create_text_elements(self):
        # Text is now handled directly by the buttons
        pass

    def destroy(self):
        """Properly destroy all widgets"""
        self.canvas.destroy()
        self.button_1.destroy()
        self.button_2.destroy()
        self.button_3.destroy()
        super().destroy()


# Example usage
if __name__ == "__main__":
    from tkinter import Tk

    root = Tk()
    app = MainGUI(root)
    root.mainloop()