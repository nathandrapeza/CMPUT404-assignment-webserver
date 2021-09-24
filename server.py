#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Citation:
# https://stackoverflow.com/questions/2104080/how-can-i-check-file-size-in-python
# User Danben, https://stackoverflow.com/users/217332/danben
# Used his code for getting a file's size

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        req_str = self.data.decode("utf-8")
        #print(f"a: {a}, a[0]: {a[0]}")
        #print(list(self.data.split(" ")))
        start_line = self.grab_start_line(req_str)

        request_data = self.process_location(start_line)
        status_line = f"HTTP/1.1 {request_data[0]}"

        # All following request_data list variables will already have \n\r
        status_code = request_data[0]
        size = request_data[1]
        content_type = request_data[2]
        message = request_data[3]
    
        #print(f"SIZE OF FILE /index.html : {os.path.getsize('./www/index.html')}")
        
        # Building the response:
        response = status_line
        response += "Connection: close\n\r"
        response += f"Content-Length: {size}\n\r"
        #if not request_data[0.startswith("404"):

        response += f"Content-Type: {content_type}"
        response += "\n\r"
        
        if content_type != None and content_type.startswith("text"):
            response += message
        #print(f"content type: {content_type}")
        #print(f"MESSAGE: {message}")
        print(response)
        
        encoded_response = response.encode(encoding = "utf-8")

        #print(f"wacky line 1 : {self.request.recv(1024).strip()}")
        
        self.request.sendall(encoded_response)
        
        #self.request.sendall(bytearray("OK",'utf-8'))

    
    # grab_start_line() method will return an array of elements from the
    # client's request startline
    # request is formatted already (self.request.rec(2012.strip()))
    # [method, target, http version]
    def grab_start_line(self, request):
        #print(f"REQ: {request}")
        #print(request)
        start_line = ""
        i = 0
        while i < len(request):
            if request[i] != '\r':
                start_line += request[i]
            else:
                i = len(request)
            i += 1

        lst = list(start_line.split())
        return lst

    # process_location() method will process the location of a startline
    # returns response code, content_type, size, and payload if applicable
    # [response code, size, content type, payload]
    def process_location(self, start_line):
        root_dir = "./www"
        size = "0\n\r"
        content_type = None
        status_code = None
        payload = None
        
        if start_line[1] == "/":
            try: # / indicates response should return /index.html from root dir
                filename = f"{root_dir}/index.html"
                payload = open(f"{root_dir}/index.html", "r")
                status_code = "200 OK\n\r"
                import os
                size = str((os.patn.getsize(f"{rootdir}/{start_line[1]}")))
                #content_type = "text/html; charset=UTF-8; charset=iso-8859-1"
                content_type = "text/html;\n\r"
                #size = os.path.getsize("{root_dir}/index.html")
                #print(f"SIZEE::::: {size}")
                payload = self.process_html_css(payload)
            except:
                status_code = "404 Not Found"
        elif start_line[1].endswith("html") or start_line[1].endswith("html/") or start_line[1].endswith("css") or start_line[1].endswith("css/"):
            try:
                payload = open(f"{root_dir}/{start_line[1]}", "r")
                status_code = "200 OK\n\r"
                if start_line[1].endswith("html") or start_line[1].endswith("html/"):
                    content_type = "text/html\n\r" #charset=UTF-8
                    payload = self.process_html_css(payload)
                    import os
                    size = str(os.path.getsize(f"{rootdir}/{start_line[1]}\n\r"))
                elif start_line[1].endswith("css") or start_line[1].endswith("css/"):
                    content_type = "text/css\n\r"
                    #content_type = "text/css; charset=UTF-8\n\r"
                    payload = self.process_html_css(payload)
            except:
                status_code = "404 Not Found\n\r"
                content_type = None
        else:
            try:
                payload = open(f"{root_dir}/{start_line[1]}", "r")
                payload = self.process_html_css(payload)
                status_code = "200 OK\n\r"
            except:
                try:
                    # it might've given us a directory, for example /deep
                    # therefore, try to find index.html inside of ./www/filepath/
                    payload = open(f"{root_dir}/{start_line[1]}/index.html", "r")
                    payload = self.process_html_css(payload)
                    content_type = "text/html; charset=UTF-8\n\r"
                except:
                    status_code = "404 Not Found\n\r"
                    content_type = None
       
        #self.process_html(payload)
        request_data = [status_code, size, content_type, payload]
        #print(request_data)
        return(request_data)

    # process_html_css goes through an HTML or CSS file and returns one to be used in the response message
    # server HTTP respnose
    # input: payload is a python file object
    def process_html_css(self, payload):
        lines = []
        for line in payload:
            lines.append(line)
        i = 0
        while i < len(lines):
            lines[i] = lines[i].replace("\t","")
            i += 1
        
        i = 0
        while i < len(lines):
            j = 0
            count = 0
            spaces = False
            #print(lines[i])

            while j < len(lines[i]):
                if lines[i][j] == " ":
                    count += 1
                else:
                    lines[i] = lines[i][count::]
                    j = len(lines[i])
                j += 1
            i += 1

        while "\n" in lines:
            lines.remove("\n")
        #print(f"lines:{lines}")
        message = "\r".join(lines)
        return message

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
