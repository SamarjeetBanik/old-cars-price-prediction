from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
cors = CORS(app)
model = pickle.load(open("Price_Prediction.pkl", "rb"))
df = pd.read_csv("Filtered_Data.csv")

@app.route("/", methods = ["GET", "POST"])
def index():
    car_models = sorted(df["name"].unique())
    companies = sorted(df["company"].unique())
    purchase_year = sorted(df["year"].unique(), reverse = True)
    fuel_types = sorted(df["fuel_type"].unique())

    companies.insert(0, "Select Company")
    purchase_year.insert(0, "Select Year")
    fuel_types.insert(0, "Select Fuel Type")
    
    return render_template("index.html", companies = companies, car_models = car_models, purchase_year = purchase_year, fuel_types = fuel_types)

@app.route("/predict", methods = ["POST"])
@cross_origin(supports_credentials = True)
def predict():
    company = request.form.get('company')
    car_model = request.form.get('car_model')
    purchase_year = request.form.get('purchase_year')
    fuel_type = request.form.get('fuel_type')
    kms_driven = request.form.get('kms_driven')

    prediction = model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'], data = np.array([car_model, company, purchase_year, kms_driven, fuel_type]).reshape(1, 5)))
    print(prediction)

    return str(np.round(prediction[0], 2))

if __name__ == "__main__":
    app.run(debug = True)