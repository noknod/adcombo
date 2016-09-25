# -*- coding: utf-8 -*-
import traceback
import json

from t3routine.permutation import ArrayPermutator


__all__ = (
    'get_type_from_request',
    'parse_array_from_request',
    'add_generator_to_session',
    'read_permutation_by_key',
    'read_permutation',
    'REQUEST_TYPE_COMMON', 
    'REQUEST_TYPE_AJAX',
)


REQUEST_TYPE_COMMON, REQUEST_TYPE_AJAX = range(1, 3)


def get_type_from_request(request):
    request_type = REQUEST_TYPE_AJAX
    try:
        if not request.is_xhr:
            request_type = REQUEST_TYPE_COMMON
    except Exception:
        traceback.print_exc()
    return request_type


def parse_array_from_request(request, request_type):
    received_data = None
    try:
        if request_type == REQUEST_TYPE_COMMON:
                received_data = request.form.get('array', None)
                received_data = list(map(int, received_data.split()))
        elif request_type == REQUEST_TYPE_AJAX:
            received_data = request.json
    except Exception:
        traceback.print_exc()
        return None
    return received_data


def add_generator_to_session(session, array, generators_dct):
    try:
        generator = ArrayPermutator(array)
        generator.start()
        generator_key = repr(generator)
        generators_dct[generator_key] = {
            'generator': generator,
            'last': None
        }
        session['generator'] = generator_key
    except Exception:
        traceback.print_exc()
        return None
    return generator_key


def read_permutation_by_key(generators_dct, generator_key):
    try:
        generator = generators_dct.get(generator_key, None)
        if (generator is None):
            return None
        permutated_array = generator['generator'].next()
        last_permutation = generator['last']
        if (permutated_array is None):
            permutated_array = []
        permutation = _permutated_array_to_str(permutated_array)
        generator['last'] = permutation
    except Exception:
        traceback.print_exc()
        return None
    return (permutation, last_permutation)


def read_permutation(session, generators_dct):
    generator_key = _get_generator_key_from_session(session, generators_dct)
    if (generator_key is None):
        return None
    return read_permutation_by_key(generators_dct, generator_key)


def stop_generator(session, generators_dct):
    generator_key = _get_generator_key_from_session(session, generators_dct)
    try:
        if generator_key in generators_dct:
            generators_dct.pop(generator_key)
        if generator_key in session:
            session.pop('generator')
    except Exception:
        traceback.print_exc()


def _get_generator_key_from_session(session, generators_dct):
    try:
        generator_key = session.get('generator', None)
    except Exception:
        traceback.print_exc()
        return None
    return generator_key


def _permutated_array_to_str(permutated_array):
    return json.dumps(permutated_array)
