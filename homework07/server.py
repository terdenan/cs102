import asyncore
import asynchat
import socket
import multiprocessing
import logging
import mimetypes
import os
from pathlib import Path, PurePath
from urllib.parse import parse_qs, urlparse
import urllib
import argparse
from time import strftime, gmtime


def url_normalize(path):
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1+3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    return path


def read_file(path):
    file = bytes()
    fp = FileProducer(open(path, 'rb'))
    while (True):
        cur_chunk = fp.more()
        if not cur_chunk:
            break
        file += cur_chunk

    return file


class FileProducer(object):

    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class AsyncServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000, handler_class=None):
        super().__init__()
        self.handler_class = handler_class
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        #log.debug(f"Incoming connection from {addr}")
        self.handler_class(sock)
        #AsyncHTTPRequestHandler(sock)

    def serve_forever(self):
        asyncore.loop()


class AsyncHTTPRequestHandler(asynchat.async_chat):

    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b"\r\n\r\n")
        self.reading_headers = True
        self.req_data = ""
        self.post_data = bytes()
        self.headers = None
        self.method = None
        self.response = ""

    def collect_incoming_data(self, data):
        if not self.reading_headers:
            self.post_data = data
        else:
            self.req_data += data.decode('utf-8')

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        if self.reading_headers:
            method, path, headers = self.req_data.split(None, 2)

            self.method = method
            self.parse_headers(headers)
            self.req_path = urlparse("http://" + self.headers['Host'] + path).path
            if (self.method == "POST"):
                clen = int(self.headers['Content-Length'])
                if clen > 0:
                    self.reading_headers = False
                    self.set_terminator(clen)
            elif (self.method == "GET"):
                self.handle_request()
        else:
            self.handle_request()

    def parse_headers(self, header):
        headers_lst = header.split('\r\n')

        self.headers = {}
        for header in headers_lst:
            if (len(header.split(':', 1)) != 2):
                continue

            keyword, value = header.split(':', 1)
            self.headers[keyword] = value

    def handle_request(self):
        method_name = 'do_' + self.method
        if not hasattr(self, method_name):
            self.send_error(405)
            self.handle_close()
            return
        handler = getattr(self, method_name)
        handler()

    def send_error(self, code, message=None):
        try:
            short_msg, long_msg = self.responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg

        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "close")
        self.end_headers()
        self.send(bytes(self.response.encode('utf-8')))
        self.close()

    def send_response(self, code, message=None):
        self.response += "HTTP/1.1 {} {}\r\n".format(code, message)

    def send_header(self, keyword, value):
        self.response += "{}: {}\r\n".format(keyword, value)

    def end_headers(self):
        self.response += "\r\n"

    def date_time_string(self):
        return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

    def translate_path(self, path):
        return url_normalize(path)

    def do_GET(self):
        p = Path('public/' + self.req_path)
        if p.is_dir():
            p = Path('public/' + self.req_path + 'index.html')
            if not p.is_file():
                self.send_error(404)
                return
            file_type, _ = mimetypes.guess_type(str(p))
            file = read_file(p)
        elif p.is_file():
            file_type, _ = mimetypes.guess_type(str(p))
            file = read_file(p)
        else:
            self.send_error(404)
            return

        self.send_response(200, "OK")
        self.send_header("Content-Type", file_type)
        self.send_header("Connection", "close")
        self.send_header("Content-Length", len(file))
        self.end_headers()
        self.send(bytes(self.response.encode('utf-8')) + file)
        self.close()

    def do_HEAD(self):
        p = Path('public/' + self.req_path)
        if p.is_dir():
            p = Path('public/' + self.req_path + 'index.html')
            if not p.is_file():
                self.send_error(404)
                return
            file_type, _ = mimetypes.guess_type(str(p))
            file = read_file(p)
        elif p.is_file():
            file_type, _ = mimetypes.guess_type(str(p))
            file = read_file(p)
        else:
            self.send_error(404)
            return

        self.send_response(200, "OK")
        self.send_header("Content-Type", file_type)
        self.send_header("Connection", "close")
        self.send_header("Content-Length", len(file))
        self.end_headers()
        self.send(bytes(self.response.encode('utf-8')))
        self.close()

    def do_POST(self):
        self.send_response(200, "OK")
        self.send_header("Content-Type", self.headers['Content-Type'])
        self.send_header("Connection", "close")
        self.send_header("Content-Length", self.headers['Content-Length'])
        self.end_headers()
        self.send(bytes(self.response.encode('utf-8')) + self.post_data)
        self.close()

    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
            'Bad request syntax or unsupported method'),
        403: ('Forbidden',
            'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
            'Specified method is invalid for this resource.'),
    }


def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default=".")
    return parser.parse_args()


def run():
    server = AsyncServer(host=args.host, port=args.port, handler_class=AsyncHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    args = parse_args()

    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")
    log = logging.getLogger(__name__)

    DOCUMENT_ROOT = args.document_root
    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run)
        p.start()
