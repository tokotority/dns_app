from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"error": "Missing parameters"}), 400

    # Query AS to get FS IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = f"TYPE=A\nNAME={hostname}"
    sock.sendto(msg.encode(), (as_ip, int(as_port)))
    response, _ = sock.recvfrom(1024)
    response = response.decode().split('\n')
    
    if len(response) != 4 or response[0] != "TYPE=A":
        return jsonify({"error": "Failed to retrieve IP from Authoritative Server"}), 500

    fs_ip = response[2].split('=')[1]

    # Query FS
    try:
        r = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci", params={"number": number})
        r.raise_for_status()
        return jsonify(r.json()), 200
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to get Fibonacci number: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)