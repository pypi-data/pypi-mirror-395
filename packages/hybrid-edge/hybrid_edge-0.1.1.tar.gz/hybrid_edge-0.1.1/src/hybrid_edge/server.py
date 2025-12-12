import os
import threading
import time
import subprocess
import re
import requests
import json
import logging
from dotenv import load_dotenv

from .proxy import run_proxy
from .utils import get_binary_path

logger = logging.getLogger("hybrid_edge.server")
logging.basicConfig(level=logging.INFO)

class HybridServer:
    """
    Manages the Flask Security Guard and Cloudflare Tunnel process.
    """
    def __init__(self, gist_id: str = None, github_token: str = None, secret_key: str = None, port: int = 5000):
        load_dotenv()
        
        self.gist_id = gist_id or os.getenv("GIST_ID")
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.secret_key = secret_key or os.getenv("SECRET_KEY")
        self.port = port
        self.tunnel_process = None

        if not self.secret_key:
            raise ValueError("SECRET_KEY is required in .env or arguments.")

        # Inject for Proxy
        os.environ["SECRET_KEY"] = self.secret_key
        os.environ["FLASK_PORT"] = str(self.port)

    def _update_service_discovery(self, new_url: str):
        if not self.gist_id or not self.github_token:
            logger.warning("Discovery Config missing. Skipping Gist update.")
            return

        logger.info(f"📝 Updating Phonebook (Gist)...")
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github+json"
        }
        data = {"files": {"tunnel.json": {"content": json.dumps({"url": new_url})}}}
        
        try:
            r = requests.patch(f"https://api.github.com/gists/{self.gist_id}", headers=headers, json=data)
            if r.status_code == 200:
                logger.info("✅ Service Discovery Updated!")
            else:
                logger.error(f"Gist Update Failed: {r.status_code}")
        except Exception as e:
            logger.error(f"Error updating Gist: {e}")

    def start(self):
        """Starts the Server. Blocks until stopped."""
        logger.info(f"🚀 Initializing Hybrid Edge Server on Port {self.port}...")
        
        # 1. Start Proxy
        proxy_thread = threading.Thread(target=run_proxy, daemon=True)
        proxy_thread.start()
        time.sleep(2) 

        # 2. Start Tunnel
        bin_path = get_binary_path()
        logger.info("🚇 Opening Secure Tunnel (HTTP2)...")
        
        cmd = [bin_path, "tunnel", "--protocol", "http2", "--url", f"http://localhost:{self.port}"]
        
        try:
            self.tunnel_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                bufsize=1
            )

            url_found = False
            while True:
                line = self.tunnel_process.stdout.readline()
                if not line: break
                
                # Print logs cleanly
                print(line.strip())
                
                match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if match and not url_found:
                    public_url = match.group(0)
                    logger.info(f"🔎 PUBLIC URL: {public_url}")
                    self._update_service_discovery(public_url)
                    url_found = True

        except KeyboardInterrupt:
            logger.info("Stopping Server...")
            self.stop()

    def stop(self):
        if self.tunnel_process:
            self.tunnel_process.terminate()

def main():
    try:
        server = HybridServer()
        server.start()
    except Exception as e:
        logger.error(str(e))