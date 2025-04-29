import tkinter as tk
import ttkbootstrap as ttk
import pyperclip
from ttkbootstrap.constants import *

# Custom color palette
PRIMARY = "#6C5CE7"
SECONDARY = "#00CEFF"
DARK = "#2D3436"
LIGHT = "#F5F6FA"

def generate_shift_sequence(key, text_length):
    """Generate a sequence of shifts based on the key for the length of the text."""
    shifts = []
    key = key.lower()
    key_index = 0

    for _ in range(text_length):
        if key_index >= len(key):
            key_index = 0
        shift = ord(key[key_index]) - 97
        shifts.append(shift)
        key_index += 1

    return shifts

def encode(text, key):
    """Encrypt text using the provided key."""
    encoded_text = ""
    shifts = generate_shift_sequence(key, len(text))

    for i, char in enumerate(text):
        shift = shifts[i]

        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encoded_text += chr((ord(char) + shift - shift_base) % 26 + shift_base)
        elif char.isdigit():
            encoded_text += chr((ord(char) + shift - 48) % 10 + 48)
        else:
            encoded_text += char

    return encoded_text

def decode(text, key):
    """Decrypt text using the provided key."""
    decoded_text = ""
    shifts = generate_shift_sequence(key, len(text))

    for i, char in enumerate(text):
        shift = shifts[i]

        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            decoded_text += chr((ord(char) - shift - shift_base) % 26 + shift_base)
        elif char.isdigit():
            decoded_text += chr((ord(char) - shift - 48) % 10 + 48)
        else:
            decoded_text += char

    return decoded_text

class NovaEncryptApp:
    def __init__(self, master):
        self.master = master
        self.setup_ui()
        
    def setup_ui(self):
        """Configure the user interface."""
        self.master.style.theme_use('superhero')  # Modern dark theme
        
        # Header frame
        header_frame = ttk.Frame(self.master, padding=10)
        header_frame.pack(fill=X)
        
        ttk.Label(
            header_frame, 
            text="Nova Encrypt", 
            font=('Helvetica', 24, 'bold'), 
            foreground=SECONDARY
        ).pack(side=LEFT)
        
        ttk.Label(
            header_frame, 
            text="Secure Text Transformation", 
            font=('Helvetica', 10), 
            foreground=LIGHT
        ).pack(side=LEFT, padx=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.master, text=" Enter Text ", padding=20)
        input_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.input_entry = ttk.Entry(
            input_frame, 
            font=('Helvetica', 12), 
            bootstyle=PRIMARY
        )
        self.input_entry.pack(fill=X, pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=X)
        
        ttk.Button(
            button_frame, 
            text="ENCRYPT", 
            command=self.encrypt, 
            bootstyle=(SUCCESS, OUTLINE),
            width=10
        ).pack(side=LEFT, expand=YES, padx=5)
        
        ttk.Button(
            button_frame, 
            text="DECRYPT", 
            command=self.decrypt, 
            bootstyle=(DANGER, OUTLINE),
            width=10
        ).pack(side=RIGHT, expand=YES, padx=5)
        
        # Output frame
        output_frame = ttk.LabelFrame(self.master, text=" Result ", padding=20)
        output_frame.pack(fill=BOTH, expand=YES, padx=10, pady=(0, 10))
        
        self.output_entry = ttk.Entry(
            output_frame, 
            font=('Helvetica', 12), 
            bootstyle=(SECONDARY),
            state="readonly"
        )
        self.output_entry.pack(fill=X)
        
        def h(e):
            pyperclip.copy(self.output_entry.get())
            self.show_status("Copied to clipboard", SUCCESS)
        
        self.output_entry.bind("<Button-1>", h)
        
        # Status bar
        self.status = ttk.Label(
            self.master, 
            text="Ready", 
            relief=SOLID, 
            anchor=W,
            font=('Helvetica', 8)
        )
        self.status.pack(fill=X, side=BOTTOM, ipady=2)
    
    def encrypt(self):
        """Handle encryption process."""
        text = self.input_entry.get()
        if not text:
            self.show_status("Please enter text to encrypt", WARNING)
            return
            
        key = "complex"
        try:
            encrypted_text = encode(text, key)
            self.show_output(encrypted_text)
            self.show_status("Text encrypted successfully", SUCCESS)
        except Exception as e:
            self.show_status(f"Error: {str(e)}", DANGER)
    
    def decrypt(self):
        """Handle decryption process."""
        text = self.input_entry.get()
        if not text:
            self.show_status("Please enter text to decrypt", WARNING)
            return
            
        key = "complex"
        try:
            decrypted_text = decode(text, key)
            self.show_output(decrypted_text)
            self.show_status("Text decrypted successfully", SUCCESS)
        except Exception as e:
            self.show_status(f"Error: {str(e)}", DANGER)
    
    def show_output(self, text):
        """Display text in the output field."""
        self.output_entry.configure(state="normal")
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, text)
        self.output_entry.configure(state="readonly")
    
    def show_status(self, message, style):
        """Update status bar with message."""
        self.status.config(text=message, bootstyle=style)

if __name__ == "__main__":
    app = ttk.Window(
        title="Nova Encrypt/Decrypt", 
        themename="superhero", 
        size=(500, 400),
        resizable=(False, False))
    NovaEncryptApp(app)
    app.mainloop()