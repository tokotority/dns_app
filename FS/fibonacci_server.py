from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = int(data['as_port'])

    msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (as_ip, as_port))
    response, _ = sock.recvfrom(1024)
    
    if response.decode() == "201":
        return "", 201
    else:
        return jsonify({"error": "Registration failed"}), 500

@app.route('/fibonacci')
def get_fibonacci():
    number = request.args.get('number')
    if not number:
        return jsonify({"error": "Missing 'number' parameter"}), 400
    
    try:
        n = int(number)
        result = fibonacci(n)
        return jsonify({"fibonacci": result})
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)