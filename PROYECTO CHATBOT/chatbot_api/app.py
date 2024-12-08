from flask import Flask, request, jsonify
import pickle
import numpy as np
import spacy
import random  # Importar random
import json
from nltk.corpus import stopwords
from sklearn.preprocessing import StandardScaler
from nltk.stem import PorterStemmer
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords

# Cargar el modelo y otros objetos necesarios
app = Flask(__name__)
CORS(app)

# Cargar el modelo de chatbot
with open("./chatbot_api/chatbot_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Cargar el vocabulario de palabras, clases y el escalador
    words = pickle.load(open('./chatbot_api/words.pkl', 'rb'))
    classes = pickle.load(open('./chatbot_api/classes.pkl', 'rb'))
    scaler = pickle.load(open('./chatbot_api/scaler.pkl', 'rb'))

# Cargar los intents (intenciones)
    with open('./chatbot_api/dataset.json', encoding='utf-8') as intents_file:
        intents = json.load(intents_file)

# Cargar el modelo de procesamiento de lenguaje natural (spaCy)
    nlp = spacy.load("es_core_news_sm")

# Inicializar stemmer
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("spanish"))

# Función para predecir la clase de un texto
def predict_class(text):
    bow = np.array([0] * len(words))  # Vector de ceros
    word_list = nlp(text)
    word_list = [token.text for token in word_list if token.text.isalpha()]
    word_list = [nlp(word)[0].lemma_ for word in word_list]  # Lematizar
    word_list = [stemmer.stem(word) for word in word_list]  # Aplicar stemming

    # Crear el vector "bag of words"
    for word in word_list:
        if word in words:
            bow[words.index(word)] = 1

    # Normalizar
    bow = scaler.transform([bow])

    # Hacer la predicción
    prediction = model.best_estimator_.predict(bow)
    predicted_class = classes[np.argmax(prediction)]
    return predicted_class
    
    # Buscar la respuesta correspondiente a la clase
def get_response(predicted_class):
    for intent in intents['intents']:
        if intent['tag'] == predicted_class:
            response = random.choice(intent['responses'])  # Seleccionar una respuesta aleatoria
            return response
    return "Lo siento, no entiendo esa pregunta."

# Endpoint para predecir el mensaje
@app.route('/predict', methods=['POST'])
def predict():
    # Obtener el texto enviado en la solicitud
    # Obtener el texto enviado en la solicitud
    data = request.get_json()
    text = data.get('pattern', '')
    
    # Predecir la clase del texto
    predicted_class = predict_class(text)
    
    # Obtener la respuesta basada en la clase predicha
    response = get_response(predicted_class)
    
    # Retornar la respuesta como un JSON
    return jsonify({'response': response})



if __name__ == "__main__":
    app.run(debug=True)
