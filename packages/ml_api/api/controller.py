from flask import Blueprint, request, jsonify

from inscharge_model.predict import make_prediction
from inscharge_model import __version__ as _version

from api.validation import validate_inputs
from api import __version__ as api_version

import pandas as pd

from api.config import get_logger
_logger = get_logger(logger_name=__name__)

prediction_app = Blueprint('prediction_app', __name__)

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

