from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import datetime
import json

app = Flask(__name__)
# CORS mit zusätzlichen Optionen konfigurieren
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],  # Vite's default port
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

db_config = {
    'user': 'ben2',
    'password': '123',
    'host': '172.22.96.1',
    'database': 'sr_legacy'
}

@app.route('/api/foods', methods=['GET'])
#def get_foods():
#     foods = [
#         {"id": 1, "name": "Apple"},
#         {"id": 2, "name": "Banana"},
#         {"id": 3, "name": "Carrot"}
#     ]
#     return jsonify(foods)
# def get_foods():
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT NDB_No AS id, Long_Desc AS name FROM prepddata")
#         foods = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         with open('foods.json', 'w') as json_file:
#             json.dump(foods, json_file, indent=4)
#         return jsonify(foods)

@app.route('/api/counts', methods=['POST', 'OPTIONS'])
def update_count():
    if request.method == 'OPTIONS':
        # Preflight request. Reply successfully:
        return jsonify({'status': 'ok'}), 200

    # POST request
    data = request.json
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n=== Neue Aktualisierung (" + current_time + ") ===")
    print(f"Aktueller Count: {data.get('count', 0)}")

    return jsonify({"status": "success", "message": "Count erfolgreich aktualisiert"})

@app.route('/api/selected_food', methods=['POST'])
def selected_food():
    data = request.json
    ndb_no = data.get('ndb_no')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=== Lebensmittel ausgewählt ({current_time}) ===")
    print(f"Ausgewählte NDB_No: {ndb_no}")
    return jsonify({"status": "success", "message": f"Ausgewählte NDB_No: {ndb_no}"})


@app.route('/api/users', methods=['POST', 'OPTIONS'])
def update_users():
    if request.method == 'OPTIONS':
        # Preflight request. Reply successfully:
        return jsonify({'status': 'ok'}), 200

    # POST request
    data = request.json
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n=== Benutzeraktualisierung (" + current_time + ") ===")
    print("\nAktuelle Benutzerdaten:")

    # Gibt die Benutzerdaten tabellarisch aus
    if data:
        print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Stadt':<15}")
        print("-" * 70)

        for user in data:
            print(f"{user['id']:<5} {user['name']:<20} {user['email']:<30} {user['address']['city']:<15}")

    return jsonify({"status": "success", "message": "Benutzerdaten erfolgreich empfangen"})


@app.route('/api/get_data', methods=['POST'])
def get_data():
    ndb_no = request.json.get('NDB_No')
    if not ndb_no:
        return jsonify({'error': 'NDB_No is required'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
               food_desc1.Shrt_Desc AS food1_id,
               food_desc2.Shrt_Desc AS food2_id,
               value1,
               value2,
               excess
            FROM result
            JOIN food_desc food_desc1 ON concat(result.food1_id) = food_desc1.NDB_No
            JOIN food_desc food_desc2 ON concat(result.food2_id) = food_desc2.NDB_No
            WHERE (food1_id = %s OR food2_id = %s)
            ORDER BY excess ASC
            LIMIT 50
        """
        #cursor.execute(query, (ndb_no, ndb_no))
        cursor.execute(query, (ndb_no, ndb_no))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

'''
Route kann Daten als Objekt oder nur die ID bekommen
'''

# @app.route('/api/get_data', methods=['POST', 'OPTIONS'])
# def get_data():
#     if request.method == "OPTIONS":
#         return jsonify({"status": "ok"}), 200
#
#     data = request.json
#     # Überprüfen ob NDB_No ein Dict ist und die ID extrahieren
#     if isinstance(data.get('NDB_No'), dict):
#         ndb_no = str(data['NDB_No'].get('id'))
#     else:
#         ndb_no = str(data.get('NDB_No'))
#
#     if not ndb_no:
#         return jsonify({'error': 'NDB_No is required'}), 400
#
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#         query = """
#             SELECT
#                food_desc1.Shrt_Desc AS food1_id,
#                food_desc2.Shrt_Desc AS food2_id,
#                value1,
#                value2,
#                excess
#             FROM result
#             JOIN food_desc food_desc1 ON concat(result.food1_id) = food_desc1.NDB_No
#             JOIN food_desc food_desc2 ON concat(result.food2_id) = food_desc2.NDB_No
#             WHERE (food1_id = %s OR food2_id = %s)
#             ORDER BY excess ASC
#             LIMIT 50
#         """
#         cursor.execute(query, (ndb_no, ndb_no))
#         results = cursor.fetchall()
#         cursor.close()
#         conn.close()
#
#         # Debug-Ausgabe
#         print(f"Query results for NDB_No {ndb_no}:", results)
#
#         return jsonify(results)
#     except mysql.connector.Error as err:
#         print(f"Database error: {str(err)}")
#         return jsonify({'error': str(err)}), 500
#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)