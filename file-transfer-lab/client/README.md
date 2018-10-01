# TCP Client

This is the TCP client side of the lab. This code allows for a user to send a PUT request to the server to
transfer a file into the server. Waits for a response from the server to see if the file already exists or
not. If not, it goes ahead and sends the file to the server.

## Usage

python fileClient.py

Options:
* -s or --server The server to try to connect to            `default: 127.0.0.1:50001`
* -f or --file   The file to get or put					    `default: constitution.txt`
* -d or --debug  To print debug statements in the code      `default: False`
* -? or --usage  Boolean to show how to run the program     `default: False`
