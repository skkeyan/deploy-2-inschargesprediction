import pathlib

from pycaret.regression import *
from inscharge_model.config import config
from inscharge_model.processing.data_management import load_dataset, remove_old_pipelines
from inscharge_model import __version__ as _version

import logging

_logger = logging.getLogger(__name__)

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'trained_models'
DATASET_DIR = PACKAGE_ROOT / 'datasets'

# data
TESTING_DATA_FILE = "inscharges-test.csv"
TRAINING_DATA_FILE = "inscharges-train.csv"
TARGET = "charges"

def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.TRAINING_DATA_FILE)

    # Feature engineering
    r2 = setup(data, target = 'charges', session_id = 123,
               normalize = True,
               polynomial_features = True, trigonometry_features = True,
               feature_interaction=True, 
               bin_numeric_features= ['age', 'bmi'],silent=True)

    # Model Training and Validation 
    lr = create_model('lr', verbose=False)

    # Prepare versioned save file name
    save_file_name = f"{config.PIPELINE_SAVE_FILE}{_version}"
    save_path = config.TRAINED_MODEL_DIR / save_file_name

    # Remove old pipelines
    keep_file_name = f"{config.PIPELINE_SAVE_FILE}{_version}.pkl"
    remove_old_pipelines(files_to_keep=keep_file_name)

    # save transformation pipeline and model 
    save_model(lr, model_name=str(save_path))
    
if __name__ == '__main__':
    run_training()
