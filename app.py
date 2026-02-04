from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# load model (Pipeline)
model = pickle.load(open('LinearRegressionModel (1).pkl', 'rb'))
print(type(model))   # <class 'sklearn.pipeline.Pipeline'>

# load data
car = pd.read_csv("cleaned Car (1).csv")



@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel = sorted(car['fuel'].unique())

    return render_template(
        'index.html',
        companies=companies,
        car_models=car_models,
        years=years,
        fuel=fuel
    )


@app.route('/predict', methods=['POST'])
def predict():
    company = request.form.get('company')
    car_model = request.form.get('car_model')
    year = int(request.form.get('year'))
    fuel = request.form.get('fuel')
    km_driven = int(request.form.get('km_driven'))

    # Column name must match training data
    input_df = pd.DataFrame(
        [[car_model, company, year, km_driven, fuel]],
        columns=['name','company','year','km_driven','fuel']
    )

    prediction = model.predict(input_df)
    return str(round(prediction[0],2))


if __name__ == '__main__':
    app.run(debug=True)
