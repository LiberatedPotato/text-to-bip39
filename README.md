# BIP-39 Seed Phrase Converter
This is a simple desktop application that converts arbitrary 12/24 word sentences into a BIP-39-compatible seed phrase using SHA-256 hashing. Its main goal is to enable an easier to remember brain wallet by turning familiar text into a valid mnemonic phrase. It features a graphical user interface (GUI) built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

## Features

- Converts any 12/24 word text into  a valid BIP-39 seedphrase
- Supports an optional passphrase for additional security
- Live word count with input validation (12 or 24 words only)
- Clean and user-friendly GUI
- Offline, deterministic, and privacy-focused

## How It Works

1. Each input word is lowercased and optionally combined with a passphrase.
2. The string is hashed using SHA-256.
3. The hash is converted into an 11-bit integer (range: 0–2047).
4. This integer is used to index a BIP-39 dictionary to retrieve the corresponding word.

## Requirements

- Python 3.8 or newer
- pandas
- customtkinter

Install dependencies using the requirements.txt file

