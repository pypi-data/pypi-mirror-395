import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Event, Thread
from typing import ClassVar, Dict, List, Optional
from urllib.parse import ParseResult, parse_qs, urlparse


class CallbackHandler(BaseHTTPRequestHandler):
    token_data_received: ClassVar[Optional[Dict[str, str]]] = None
    token_event: ClassVar[Event] = Event()

    def do_GET(self) -> None:
        parsed: ParseResult = urlparse(self.path)
        if parsed.path == "/callback":
            params: Dict[str, List[str]] = parse_qs(parsed.query)

            access_token_list: List[str] = params.get("access_token", [])
            refresh_token_list: List[str] = params.get("refresh_token", [])

            access_token = access_token_list[0] if access_token_list else None
            refresh_token = refresh_token_list[0] if refresh_token_list else None

            if access_token and refresh_token:
                CallbackHandler.token_data_received = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                CallbackHandler.token_event.set()

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html: bytes = """
                <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 100px;">
                    <h1>✓ Успешно!</h1>
                    <p>Авторизация завершена. Можете закрыть это окно.</p>
                </body>
                </html>
                """.encode("utf-8")
                self.wfile.write(html)
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    b"<html><body><h1>Error</h1><p>Invalid auth response: missing tokens</p></body></html>"
                )
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass


class LocalAuthServer:
    def __init__(self, start_port: int = 8080) -> None:
        self.port: int = self._find_free_port(start_port)
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[Thread] = None

    def _find_free_port(self, start_port: int) -> int:
        for port in range(start_port, start_port + 100):
            try:
                sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(("localhost", port))
                sock.close()
                return port
            except OSError:
                continue
        raise RuntimeError("No free ports in range 8080-8179")

    def start(self) -> None:
        CallbackHandler.token_data_received = None
        CallbackHandler.token_event.clear()

        self.server = HTTPServer(("localhost", self.port), CallbackHandler)

        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def is_token_received(self) -> bool:
        return CallbackHandler.token_event.is_set()

    def get_token_data(self) -> Dict[str, str]:
        token_data: Optional[Dict[str, str]] = CallbackHandler.token_data_received
        if token_data is None:
            raise RuntimeError("Token not received")
        return token_data

    def get_token(self) -> str:
        """Returns access token for backward compatibility."""
        token_data = self.get_token_data()
        if "access_token" in token_data:
            return token_data["access_token"]
        raise RuntimeError("No access token found in callback data")

    def shutdown(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server = None
        self.server_thread = None

    def start_and_wait_for_callback(self, timeout: int = 300) -> Dict[str, str]:
        self.start()

        received: bool = CallbackHandler.token_event.wait(timeout)
        if not received:
            self.shutdown()
            raise TimeoutError("Auth callback timeout (5 minutes)")

        self.shutdown()
        return self.get_token_data()
