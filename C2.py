import base64
import socket
from dnslib import DNSRecord, QTYPE
import datetime

file_path = r'Set_your_filepath_here'
# Function to decode the payload from DNS queries

def receive_data():
    encoded_data = ""
    end_marker = "!EN!"
    while True:
        # Receive DNS query
        query_data, client = server_socket.recvfrom(4096)
        dns_query = DNSRecord.parse(query_data)

        # Extract the chunk from the query and append it to the data
        #chunk = str(dns_query.q.qname).rstrip(".")
        chunk = str(dns_query.q.qname).split('.', 1)[0]

        #Look for end marker to catch last chunk
        if end_marker in chunk:
            chunk = chunk.replace(end_marker, "")
            encoded_data += chunk
            break

        encoded_data += chunk

    # Decode the final payload
    payload = base64.b64decode(encoded_data).decode()
    return payload, client


# Create a socket and bind it to port 53
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 53))

print("DNS server listening on port 53...")

# Start listening for DNS queries
while True:
    # Extract the encoded payload from the query

    payload, client_address = receive_data()

    # Format data and save to file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_data = f"{client_address} >> {timestamp}: {payload}\n"
    with open(file_path, "a") as file:
        file.write(formatted_data)

    # Print the decoded payload
    print("Received payload:", payload)


