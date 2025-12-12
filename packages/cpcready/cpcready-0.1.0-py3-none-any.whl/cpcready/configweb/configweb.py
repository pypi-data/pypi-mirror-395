# Copyright 2025 David CH.F (destroyer)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

import click
import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path
from cpcready.utils.click_custom import CustomCommand
from cpcready.utils.console import ok, error, blank_line, info2

@click.command(cls=CustomCommand)
def configweb():
    """Configure CPCReady options via web interface."""
    try:
        # Ruta al script de Streamlit
        script_path = Path(__file__).parent / "streamlit_app.py"
        
        blank_line(1)
        ok("Starting web configuration interface...")
        
        # Ejecutar Streamlit completamente en segundo plano (daemon)
        # Usando nohup para desacoplar del proceso padre
        if sys.platform == "win32":
            # Windows
            subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", str(script_path),
                 "--server.headless", "true",
                 "--browser.gatherUsageStats", "false"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            # Unix/Linux/macOS
            subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", str(script_path),
                 "--server.headless", "true",
                 "--browser.gatherUsageStats", "false"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                preexec_fn=os.setpgrp
            )
        
        # Esperar un poco para que Streamlit inicie
        time.sleep(2)
        
        # Abrir el navegador automáticamente
        url = "http://localhost:8501"
        webbrowser.open(url)
        
        ok(f"Web interface opened at: {url}")
        info2("Server running in background. To stop: pkill -f 'streamlit run'")
        blank_line(1)
        
    except FileNotFoundError:
        blank_line(1)
        error("Streamlit is not installed. Install it with: pip install streamlit")
        blank_line(1)
    except Exception as e:
        blank_line(1)
        error(f"Error running web interface: {e}")
        blank_line(1)
