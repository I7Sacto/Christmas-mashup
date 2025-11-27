# client.py
import socket

SOCK_PATH = "/tmp/myservice.sock"
sock_exist = False
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(SOCK_PATH)
text = ""
end_seq=f'\0' * 16

while True:
    data = s.recv(1024)
    if not data:
        break
    text+=data.decode('utf-8', errors='replace')
    if(end_seq in text):
        index = text.index(end_seq)
        print(text[0:index], end='')
        text = text[index + 16:-1]
