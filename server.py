#!/usr/bin/env python3


#you should not need to modify this file;
#put local modifications in monkey.py instead.

import http.server
import cgi
import os
import os.path
import mimetypes
import sys
import traceback
import io
import monkey

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.handlereq()
    def do_POST(self):
        self.handlereq()

    def handlereq(self):
        path=self.path

        #if path had a query string, fetch the resource component
        #and discard the query string
        path=path.split("?")[0]

        #if empty: Serve index file
        if path=='' or path=='/':
            path='/index.html'

        #remove leading slash
        if path[0] == '/':
            path=path[1:]

        #convert to OS's native format
        path=path.replace("/",os.path.sep)

        #make it relative to the content folder
        path=os.path.join(sys.path[0],"public",path)

        #canonicalize path
        path=os.path.abspath(path)

        #everything we are permitted to serve is
        #under this path
        ok=os.path.join(sys.path[0],"public")
        ok=os.path.abspath(ok)

        #if path is not under public dir or path doesn't exist,
        #return a generic error
        if not path.startswith(ok) or not os.access(path,os.F_OK):
            self.send_response(400)
            self.send_header("Content-type","text/html")
            self.end_headers()

            #cross site scripting vulnerability:
            #For example/demo purposes
            self.wfile.write("<HTML>The path ".encode())
            self.wfile.write(self.path.encode())
            self.wfile.write(" was not accessible.</HTML>".encode())
        elif path.endswith(".html"):

            #read any form submission data and store to self.fs
            env={}
            env["REQUEST_METHOD"]=self.command
            env["CONTENT_LENGTH"]=self.headers.get("content-length",0)
            env["CONTENT_TYPE"]=self.headers.get("content-type","text/plain")
            tmp=self.path.split("?",1)
            if len(tmp) > 1:
                env["QUERY_STRING"]=tmp[1]
            self.fs = cgi.FieldStorage(fp=self.rfile,environ=env)


            self.responsecode = 200
            #We buffer so the user can write headers and content
            #intermingled and they get sent out correctly.
            self.remote = io.StringIO()

            fp=open(path)
            dat=fp.read()
            fp.close()
            si=0
            line=1
            try:
                #content between <% %> is interpreted
                #as python code to execute. This is like
                #Python Server Pages (which in turn is similar
                #in concept to PHP). The implementation here
                #is particularly inefficient.
                while si < len(dat):
                    #look for a <% sequence
                    ei=dat.find("<%",si)

                    #if none found: end index will be the end of the document
                    if ei == -1:
                        ei=len(dat)

                    #this is ordinary html. write it.
                    substr = dat[si:ei]
                    self.remote.write(substr)

                    line += substr.count("\n")

                    #if we had <% code to execute: do the execute
                    if ei < len(dat):

                        #ending ending index
                        eei = dat.find("%>",ei)
                        if eei == -1:
                            raise Exception(path+": line "+str(line)+": Found <% without %>")
                        else:
                            srccode=dat[ei+2:eei]

                            #if we were interested in efficiency, we would
                            #cache this code object somewhere
                            execode = compile(srccode,path,"exec")

                            D={'self':self,'monkey':monkey}
                            exec(execode,D,{})
                        si=eei+2
                        line += srccode.count("\n")
                    else:
                        si=ei
            except Exception as e:
                #if the evaluation broke, print exception to screen
                #and to remote side. In a real server app,
                #we wouldn't print errors to the remote side
                #(at least not in production mode)
                extype , exval , extb = sys.exc_info()
                try:
                    ti1 = traceback.extract_tb(extb)
                    ti=["Error in embedded code"]
                    for filename,linenum,funcname,text in ti1:
                        ti.append("File "+filename+", line "+str(linenum+line-1)+
                            " in function "+funcname+": ")
                    ti.append(str(extype))
                    ti.append(str(exval))

                    x="\n".join(ti)

                    print(x)

                    self.remote.write("<body><pre style='position: absolute; left: 0; top: 0; ")
                    self.remote.write("background: #ff8080; font-size: 14pt;")
                    self.remote.write("white-space: pre-wrap;'>")
                    self.remote.write(x.replace("&","&amp;").replace("<","&lt;"))
                    self.remote.write("</pre>")

                finally:
                    del extb

            s=self.remote.getvalue().encode()

            self.send_response(self.responsecode)
            self.send_header("Content-type","text/html")
            self.send_header("Content-length",len(s))
            self.end_headers()
            self.wfile.write( s )

        else:
            self.send_response(200)
            ty = mimetypes.guess_type(path,strict=False)
            if not ty[0]:
                M={".css":"text/css",
                   ".htm":"text/html",
                   ".html":"text/html",
                   ".png":"image/png",
                   ".gif":"image/gif",
                   ".jpg":"image/jpeg",
                   ".jpeg":"image/jpeg",
                }
                tmp=path.split(".")[-1]
                ty=( M.get(tmp,"text/html"),None )
            self.send_header("Content-type",ty[0])
            self.end_headers()
            count=0
            fp=open(path,"rb")
            while 1:
                z=fp.read(1000)
                if len(z) == 0:
                    break
                self.wfile.write(z)
                count += len(z)
            fp.close()


def main():
    srv = http.server.HTTPServer( ('127.0.0.1',4444) , Handler )
    #srv = http.server.HTTPServer( ('192.168.0.5',4444) , Handler )
    srv.serve_forever()

main()