import socket
import ssl
import sys

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
    
    def request(self):
        # define socket
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        # define request
        request = f'GET {self.path} HTTP/1.0\r\n'
        request += f'Host: {self.host}\r\n'
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
        response = s.makefile('r', encoding='utf8', newline='\r\n')

        # close socket
        s.close()

        # read statusline
        statusline = response.readline()
        version, status, description = statusline.split(' ', 2)

        # read headers
        response_headers = {}
        while (line := response.readline()) != '\r\n':
            header, value = line.split(':', 1)
            response_headers[header.lower()] = value.strip()
       
        # check for compressed data (not currently supported)
        assert 'transfer-encoding' not in response_headers
        assert 'content-encoding' not in response_headers

        # read body
        body = response.read()
        return body

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
    body = url.request()
    show(body)

if __name__ == '__main__':
    load(URL(sys.argv[1]))
