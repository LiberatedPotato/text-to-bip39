import customtkinter as ctk
import pandas as pd
import hashlib
import os

# -------------------- Data --------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DICTIONARY_PATH = os.path.join(SCRIPT_DIR, "dictionary.csv")

_df = pd.read_csv(DICTIONARY_PATH, dtype={"binary": str})
_df["binary"] = _df["binary"].str.strip()
_df["word"] = _df["word"].str.strip()
_binary_to_word = dict(zip(_df["binary"], _df["word"]))

# -------------------- Core logic --------------------

def hash_to_11bit(value: str) -> int:
    """Return an 11-bit integer derived from SHA-256 of *value*."""
    h = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(h, 16) % 2048


def process_seed_input(seed_input: str, password: str = "") -> tuple[list[str], list[str]]:
    """Hash every word in *seed_input* (optionally salted with *password*) to a BIP-39 word."""
    words = [w.lower() for w in seed_input.replace("\n", " ").split() if w.isalpha()]
    original = words.copy()
    converted = [
        _binary_to_word[format(hash_to_11bit(word + password), "011b")] for word in words
    ]
    return original, converted

# -------------------- GUI --------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("BIP-39 Seed Phrase Converter")
app.geometry("800x650")

# ── Additional password (top) ──────────────────────────────────────
password_enabled_var = ctk.BooleanVar(value=False)

password_checkbox = ctk.CTkCheckBox(
    app,
    text="Enable additional password",
    variable=password_enabled_var,
)
password_checkbox.pack(pady=(20, 5))

password_label = ctk.CTkLabel(app, text="Enter optional passphrase:", state="disabled")
password_label.pack(pady=(2, 2))

password_box = ctk.CTkEntry(app, width=250, state="disabled")
password_box.pack()


def toggle_password_widgets():
    state = "normal" if password_enabled_var.get() else "disabled"
    password_label.configure(state=state)
    password_box.configure(state=state)
    if state == "disabled":
        password_box.delete(0, "end")

password_checkbox.configure(command=toggle_password_widgets)

# ── Seed words section ────────────────────────────────────────────
input_label = ctk.CTkLabel(app, text="Enter custom seed words:")
input_label.pack(pady=(20, 5))

input_box = ctk.CTkTextbox(app, width=700, height=100, wrap="word")
input_box.pack()

word_count_var = ctk.StringVar(value="Word Count: 0")
word_count_label = ctk.CTkLabel(app, textvariable=word_count_var)
word_count_label.pack(pady=5)

error_label = ctk.CTkLabel(app, text="", text_color="red")
error_label.pack()

# ── Live word counter for seed phrase ─────────────────────────────

def update_word_count(event=None):
    words = [w for w in input_box.get("1.0", "end").replace("\n", " ").split() if w.isalpha()]
    word_count_var.set(f"Word Count: {len(words)}")

input_box.bind("<KeyRelease>", update_word_count)

# ── Generate button logic ─────────────────────────────────────────

def on_generate():
    seed_text = input_box.get("1.0", "end").strip()
    words = [w for w in seed_text.replace("\n", " ").split() if w.isalpha()]
    count = len(words)
    word_count_var.set(f"Word Count: {count}")

    # Validate seed length
    if count not in (12, 24):
        error_label.configure(text="Seed phrase must contain exactly 12 or 24 words.")
        output_box.delete("1.0", "end")
        return

    # Handle optional password
    pwd = ""
    if password_enabled_var.get():
        pwd = password_box.get().strip()
        if " " in pwd or "\n" in pwd:
            error_label.configure(text="password can't have any spaces")
            output_box.delete("1.0", "end")
            return
    
    error_label.configure(text="")
    original, converted = process_seed_input(seed_text, pwd)

    output_box.delete("1.0", "end")
    output_box.insert(
        "1.0",
        "Original / Custom Seed Phrase:\n" + " ".join(original) +
        "\n\nMapped BIP-39-Compliant Seed Phrase:\n" + " ".join(converted)
    )

ctk.CTkButton(app, text="Generate BIP-39 Seed Phrase", command=on_generate).pack(pady=10)

# ── Output box ────────────────────────────────────────────────────
ctk.CTkLabel(app, text="Output:").pack(pady=(15, 5))

output_box = ctk.CTkTextbox(app, width=700, height=200, wrap="word")
output_box.pack()

# -------------------- Main loop --------------------
app.mainloop()