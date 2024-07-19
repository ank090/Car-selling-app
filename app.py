from flask import Flask, request, jsonify
import pandas as pd
import joblib
import pickle
from helpers import Prediction
import io
from models import Models
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Car Becho."

@app.route('/bulk_price_preditor', methods=['POST'])
def bulk_predictor():
    """
    Takes csv file as an input with all the details and predict the price of the car based on the parameters.
    
    """
    prediction = Prediction()
    file = request.files['file']
    data = pd.read_csv(file)
    try:
        predicted_price = prediction.make_bulk_prediction(data)
    except KeyError as e:
        print('e:',e)
        return jsonify({'error':str(e)}),400
    data = pd.concat([data, predicted_price], axis=1)
    response = jsonify(data.to_dict(orient='records'))
    headers = {
    "Content-Disposition": "attachment; filename=output.csv",
    "Content-Type": "text/csv",
    }
    return response, 200

@app.route('/price_predictor', methods=['POST'])
def predictor():
    """
    Takes all the required parameters as a part of request parameter for a single car and predict the price.
    """
    prediction = Prediction()
    data = {key: [request.form.get(key)] for key in request.form}
    print(data)
    data = pd.DataFrame(data)
    try:
        predicted_price = prediction.make_prediction(data)
    except KeyError as e:
        return jsonify({'error': str(e)})
    data = pd.concat([data, predicted_price], axis=1)
    response = jsonify(data.to_dict(orient='records'))
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)