from flask import Blueprint, request, jsonify, render_template, url_for, redirect

from inscharge_model.predict import make_prediction
from inscharge_model import __version__ as _version

from api.validation import validate_inputs
from api import __version__ as api_version

import pandas as pd
import numpy as np

from api.config import get_logger
_logger = get_logger(logger_name=__name__)

prediction_app = Blueprint('prediction_app', __name__)

cols = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

@prediction_app.route('/')
def home():
    return render_template("home.html")

@prediction_app.route('/inputformpredict',methods=['POST'])
def inputformpredict():
    input_features = [x for x in request.form.values()]
    final = np.array(input_features)
    data_unseen = pd.DataFrame([final], columns = cols)

    input_data = data_unseen.to_json(orient='records')
    _logger.info(f'Inputs: {input_data}')
    validated_data, errors = validate_inputs(input_data=input_data)
    result = make_prediction(input_data=validated_data)
    prediction = (result.get('predictions')['Label']).values[0]

    #prediction = predict_model(model, data=data_unseen, round = 0)
    #prediction = int(prediction.Label[0])
    return render_template('home.html',pred='Expected Bill will be {}'.format(prediction))

@prediction_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        _logger.info('health status OK')
        return 'Insurance Charge Prediction - Health Endpoint is OK'

@prediction_app.route('/version', methods=['GET'])
def version():
    if request.method == 'GET':
        return jsonify({'model_version': _version,
                        'api_version': api_version})

@prediction_app.route('/v1/predict/inscharge', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        if (type(json_data) != str):
            json_data = pd.DataFrame(json_data)
            input_data = json_data.to_json(orient='records')
        else:
            input_data = json_data

        _logger.info(f'Inputs in POST controller: {input_data}')
        _logger.info(f'Type of input: {type(input_data)}')

        # Step 2: Validate the input using marshmallow schema
        validated_data, errors = validate_inputs(input_data=input_data)
        _logger.info(f'Inputs: {input_data}')
        _logger.info(f'Inputs: {errors}')

        # Step 3: Model prediction
        result = make_prediction(input_data=validated_data)

        # Step 4: Get the prediction and model version
        predictions = (result.get('predictions')['Label']).values[0]
        version = result.get('version')

        _logger.info(f'predictions: {predictions}')
        
        # Step 5: Return the response as JSON
        
        return jsonify({'predictions': predictions,
                        'version': version,
                        'errors': errors})

