import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
# CORS permet à votre site sur OVH de communiquer en toute sécurité avec cette API
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialisation du client OpenAI avec la clé API cachée dans l'environnement
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Le message ne peut pas être vide"}), 400

        # Envoi de la requête à OpenAI (Modèle GPT-4o mini, idéal pour les chatbots rapides et économiques)
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es l'assistant virtuel expert d'Exalio. Tu réponds de manière professionnelle, claire et engageante."},
                {"role": "user", "content": user_message}
            ]
        )

        ai_reply = response.choices[0].message.content
        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Le port 10000 est la configuration standard exigée par Render
    app.run(host='0.0.0.0', port=10000)
