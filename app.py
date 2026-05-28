import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configuration de Gemini avec la clé d'environnement
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Message manquant'}), 400

    try:
        # Utilisation du modèle Gemini 1.5 Flash (rapide et gratuit)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render utilise la variable d'environnement PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
