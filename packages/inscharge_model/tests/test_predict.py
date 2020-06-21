import math

from inscharge_model.predict import make_prediction
from inscharge_model.processing.data_management import load_dataset


def test_make_single_prediction():
    # Given
    test_data = load_dataset(file_name='inscharges-test.csv')
    single_test_json = test_data[0:1].to_json(orient='records')

    # When
    subject = make_prediction(input_data=single_test_json)

    predicted_value = (subject.get('predictions')['Label']).values[0]

    # Then
    assert subject is not None
    assert isinstance(predicted_value, float)
    #assert math.ceil(subject.get('predictions')[0]) == 9536


def test_make_multiple_predictions():
    # Given
    test_data = load_dataset(file_name='inscharges-test.csv')
    original_data_length = len(test_data)
    multiple_test_json = test_data.to_json(orient='records')

    # When
    subject = make_prediction(input_data=multiple_test_json)

    # Then
    assert subject is not None
    assert len(subject.get('predictions')) == 20

    # We expect no rows to be filtered out
    assert len(subject.get('predictions')) == original_data_length
