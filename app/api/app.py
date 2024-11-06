from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import json
import os

app = Flask(__name__)

# Charger le modèle
with open('model_v1.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Valeurs nutritionnelles maximales
nutritional_values_max = {
    'energy-kcal_100g': 600,
    'saturated-fat_100g': 10,
    'carbohydrates_100g': 50,
    'sugars_100g': 22.5,
    'fiber_100g': 35,  
    'proteins_100g': 20,
    'salt_100g': 3
}

# Chemin pour sauvegarder les résultats JSON
RESULTS_FILE = 'results.json'

def save_to_json(data):
    """Enregistre les résultats dans un fichier JSON."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as file:
            results = json.load(file)
    else:
        results = []

    results.append(data)

    with open(RESULTS_FILE, 'w') as file:
        json.dump(results, file, indent=4)

@app.route('/')
def default():
    return render_template('login.html', show_navbar=False)

@app.route('/login')
def login():
    return render_template('login.html', show_navbar=False)

@app.route('/home')
def home():
    return render_template('home.html', show_navbar=True)

@app.route('/search')
def search():
    return render_template('search.html', show_navbar=True)

@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        data = {
            "energy-kcal_100g": float(request.form['energy']),
            "saturated-fat_100g": float(request.form['saturated_fat']),
            "carbohydrates_100g": float(request.form['carbohydrates']),
            "sugars_100g": float(request.form['sugars']),
            "fiber_100g": float(request.form.get('fiber', 0)),
            "proteins_100g": float(request.form.get('proteins', 0)),
            "salt_100g": float(request.form['salt'])
        }

        # Validation des données
        errors = []
        for key, max_value in nutritional_values_max.items():
            if data[key] > max_value:
                errors.append(f"{key.replace('_', ' ').capitalize()} dépasse la limite recommandée.")

        if errors:
            return render_template('product.html', show_navbar=True, prediction=None, errors=errors, nutritional_values_max=nutritional_values_max)
        
        # Prédiction
        input_data = np.array([[data[key] for key in data]])
        prediction = loaded_model.predict(input_data)[0]
        grade_image = f'grade_{prediction}.png'

        # Sauvegarder le résultat en JSON
        save_to_json({
            "input": data,
            "prediction": prediction,
            "grade_image": grade_image
        })

        return render_template('product.html', show_navbar=True, prediction=prediction, grade_image=grade_image, errors=None, nutritional_values_max=nutritional_values_max)

    return render_template('product.html', show_navbar=True, prediction=None, grade_image=None, errors=None, nutritional_values_max=nutritional_values_max)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html', show_navbar=True)

@app.route('/results', methods=['GET'])
def get_results():
    """Affiche tous les résultats sauvegardés en JSON."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as file:
            results = json.load(file)
    else:
        results = []

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
