# ClipboardStealer
# DNS Payload Clipboard Sender

This program periodically captures the contents of the clipboard, encodes the data into a DNS payload, and sends it to a command and control (C2) server. The purpose of this program is to demonstrate a covert channel for exfiltrating data using DNS queries.

## Prerequisites

- Python 3.x
- Pyperclip
- dnslib
- dns.resolver

## Usage

1. Install the required dependencies by running the following command:
pip install pyperclip dnslib dnspython

2. Run the program by executing the `clipboard_sender.py` script:
python clipboard_sender.py

3. The program will continuously monitor the clipboard for changes and send the data in the clipboard to the C2 server every 15 minutes.

## How It Works

1. The `pasteClipBoard()` function retrieves the contents of the clipboard using the `pyperclip` library. The data is then encoded using base64 and appended with a special delimiter `!EN!`.

2. The `sendPayload(encodedData, domain, dns_server)` function encapsulates the encoded data into DNS queries and sends them to the C2 server. If the encoded data exceeds a certain size, it is split into chunks of 20 characters each.

3. The program continuously monitors the clipboard for changes. If the clipboard contents remain the same as the previous iteration, the program sleeps for 15 minutes before checking again. This prevents redundant data transmissions.

4. The `main` section initializes a variable to store the previous value of the clipboard. It compares the current clipboard value with the previous value to determine if any changes have occurred. If a change is detected, the payload is extracted from the clipboard and sent to the C2 server.

## Configuration

- `domain`: Specify the domain name to be used for DNS queries. Update the `'shahin.com'` value in the `sendPayload()` function with your desired domain.

- `dns_server`: Specify the IP address or hostname of the DNS server to send the queries. Update the `'127.0.0.1'` value in the `sendPayload()` function with your desired DNS server.

## Note

This program is intended for educational and demonstration purposes only. The use of covert channels may have legal and ethical implications, so use this code responsibly and with proper authorization.

