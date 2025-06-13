import socket
import sys

class URL:

    def __init__(self, url):
        split_url = url.split('://', 1)
        url = split_url[-1]
        
        # allow url to be specified without scheme
        if len(split_url) == 2:
            self.scheme = split_url[0]
        else:
            self.scheme = 'http'

        # browser only supports http
        assert self.scheme == 'http'

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
        s.connect((self.host, 80))

        # send request
        s.send(request.encode('utf8'))

        # receive response
        response = s.makefile('r', encoding='utf8', newline='\r\n')

        # close socket
        s.close()

        # read statusline
        statusline = response.readline()
        version, status, description = statusline.split(" ", 2)

        # read headers
        response_headers = {}
        while (line := response.readline()) != '\r\n':
            header, value = line.split(':', 1)
            response_headers[header.lower()] = value.strip()
       
        # check for compressed data (not currently supported)
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        # read body
        body = response.read()
        return body

def show(body):
    # prints text without tags from html file
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = url.request()
    show(body)

if __name__ == "__main__":
    load(URL(sys.argv[1]))
