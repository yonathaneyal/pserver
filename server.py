from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import socketserver

class Server(BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        #self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        if self.path == '/metrics':
            self.get_status_code_and_response('https://httpstat.us/200')
            self.get_status_code_and_response('https://httpstat.us/503')

    def get_status_code_and_response(self,host):
        try:
            r = requests.get(host)
            self.wfile.write ("\nsample_external_url_up{{url=\"{}\"}}={}\n".format(host, '1' if r.status_code == 200 else '0').encode('utf-8'))
            self.wfile.write ("sample_external_url_response_ms{{url=\"{}\"}}={}".format(host, r.elapsed.microseconds/1000).encode('utf-8'))
        except requests.exceptions.RequestException as e:
            self.wfile.write ("Error:",e)


def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print ("Starting httpd on port %d..." % port) 
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
