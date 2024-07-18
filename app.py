from flask import Flask, request, Response
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
    predicted_price = prediction.make_bulk_prediction(data)
    data = pd.concat([data, predicted_price], axis=1)
    result_file = data.to_csv(index=False)
    headers = {
    "Content-Disposition": "attachment; filename=output.csv",
    "Content-Type": "text/csv",
    }
    return Response(
        io.BytesIO(result_file.encode()),
        status=200,
        headers=headers
    )
if __name__ == '__main__':
    print()
    app.run(debug=True)