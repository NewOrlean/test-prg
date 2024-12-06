from flask import Flask, request, jsonify

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)


