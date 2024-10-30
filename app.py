from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the RandomForest model
with open('RF_model.pkl', 'rb') as rf_file:
    randomForestModel = pickle.load(rf_file)

with open('model2.pkl', 'rb') as xgb_file:
    XGBoostModel = pickle.load(xgb_file)

with open('areaPrediction.pkl', 'rb') as xgb_root_file:
    XGBoostArea = pickle.load(xgb_root_file)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Extracting form data
            area = float(request.form['area'])
            temperature = float(request.form['temperature'])
            wind_speed = float(request.form['wind_speed'])
            pressure = float(request.form['pressure'])
            humidity = float(request.form['humidity'])
            N = float(request.form['n'])
            P = float(request.form['p'])
            K = float(request.form['k'])
            soil_type = request.form['soil_type']

            # Form features array for prediction
            features = np.array([[area, temperature, wind_speed, pressure, humidity, N, P, K]], dtype=float)

            # Make the prediction
            predicted_yield = (randomForestModel.predict(features)[0] + XGBoostModel.predict(features)[0])/2
            
            input_data = pd.DataFrame({
                'N': [N],
                'P': [P],
                'K': [K],
                'Temperature': [temperature]
            })

            X_train_columns = ['N', 'P', 'K', 'Temperature' , 'Soil_Type_Loamy','Soil_Type_Sandy', 'Soil_Type_Silty']

            soil_types = ['Soil_Type_Loamy', 'Soil_Type_Sandy', 'Soil_Type_Silty']

    
            for soil in soil_types:
                input_data[soil] = 0

            input_data[f'Soil_Type_{soil_type}'] = 1

            missing_cols = set(X_train_columns) - set(input_data.columns)
            for col in missing_cols:
                input_data[col] = 0
            input_data = input_data[X_train_columns]

            
            predicted_root_length = XGBoostArea.predict(input_data)[0]
            print(predicted_root_length)
            
            area = 3.14 * predicted_root_length * predicted_root_length



            # Return the prediction as JSON
            return jsonify({
                'output': round(predicted_yield, 2),
                'predicted_area': round(area,2)
            })

        except ValueError as ve:
            return jsonify({'error': f"Error converting input to numeric types: {ve}"})
        except Exception as e:
            return jsonify({'error': f"An error occurred: {e}"})


if __name__ == "__main__":
    app.run(debug=True)
