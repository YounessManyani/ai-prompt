import pickle
from flask import Flask, request, render_template
import pandas as pd

# Initialiser l'application Flask
app = Flask(__name__)

# Charger le modèle sauvegardé
with open("pipeline.pkl", "rb") as file:
    model = pickle.load(file)

# Route principale pour afficher le formulaire
@app.route("/")
def form():
    return render_template("form.html")

# Route pour traiter les données et afficher le résultat
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Récupérer les données du formulaire
        data = request.form.to_dict()

        # Convertir les données en types appropriés
        for key in data:
            if key not in ["type", "region"]:
                data[key] = float(data[key])

        # Créer un DataFrame à partir des données
        input_data = pd.DataFrame([data])

        # Effectuer la prédiction
        prediction = model.predict(input_data)[0]

        # Afficher le résultat dans une page HTML
        return render_template("result.html", prediction=round(prediction, 2), data=data)

    except Exception as e:
        return f"Erreur : {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
