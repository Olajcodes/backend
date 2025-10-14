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
},
    {
    "Name": "Ayyub",
    "Age": 60
},
    {
    "Name": "Mike",
    "Age": 45
}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
        
    def do_DELETE(self):
        index = int(self.path.strip("/"))
        if index >= len(data):
            self.send_data({
                "Error": "Invalid Index (Out_of_range)"
            }, status=400)
            return
        
        deleted = data.pop(index)   # Removing from a database
        self.send_data({
            "Message": "Record deleted",
            "Record Deleted": deleted
        })
        
def run():
    HTTPServer(('localhost', 7000), BasicAPI).serve_forever()
    
print(f"Server connected to port 7000")
run()