#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway Track Monitoring System - Dependency Installation Helper
Enhanced Track Visualization Edition
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    print("🚄 Railway Track Monitoring System - Enhanced Track Visualization")
    print("=" * 70)
    print("📦 Dependency Installation Helper")
    print("🗺️  Installing packages for highlighted track visualization")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_requirements():
    """Install packages from requirements.txt"""
    print("\n📦 Installing required packages...")

    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False

    try:
        # Upgrade pip first
        print("📈 Upgrading pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)

        # Install requirements
        print("📦 Installing packages from requirements.txt...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ All packages installed successfully!")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error during installation: {e}")
        return False

def verify_installation():
    """Verify that key packages are installed"""
    print("\n🔍 Verifying installation...")

    required_packages = [
        ("pandas", "Data handling"),
        ("streamlit", "Web application framework"),
        ("tkinter", "Desktop GUI framework"),
        ("folium", "Interactive maps"),
        ("tkintermapview", "Tkinter map widget")
    ]

    installed = []
    missing = []

    for package, description in required_packages:
        try:
            if package == "tkinter":
                import tkinter
            else:
                __import__(package)
            print(f"✅ {package:<15} - {description}")
            installed.append(package)
        except ImportError:
            print(f"❌ {package:<15} - {description} (MISSING)")
            missing.append(package)

    print(f"\n📊 Installation Summary:")
    print(f"   ✅ Installed: {len(installed)}")
    print(f"   ❌ Missing:   {len(missing)}")

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("💡 Try running: pip install -r requirements.txt")
        return False
    else:
        print("\n🎉 All required packages are installed!")
        return True

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if sys.platform != "win32":
        return

    try:
        import winshell
        from win32com.client import Dispatch

        desktop = winshell.desktop()
        path = os.path.join(desktop, "Railway Track Monitor.lnk")
        target = os.path.join(os.getcwd(), "run_application.py")
        wDir = os.getcwd()
        icon = target

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()

        print("✅ Desktop shortcut created!")
    except ImportError:
        print("💡 Install pywin32 for desktop shortcut creation")
    except Exception as e:
        print(f"⚠️  Could not create shortcut: {e}")

def main():
    print_header()

    if not check_python_version():
        input("\n❌ Press Enter to exit...")
        return

    if not install_requirements():
        print("\n❌ Installation failed. Please check your internet connection and try again.")
        input("Press Enter to exit...")
        return

    if verify_installation():
        print("\n🎯 Next Steps:")
        print("1. Run: python run_application.py")
        print("2. Or directly: python railway_track_monitoring_tkinter.py")
        print("3. Or web app: streamlit run railway_track_monitoring_streamlit.py")

        # Create shortcut on Windows
        if sys.platform == "win32":
            create_shortcut = input("\n🔗 Create desktop shortcut? (y/n): ").lower().strip()
            if create_shortcut in ['y', 'yes']:
                create_desktop_shortcut()

        print("\n🚄 Railway Track Monitoring System is ready!")
        print("🗺️  Enhanced with highlighted track visualization!")

    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
