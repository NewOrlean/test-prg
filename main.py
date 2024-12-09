from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='frontend/build')

# API маршрут
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

# Маршрут для React
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Привязываем сервер к адресу 0.0.0.0, чтобы он был доступен извне
    app.run(host="0.0.0.0", port=5000, debug=True)

