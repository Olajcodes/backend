from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {
    "Name": "Olajcodes",
    "Age": 35
},
    {
    "Name": "Debby",
    "Age": 40
}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 201):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
        
    def do_PUT(self):  
        index = int(self.path.strip("/"))
        if index >= len(data):
            self.send_data({
                "Error": "invalid index"
            }, status=400)
            return
        content_size = int(self.headers.get("COntent-Length", 0))
        parsed_data = self.rfile.read(content_size)
        put_data = json.loads(parsed_data)
        print(put_data)
        
        data[index] = put_data      # Updating from a database
        self.send_data({
            "Message": "Data Updated",
            "data": put_data
        })
        
# Using this function to run the "HTTPServer" just for modular sake.
def run():
    HTTPServer(('localhost', 5000), BasicAPI).serve_forever()       # .serve_forever() is used to keep our server running without ending itself except stated otherwise

print("Application is running!!!")
run()
    