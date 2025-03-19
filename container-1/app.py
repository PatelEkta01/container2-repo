from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Persistent volume directory
PV_DIR = "/data"

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.json
    if not data or 'file' not in data or 'data' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    file_data = data['data']

    # Prevent storing empty files
    if not file_data.strip():
        return jsonify({"file": file_name, "error": "File content cannot be empty."}), 400

    try:
        # Write file to persistent volume
        with open(os.path.join(PV_DIR, file_name), 'w') as f:
            f.write(file_data)
        return jsonify({"file": file_name, "message": "Success."}), 200
    except Exception as e:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    if not data or 'file' not in data or 'product' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data['product']

    try:
        # Read file from persistent volume
        with open(os.path.join(PV_DIR, file_name), 'r') as f:
            lines = f.readlines()
        
        # Calculate total for the product
        total = 0
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(',')
            if parts[0] == product:
                total += int(parts[1])
        
        return jsonify({"file": file_name, "sum": total}), 200
    except FileNotFoundError:
        return jsonify({"file": file_name, "error": "File not found."}), 404
    except Exception as e:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)