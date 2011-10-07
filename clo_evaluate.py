import sublime
import sublime_plugin
import threading
import socket
import Queue

def show(x):
    sublime.status_message(x)

def separator():
    return '\x1e'

class CloEvaluateCommand(sublime_plugin.TextCommand):

    def init_client(self):
        try:
            self.client = EvaluateClient()
            self.client.start()
        except socket.error, e:
            pass

    def alive(self):
        return hasattr(self, 'client') and self.client.is_alive()

    def run(self, edit):
        if self.view.settings().get('syntax').find('Clojure') < 0:
            return

        sels = self.view.sel()

        if not self.alive():
            self.init_client()

        if self.alive():
            for sel in sels:
                string = self.view.substr(sel)
                if len(string) > 0:
                    resp = self.client.execute(string)
                    show(resp)
        else:
            show('Can\'t connect to REPL server')

class EvaluateClient(threading.Thread):
    def __init__(self, host='localhost', port=9999):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.pool = Queue.Queue()
        self.out = Queue.Queue()
        threading.Thread.__init__(self)

    def execute(self, string):
        self.pool.put(string)
        try:
            return self.out.get(True, 10)
        except Queue.Empty, e:
            return 'Can\'t connect to REPL server'

    def send(self, string):
        self.client.send(string)
        self.client.send(separator())
        response = ''
        c = ''
        while c != separator():
            c = self.client.recv(1)
            response += c
        return response[:-1]

    def run(self):
        try:
            while True:
                request = self.pool.get()
                response = self.send(request)
                self.out.put(response)
        except Exception, e:
            self.out.put('Can\'t connect to REPL server')
