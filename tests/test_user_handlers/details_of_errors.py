"""Content of error's detail for testing 'user handlers'."""

detail_for_empty_fields = {'detail': [
    {'type': 'missing', 'loc': ['body', 'name'], 'msg': 'Field required',
     'input': {}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'surname'],
     'msg': 'Field required', 'input': {},
     'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required',
     'input': {}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'password'], 'msg': 'Field required',
     'input': {}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'}]}

detail_for_empty_fields_update = {'detail': [
    {'type': 'missing', 'loc': ['body', 'name'], 'msg': 'Field required',
     'input': {}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'surname'], 'msg': 'Field required',
     'input': {}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required',
     'input': {}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'}]}

detail_for_wrong_email = {'detail': [
    {'type': 'value_error', 'loc': ['body', 'email'],
     'msg': 'value is not a valid email address:'
            ' The email address is not valid. It must have exactly one @-sign.',
     'input': 'John', 'ctx': {'reason': 'The email address is not valid. '
                                        'It must have exactly one @-sign.'}}
]
}

detail_incorrect_user_id = {'detail': [
    {'type': 'is_instance_of', 'loc': ['query', 'user_id', 'is-instance[UUID]'],
     'msg': 'Input should be an instance of UUID', 'input': 'not_valid_user_id',
     'ctx': {'class': 'UUID'}, 'url': 'https://errors.pydantic.dev/2.1.2/v/is_instance_of'},
    {'type': 'uuid_parsing', 'loc':
        ['query', 'user_id', 'function-after[uuid_validator(), union[str,bytes]]'],
     'msg': 'Input should be a valid UUID, unable to parse string as an UUID',
     'input': 'not_valid_user_id'}]}

detail_for_wrong_email_from_update = {'detail': [
    {'type': 'missing', 'loc': ['body', 'name'],
     'msg': 'Field required', 'input': {'email': 'John'},
     'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'surname'], 'msg': 'Field required',
     'input': {'email': 'John'}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'value_error', 'loc': ['body', 'email'],
     'msg': 'value is not a valid email address: The email address is not valid. '
            'It must have exactly one @-sign.', 'input': 'John',
     'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}}]}

detail_for_blank_email_update = {'detail': [
    {'type': 'missing', 'loc': ['body', 'name'],
     'msg': 'Field required', 'input': {'email': ''},
     'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'surname'],
     'msg': 'Field required', 'input': {'email': ''},
     'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'value_error', 'loc': ['body', 'email'],
     'msg': 'value is not a valid email address: The email address is not valid. '
            'It must have exactly one @-sign.', 'input': '',
     'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}}]}


detail_string_too_short = {'detail': [
    {'type': 'string_too_short', 'loc': ['body', 'name'],
     'msg': 'String should have at least 1 characters', 'input': '',
     'ctx': {'min_length': 1}, 'url': 'https://errors.pydantic.dev/2.1.2/v/string_too_short'},
    {'type': 'missing', 'loc': ['body', 'surname'], 'msg': 'Field required',
     'input': {'name': ''}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'},
    {'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required',
     'input': {'name': ''}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'}]}

detail_update_invalid_user_id = {'detail': [
    {'type': 'is_instance_of', 'loc': ['query', 'user_id', 'is-instance[UUID]'],
     'msg': 'Input should be an instance of UUID', 'input': '123',
     'ctx': {'class': 'UUID'}, 'url': 'https://errors.pydantic.dev/2.1.2/v/is_instance_of'},
    {'type': 'uuid_parsing', 'loc': ['query', 'user_id',
                                     'function-after[uuid_validator(), union[str,bytes]]'],
     'msg': 'Input should be a valid UUID, unable to parse string as an UUID', 'input': '123'}]}

