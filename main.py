from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Разрешаем CORS для всех доменов (если нужно разрешить только конкретные, можно настроить параметры)
CORS(app)

# Конфигурация подключения
username = "root"
password = "WHPEyXccovnMGaMCqdhKRhXZwJECLIal"
host = "junction.proxy.rlwy.net"
database = "railway"
port = 42122


# mysql://root:WHPEyXccovnMGaMCqdhKRhXZwJECLIal@junction.proxy.rlwy.net:42122/railway


def execute(query):
    # Создаём объект engine
    engine = create_engine(
        f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    )

    # Используем транзакцию через begin()
    with engine.connect() as connection:
        # Открываем транзакцию
        with connection.begin():
            result = connection.execute(query)
    return result


@app.route('/api/data', methods=['POST'])
def handle_data():
    # Получаем данные из запроса
    data = request.json

    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    # Обрабатываем данные
    name = data.get('name', 'Unknown')
    age = data.get('age', 'Unknown')

    # Ответ
    return jsonify({
        "message": f"Hello, {name}! You are {age} years old.",
        "received_data": data
    })


@app.route('/api/users/insert', methods=['POST'])
def insert_data():
    # Получаем данные из запроса
    data = request.json

    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    # Обрабатываем данные
    name = data.get('name', 'Unknown')
    age = data.get('age', 'Unknown')

    # Ввод нового user
    insert_query = f"""
    insert users(name, age) values ('{name}', {age});
    """
    # Преобразуем в объект text
    insert_query_text = text(insert_query)

    # Вызываем коннектор
    execute(insert_query_text)

    # Ответ
    return jsonify({
        "message": f"User with name: {name} and age: {age} added.",
        "received_data": data
    })


@app.route('/api/users/update/<int:_id>', methods=['PUT'])
def update_data(_id: int):
    # Получаем данные из запроса
    data = request.json

    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    # Обрабатываем данные
    name = data.get('name', 'Unknown')
    age = data.get('age', 'Unknown')

    # Ввод нового user
    update_query = f"""
    update users  set name = '{name}', age = {age} where id = {_id};
    """
    # Преобразуем в объект text
    update_query_text = text(update_query)

    try:
       execute(update_query_text)
    except Exception as e:
       return jsonify(f'User with id {_id} is missing. Error: {e}' ), 500

    return jsonify(f'User with id {_id} renamed to {name} with age {age}.')


@app.route('/api/users/select', methods=['GET'])
def select_data():
    # Получение всех user
    select_query = f"""
    select * from users;
    """

    # Преобразуем в объект text
    select_query_text = text(select_query)

    # Вызываем коннектор и вытягиваем всех users
    result = execute(select_query_text)
    users = [
        {'name': i.name, 'age': i.age}
        for i in result
    ]

    # Ответ
    return jsonify(users)


@app.route('/api/users/select/<int:_id>', methods=['GET'])
def select_id_data(_id: int):
    # Получение всех user
    select_query = f"""
    select name, age from users where id = {_id};
    """

    # Преобразуем в объект text
    select_query_text = text(select_query)

    try:
        # Вызываем коннектор и вытягиваем конкретного user
        result = execute(select_query_text).fetchone()
    except Exception as e:
        return jsonify(f'There is no user with the selected id!: {e}'), 500

    user = {'name': result.name, 'age': result.age}
    return jsonify(user)


@app.route('/api/users/delete/<int:_id>', methods=['DELETE'])
def delete_id_data(_id: int):
    # Удаление user по id
    delete_query = f"""
    delete from users where id = {_id};
    """

    # Преобразуем в объект text
    delete_query_text = text(delete_query)

    try:
       execute(delete_query_text)
    except Exception as e:
       return jsonify(f'User with id {_id} is missing. Error: {e}' ), 500

    return jsonify(f'User with id {_id} deleted.')

if __name__ == '__main__':
    # Привязываем сервер к адресу 0.0.0.0, чтобы он был доступен извне
    app.run(host="0.0.0.0", port=5000, debug=True)
