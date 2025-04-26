from pathlib import Path
from tkinter import Tk, Frame, Canvas, Entry, Button, PhotoImage, Text, messagebox
import mysql.connector

# Funkcja do pobierania danych z bazy
def fetch_pokemons(username, password, filters=None):
    try:
        # Połączenie z bazą danych
        mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
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
    results = fetch_pokemons(username, password, filters)  # Przekaż filtry do funkcji pobierającej dane
    text_field.config(state="normal")  # Odblokuj pole tekstowe, aby wstawić tekst
    text_field.delete("1.0", "end")  # Wyczyszczenie pola tekstowego
    text_field.insert("1.0", results)  # Wstawienie wyników
    text_field.config(state="disabled")  # Zablokuj pole tekstowe po wstawieniu

class PokemonGUI(Frame):
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
        self.assets_path = self.output_path / Path(r"assets\frame8")

        self.create_widgets()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def claim_pokemon_from_region(self):
        try:
            # Pobierz Region_ID z pola tekstowego
            region_id_entry = self.entries.get("Pokemon_ID")
            if not region_id_entry:
                raise ValueError("Pole 'Pokemon_ID' nie zostało skonfigurowane.")

            region_id = region_id_entry.get()
            if not region_id.isdigit():
                raise ValueError("Wartość 'Pokemon_ID' musi być liczbą całkowitą.")

            region_id = int(region_id)  # Konwersja na liczbę całkowitą

            # Połączenie z bazą danych
            mydb = mysql.connector.connect(
                host="localhost",
                user=self.username,
                password=self.password,
                database="bazy_danych_projekt_mysql"
            )
            mycursor = mydb.cursor()

            # Pobierz User_ID na podstawie Username
            user_query = "SELECT User_ID FROM Users WHERE Username = %s"
            mycursor.execute(user_query, (self.username,))
            result = mycursor.fetchone()

            if not result:
                raise ValueError(f"Użytkownik '{self.username}' nie istnieje w bazie danych.")

            user_id = result[0]  # Pobierz User_ID

            # Wywołanie procedury claim_pokemon
            mycursor.callproc('claim_pokemon', [user_id, region_id])

            mydb.commit()

            # Pobranie wyników zwróconych przez procedurę
            messages = []
            for result in mycursor.stored_results():
                messages.extend(result.fetchall())

            # Wyświetlenie komunikatów w GUI
            message_text = "\n".join([str(message[0]) for message in messages])
            if message_text:
                messagebox.showinfo("Sukces", f"Operacja zakończona pomyślnie:\n{message_text}")
            else:
                messagebox.showinfo("Sukces", "Operacja zakończona pomyślnie!")



        except ValueError as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")  # Wyskakujące okno z komunikatem
        except mysql.connector.Error as err:
            if err.errno == 4500:
                messagebox.showerror("Błąd", "Nie można przejąć tego Pokemona. Spróbuj innego.")
            else:
                messagebox.showerror("Błąd bazy danych", f"Wystąpił błąd bazy danych: {err}")
        finally:
            if 'mydb' in locals() and mydb.is_connected():
                mydb.close()

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
            text="Pokémons",
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
        # Claim button
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.master,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.claim_pokemon_from_region,
            relief="flat",
            text="Claim!",
            font=("Mohave Regular", 24),
            fg="#000000",
            compound="center"
        )
        self.button_3.place(x=39.0, y=43.0, width=149.0, height=42.0)

        # Delete button
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.master,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat",
            text="Delete",
            font=("Mohave Regular", 24),
            fg="#000000",
            compound="center"
        )
        self.button_2.place(x=206.0, y=43.0, width=149.0, height=42.0)

        # Start Game button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat",
            text="Start a Game",
            font=("Mohave Regular", 24),
            fg="#FFFFFF",
            compound="center"
        )
        self.button_1.place(x=39.0, y=580.0, width=316.0, height=107.0)

    def setup_entries(self):
        # Entry configurations with labels
        entry_configs = [
            # ("Region_ID", "Region:", 103.0),
            ("Pokemon_ID", "Pokemon ID:", 171.0),
            # ("Energy_ID", "Energy Type:", 171.0),
            # ("Rarity_ID", "Rarity:", 241.0),
            # ("Color_ID", "Color:", 311.0),
            # ("Evolution_Stage", "Evolution Stage:", 381.0),
            # ("Strength", "Strength:", 451.0)
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
                font=("Mohave Regular", 20)
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
            entry_x = label_x + label_width + 10
            entry_width = 316.0 - (entry_x - 39.0)

            entry.place(
                x=entry_x,
                y=y_pos + 10,
                width=entry_width,
                height=40
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
        display_pokemons(text_field=self.text_field, username=self.username, password=self.password)

        # Ustawienie pola tekstowego na "disabled" po wstawieniu tekstu
        self.text_field.config(state="disabled")

    def destroy(self):
        """Properly destroy all widgets"""
        self.canvas.destroy()
        for entry in self.entries.values():
            entry.destroy()
        self.button_1.destroy()
        self.button_2.destroy()
        self.button_3.destroy()
        super().destroy()


# Example usage
if __name__ == "__main__":
    root = Tk()
    app = PokemonGUI(root)
    root.mainloop()