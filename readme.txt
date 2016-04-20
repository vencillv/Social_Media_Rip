Outline of files and their purpose:

server.py
This implements a simple "Python server pages" like server.
    The concept is similar to PHP: Executable code is embedded
    within a web page between <% %> tags.
    When the page is displayed, the content is executed.
    
monkey.py
Put your customizations here. The contents of this file will be accessible
    from your .html files from the monkey.* module
    
public/ 
Files that the server will send are located here.



Blocks in HTML files delimited with <% %> are treated as executable
python code. Within the code, the following variables are available:

monkey: A handle to the monkey.py module
self: A handle to an object describing the current http request that is being completed.
    The self object is an instance of http.server.BaseHTTPRequestHandler and has these items:
        -client_address: (host,port)
        -server: the server object
        -command: the HTTP command ('GET' or 'POST' usually)
        -path: the path as sent in by the client -- not the final on-disk path
        -request_version: HTTP/1.0 or HTTP/1.1
        -headers: A dictionary-like object of headers from the client request. Key=header, value=content of header
        -responsecode: A numeric HTTP response code. Default is 200; this may be changed to report an error.
        -remote: Data written here goes to the remote side. Use remote.write() to write the data.
        -fs: A CGI FieldStorage object that allows access to submitted data. Methods include:
            -getfirst(name): Get item with the given name, or None if doesn't exist
            -If a particular field is an uploaded file object: Access like so:
                self.fs["thing"].file.read()
    The self object also has these methods:
        -send_header(key,value): Set a header on the response
        
    
