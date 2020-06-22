from marshmallow import Schema, fields
from marshmallow import ValidationError

import typing as t
import json

from api.config import get_logger
_logger = get_logger(logger_name=__name__)

class InvalidInputError(Exception):
    """Invalid model input."""

class InsChargeDataRequestSchema(Schema):
    age = fields.Integer(allow_none=True)
    sex = fields.Str(allow_none=True)
    bmi = fields.Float(allow_none=True)
    children = fields.Integer(allow_none=True)
    smoker = fields.Str(allow_none=True)
    region = fields.Str(allow_none=True)


def _filter_error_rows(errors: dict,
                       validated_input: t.List[dict]
                       ) -> t.List[dict]:
    """Remove input data rows with errors."""

    indexes = errors.keys()
    # delete them in reverse order so that you
    # don't throw off the subsequent indexes.
    for index in sorted(indexes, reverse=True):
        del validated_input[index]

    return validated_input


def validate_inputs(input_data):
    """Check prediction inputs against schema."""

    # set many=True to allow passing in a list
    schema = InsChargeDataRequestSchema(strict=True, many=True)

    errors = None

    _logger.info(f'Inputs: {input_data}')

    try:
        schema.loads(input_data)
    except ValidationError as exc:
        errors = exc.messages

    _logger.info(f'Errors: {errors}')

    if errors:
        validated_input = _filter_error_rows(
            errors=errors,
            validated_input=input_data)
    else:
        validated_input = input_data
    

    return validated_input, errors
