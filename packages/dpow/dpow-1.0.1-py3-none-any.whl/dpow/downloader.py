import requests
import platform
import sys
import os
import hashlib
from pathlib import Path
import tempfile

def get_current_platform_info():
    """
    Dynamically detect OS and architecture with Android support.
    Returns dict with 'platform' and 'architecture' keys.
    """
    system = platform.system().lower()
    
    # Detect OS
    if hasattr(sys, 'getandroidapilevel') or 'ANDROID_ROOT' in os.environ:
        os_name = "android"
    elif system == "darwin":
        os_name = "macos"
    elif system == "windows":
        os_name = "windows"
    elif system == "linux":
        if os.path.exists('/system/build.prop'):
            os_name = "android"
        else:
            os_name = "linux"
    else:
        os_name = system
    
    # Detect architecture
    machine = platform.machine().lower()
    
    # Architecture mapping
    if machine in ("x86_64", "amd64", "x64"):
        arch = "64"
    elif machine in ("x86", "i386", "i686", "i586"):
        if os_name == "android":
            arch = "x86"
        else:
            arch = "32"
    elif machine in ("arm64", "aarch64", "armv8", "armv8l"):
        arch = "arm64"
    elif machine in ("armv7", "armv7l", "armv7a"):
        arch = "armv7"
    elif machine in ("armv6", "armv6l"):
        arch = "armv6"
    else:
        arch = machine
    
    # Special case: Android x86_64 uses "x86_64" key
    if os_name == "android" and arch == "64":
        arch = "x86_64"
    
    return {
        "platform": os_name,
        "architecture": arch,
        "raw_system": platform.system(),
        "raw_machine": platform.machine()
    }


def fetch_binaries_data():
    """Fetch binary metadata from GitHub."""
    url = "https://github.com/QudsLab/Proof-of-work/raw/refs/heads/main/bin/binaries.json"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Error fetching binary data: {e}")
        return None


def calculate_md5(filepath):
    """Calculate MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def download_file(url, destination, expected_md5=None):
    """Download a file and optionally verify its MD5 hash."""
    try:
        print(f"[INFO] Downloading: {url}")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # if total_size:
                    #     progress = (downloaded / total_size) * 100
                    #     print(f"\r   Progress: {progress:.1f}%", end='', flush=True)
        
        print(f"   Saved to: {destination}")
        
        # Verify MD5 if provided
        if expected_md5:
            # print(f"[INFO] Verifying MD5 hash...")
            actual_md5 = calculate_md5(destination)
            if actual_md5.lower() == expected_md5.lower():
                # print(f"[OK] MD5 verified: {actual_md5}")
                pass
            else:
                print(f"[ERROR] MD5 mismatch!")
                print(f"   Expected: {expected_md5}")
                print(f"   Got:      {actual_md5}")
                os.remove(destination)
                return False
        
        return True
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        if os.path.exists(destination):
            os.remove(destination)
        return False


def get_binary_path(binary_type='client'):
    """
    Get the path to the binary, downloading it if necessary.
    binary_type: 'client' or 'server'
    """
    package_dir = Path(__file__).parent
    # Check if binary exists in package directory (e.g. installed from wheel with binaries)
    local_bin_dir = package_dir / "bin"
    
    platform_info = get_current_platform_info()
    os_name = platform_info['platform']
    
    # Determine expected filename
    filename = "unknown"
    if os_name == "windows":
        filename = f"{binary_type}.dll"
    elif os_name == "macos":
        filename = f"lib{binary_type}.dylib"
    else: # linux/android
        filename = f"lib{binary_type}.so"
    
    # 1. Check local package bin directory
    local_destination = local_bin_dir / filename
    if local_destination.exists():
        return str(local_destination)

    # 2. If not found locally, use temp directory
    temp_dir = Path(tempfile.gettempdir()) / "dpow_bin"
    temp_dir.mkdir(parents=True, exist_ok=True)
    destination = temp_dir / filename
    
    # If exists, return path (maybe verify hash too? for now just check existence to be fast)
    if destination.exists():
        return str(destination)
        
    # If not exists, try to download
    print(f"Binary {binary_type} not found at {destination}. Attempting to download...")
    return download_specific_binary(binary_type, destination, platform_info)

def download_specific_binary(binary_type, destination, platform_info):
    data = fetch_binaries_data()
    if not data:
        raise RuntimeError("Failed to fetch binary metadata")
        
    os_name = platform_info['platform']
    arch = platform_info['architecture']
    
    platforms = data.get('platforms', {})
    if os_name not in platforms:
        raise RuntimeError(f"Platform '{os_name}' not supported for binaries")
        
    architectures = platforms[os_name]
    if arch not in architectures:
        raise RuntimeError(f"Architecture '{arch}' not supported on '{os_name}'")
        
    binaries = architectures[arch]
    if binary_type not in binaries:
        raise RuntimeError(f"Binary type '{binary_type}' not found for {os_name}/{arch}")
        
    bin_info_list = binaries[binary_type]
    if not bin_info_list:
        raise RuntimeError(f"No binary info for {binary_type}")
        
    bin_data = bin_info_list[0]
    url = bin_data.get('url')
    md5_hash = bin_data.get('hashes', {}).get('md5')
    
    if download_file(url, destination, md5_hash):
        return str(destination)
    else:
        raise RuntimeError(f"Failed to download {binary_type} binary")

def ensure_binaries():
    """Ensure both client and server binaries are present."""
    get_binary_path('client')
    get_binary_path('server')

if __name__ == "__main__":
    ensure_binaries()
