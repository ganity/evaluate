import sublime
import sublime_plugin
import threading
import socket
import Queue

def show(x):
    print 'Clojure:', x

def generate_header(message):
    count = str(len(message))
    return '000000'[:-len(count)] + count

def generate_namespace(view):
    count = str(view.id())
    # count = "0"
    return '0000000000'[:-len(count)] + count

def parse_header(header):
    return int(header)

class CloEvaluateCommand(sublime_plugin.TextCommand):

    def init_client(self, host='localhost', port=9999):
        # return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            return sock
        except socket.error, e:
            return None

    def send(self, sock, string):
        header = generate_header(string)
        ns = generate_namespace(self.view)
        sock.send(header)
        sock.send(ns)
        sock.send(string)

        header = sock.recv(6)
        count = parse_header(header)

        return sock.recv(count)

    def run(self, edit):
        return
        if self.view.settings().get('syntax').find('Clojure') < 0:
            return

        sels = self.view.sel()
        sock = self.init_client()

        msgs = []
        if sock:
            for sel in sels:
                string = self.view.substr(sel)
                if len(string) > 0:
                    try:
                        response = self.send(sock, string)
                        show(response)
                    except Exception, e:
                        show('Can\'t connect to REPL server')
        else:
            show('Can\'t connect to REPL server')

# class EvaluateClient(threading.Thread):
#     def __init__(self, socket, messages):
#         self.socket = socket
#         self.messages = messages
#         threading.Thread.__init__(self)

#     def send(self, string):
#         header = generate_header(string)
#         self.socket.send(header)
#         self.socket.send(string)

#         header = self.socket.recv(6)
#         count = parse_header(header)

#         return self.socket.recv(count)

#     def run(self):
#         try:
#             for msg in self.messages:
#                 response = self.send(msg)
#                 show(response)
#         except Exception, e:
#             show('Can\'t connect to REPL server')
