import numpy as np
import pandas as pd

from pycaret.regression import *

from inscharge_model.config import config
#from inscharge_model.processing.validation import validate_inputs
from inscharge_model import __version__ as _version

import logging

_logger = logging.getLogger(__name__)

file_name = f"{config.PIPELINE_SAVE_FILE}{_version}"
pipeline_file_name = config.TRAINED_MODEL_DIR / file_name
_inscharge_pipe = load_model(str(pipeline_file_name)) 

def make_prediction(*, input_data) -> dict:
    """Make a prediction using the saved model pipeline."""

    data = pd.read_json(input_data)
    #validated_data = validate_inputs(input_data=data)
    validated_data = data
    prediction = predict_model(_inscharge_pipe, validated_data[config.FEATURES])

    output = prediction

    results = {"predictions": output, "version": _version}

    _logger.info(
        f"Making predictions with model version: {_version} "
        f"Inputs: {validated_data} "
        f"Predictions: {results}"
    )

    return results
