from flask import Flask, request
import pandas as pd
import numpy as np
import pickle
from loguru import logger
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)


MODEL_PATH = "/Users/shaunaksen/Documents/personal-projects/ML_Deployment/Docker for Data Scientists/docker-end-to-end/data/classifier.pkl"

def load_model():
    model = pickle.load(open(MODEL_PATH, "rb"))
    return model

@app.route("/")
def welcome() -> str:
    return "Welcome"

@app.route("/predict")
def predict_note_authentication():
    """Let's Authenticate the Banks Note 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: variance
        in: query
        type: number
        required: true
      - name: skewness
        in: query
        type: number
        required: true
      - name: curtosis
        in: query
        type: number
        required: true
      - name: entropy
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
        
    """
    # model = load_model()
    variance = request.args.get("variance")
    skewness = request.args.get("skewness")
    curtosis = request.args.get("curtosis")
    entropy = request.args.get("entropy")

    # prediction = model.predict([[variance, skewness, curtosis, entropy]])

    prediction = np.random.choice([0, 1])

    return f"Prediction: {prediction}"

@app.route("/predict_file", methods=["POST"])
def predict_note_authentication_from_file():
    """Let's Authenticate the Banks Note 
    This is using docstrings for specifications.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
        
    """
    file = request.files.get("file")
    logger.info(file)
    logger.info(type(file))
    df_test = pd.read_csv(file)

    df_test['prediction'] = np.random.choice([0, 1], size=len(df_test))

    return f"Predictions: {df_test['prediction'].tolist()}"


if __name__ == "__main__":
    app.run()


