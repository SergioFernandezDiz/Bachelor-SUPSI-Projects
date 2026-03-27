def check_type_values(data, type_fields, expected_type=str):
    for field in type_fields:
        if field in data and not isinstance(data[field], expected_type):
            expected_type_name = (
                ', '.join([t.__name__ for t in expected_type]) if isinstance(expected_type, tuple)
                else expected_type.__name__
            )
            return {'error': 'Invalid data type',
                    'message': f'{field} must be a {expected_type_name}'}, 400

    return None
def check_key_values(data, key_fields):
    if not data or not all(k in data for k in key_fields):
        return {'error': 'Missing required fields',
                'message': f'The request body is empty or missing required fields {key_fields} '
                }, 400