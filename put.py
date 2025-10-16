from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {"name": "Jahmiu", "Username": "jayboy"},
    {"name": "Jide", "Username": "olam"}

]


class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_PUT(self):
        content_size = int(self.headers.get("Content-Length", 0))
        update_data = self.rfile.read(content_size)
        put_data = json.loads(update_data)
        name = put_data.get("name")

        if name is None:
            self.send_data(
                {"error": "Missing 'name' in request body"}, status=400)
            return

        for record in data:
            if record["name"] == name:
                record.update(put_data)
                self.send_data({
                    "message": "Data updated successfully",
                    "updated_data": record
                })
                return

        self.send_data({"error": f"Record {name} not found"}, status=404)


def run():
    HTTPServer(('localhost', 6000), BasicAPI).serve_forever()


print("Applicaton is running")
run()
