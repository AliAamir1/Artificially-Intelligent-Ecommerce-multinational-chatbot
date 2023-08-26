from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Load the saved model from the pickle file
with open('lr_model.pkl', 'rb') as f:
    lr = pickle.load(f)

app = Flask(__name__)


@app.route('/predict_average_price', methods=['POST'])
def predict_average_price():
    # Get feature values from the request body
    feature_values = request.json

    # Create a dictionary from the feature values
    input_dict = {
        "Total Volume": feature_values['Total Volume'],
        "4046": feature_values['4046'],
        "4225": feature_values['4225'],
        "4770": feature_values['4770'],
        "Total Bags": feature_values['Total Bags'],
        "Small Bags": feature_values['Small Bags'],
        "Large Bags": feature_values['Large Bags'],
        "XLarge Bags": feature_values['XLarge Bags'],
    }

    # Convert the dictionary into a DataFrame
    input_df = pd.DataFrame([input_dict])

    # Make the prediction using the trained linear regression model
    prediction = lr.predict(input_df)

    # Return the predicted average price in JSON format
    return jsonify({'predicted_average_price': round(prediction[0], 2)})


if __name__ == '__main__':
    app.run(debug=True)
