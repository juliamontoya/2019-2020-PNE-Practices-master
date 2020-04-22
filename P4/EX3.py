# Extend the previous web server for accessing to the web pages of the C base, in addition to the A base
import socket
import termcolor
from seq0 import *
from pathlib import Path


# -- Server network parameters
IP = "127.0.0.1"
PORT = 8080

FOLDER = "../P4/"
FILENAME = "A.html" "C.html"
EMPTYFIL = "index.html"


def seq_read_fasta(filename):
    file_contents = Path(filename).read_text()
    content = file_contents.split("\n")[1:]
    e = "".join(content)
    return e


def process_client(s):
    # -- Receive the request message
    req_raw = s.recv(2000)
    req = req_raw.decode()

    print("Message FROM CLIENT: ")

    # -- Split the request messages into lines
    lines = req.split('\n')

    # -- The request line is the first
    req_line = lines[0]

    print("Request line: ", end="")
    termcolor.cprint(req_line, "green")

    # -- Generate the response message
    # It has the following lines
    # Status line
    # header
    # blank line
    # Body (content to send)

    # This new contents are written in HTML language
    if "info/A" in req:
        FILENAME = "A.html"
        body = seq_read_fasta(FOLDER + FILENAME)
    elif "info/C" in req:
        FILENAME = "C.html"
        body = seq_read_fasta(FOLDER + FILENAME)
    else:
        body = seq_read_fasta(FOLDER + EMPTYFIL)

    # -- Status line: We respond that everything is ok (200 code)
    status_line = "HTTP/1.1 200 OK\n"

    # -- Add the Content-Type header
    header = "Content-Type: text/html\n"

    # -- Add the Content-Length
    header += f"Content-Length: {len(body)}\n"

    # -- Build the message by joining together all the parts
    response_msg = status_line + header + "\n" + body
    cs.send(response_msg.encode())


# -------------- MAIN PROGRAM
# ------ Configure the server
# -- Listening socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Setup up the socket's IP and PORT
ls.bind((IP, PORT))

# -- Become a listening socket
ls.listen()

print("SEQ Server configured!")

# --- MAIN LOOP
while True:
    print("Waiting for clients....")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server Stopped!")
        ls.close()
        exit()
    else:

        # Service the client
        process_client(cs)

        # -- Close the socket
        cs.close()