# http & server is an inbuilt module from python
# HTTPServer is used to run the endpoint

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# This is just on our RAM but ideally it should be from database
data = []

# Creating a class for base 
# (API is same as Endpoint)
class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 201):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
        
    def do_POST(self):
        content_size = int(self.headers.get("COntent-Length", 0))
        parsed_data = self.rfile.read(content_size)
        
        post_data = json.loads(parsed_data)
        print(post_data)
        data.append(post_data)      # Saving to a database
        self.send_data({
            "Message": "Data Received",
            "data": post_data
        })
        
# Using this function to run the "HTTPServer" just for modular sake.
def run():
    HTTPServer(('localhost', 5000), BasicAPI).serve_forever()       # .serve_forever() is used to keep our funning running without ending itself except stated otherwise

print("Application is running!!!")
run()
    