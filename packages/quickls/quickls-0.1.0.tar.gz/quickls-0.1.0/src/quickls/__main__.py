import http.server
import socketserver
import argparse
from pathlib import Path
import socket


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()


class PrettyHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        fullpath = self.translate_path(self.path)

        
        if Path(fullpath).is_file():
            filename = Path(fullpath).name
            try:
                with open(fullpath, "rb") as f:
                    content = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            except:
                self.send_error(404, "File not found")
                return

        
        return super().do_GET()

    def list_directory(self, path):
        items = list(Path(path).iterdir())

        html_items = ""
        for item in items:
            name = item.name + ("/" if item.is_dir() else "")
            html_items += f"<li><a href='{name}'>{name}</a></li>"

        template = Path(__file__).with_name("ui.html").read_text("utf-8")
        final_html = template.replace("{{items}}", html_items)

        encoded = final_html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None


def start_server(bind, port):
    real_ip = get_local_ip()
    print(f"Serving at: http://{real_ip}:{port}")

    with socketserver.TCPServer((bind, port), PrettyHandler) as server:
        try:
            server.serve_forever(poll_interval=0.5)   
        except KeyboardInterrupt:
            print("\nCtrl+C received — stopping server...")
            server.shutdown()   
        finally:
            server.server_close()
            print("Server closed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", "-b", default="0.0.0.0")
    parser.add_argument("port", nargs="?", default=1108, type=int)
    args = parser.parse_args()

    start_server(args.bind, args.port)


if __name__ == "__main__":
    main()
