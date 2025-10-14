# http & server is an inbuilt module from python
# HTTPServer is used to run the endpoint

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# This is just on our RAM but ideally it should be from database
data = [
    {
       "name": "Sam Larry",
       "track": "AI Developer"
    },
    {
        "name": "Abioye Olajide",
        "track": "AI Engineer"
    }
]

# Creating a class for base 
# (API is same as Endpoint)
class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status = 201):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        
    def do_GET(self):
        self.send_data(data)
        
# Using this function to run the "HTTPServer" just for modular sake.
def run():
    HTTPServer(('localhost', 8000), BasicAPI).serve_forever()       # .serve_forever() is used to keep our funning running without ending itself except stated otherwise

print("Application is running!!!")
run()
    