import os
import sys
import json
import math
import subprocess

OUT_DIR = r"C:\Users\sk\Desktop\drip irrigation moringa\irrigation_package"
os.makedirs(OUT_DIR, exist_ok=True)

CADCRAFT = r"C:\Program Files\CADCraft\cadcraft-cli.exe"
VECTORCRAFT = r"C:\Program Files\VectorCraft\vectorcraft-cli.exe"
GRIDCRAFT = r"C:\Program Files\GridCraft\gridcraft-cli.exe"
WORDCRAFT = r"C:\Program Files\WordCraft\wordcraft-cli.exe"
DECKCRAFT = r"C:\Program Files\DeckCraft\deckcraft-cli.exe"
PDFCRAFT = r"C:\Program Files\PdfCraft\pdfcraft-cli.exe"

print("--- Starting Drip Irrigation Engineering Package Generation ---")
