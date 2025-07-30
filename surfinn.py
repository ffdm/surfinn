import socket
import ssl
import sys
import tkinter

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

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

class Browser:

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<MouseWheel>", self.mousescroll)

    def mousescroll(self, event):
        # MacOS 
        self.scroll -= event.delta
        if self.scroll < 0: self.scroll = 0
        self.draw()

    def scrolldown(self, event):
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, event):
        self.scroll -= SCROLL_STEP
        # prevent scrolling above page top
        if self.scroll < 0: self.scroll = 0
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
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
        text = lex(response.body)
        self.display_list = layout(text)
        self.draw()


def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list

def lex(body):
    # returns text without tags from html file
    text = ""
    in_tag = False
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            text += c
    return text

if __name__ == '__main__':
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()

