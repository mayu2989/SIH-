#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway Track Monitoring System - Enhanced Track Visualization Launcher
Allows you to choose between Desktop (Tkinter) and Web (Streamlit) applications
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['tkinter', 'pandas']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"⚠️  Missing required packages: {', '.join(missing)}")
        print("🔧 Install with: pip install -r requirements.txt")
        return False
    return True

def run_tkinter_app():
    """Launch the Tkinter desktop application"""
    print("🖥️  Launching Desktop Application (Tkinter)...")
    print("🗺️  Features: Interactive maps, highlighted tracks, canvas visualization")

    try:
        subprocess.run([sys.executable, "railway_track_monitoring_tkinter.py"])
    except FileNotFoundError:
        print("❌ Error: railway_track_monitoring_tkinter.py not found!")
    except Exception as e:
        print(f"❌ Error launching desktop app: {e}")

def run_streamlit_app():
    """Launch the Streamlit web application"""
    print("🌐 Launching Web Application (Streamlit)...")
    print("🗺️  Features: Enhanced track visualization, interactive maps, real-time updates")

    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "railway_track_monitoring_streamlit.py"])
    except FileNotFoundError:
        print("❌ Error: railway_track_monitoring_streamlit.py not found!")
    except Exception as e:
        print(f"❌ Error launching web app: {e}")

def main():
    print("🚄 Railway Track Monitoring System - Enhanced Track Visualization")
    print("=" * 70)
    print("🗺️  New Feature: Highlighted railway tracks instead of point markers!")
    print("🎨 Enhanced visualization with color-coded congestion analysis")
    print("=" * 70)

    if not check_dependencies():
        return

    print("\nSelect the application you want to launch:")
    print("1. 🖥️  Desktop Application (Tkinter)")
    print("   • Interactive maps with tkintermapview")
    print("   • Canvas-based track visualization")
    print("   • Offline functionality")
    print()
    print("2. 🌐 Web Application (Streamlit)")
    print("   • Enhanced Folium maps with polylines")
    print("   • Advanced track highlighting")
    print("   • Real-time interactive dashboard")
    print()
    print("3. 🔧 Install Dependencies")
    print("4. ❌ Exit")

    while True:
        try:
            choice = input("\n🎯 Enter your choice (1-4): ").strip()

            if choice == "1":
                run_tkinter_app()
                break
            elif choice == "2":
                run_streamlit_app()
                break
            elif choice == "3":
                print("📦 Installing dependencies...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print("✅ Dependencies installed!")
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
