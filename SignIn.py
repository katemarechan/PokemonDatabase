from pathlib import Path
import mysql.connector
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, Frame, Label

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def login_to_database(username, password):
    """
    Funkcja logowania do bazy danych MySQL.
    :param username: Nazwa użytkownika wprowadzona w GUI.
    :param password: Hasło użytkownika wprowadzone w GUI.
    :return: True jeśli logowanie powiodło się, False w przeciwnym razie.
    """
    try:
        # Upewnij się, że username i password to str
        username = str(username)
        password = str(password)

        connection = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="bazy_danych_projekt_mysql"  # Podaj swoją nazwę bazy danych
        )
        if connection.is_connected():
            connection.close()
            return True  # Logowanie powiodło się
    except mysql.connector.Error as err:
        print(f"Failed to connect: {err}")
    return False  # Logowanie nie powiodło się


class SignInGUI(Frame):
    def __init__(self, master=None, switch_callback=None):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback

        # Setup the initial window configuration
        self.master.geometry("600x400")
        self.master.configure(bg="#2A2522")

        # Setup assets path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"assets\frame2")

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

        # Create yellow rectangle
        self.canvas.create_rectangle(
            458.0,
            0.0,
            600.0,
            400.0,
            fill="#FAF193",
            outline=""
        )

        # Load and create images
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(458.0, 200.0, image=self.image_1)

        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(458.0, 200.0, image=self.image_2)

        # Create text elements
        self.canvas.create_text(
            39.0,
            39.0,
            anchor="nw",
            text="Sign In",
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
            highlightthickness=0,
            show = "*"
        )
        self.entry_2.place(
            x=39.0,
            y=188.0,
            width=217.0,
            height=23.0
        )

        # Create button and text as a single unit
        self.button_image = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button = Button(
            self.master,
            image=self.button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.attempt_login,
            relief="flat",
            text="Sign In",  # Add text directly to button
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

    def destroy(self):
        """Usuwa wszystkie elementy GUI."""
        self.canvas.destroy()
        self.entry_1.destroy()
        self.entry_2.destroy()


    def attempt_login(self):
        username = self.entry_1.get()
        password = self.entry_2.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        success = login_to_database(username, password)
        if success:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            if self.switch_callback:
                self.switch_callback(True, username, password)  # Przekazanie dwóch argumentów
        else:
            messagebox.showerror("Error", "Invalid credentials or database connection failed.")
            if self.switch_callback:
                self.switch_callback(False, None, None)


if __name__ == "__main__":
    root = Tk()
    app = SignInGUI(root)
    root.mainloop()
