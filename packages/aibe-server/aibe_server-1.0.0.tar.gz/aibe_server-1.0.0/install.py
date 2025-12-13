#!/usr/bin/env python3
"""
AIBE Server Installation Script
Automatically creates a virtual environment and installs the server
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def create_venv(venv_path):
    """Create a virtual environment"""
    print(f"Creating virtual environment at {venv_path}")
    venv.create(venv_path, with_pip=True)

def get_venv_python(venv_path):
    """Get the Python executable path for the virtual environment"""
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        return venv_path / "bin" / "python"

def get_venv_pip(venv_path):
    """Get the pip executable path for the virtual environment"""  
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "pip.exe"
    else:  # Unix/Linux/macOS
        return venv_path / "bin" / "pip"

def install_package(venv_path, package_path):
    """Install the package in the virtual environment"""
    pip_exe = get_venv_pip(venv_path)
    
    # Upgrade pip first
    run_command([str(pip_exe), "install", "--upgrade", "pip"])
    
    # Install the package in development mode
    run_command([str(pip_exe), "install", "-e", str(package_path)])

def create_launcher_script(venv_path, install_dir):
    """Create launcher scripts for easy execution"""
    python_exe = get_venv_python(venv_path)
    
    if os.name == 'nt':  # Windows
        launcher_path = install_dir / "aibe-server.bat"
        launcher_content = f'''@echo off
echo Starting AIBE Server...
"{python_exe}" -c "from aibe_server.main import run_server; run_server()"
'''
    else:  # Unix/Linux/macOS
        launcher_path = install_dir / "aibe-server.sh"
        launcher_content = f'''#!/bin/bash
echo "Starting AIBE Server..."
"{python_exe}" -c "from aibe_server.main import run_server; run_server()"
'''
    
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    if os.name != 'nt':
        os.chmod(launcher_path, 0o755)
    
    return launcher_path

def main():
    """Main installation process"""
    install_dir = Path.home() / ".aibe-server"
    
    print("🤖 AIBE Server Installation")
    print("=" * 40)
    print(f"Installing to: {install_dir}")
    
    # Create installation directory
    install_dir.mkdir(exist_ok=True)
    
    # Create virtual environment
    venv_path = install_dir / "venv"
    if venv_path.exists():
        print("Virtual environment already exists, using existing...")
    else:
        create_venv(venv_path)
    
    # Install the package
    current_dir = Path(__file__).parent
    install_package(venv_path, current_dir)
    
    # Create launcher script
    launcher_path = create_launcher_script(venv_path, install_dir)
    
    print("\n✅ Installation Complete!")
    print("=" * 40)
    print(f"Virtual environment: {venv_path}")
    print(f"Launcher script: {launcher_path}")
    print("\nTo start the server:")
    if os.name == 'nt':
        print(f"  {launcher_path}")
    else:
        print(f"  {launcher_path}")
        print(f"  # Or add to PATH: export PATH=\"{install_dir}:$PATH\"")
    
    print(f"\nServer will be available at: http://localhost:3001")
    print(f"Status page: http://localhost:3001/status")
    
    # Offer to start the server immediately
    response = input("\nStart the server now? (y/N): ").strip().lower()
    if response == 'y':
        python_exe = get_venv_python(venv_path)
        print("\nStarting server...")
        try:
            subprocess.run([str(python_exe), "-c", "from aibe_server.main import run_server; run_server()"])
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()