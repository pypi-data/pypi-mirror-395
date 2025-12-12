import socket
import requests

class IP:
    @staticmethod
    def lokal():
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception as e:
            return f"Hata: {e}"

    @staticmethod
    def clop():
        try:
            return requests.get("https://api.ipify.org").text
        except Exception as e:
            return f"Hata: {e}"