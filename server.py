# -*- coding: utf-8 -*-
from flask import Flask, request, url_for, render_template, redirect, \
    session, jsonify, flash, get_flashed_messages

from t3routine.handlers import get_type_from_request, stop_generator, \
    parse_array_from_request, add_generator_to_session, read_permutation, \
    read_permutation_by_key, REQUEST_TYPE_COMMON, REQUEST_TYPE_AJAX


FLASK_RUN_IN_DEBUG_MODE = True


app = Flask(__name__)

# Ограничить длину получаемого сообщения 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


generators_dct = {}


@app.route('/')
def index():
    print('\nindex: generators_dct:\n', generators_dct, '\n')
    print(get_flashed_messages())
    return render_template(
        'index.html', 
        message='Введите массив (числа, разделённые пробелами)'
    )


@app.route('/v1/init', methods=['POST'])
def post_array():
    stop_generator(session, generators_dct)

    request_type = get_type_from_request(request)

    array = parse_array_from_request(request, request_type)

    if (array is None):
        return _response_on_error('Ошибка в ведённых данных!', request_type)

    generator_key = add_generator_to_session(session, array, generators_dct)

    if (generator_key is None):
        return _response_on_error('Ошибка в ведённых данных!', request_type)
   
    permutation = read_permutation_by_key(generators_dct, generator_key)

    if (permutation is None):
        return _response_on_error(
            'Ошибка при вычислении первой перестановки!', request_type
            )

    permutation = permutation[0]
    if (request_type == REQUEST_TYPE_COMMON):
        return render_template(
            'next.html', 
            permutation=permutation,
            message='Массив получен'
        )
    elif (request_type == REQUEST_TYPE_AJAX):
        return permutation


@app.route('/v1/next', methods=['GET'])
def next_permutation():
    request_type = get_type_from_request(request)

    data = read_permutation(session, generators_dct)

    if (data is None):
        return _response_on_error(
            'Ошибка в генераторе перестановок!', request_type
            )

    if (request_type == REQUEST_TYPE_COMMON):
        return render_template(
            'next.html', 
            permutation=data[0],
            last_permutation=data[1],
            message='Следующая перестановка'
        )

    elif (request_type == REQUEST_TYPE_AJAX):
            return data[0]


@app.route('/v1/stop', methods=['GET'])
def stop():
    stop_generator(session, generators_dct)
    return redirect(url_for('index'))


def _response_on_error(message, request_type):
    stop_generator(session, generators_dct)
    if (request_type == REQUEST_TYPE_COMMON):
        if message is not None:
            flash(message)
        return redirect(url_for('index'))
    elif (request_type == REQUEST_TYPE_AJAX):
        return jsonify(message)


app.secret_key = 'Azuf67-pn436de1'


def main():
    app.run(debug=FLASK_RUN_IN_DEBUG_MODE)


if __name__ == '__main__':
    main()
