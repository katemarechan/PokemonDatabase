from pathlib import Path
from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox
import mysql.connector

class SignUpGUI(Frame):
    def __init__(self, master=None, switch_callback=None):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback

        # Setup the initial window configuration
        self.master.geometry("600x400")
        self.master.configure(bg="#2A2522")

        # Setup assets path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"assets\frame3")

        self.create_widgets()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def create_widgets(self):
        # Create and configure the canvas
        self.canvas = Canvas(
            self.master,
            bg="#2A2522",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create red rectangle
        self.canvas.create_rectangle(
            458.0,
            0.0,
            600.0,
            400.0,
            fill="#C01B1B",
            outline=""
        )

        # Load and create images
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(458.0, 200.0, image=self.image_1)

        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(458.0, 200.0, image=self.image_2)

        self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(244.0, 259.0, image=self.image_3)

        # Create text elements
        self.canvas.create_text(
            37.0,
            39.0,
            anchor="nw",
            text="Sign Up",
            fill="#FFFFFF",
            font=("Mohave Regular", 20 * -1)
        )

        self.canvas.create_text(
            39.0,
            96.0,
            anchor="nw",
            text="Nickname",
            fill="#FFFFFF",
            font=("Mohave Regular", 15 * -1)
        )

        self.canvas.create_text(
            38.0,
            159.0,
            anchor="nw",
            text="Password",
            fill="#FFFFFF",
            font=("Mohave Regular", 15 * -1)
        )

        self.canvas.create_text(
            39.0,
            219.0,
            anchor="nw",
            text="Region",
            fill="#FFFFFF",
            font=("Mohave Regular", 15 * -1)
        )

        # Create entries
        self.entry_bg_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(147.5, 137.5, image=self.entry_bg_1)

        self.entry_1 = Entry(
            self.master,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=39.0,
            y=125.0,
            width=217.0,
            height=23.0
        )

        self.entry_bg_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(147.5, 200.5, image=self.entry_bg_2)

        self.entry_2 = Entry(
            self.master,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(
            x=39.0,
            y=188.0,
            width=217.0,
            height=23.0
        )


        self.entry_bg_3 = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.canvas.create_image(147.5, 137.5, image=self.entry_bg_1)

        self.entry_3 = Entry(
            self.master,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_3.place(
            x=39.0,
            y=249.0,
            width=217.0,
            height=23.0
        )

        # Create button with text directly on it
        self.button_image = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button = Button(
            self.master,
            image=self.button_image,
            borderwidth=0,
            highlightthickness=0,
            command= self.button_click,
            relief="flat",
            text="Sign Up",  # Add text directly to button
            compound="center",  # Center the text over the image
            font=("Mohave Regular", 15 * -1),  # Match the size of other text elements
            fg="#386ABB",  # Blue text color
            bg="#D9D9D9"  # Match button background
        )
        self.button.place(
            x=473.0,
            y=352.0,
            width=113.0,
            height=24.0
        )

        self.master.resizable(False, False)

    def button_click(self):
        # Pobranie danych z pól tekstowych
        nickname = self.entry_1.get()
        password = self.entry_2.get()
        region = self.entry_3.get()

        # Wywołanie procedury `register_User` w bazie danych
        try:
            result = self.register_user_in_db(nickname, password, region)
            messagebox.showinfo("Success", f"User registered successfully: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")

    def destroy(self):
        """Properly destroy all widgets"""
        self.canvas.destroy()
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.button.destroy()
        super().destroy()

    def register_user_in_db(self, username, password, region):
        """Łączy się z bazą danych i wywołuje procedurę `register_User`."""
        # Połączenie z bazą danych
        connection = mysql.connector.connect(
            host="localhost",  # Zmień na adres serwera bazy danych
            user="unlogged_User",  # Użytkownik bazy danych
            password="password",  # Hasło do bazy danych
            database="bazy_danych_projekt_mysql"  # Nazwa bazy danych
        )

        try:
            cursor = connection.cursor()
            # Wywołanie procedury składowanej
            cursor.callproc('Register_User', [username, password, region])
            connection.commit()
            return f"Nickname: {username}, Region: {region}"  # Informacja zwrotna
        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    from tkinter import Tk

    root = Tk()
    app = SignUpGUI(root)
    root.mainloop()