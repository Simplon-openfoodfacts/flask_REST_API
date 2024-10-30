import tkinter as tk
from tkinter import messagebox
import json
import numpy as np
import re

# Valeurs nutritionnelles maximales
nutritional_values_max = {
    'energy-kcal': [600, "kcal/100g"],
    'fat': [20, "g/100g"],
    'saturated-fat': [10, "g/100g"],
    'cholesterol': [300, "mg/100g"],
    'carbohydrates': [50, "g/100g"],
    'sugars': [22.5, "g/100g"],
    'proteins': [20, "g/100g"],
    'salt': [3, "g/100g"],
    'sodium': [1200, "mg/100g"],
    'vitamin-c': [80, "mg/100g"],
    'potassium': [2000, "mg/100g"],
    'calcium': [1200, "mg/100g"],
    'iron': [15, "mg/100g"],
    'magnesium': [350, "mg/100g"],
    'zinc': [10, "mg/100g"],
    'fibre':[35,'mg/100g']
}

class NutritionalInputApp:
    def __init__(self, master):
        self.master = master
        master.title("Input Nutritional Values")
        master.geometry("600x800")
        
        # Configuration de la grille pour centrer les éléments
        self.master.grid_columnconfigure(0, weight=1)
        
        # Champ de saisie du nom du produit
        self.product_label = tk.Label(master, text="Nom du produit :", font=("Arial", 12))
        self.product_label.grid(row=0, column=0, pady=(20, 5), sticky="n")

        self.product_entry = tk.Entry(master, width=30, font=("Arial", 12), justify="center")
        self.product_entry.grid(row=1, column=0, pady=(0, 20))
        self.product_entry.bind("<KeyRelease>", self.validate_name)

        # Cadre principal pour les entrées
        entry_frame = tk.Frame(master)
        entry_frame.grid(row=2, column=0, pady=5)
        
        # Configuration des colonnes pour le cadre principal
        entry_frame.grid_columnconfigure(0, weight=1)
        entry_frame.grid_columnconfigure(1, weight=1)
        entry_frame.grid_columnconfigure(2, weight=1)
        entry_frame.grid_columnconfigure(3, weight=1)

        # Champs de saisie des valeurs nutritionnelles avec alignement et taille uniforme
        self.entries = {}
        self.icons = {}

        for idx, (nutrient, (max_value, unit)) in enumerate(nutritional_values_max.items()):
            # Label du nutriment
            label = tk.Label(entry_frame, text=f"{nutrient}", font=("Arial", 19), anchor="e")
            label.grid(row=idx, column=0, padx=5, sticky="e")

            # Champ de saisie du nutriment avec largeur fixe
            entry = tk.Entry(entry_frame, width=20, font=("Arial", 17), justify="center")
            entry.grid(row=idx, column=1, padx=5, sticky="w")
            entry.bind("<KeyRelease>", lambda e, nutrient=nutrient: self.validate_entry(nutrient))
            self.entries[nutrient] = entry

            # Icône de validation (vide si non validé)
            icon_label = tk.Label(entry_frame, text="", font=("Arial", 12))
            icon_label.grid(row=idx, column=2, padx=5)
            self.icons[nutrient] = icon_label

            # Unité de mesure à droite de chaque champ de saisie
            unit_label = tk.Label(entry_frame, text=f"[up to {max_value} {unit}]", font=("Arial", 10), anchor="w")
            unit_label.grid(row=idx, column=3, padx=5, sticky="w")

        # Bouton de soumission stylisé (désactivé par défaut)
        self.submit_button = tk.Button(master, text="Valider", command=self.validate_input, font=("Arial", 12),
                                       bg="green", fg="white", width=20, state="disabled")
        self.submit_button.grid(row=3, column=0, pady=30)

    def validate_name(self, event=None):
        product_name = self.product_entry.get()
        # Vérifie que le nom contient uniquement des lettres
        if re.fullmatch(r'[A-Za-z\s]+', product_name):
            self.product_entry.config(fg="green")
            self.name_valid = True
        else:
            self.product_entry.config(fg="red")
            self.name_valid = False
        self.update_submit_button()

    def validate_entry(self, nutrient):
        entry = self.entries[nutrient]
        icon_label = self.icons[nutrient]
        value = entry.get()
        max_value, unit = nutritional_values_max[nutrient]

        # Nettoyer l'icône si la valeur est vide
        if not value:
            icon_label.config(text="")
            return

        try:
            # Validation de la valeur numérique
            value = float(value)
            if 0 <= value <= max_value:
                icon_label.config(text="✔", fg="green")
                self.entry_status = True
            else:
                icon_label.config(text="✘", fg="red")
                self.entry_status = False
        except ValueError:
            icon_label.config(text="✘", fg="red")
            self.entry_status = False
        self.update_submit_button()

    def update_submit_button(self):
        # Active le bouton si le nom est valide et les autres champs sont vides ou valides
        if self.name_valid:
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")

    def validate_input(self):
        product_name = self.product_entry.get().strip()
        if not product_name:
            messagebox.showerror("Erreur de saisie", "Le nom du produit ne peut pas être vide.")
            return

        nutritional_values = {"product_name": product_name}

        for nutrient, entry in self.entries.items():
            value = entry.get()
            max_value, _ = nutritional_values_max[nutrient]

            # Enregistre NaN si le champ est vide
            if not value:
                nutritional_values[nutrient] = np.nan
                continue

            try:
                value = float(value)
                if 0 <= value <= max_value:
                    nutritional_values[nutrient] = value
                else:
                    messagebox.showerror("Erreur de saisie", f"{nutrient} doit être entre 0 et {max_value}.")
                    return
            except ValueError:
                messagebox.showerror("Erreur de saisie", f"Entrée invalide pour {nutrient}. Entrez un nombre.")
                return

        with open("nutritional_values.json", "w") as json_file:
            json.dump(nutritional_values, json_file, indent=4, default=str)

        messagebox.showinfo("Succès", "Toutes les valeurs sont valides et ont été enregistrées.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionalInputApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Programme fermé.")
