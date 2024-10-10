import socket
import json

DNS_FILE = "dns_records.json"

def load_dns_records():
    try:
        with open(DNS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_dns_records(records):
    with open(DNS_FILE, 'w') as f:
        json.dump(records, f, indent=2)

def handle_request(data):
    lines = data.strip().split('\n')
    request_type = "REGISTER" if len(lines) == 4 else "QUERY"
    
    if request_type == "REGISTER":
        return handle_registration(lines)
    else:
        return handle_query(lines)

def handle_registration(lines):
    record = {}
    for line in lines:
        key, value = line.split('=')
        record[key] = value

    dns_records = load_dns_records()
    dns_records[record['NAME']] = {
        'TYPE': record['TYPE'],
        'VALUE': record['VALUE'],
        'TTL': record['TTL']
    }
    save_dns_records(dns_records)
    return "201"

def handle_query(lines):
    query = {}
    for line in lines:
        key, value = line.split('=')
        query[key] = value

    dns_records = load_dns_records()
    if query['NAME'] in dns_records:
        record = dns_records[query['NAME']]
        return f"TYPE={record['TYPE']}\nNAME={query['NAME']}\nVALUE={record['VALUE']}\nTTL={record['TTL']}"
    else:
        return "404"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))
    print("Authoritative Server is running on port 53533")

    while True:
        data, addr = server_socket.recvfrom(1024)
        response = handle_request(data.decode())
        server_socket.sendto(response.encode(), addr)

if __name__ == "__main__":
    main()