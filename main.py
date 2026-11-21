
# Import Tkinter to build the desktop graphical user interface.
import tkinter as tk
# Import file dialogs, popup messages, and themed table widgets.
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
# datetime provides the current date and time for operation history.
from datetime import datetime
# csv is used to save and read the operation history file.
import csv

# Import the encryption functions from the separate encryption.py module.
from encryption import encrypt_file, decrypt_file


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

# The title displayed in the application window.
APP_TITLE = "AES-Based File Encryption and Decryption"

# Find the folder where this Python file is located.
BASE_DIR = Path(__file__).resolve().parent

# Define the default folder for encrypted output files.
ENCRYPTED_DIR = BASE_DIR / "encrypted_files"
# Define the default folder for recovered (decrypted) files.
DECRYPTED_DIR = BASE_DIR / "decrypted_files"

# Define the CSV file used to store operation history.
HISTORY_FILE = BASE_DIR / "operation_history.csv"

# Create the output folders if they do not already exist.
ENCRYPTED_DIR.mkdir(exist_ok=True)
DECRYPTED_DIR.mkdir(exist_ok=True)


# ==========================================
# TEAM MEMBERS
# ==========================================

# Store the names and university IDs displayed in the application.
STUDENTS = [
    ("Aljohara Alsayaari", "202308374"),
    ("Rahaf Aljaal", "202107176"),
    ("Shahad saifaldeen", "202002676"),
    ("Alreem Alshaikh", "202002033")
]


# ==========================================
# DARK THEME COLORS
# ==========================================

# Define the dark background color used by the interface.
BG_COLOR = "#101827"
# Define the color used for the main interface panels.
CARD_COLOR = "#1B293D"
# Define the background color used for input fields and the history table.
INPUT_COLOR = "#26364D"

# Blue color used for primary actions such as encryption.
ACCENT_COLOR = "#3B82F6"
# Green color used for successful operations and the decrypt button.
GREEN_COLOR = "#16A34A"
# Red color used to display errors.
RED_COLOR = "#DC2626"

# Main text color.
TEXT_COLOR = "#F8FAFC"
# Softer text color used for subtitles and less important labels.
MUTED_COLOR = "#A7B4C8"


# ==========================================
# MAIN APPLICATION
# ==========================================

# Main application class: it creates the interface and handles user actions.
class AESApplication:

    # Initialize the application and connect it to the main Tkinter window.
    def __init__(self, root):

        # Keep a reference to the main window so other methods can use it.
        self.root = root

        # Set the title shown in the window title bar.
        self.root.title(APP_TITLE)
        # Set the starting width and height of the application window.
        self.root.geometry("900x820")
        # Prevent the window from becoming too small.
        self.root.minsize(750, 750)

        # Apply the dark background color to the main window.
        self.root.configure(bg=BG_COLOR)

        # Store the path of the file selected by the user.
        self.selected_file = tk.StringVar()
        # Store the password entered in the password field.
        self.password = tk.StringVar()

        # Create a variable that controls the operation status message.
        self.status = tk.StringVar(
            value="Ready - Select a file to begin."
        )

        # Build all buttons, labels, input fields, and the history table.
        self.create_interface()
        # Load previously saved operations into the history table.
        self.load_history()

    # ======================================
    # CREATE GUI
    # ======================================

    # Create and arrange all visual elements of the application.
    def create_interface(self):

        # Project title

        # Create the main title label.
        title = tk.Label(
            self.root,
            text="AES-Based File Encryption and Decryption",
            font=("Segoe UI", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        title.pack(pady=(18, 5))

        # Create a short subtitle below the project title.
        subtitle = tk.Label(
            self.root,
            text="Protect your files with advanced encryption",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        )

        subtitle.pack(pady=(0, 12))

        # ==================================
        # TEAM MEMBERS SECTION
        # ==================================

        # Create a frame to group the team member names.
        team_frame = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        team_frame.pack(pady=(0, 12))

        tk.Label(
            team_frame,
            text="PROJECT TEAM MEMBERS",
            font=("Segoe UI", 10, "bold"),
            bg=BG_COLOR,
            fg="#60A5FA"
        ).pack(pady=(0, 5))

        # Add each team member's name and university ID to the interface.
        for name, quid in STUDENTS:

            tk.Label(
                team_frame,
                text=f"{name}     |     {quid}",
                font=("Segoe UI", 9),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            ).pack(pady=1)

        # ==================================
        # MAIN CARD
        # ==================================

        # Create the main panel that contains file and password controls.
        card = tk.Frame(
            self.root,
            bg=CARD_COLOR,
            padx=25,
            pady=18
        )

        card.pack(
            fill="x",
            padx=35,
            pady=5
        )

        # The next widgets allow the user to choose a file.
        # File selection

        tk.Label(
            card,
            text="SELECT FILE",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w")

        file_frame = tk.Frame(
            card,
            bg=CARD_COLOR
        )

        file_frame.pack(
            fill="x",
            pady=(8, 15)
        )

        # Display the selected file path in a read-only text field.
        self.file_entry = tk.Entry(
            file_frame,
            textvariable=self.selected_file,
            font=("Segoe UI", 10),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            state="readonly"
        )

        self.file_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        # Create the Browse button and connect it to browse_file().
        self.make_button(
            file_frame,
            "Browse",
            self.browse_file,
            ACCENT_COLOR
        ).pack(
            side="right",
            padx=(10, 0)
        )

        # The next widgets collect the user's secret password.
        # Password section

        tk.Label(
            card,
            text="SECRET PASSWORD",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w")

        # Create the password input field; show='*' hides typed characters.
        self.password_entry = tk.Entry(
            card,
            textvariable=self.password,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            show="*",
            relief="flat"
        )

        self.password_entry.pack(
            fill="x",
            pady=(8, 8),
            ipady=10
        )

        # Track whether the password should be visible or hidden.
        self.show_password = tk.BooleanVar(
            value=False
        )

        # Add a checkbox that calls toggle_password() when clicked.
        tk.Checkbutton(
            card,
            text="Show password",
            variable=self.show_password,
            command=self.toggle_password,
            bg=CARD_COLOR,
            fg=MUTED_COLOR,
            activebackground=CARD_COLOR,
            activeforeground=TEXT_COLOR,
            selectcolor=INPUT_COLOR,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        # ==================================
        # ENCRYPT AND DECRYPT BUTTONS
        # ==================================

        # Group the Encrypt and Decrypt buttons in one row.
        button_frame = tk.Frame(
            card,
            bg=CARD_COLOR
        )

        button_frame.pack(
            fill="x",
            pady=5
        )

        self.make_button(
            button_frame,
            "ENCRYPT FILE",
            # Connect the Encrypt button to the encrypt_action() method.
            self.encrypt_action,
            ACCENT_COLOR
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 7),
            ipady=8
        )

        self.make_button(
            button_frame,
            "DECRYPT FILE",
            # Connect the Decrypt button to the decrypt_action() method.
            self.decrypt_action,
            GREEN_COLOR
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(7, 0),
            ipady=8
        )

        # ==================================
        # OPERATION STATUS
        # ==================================

        status_frame = tk.Frame(
            self.root,
            bg=CARD_COLOR,
            padx=20,
            pady=12
        )

        status_frame.pack(
            fill="x",
            padx=35,
            pady=12
        )

        tk.Label(
            status_frame,
            text="OPERATION STATUS",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_COLOR,
            fg=MUTED_COLOR
        ).pack(anchor="w")

        # Link the visible status label to the status variable.
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status,
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            wraplength=720,
            justify="left"
        )

        self.status_label.pack(
            anchor="w",
            pady=(6, 0)
        )

        # ==================================
        # OPERATION HISTORY
        # ==================================

        tk.Label(
            self.root,
            text="OPERATION HISTORY",
            font=("Segoe UI", 12, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=35,
            pady=(5, 10)
        )

        history_frame = tk.Frame(
            self.root,
            bg=CARD_COLOR
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 8)
        )

        # Define the internal column names used by the history table.
        columns = (
            "time",
            "action",
            "file",
            "result"
        )

        # Create the table that displays previous operations.
        self.history_table = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=7
        )

        self.history_table.heading(
            "time",
            text="Date / Time"
        )

        self.history_table.heading(
            "action",
            text="Action"
        )

        self.history_table.heading(
            "file",
            text="File Name"
        )

        self.history_table.heading(
            "result",
            text="Result"
        )

        self.history_table.column(
            "time",
            width=155
        )

        self.history_table.column(
            "action",
            width=100
        )

        self.history_table.column(
            "file",
            width=250
        )

        self.history_table.column(
            "result",
            width=100
        )

        # Customize the colors, row height, and fonts of the history table.
        # Table style

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=INPUT_COLOR,
            foreground=TEXT_COLOR,
            fieldbackground=INPUT_COLOR,
            rowheight=30,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background=CARD_COLOR,
            foreground=TEXT_COLOR,
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", ACCENT_COLOR)
            ]
        )

        # Add a vertical scrollbar for the history table.
        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_table.yview
        )

        self.history_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.history_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==================================
        # FOOTER
        # ==================================

        tk.Label(
            self.root,
            text="AES-256-GCM | Secure File Protection",
            font=("Segoe UI", 9),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        ).pack(pady=(5, 12))

    # ======================================
    # BUTTON HELPER
    # ======================================

    # Reusable helper method that creates consistently styled buttons.
    def make_button(
        self,
        parent,
        text,
        command,
        color
    ):

        # Return a Tkinter button with the requested text, action, and color.
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9
        )

    # ======================================
    # BROWSE FILE
    # ======================================

    # Open a file picker so the user can select an input file.
    def browse_file(self):

        # Show the Windows file selection dialog.
        path = filedialog.askopenfilename(
            title="Select a file"
        )

        # Continue only if the user selected a file instead of cancelling.
        if path:

            # Store the selected file path in the interface.
            self.selected_file.set(path)

            # Display the decryption error in the status area.
            self.status.set(
                "File selected successfully."
            )

            # Change the status text color to green.
            self.status_label.config(
                fg=TEXT_COLOR
            )

    # ======================================
    # SHOW / HIDE PASSWORD
    # ======================================

    # Show or hide the password based on the checkbox state.
    def toggle_password(self):

        # Check whether the user selected the Show password checkbox.
        if self.show_password.get():

            self.password_entry.config(
                # An empty show value displays the password characters normally.
                show=""
            )

        else:

            self.password_entry.config(
                # An asterisk masks the password characters.
                show="*"
            )

    # ======================================
    # SAVE OPERATION HISTORY
    # ======================================

    # Save one operation to the CSV file and add it to the visible table.
    def save_history(
        self,
        action,
        filename,
        result
    ):

        # Create a readable timestamp for this operation.
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Check whether the history CSV file already exists.
        file_exists = HISTORY_FILE.exists()

        # Open the history file in append mode so earlier records are preserved.
        with open(
            HISTORY_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            # Create a CSV writer to write rows safely.
            writer = csv.writer(file)

            # Add column headings only when creating the history file for the first time.
            if not file_exists:

                # Write the operation details as one CSV row.
                writer.writerow([
                    "Date / Time",
                    "Action",
                    "File Name",
                    "Result"
                ])

            # Store the timestamp, operation type, filename, and success/failure result.
            writer.writerow([
                timestamp,
                action,
                filename,
                result
            ])

        # Also show the new operation immediately in the GUI table.
        self.history_table.insert(
            "",
            "end",
            values=(
                timestamp,
                action,
                filename,
                result
            )
        )

    # ======================================
    # LOAD PREVIOUS HISTORY
    # ======================================

    # Read saved history records when the application starts.
    def load_history(self):

        # If no history file exists yet, there is nothing to load.
        if not HISTORY_FILE.exists():
            return

        try:

            with open(
                HISTORY_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                # Read the CSV file row by row.
                reader = csv.reader(file)

                # Skip the first row because it contains column headings.
                next(reader, None)

                # Process each saved operation record.
                for row in reader:

                    # Load only rows that contain all four expected fields.
                    if len(row) == 4:

                        self.history_table.insert(
                            "",
                            "end",
                            values=row
                        )

        # Handle file access problems without crashing the whole application.
        except OSError:

            self.status.set(
                "Warning: Could not load operation history."
            )

    # ======================================
    # ENCRYPT FILE
    # ======================================

    # Handle the full encryption workflow after the user clicks Encrypt File.
    def encrypt_action(self):

        # Get the selected input file path from the interface.
        input_path = self.selected_file.get()

        # Read the password entered by the user.
        password = self.password.get()

        # Stop if the user has not selected a file.
        if not input_path:

            messagebox.showwarning(
                "Missing File",
                "Please select a file first."
            )

            return

        # Stop if the password field is empty.
        if not password:

            messagebox.showwarning(
                "Missing Password",
                "Please enter your secret password."
            )

            return

        # Convert the selected path string into a Path object.
        source = Path(input_path)

        # Suggest an output filename ending in .enc.
        default_name = source.name + ".enc"

        # Ask where the recovered file should be saved.
        output_path = filedialog.asksaveasfilename(
            title="Save Encrypted File",
            initialdir=str(ENCRYPTED_DIR),
            initialfile=default_name,
            defaultextension=".enc",
            filetypes=[
                ("Encrypted Files", "*.enc"),
                ("All Files", "*.*")
            ]
        )

        # Stop if the user cancels the Save dialog.
        if not output_path:
            return

        try:

            # Call encrypt_file() from encryption.py to perform AES-GCM encryption.
            encrypt_file(
                source,
                output_path,
                # Do nothing if saving the failure record also fails.
                password
            )

            self.status.set(
                "SUCCESS: File encrypted successfully!"
            )

            self.status_label.config(
                fg=GREEN_COLOR
            )

            # Record the successful decryption in the history.
            self.save_history(
                "Encryption",
                source.name,
                "Success"
            )

            # Confirm recovery and show the location of the decrypted file.
            messagebox.showinfo(
                "Encryption Successful",
                "Your file has been encrypted successfully!\n\n"
                f"Saved to:\n{output_path}"
            )

        # Catch encryption errors and show them to the user.
        except Exception as error:

            self.status.set(
                f"Encryption failed: {error}"
            )

            self.status_label.config(
                fg=RED_COLOR
            )

            try:

                # Try to record the failed encryption operation.
                self.save_history(
                    "Encryption",
                    source.name,
                    "Failed"
                )

            # Ignore a history-writing error so it does not hide the original error.
            except OSError:
                pass

            # Show a popup explaining why decryption failed.
            messagebox.showerror(
                "Encryption Error",
                str(error)
            )

    # ======================================
    # DECRYPT FILE
    # ======================================

    # Handle the full decryption workflow after the user clicks Decrypt File.
    def decrypt_action(self):

        input_path = self.selected_file.get()

        password = self.password.get()

        if not input_path:

            messagebox.showwarning(
                "Missing File",
                "Please select an encrypted file first."
            )

            return

        if not password:

            messagebox.showwarning(
                "Missing Password",
                "Please enter your secret password."
            )

            return

        source = Path(input_path)

        # Accept only files with the .enc extension for decryption.
        if source.suffix.lower() != ".enc":

            messagebox.showwarning(
                "Invalid File",
                "Please select a file with .enc extension."
            )

            return

        # Suggest an output filename without the .enc extension.
        default_name = source.stem or "recovered_file"

        output_path = filedialog.asksaveasfilename(
            title="Save Decrypted File",
            initialdir=str(DECRYPTED_DIR),
            initialfile=default_name,
            filetypes=[
                ("All Files", "*.*")
            ]
        )

        if not output_path:
            return

        try:

            # Call decrypt_file() from encryption.py to authenticate and decrypt the file.
            decrypt_file(
                source,
                output_path,
                password
            )

            self.status.set(
                "SUCCESS: File decrypted successfully!"
            )

            self.status_label.config(
                fg=GREEN_COLOR
            )

            self.save_history(
                "Decryption",
                source.name,
                "Success"
            )

            messagebox.showinfo(
                "Decryption Successful",
                "Your file has been recovered successfully!\n\n"
                f"Saved to:\n{output_path}"
            )

        except Exception as error:

            self.status.set(
                f"Decryption failed: {error}"
            )

            self.status_label.config(
                fg=RED_COLOR
            )

            try:

                self.save_history(
                    "Decryption",
                    source.name,
                    "Failed"
                )

            except OSError:
                pass

            messagebox.showerror(
                "Decryption Error",
                str(error)
            )


# ==========================================
# RUN APPLICATION
# ==========================================

# Run this block only when main.py is started directly, not when imported by another file.
if __name__ == "__main__":

    # Create the main Tkinter window.
    root = tk.Tk()

    # Create the application and build its interface.
    app = AESApplication(root)

    # Start Tkinter's event loop so the window stays open and responds to user actions.
    root.mainloop()
