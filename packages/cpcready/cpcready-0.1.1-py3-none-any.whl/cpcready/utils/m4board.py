
# Copyright (C) 2025 David CH.F (destroyer)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# This code is inspired by and adapted from the M4Board code available at:
# https://github.com/M4Duke/cpcxfer
# created by Duke (M4Duke) and Romain Giot

import requests
import os
import socket
from pathlib import Path
from cpcready.utils.console import debug, error, warn, ok
from cpcready.utils.toml_config import ConfigManager


class M4Board:
    """M4Board communication manager."""
    
    def __init__(self, ip=None):
        """
        Initialize M4Board manager.
        
        Args:
            ip: M4Board IP address. If None, reads from config.
        """
        if ip is None:
            config = ConfigManager()
            ip = config.get("m4board", "ip", "")
            
            if not ip:
                raise ValueError("M4Board IP not configured. Edit the configuration file.")
        
        self.ip = ip
    
    def _get_url(self, path):
        """Build URL for M4Board endpoint."""
        return f"http://{self.ip}/{path}"
    
    def _get_headers(self):
        """Get default headers for requests."""
        return {"user-agent": "cpcready"}
    
    def check_connection(self, timeout=2):
        """
        Check if M4Board is reachable.
        
        Args:
            timeout: Connection timeout in seconds
            
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            # Intentar conectar al socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((self.ip, 80))
            sock.close()
            
            if result == 0:
                debug(f"M4Board connection OK: {self.ip}")
                return True
            else:
                warn(f"M4Board not reachable at {self.ip}")
                return False
                
        except socket.error as e:
            error(f"Connection error: {e}")
            return False
    
    def reset_m4(self):
        """Reset M4Board."""
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        try:
            url = self._get_url("config.cgi?mres")
            debug("Resetting M4Board")
            
            r = requests.get(url, headers=self._get_headers(), timeout=5)
            
            if r.status_code == 200:
                ok("M4Board reset successful")
                return True
            else:
                error(f"Reset failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"Reset error: {e}")
            return False
    
    def reset_cpc(self):
        """Reset CPC."""
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        try:
            url = self._get_url("config.cgi?cres")
            debug("Resetting CPC")
            
            r = requests.get(url, headers=self._get_headers(), timeout=5)
            
            if r.status_code == 200:
                ok("CPC reset successful")
                return True
            else:
                error(f"Reset failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"Reset error: {e}")
            return False
    
    def upload_file(self, file_path, destination="/", with_header=False):
        """
        Upload a file to M4Board SD card.
        
        Args:
            file_path: Local file path to upload
            destination: Destination directory on SD card
            with_header: Add AMSDOS header if True
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        file_path = Path(file_path)
        
        if not file_path.is_file():
            error(f"File not found: {file_path}")
            return False
        
        if with_header:
            error("AMSDOS header not yet implemented")
            return False
        
        try:
            debug(f"Uploading {file_path} to {destination}")
            url = self._get_url("upload.html")
            
            with open(file_path, 'rb') as f:
                files = {
                    "upfile": (
                        f"{destination}/{file_path.name}".replace("//", "/"),
                        f,
                        "application/octet-stream",
                        {'Expires': '0'}
                    )
                }
                
                r = requests.post(url, files=files, timeout=30)
            
            if r.status_code == 200:
                ok(f"File uploaded: {file_path.name}")
                return True
            else:
                error(f"Upload failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"Upload error: {e}")
            return False
    
    def download_file(self, cpc_path, local_path=None):
        """
        Download a file from M4Board SD card.
        
        Args:
            cpc_path: Path on CPC SD card
            local_path: Local destination path (default: current directory)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        try:
            debug(f"Downloading {cpc_path}")
            url = self._get_url(f"sd/{cpc_path}")
            
            r = requests.get(url, timeout=30)
            
            if r.status_code == 200:
                if local_path is None:
                    local_path = os.path.basename(cpc_path)
                
                with open(local_path, 'wb') as f:
                    f.write(r.content)
                
                ok(f"File downloaded: {local_path}")
                return True
            else:
                error(f"Download failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"Download error: {e}")
            return False
    
    def execute(self, cpc_file):
        """
        Execute a file on CPC.
        
        Args:
            cpc_file: File path on CPC SD card
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        try:
            debug(f"Executing {cpc_file}")
            url = self._get_url("config.cgi")
            
            r = requests.get(url, params={"run2": cpc_file}, timeout=5)
            
            if r.status_code == 200:
                ok(f"Executing: {cpc_file}")
                return True
            else:
                error(f"Execute failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"Execute error: {e}")
            return False
    
    def mkdir(self, folder):
        """
        Create directory on M4Board SD card.
        
        Args:
            folder: Directory path to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        if not folder.startswith("/"):
            folder = "/" + folder
        
        try:
            debug(f"Creating directory {folder}")
            url = self._get_url("config.cgi")
            
            r = requests.get(
                url,
                params={"mkdir": folder},
                headers=self._get_headers(),
                timeout=5
            )
            
            if r.status_code == 200:
                ok(f"Directory created: {folder}")
                return True
            else:
                error(f"mkdir failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"mkdir error: {e}")
            return False
    
    def cd(self, folder):
        """
        Change current directory on CPC.
        
        Args:
            folder: Directory path
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        try:
            url = self._get_url("config.cgi")
            r = requests.get(url, params={"cd": folder}, timeout=5)
            
            if r.status_code == 200:
                debug(f"Changed directory to: {folder}")
                return True
            else:
                error(f"cd failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"cd error: {e}")
            return False
    
    def rm(self, cpc_file):
        """
        Remove file or empty directory on CPC.
        
        Args:
            cpc_file: File or directory to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        try:
            url = self._get_url("config.cgi")
            r = requests.get(url, params={"rm": cpc_file}, timeout=5)
            
            if r.status_code == 200:
                ok(f"Removed: {cpc_file}")
                return True
            else:
                error(f"rm failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"rm error: {e}")
            return False
    
    def pause(self):
        """
        Pause CPC execution.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return False
        
        try:
            url = self._get_url("config.cgi")
            r = requests.get(url, params={"chlt": "CPC+Pause"}, timeout=5)
            
            if r.status_code == 200:
                ok("CPC paused")
                return True
            else:
                error(f"pause failed with status {r.status_code}")
                return False
                
        except requests.RequestException as e:
            error(f"pause error: {e}")
            return False
    
    def ls(self, folder=""):
        """
        List files in directory on CPC.
        
        Args:
            folder: Directory to list (default: current)
            
        Returns:
            str: Directory listing or None if failed
        """
        if not self.check_connection():
            error("Cannot connect to M4Board")
            return None
        
        try:
            url = self._get_url("config.cgi")
            r = requests.get(url, params={"ls": folder}, timeout=5)
            
            if r.status_code != 200:
                error(f"ls failed with status {r.status_code}")
                return None
            
            # Obtener el archivo de directorio
            url = self._get_url("sd/m4/dir.txt")
            r = requests.get(url, timeout=5)
            
            if r.status_code == 200:
                return r.text
            else:
                error(f"Failed to read directory listing")
                return None
                
        except requests.RequestException as e:
            error(f"ls error: {e}")
            return None
