from pathlib import Path
from tkinter import Tk, Frame, Canvas, Entry, Button, PhotoImage, Text
import mysql.connector

# Funkcja do pobierania danych z bazy
def fetch_users(filters=None):
    try:
        # Połączenie z bazą danych
        mydb = mysql.connector.connect(
            host="localhost",
            user="unlogged_User",
            password="password",
            database="bazy_danych_projekt_mysql"
        )
        mycursor = mydb.cursor()

        # Budowanie zapytania SQL
        query = "SELECT * FROM users"
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
def display_users(text_field=None, filters=None):
    results = fetch_users(filters)  # Przekaż filtry do funkcji pobierającej dane
    text_field.config(state="normal")  # Odblokuj pole tekstowe, aby wstawić tekst
    text_field.delete("1.0", "end")  # Wyczyszczenie pola tekstowego
    text_field.insert("1.0", results)  # Wstawienie wyników
    text_field.config(state="disabled")  # Zablokuj pole tekstowe po wstawieniu

class TrainerGUI(Frame):
    def __init__(self, master=None, switch_callback=None):
        super().__init__(master)
        self.text_field = None
        self.master = master
        self.switch_callback = switch_callback

        # Setup the initial window configuration
        self.master.geometry("1280x720")
        self.master.configure(bg="#2A2522")

        # Setup assets path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"assets\frame10")

        self.create_widgets()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def apply_filters(self):
        filters = {}
        for entry_name, entry_widget in self.entries.items():
            value = entry_widget.get().strip()  # Pobierz wartość z entry i usuń nadmiarowe spacje
            if value:  # Uwzględnij tylko wypełnione pola
                filters[entry_name] = value

        # Wywołaj funkcję wyświetlania danych z uwzględnieniem filtrów
        display_users(
            text_field=self.text_field,
            filters=filters
        )

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

        # Create title text (centered)
        self.canvas.create_text(
            594.0,
            16.0,
            anchor="nw",
            text="Trainers",
            fill="#FFFFFF",
            font=("Mohave Regular", 48 * -1)
        )

        # Create rectangles
        self.create_rectangles()

        # Setup buttons
        self.setup_buttons()

        # Setup entries
        self.setup_entries()

        # Create text elements
        self.create_text_elements()

        # Setup images
        self.setup_images()

        self.master.resizable(False, False)

    def create_rectangles(self):
        # Left rectangle (search filters)
        self.canvas.create_rectangle(
            39.0,
            103.0,
            355.0,
            683.0,
            fill="#D9D9D9",
            outline=""
        )

        # Right rectangle (display area)
        self.canvas.create_rectangle(
            423.0,
            100.0,
            1248.0,
            680.0,
            fill="#D9D9D9",
            outline=""
        )

    def setup_buttons(self):
        # Search button
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.master,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command= self.apply_filters,
            relief="flat",
            text="Search",
            font=("Mohave Regular", 24),
            fg="#FFFFFF",
            compound="center"  # This makes the text appear on top of the image
        )
        self.button_2.place(x=120.0, y=37.0, width=149.0, height=42.0)

        # Start Game button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
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
            compound="center"  # This makes the text appear on top of the image
        )
        self.button_1.place(x=39.0, y=580.0, width=316.0, height=107.0)

    def setup_entries(self):
        # Entry configurations matching the image
        entry_configs = [
            ("Region_ID", "Region:", 103.0),
            ("Pokemon_Count", "Pokemon Count:", 171.0),
            ("Status_ID", "Status:", 241.0)
        ]

        self.entries = {}
        self.entry_images = {}

        for entry_name, label_text, y_pos in entry_configs:
            # Create entry background image
            entry_image = PhotoImage(file=self.relative_to_assets(f"{entry_name}.png"))
            self.entry_images[entry_name] = entry_image

            # Create background image
            entry_bg = self.canvas.create_image(
                197.0,
                y_pos + 31.5,
                image=entry_image
            )

            # Create the label first
            label_x = 56.0
            label_y = y_pos + 15.0

            # Create entry widget with initial text
            entry = Entry(
                self.master,
                bd=0,
                bg="#B7B5B5",
                fg="#000000",
                highlightthickness=0,
                font=("Mohave Regular", 20)  # Increased font size for better visibility
            )

            # Calculate entry position to not overlap with label
            label = self.canvas.create_text(
                label_x,
                label_y,
                anchor="nw",
                text=label_text,
                fill="#000000",
                font=("Mohave Regular", 24)
            )

            # Get label width
            bbox = self.canvas.bbox(label)
            label_width = bbox[2] - bbox[0]

            # Position entry after label
            entry_x = label_x + label_width + 10  # Add some padding
            entry_width = 316.0 - (entry_x - 39.0)  # Adjust width based on label size

            entry.place(
                x=entry_x,
                y=y_pos + 10,  # Adjusted y position for better vertical alignment
                width=entry_width,
                height=40  # Fixed height for all entries
            )

            self.entries[entry_name] = entry

    def setup_images(self):
        # Login button icon
        self.image_1_photo = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            195.0,
            579.0,
            image=self.image_1_photo
        )

    def create_text_elements(self):
        # Tworzenie pola tekstowego
        self.text_field = Text(
            bd=0,
            bg="#FFFFFF",
            fg="#000000",
            highlightthickness=0,
            wrap="none",  # Wyłączenie zawijania tekstu
            state="normal"  # Ustawione na "normal" na początku, aby można było dodać tekst
        )
        self.text_field.place(
            x=423.0,
            y=100.0,
            width=825.0,
            height=580.0
        )

        # Wyświetlanie wyników z bazy danych w polu tekstowym
        display_users(text_field=self.text_field)

        # Ustawienie pola tekstowego na "disabled" po wstawieniu tekstu
        self.text_field.config(state="disabled")

    def destroy(self):
        """Properly destroy all widgets"""
        self.canvas.destroy()
        for entry in self.entries.values():
            entry.destroy()
        self.button_1.destroy()
        self.button_2.destroy()
        super().destroy()


# Example usage
if __name__ == "__main__":
    root = Tk()
    app = TrainerGUI(root)
    root.mainloop()