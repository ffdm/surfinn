from PyQt6 import QtWidgets
import socket
import ssl
import sys

class Response:
    def __init__(self, response):
        # read statusline
        self.version, self.status, self.description = response.readline().split(' ', 2)

        # read headers
        self.headers = {}
        while (line := response.readline()) != '\r\n':
            header, value = line.split(':', 1)
            self.headers[header.lower()] = value.strip()
       
        # check for compressed data (not currently supported)
        assert 'transfer-encoding' not in self.headers
        assert 'content-encoding' not in self.headers

        # read body
        self.body = response.read()

    def __str__(self):
        string = f"{self.version} {self.status} {self.description}\n"
        for header, value in self.headers.items():
            string += f"{header}: {value}\n"
        string += self.body
        return string

class URL:

    def __init__(self, url):
        split_url = url.split('://', 1)
        url = split_url[-1]
        
        # give url default scheme
        if len(split_url) == 2:
            self.scheme = split_url[0]
        else:
            self.scheme = 'https'

        assert self.scheme in ['http', 'https']

        if self.scheme == 'http':
            self.port = 80
        elif self.scheme == 'https':
            self.port = 443

        if '/' not in url:
            url += '/'
        self.host, url = url.split('/', 1)
        self.path = '/' + url

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
    
    def request(self):
        # define socket
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        # define request
        request = f'GET {self.path} HTTP/1.1\r\n'

        # include headers
        headers = {}
        headers['Host'] = self.host
        headers['Connection'] = "close"
        headers['User-Agent'] = "Surfinn"
        for header, value in headers.items():
            request += f"{header}: {value}\r\n"

        # extra new line
        request += '\r\n'

        # connect to socket 
        s.connect((self.host, self.port))

        # encrypt connection if https
        if self.scheme == 'https':
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        # send request
        s.send(request.encode('utf8'))

        # receive response
        response_data = s.makefile('r', encoding='utf8', newline='\r\n')
        
        # parse response
        response = Response(response_data)

        # close socket
        s.close()

        return response
        
class Browser:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QWidget()

    def load(self, url):
        self.window.show()

def show(body):
    # prints text without tags from html file
    in_tag = False
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            print(c, end='')

def load(url):
    response = url.request()

    # handle redirects
    redirect_count = 0
    while response.status[0] == '3' and redirect_count < 5:
        redirect_count += 1
        
        # handle same host/scheme case
        if response.headers['location'][0] == '/':
            response = URL(url.scheme+'://'+url.host+response.headers['location']).request()
        else: 
            response = URL(response.headers['location']).request()

    # display html body
    show(response.body)

if __name__ == '__main__':
    browser = Browser()
    browser.load(URL(sys.argv[1]))
    browser.app.exec()

