from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
# CORS mit zusätzlichen Optionen konfigurieren
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],  # Vite's default port
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)