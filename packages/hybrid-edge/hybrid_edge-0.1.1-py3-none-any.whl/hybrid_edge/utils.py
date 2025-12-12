import os
import platform
import requests
import stat
import sys

def get_binary_path():
    """Returns the path to the cloudflared binary, downloading it if missing."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Determine binary name and URL based on OS
    if system == 'windows':
        binary_name = "cloudflared.exe"
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    elif system == 'linux':
        binary_name = "cloudflared"
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    elif system == 'darwin': # MacOS
        binary_name = "cloudflared"
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64"
    else:
        raise OSError(f"Unsupported OS: {system}")

    # Path to store binary (inside the package folder)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bin_path = os.path.join(base_dir, binary_name)

    if os.path.exists(bin_path):
        return bin_path

    print(f"⬇️ Cloudflared not found. Downloading for {system}...")
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(bin_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Make executable on Unix/Mac
        if system != 'windows':
            st = os.stat(bin_path)
            os.chmod(bin_path, st.st_mode | stat.S_IEXEC)
            
        print(f"✅ Downloaded to: {bin_path}")
        return bin_path
    except Exception as e:
        print(f"❌ Failed to download cloudflared: {e}")
        sys.exit(1)