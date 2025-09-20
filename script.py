# Now I'll create the complete Railway Track Monitoring System with highlighted tracks instead of markers
import os
import zipfile

# Create project directory
project_dir = "Railway_Track_Monitoring_System"
if os.path.exists(project_dir):
    import shutil
    shutil.rmtree(project_dir)
os.makedirs(project_dir)
os.makedirs(os.path.join(project_dir, "data"))

print(f"✅ Created project directory: {project_dir}")

# 1. Updated Tkinter Application with Highlighted Tracks
tkinter_code = '''import tkinter as tk
from tkinter import ttk, messagebox, canvas
import random
import datetime
import math

# Try to import tkintermapview for map functionality
try:
    import tkintermapview
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

class RailwayTrackMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Railway Track Monitoring System - Enhanced with Track Visualization")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        # Initialize mock data with route coordinates
        self.initialize_mock_data()
        
        # Create main container
        self.create_main_container()
        
        # Create navigation buttons
        self.create_navigation()
        
        # Create content area
        self.create_content_area()
        
        # Show default section
        self.show_live_tracks()
        
    def initialize_mock_data(self):
        """Initialize mock data for the railway system with route coordinates"""
        self.tracks_data = {
            'live_tracks': [
                {
                    'track_id': 'T001', 'route': 'Delhi-Mumbai', 'train': 'Rajdhani Express', 
                    'status': 'Running', 'speed': '110 km/h', 'location': 'Kilometer 250',
                    'route_coords': [(28.7041, 77.1025), (21.7679, 78.8718), (19.0760, 72.8777)]
                },
                {
                    'track_id': 'T002', 'route': 'Chennai-Kolkata', 'train': 'Coromandel Express', 
                    'status': 'Running', 'speed': '95 km/h', 'location': 'Kilometer 180',
                    'route_coords': [(13.0827, 80.2707), (17.3850, 78.4867), (22.5726, 88.3639)]
                },
                {
                    'track_id': 'T003', 'route': 'Bangalore-Delhi', 'train': 'Karnataka Express', 
                    'status': 'Running', 'speed': '120 km/h', 'location': 'Kilometer 320',
                    'route_coords': [(12.9716, 77.5946), (17.3850, 78.4867), (28.7041, 77.1025)]
                },
                {
                    'track_id': 'T005', 'route': 'Mumbai-Chennai', 'train': 'Chennai Express', 
                    'status': 'Running', 'speed': '105 km/h', 'location': 'Kilometer 145',
                    'route_coords': [(19.0760, 72.8777), (15.2993, 74.1240), (13.0827, 80.2707)]
                }
            ],
            'congested_tracks': [
                {
                    'track_id': 'T004', 'route': 'Mumbai-Pune', 'congestion_level': 'High', 
                    'trains_count': 8, 'delay': '45 min', 'severity': 'high',
                    'route_coords': [(19.0760, 72.8777), (18.5204, 73.8567)]
                },
                {
                    'track_id': 'T007', 'route': 'Delhi-Jaipur', 'congestion_level': 'Medium', 
                    'trains_count': 5, 'delay': '20 min', 'severity': 'medium',
                    'route_coords': [(28.7041, 77.1025), (26.9124, 75.7873)]
                },
                {
                    'track_id': 'T012', 'route': 'Kolkata-Bhubaneswar', 'congestion_level': 'High', 
                    'trains_count': 7, 'delay': '35 min', 'severity': 'high',
                    'route_coords': [(22.5726, 88.3639), (20.2961, 85.8245)]
                },
                {
                    'track_id': 'T018', 'route': 'Bangalore-Mysore', 'congestion_level': 'Medium', 
                    'trains_count': 4, 'delay': '15 min', 'severity': 'medium',
                    'route_coords': [(12.9716, 77.5946), (12.2958, 76.6394)]
                }
            ],
            'blocked_tracks': [
                {
                    'track_id': 'T008', 'route': 'Hyderabad-Vijayawada', 'reason': 'Maintenance Work', 
                    'estimated_clearance': '2 hours',
                    'route_coords': [(17.3850, 78.4867), (16.5062, 80.6480)]
                },
                {
                    'track_id': 'T015', 'route': 'Ahmedabad-Rajkot', 'reason': 'Signal Failure', 
                    'estimated_clearance': '30 min',
                    'route_coords': [(23.0225, 72.5714), (22.3039, 70.8022)]
                },
                {
                    'track_id': 'T022', 'route': 'Pune-Nashik', 'reason': 'Track Repair', 
                    'estimated_clearance': '4 hours',
                    'route_coords': [(18.5204, 73.8567), (19.9975, 73.7898)]
                }
            ],
            'free_tracks': [
                {
                    'track_id': 'T020', 'route': 'Lucknow-Kanpur', 'capacity': '100%', 
                    'next_scheduled': '14:30',
                    'route_coords': [(26.8467, 80.9462), (26.4499, 80.3319)]
                },
                {
                    'track_id': 'T025', 'route': 'Surat-Vadodara', 'capacity': '100%', 
                    'next_scheduled': '16:45',
                    'route_coords': [(21.1702, 72.8311), (22.3072, 73.1812)]
                },
                {
                    'track_id': 'T030', 'route': 'Indore-Bhopal', 'capacity': '100%', 
                    'next_scheduled': '18:20',
                    'route_coords': [(22.7196, 75.8577), (23.2599, 77.4126)]
                },
                {
                    'track_id': 'T035', 'route': 'Jaipur-Udaipur', 'capacity': '100%', 
                    'next_scheduled': '19:15',
                    'route_coords': [(26.9124, 75.7873), (24.5854, 73.7125)]
                }
            ]
        }
        
        self.ai_recommendations = [
            "Reroute 2 trains from T004 to alternate tracks T021 and T022",
            "Implement dynamic scheduling to reduce peak hour congestion",
            "Use predictive maintenance to prevent signal failures",
            "Optimize train speeds during congested periods to improve flow"
        ]

    def create_main_container(self):
        """Create the main container frame"""
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_navigation(self):
        """Create navigation buttons including Railway Map"""
        nav_frame = tk.Frame(self.main_frame, bg="#34495e", height=60)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        nav_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(nav_frame, text="🚄 Railway Track Monitoring System - Track Visualization", 
                              font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#34495e")
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Navigation buttons
        button_frame = tk.Frame(nav_frame, bg="#34495e")
        button_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        buttons = [
            ("🚄 Live Tracks", self.show_live_tracks, "#3498db"),
            ("⚠️ Congested Tracks", self.show_congested_tracks, "#e74c3c"),
            ("🗺️ Railway Map", self.show_railway_map, "#f39c12"),
            ("🚫 Blocked Tracks", self.show_blocked_tracks, "#95a5a6"),
            ("✅ Free Tracks", self.show_free_tracks, "#27ae60")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                           bg=color, fg="white", font=("Arial", 9, "bold"),
                           padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=3)

    def create_content_area(self):
        """Create the content area"""
        self.content_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_railway_map(self):
        """Display railway map section with highlighted track visualization"""
        self.clear_content()
        
        # Header
        header = tk.Label(self.content_frame, text="🗺️ Railway Network Map - Highlighted Track Visualization", 
                         font=("Arial", 20, "bold"), fg="#f39c12", bg="#ecf0f1")
        header.pack(pady=20)
        
        if MAP_AVAILABLE:
            # Create interactive map widget with polylines
            self.create_interactive_map_with_tracks()
        else:
            # Fallback to Canvas-based track visualization
            self.create_canvas_track_map()
        
    def create_interactive_map_with_tracks(self):
        """Create interactive map using tkintermapview with highlighted tracks"""
        # Control buttons
        control_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        control_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(control_frame, text="🎛️ Track Visualization Controls:", font=("Arial", 12, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(control_frame, text="🔄 Refresh Tracks", 
                               command=self.refresh_track_data,
                               bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                               padx=15, pady=5, cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        center_btn = tk.Button(control_frame, text="📍 Center View", 
                              command=self.center_map,
                              bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                              padx=15, pady=5, cursor="hand2")
        center_btn.pack(side=tk.LEFT, padx=5)
        
        toggle_btn = tk.Button(control_frame, text="🎨 Toggle View", 
                              command=self.toggle_track_view,
                              bg="#9b59b6", fg="white", font=("Arial", 10, "bold"),
                              padx=15, pady=5, cursor="hand2")
        toggle_btn.pack(side=tk.LEFT, padx=5)
        
        # Map container
        map_frame = tk.Frame(self.content_frame, bg="#ecf0f1", relief=tk.RIDGE, bd=2)
        map_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Map widget
        self.map_widget = tkintermapview.TkinterMapView(map_frame, width=1000, height=450)
        self.map_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Set center of India
        self.map_widget.set_position(20.5937, 78.9629)  # Center of India
        self.map_widget.set_zoom(5)
        
        # Draw highlighted tracks instead of markers
        self.draw_highlighted_tracks()
        
        # Enhanced Legend
        self.create_enhanced_track_legend(map_frame)
    
    def draw_highlighted_tracks(self):
        """Draw highlighted track lines with different colors based on status"""
        try:
            # Clear existing paths/markers
            try:
                self.map_widget.delete_all_marker()
                self.map_widget.delete_all_path()
            except:
                pass
            
            # Draw congested tracks (RED for high, ORANGE for medium)
            for track in self.tracks_data['congested_tracks']:
                color = "#dc3545" if track['severity'] == 'high' else "#fd7e14"
                if 'route_coords' in track and len(track['route_coords']) >= 2:
                    try:
                        path = self.map_widget.set_path(
                            track['route_coords'],
                            color=color,
                            width=8
                        )
                        # Add tooltip info
                        for i, coord in enumerate(track['route_coords']):
                            if i == len(track['route_coords']) // 2:  # Middle point
                                marker = self.map_widget.set_marker(
                                    coord[0], coord[1],
                                    text=f"⚠️ {track['track_id']}: {track['route']}\\nCongestion: {track['congestion_level']}\\nDelay: {track['delay']}",
                                    marker_color_circle=color,
                                    marker_color_outside=color
                                )
                    except Exception as e:
                        print(f"Error drawing congested track {track['track_id']}: {e}")
            
            # Draw live tracks (GREEN)
            for track in self.tracks_data['live_tracks']:
                color = "#28a745"
                if 'route_coords' in track and len(track['route_coords']) >= 2:
                    try:
                        path = self.map_widget.set_path(
                            track['route_coords'],
                            color=color,
                            width=6
                        )
                        # Add tooltip info
                        for i, coord in enumerate(track['route_coords']):
                            if i == len(track['route_coords']) // 2:  # Middle point
                                marker = self.map_widget.set_marker(
                                    coord[0], coord[1],
                                    text=f"🚄 {track['track_id']}: {track['route']}\\nTrain: {track['train']}\\nSpeed: {track['speed']}",
                                    marker_color_circle=color,
                                    marker_color_outside=color
                                )
                    except Exception as e:
                        print(f"Error drawing live track {track['track_id']}: {e}")
            
            # Draw blocked tracks (GRAY, dashed style simulated with thicker line)
            for track in self.tracks_data['blocked_tracks']:
                color = "#6c757d"
                if 'route_coords' in track and len(track['route_coords']) >= 2:
                    try:
                        path = self.map_widget.set_path(
                            track['route_coords'],
                            color=color,
                            width=7
                        )
                        # Add tooltip info
                        for i, coord in enumerate(track['route_coords']):
                            if i == len(track['route_coords']) // 2:  # Middle point
                                marker = self.map_widget.set_marker(
                                    coord[0], coord[1],
                                    text=f"🚫 {track['track_id']}: {track['route']}\\nReason: {track['reason']}\\nClearance: {track['estimated_clearance']}",
                                    marker_color_circle=color,
                                    marker_color_outside=color
                                )
                    except Exception as e:
                        print(f"Error drawing blocked track {track['track_id']}: {e}")
            
            # Draw free tracks (BLUE, semi-transparent)
            for track in self.tracks_data['free_tracks']:
                color = "#007bff"
                if 'route_coords' in track and len(track['route_coords']) >= 2:
                    try:
                        path = self.map_widget.set_path(
                            track['route_coords'],
                            color=color,
                            width=5
                        )
                        # Add tooltip info
                        for i, coord in enumerate(track['route_coords']):
                            if i == len(track['route_coords']) // 2:  # Middle point
                                marker = self.map_widget.set_marker(
                                    coord[0], coord[1],
                                    text=f"✅ {track['track_id']}: {track['route']}\\nCapacity: {track['capacity']}\\nNext: {track['next_scheduled']}",
                                    marker_color_circle=color,
                                    marker_color_outside=color
                                )
                    except Exception as e:
                        print(f"Error drawing free track {track['track_id']}: {e}")
                        
        except Exception as e:
            print(f"Error in draw_highlighted_tracks: {e}")
            messagebox.showwarning("Map Error", f"Error drawing tracks: {e}")
    
    def create_canvas_track_map(self):
        """Create Canvas-based track visualization when tkintermapview is not available"""
        # Installation message
        install_frame = tk.Frame(self.content_frame, bg="#fff3cd", relief=tk.RIDGE, bd=2)
        install_frame.pack(fill=tk.X, padx=20, pady=10)
        
        install_label = tk.Label(install_frame, 
                              text="📦 For interactive maps, install: pip install tkintermapview",
                              font=("Arial", 12, "bold"), fg="#856404", bg="#fff3cd")
        install_label.pack(pady=15)
        
        # Canvas-based track visualization
        canvas_frame = tk.Frame(self.content_frame, bg="#f8f9fa", relief=tk.RIDGE, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create canvas
        self.track_canvas = tk.Canvas(canvas_frame, bg="#f0f8ff", height=450)
        self.track_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Draw schematic railway network
        self.draw_schematic_tracks()
        
        # Canvas legend
        self.create_canvas_track_legend(canvas_frame)
    
    def draw_schematic_tracks(self):
        """Draw schematic railway tracks on canvas"""
        # Clear canvas
        self.track_canvas.delete("all")
        
        # Canvas dimensions
        canvas_width = 1000
        canvas_height = 430
        
        # Draw title
        self.track_canvas.create_text(canvas_width//2, 30, text="🗺️ Railway Network - Track Status Visualization", 
                                     font=("Arial", 16, "bold"), fill="#2c3e50")
        
        # Define track segments with coordinates (simplified schematic)
        track_segments = [
            # Congested tracks (RED/ORANGE)
            {"name": "Mumbai-Pune (HIGH)", "coords": [(100, 200), (200, 180)], "color": "#dc3545", "width": 8, "type": "🔴"},
            {"name": "Delhi-Jaipur (MED)", "coords": [(300, 120), (400, 140)], "color": "#fd7e14", "width": 6, "type": "🟠"},
            {"name": "Kolkata-Bhubaneswar (HIGH)", "coords": [(700, 150), (800, 130)], "color": "#dc3545", "width": 8, "type": "🔴"},
            {"name": "Bangalore-Mysore (MED)", "coords": [(200, 350), (300, 330)], "color": "#fd7e14", "width": 6, "type": "🟠"},
            
            # Live tracks (GREEN)
            {"name": "Delhi-Mumbai", "coords": [(300, 120), (100, 200)], "color": "#28a745", "width": 5, "type": "🟢"},
            {"name": "Chennai-Kolkata", "coords": [(400, 380), (700, 150)], "color": "#28a745", "width": 5, "type": "🟢"},
            {"name": "Bangalore-Delhi", "coords": [(200, 350), (300, 120)], "color": "#28a745", "width": 5, "type": "🟢"},
            {"name": "Mumbai-Chennai", "coords": [(100, 200), (400, 380)], "color": "#28a745", "width": 5, "type": "🟢"},
            
            # Blocked tracks (GRAY, dashed)
            {"name": "Hyderabad-Vijayawada", "coords": [(500, 280), (600, 260)], "color": "#6c757d", "width": 6, "type": "🚫", "dash": True},
            {"name": "Ahmedabad-Rajkot", "coords": [(150, 250), (250, 270)], "color": "#6c757d", "width": 6, "type": "🚫", "dash": True},
            {"name": "Pune-Nashik", "coords": [(200, 180), (180, 150)], "color": "#6c757d", "width": 6, "type": "🚫", "dash": True},
            
            # Free tracks (BLUE)
            {"name": "Lucknow-Kanpur", "coords": [(550, 180), (650, 190)], "color": "#007bff", "width": 4, "type": "✅"},
            {"name": "Surat-Vadodara", "coords": [(120, 240), (170, 220)], "color": "#007bff", "width": 4, "type": "✅"},
            {"name": "Indore-Bhopal", "coords": [(400, 220), (500, 200)], "color": "#007bff", "width": 4, "type": "✅"},
            {"name": "Jaipur-Udaipur", "coords": [(400, 140), (350, 200)], "color": "#007bff", "width": 4, "type": "✅"}
        ]
        
        # Draw track segments
        for segment in track_segments:
            coords = segment["coords"]
            if len(coords) >= 2:
                # Flatten coordinates for canvas
                flat_coords = []
                for coord in coords:
                    flat_coords.extend(coord)
                
                # Draw line
                if segment.get("dash", False):
                    self.track_canvas.create_line(flat_coords, fill=segment["color"], width=segment["width"], 
                                                 dash=(10, 5), capstyle=tk.ROUND)
                else:
                    self.track_canvas.create_line(flat_coords, fill=segment["color"], width=segment["width"], 
                                                 capstyle=tk.ROUND)
                
                # Add label
                mid_x = sum(coord[0] for coord in coords) // len(coords)
                mid_y = sum(coord[1] for coord in coords) // len(coords) - 15
                self.track_canvas.create_text(mid_x, mid_y, text=f"{segment['type']} {segment['name']}", 
                                            font=("Arial", 8, "bold"), fill=segment["color"])
        
        # Add major cities
        cities = [
            {"name": "Delhi", "pos": (300, 120), "color": "#2c3e50"},
            {"name": "Mumbai", "pos": (100, 200), "color": "#2c3e50"},
            {"name": "Chennai", "pos": (400, 380), "color": "#2c3e50"},
            {"name": "Kolkata", "pos": (700, 150), "color": "#2c3e50"},
            {"name": "Bangalore", "pos": (200, 350), "color": "#2c3e50"},
            {"name": "Hyderabad", "pos": (500, 280), "color": "#2c3e50"}
        ]
        
        for city in cities:
            x, y = city["pos"]
            # Draw city circle
            self.track_canvas.create_oval(x-8, y-8, x+8, y+8, fill="#34495e", outline="#2c3e50", width=2)
            # City name
            self.track_canvas.create_text(x, y+20, text=city["name"], font=("Arial", 9, "bold"), fill=city["color"])
    
    def create_enhanced_track_legend(self, parent):
        """Create enhanced legend for track visualization"""
        legend_frame = tk.Frame(parent, bg="#ffffff", relief=tk.RIDGE, bd=2)
        legend_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Legend title
        title_label = tk.Label(legend_frame, text="🗺️ Railway Track Status Legend", 
                              font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50")
        title_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Legend items with track visualization
        legend_items = [
            ("🔴 High Congestion Tracks - Critical delays (8px width)", "#dc3545"),
            ("🟠 Medium Congestion Tracks - Moderate delays (6px width)", "#fd7e14"), 
            ("🟢 Live Tracks - Normal operations (5px width)", "#28a745"),
            ("🚫 Blocked Tracks - Maintenance/Emergency (dashed)", "#6c757d"),
            ("✅ Free Tracks - Available for scheduling (4px width)", "#007bff")
        ]
        
        for item, color in legend_items:
            item_frame = tk.Frame(legend_frame, bg="#ffffff")
            item_frame.pack(anchor=tk.W, padx=15)
            tk.Label(item_frame, text=f"━━ {item}", font=("Arial", 9), 
                    bg="#ffffff", fg=color).pack(side=tk.LEFT, pady=1)
    
    def create_canvas_track_legend(self, parent):
        """Create legend for canvas-based track visualization"""
        legend_frame = tk.Frame(parent, bg="#ffffff", relief=tk.RIDGE, bd=2)
        legend_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Legend title
        title_label = tk.Label(legend_frame, text="🗺️ Schematic Railway Network Legend", 
                              font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50")
        title_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Legend items
        legend_items = [
            ("🔴 High Congestion - Thick red lines", "#dc3545"),
            ("🟠 Medium Congestion - Orange lines", "#fd7e14"), 
            ("🟢 Live Tracks - Green lines", "#28a745"),
            ("🚫 Blocked Tracks - Dashed gray lines", "#6c757d"),
            ("✅ Free Tracks - Blue lines", "#007bff"),
            ("● Major Railway Stations", "#34495e")
        ]
        
        for item, color in legend_items:
            item_frame = tk.Frame(legend_frame, bg="#ffffff")
            item_frame.pack(anchor=tk.W, padx=15)
            tk.Label(item_frame, text=f"• {item}", font=("Arial", 9), 
                    bg="#ffffff", fg=color).pack(side=tk.LEFT, pady=1)
    
    def refresh_track_data(self):
        """Refresh track visualization with updated data"""
        if MAP_AVAILABLE and hasattr(self, 'map_widget'):
            self.draw_highlighted_tracks()
        elif hasattr(self, 'track_canvas'):
            self.draw_schematic_tracks()
        messagebox.showinfo("Tracks Refreshed", "Railway track visualization has been updated with latest information!")
    
    def center_map(self):
        """Center map view on India"""
        if MAP_AVAILABLE and hasattr(self, 'map_widget'):
            self.map_widget.set_position(20.5937, 78.9629)
            self.map_widget.set_zoom(5)
    
    def toggle_track_view(self):
        """Toggle between different track visualization modes"""
        messagebox.showinfo("View Toggle", "Switching between detailed and simplified track view...")
        self.refresh_track_data()

    # Keep all other existing methods (show_live_tracks, show_congested_tracks, etc.)
    def show_live_tracks(self):
        """Display live railway tracks section"""
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="🚄 Live Railway Tracks", 
                         font=("Arial", 20, "bold"), fg="#2c3e50", bg="#ecf0f1")
        header.pack(pady=20)
        
        columns = ("Track ID", "Route", "Train", "Status", "Speed", "Current Location")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor=tk.CENTER)
        
        for track in self.tracks_data['live_tracks']:
            tree.insert("", tk.END, values=(
                track['track_id'], track['route'], track['train'], 
                track['status'], track['speed'], track['location']
            ))
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, pady=20, padx=(20, 0), fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))
        
        button_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        button_frame.pack(side=tk.BOTTOM, pady=10)
        
        refresh_btn = tk.Button(button_frame, text="🔄 Refresh Data", 
                               command=self.refresh_live_data,
                               bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                               padx=20, pady=10, cursor="hand2")
        refresh_btn.pack(pady=10)

    def show_congested_tracks(self):
        """Display congested tracks section with AI recommendations"""
        self.clear_content()
        
        canvas = tk.Canvas(self.content_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        header = tk.Label(scrollable_frame, text="⚠️ Congested Railway Tracks", 
                         font=("Arial", 20, "bold"), fg="#e74c3c", bg="#ecf0f1")
        header.pack(pady=(20, 10))
        
        columns = ("Track ID", "Route", "Congestion Level", "Trains Count", "Average Delay")
        tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor=tk.CENTER)
        
        for track in self.tracks_data['congested_tracks']:
            tree.insert("", tk.END, values=(
                track['track_id'], track['route'], track['congestion_level'], 
                track['trains_count'], track['delay']
            ))
        
        tree.pack(pady=(0, 20), padx=20, fill=tk.X)
        
        # AI Recommendations subsection
        ai_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief=tk.RIDGE, bd=2)
        ai_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 20), padx=20)
        
        ai_header = tk.Label(ai_frame, text="🤖 AI Recommendations to Reduce Congestion", 
                            font=("Arial", 16, "bold"), fg="#8e44ad", bg="#f8f9fa")
        ai_header.pack(pady=15)
        
        for i, recommendation in enumerate(self.ai_recommendations, 1):
            rec_frame = tk.Frame(ai_frame, bg="#ffffff", relief=tk.FLAT, bd=1)
            rec_frame.pack(fill=tk.X, padx=20, pady=5)
            
            rec_label = tk.Label(rec_frame, text=f"{i}. {recommendation}", 
                                font=("Arial", 11), fg="#2c3e50", bg="#ffffff",
                                wraplength=800, justify=tk.LEFT)
            rec_label.pack(pady=10, padx=15, anchor=tk.W)
        
        apply_btn = tk.Button(ai_frame, text="📊 Generate New Recommendations", 
                             command=self.generate_ai_recommendations,
                             bg="#8e44ad", fg="white", font=("Arial", 12, "bold"),
                             padx=20, pady=10, cursor="hand2")
        apply_btn.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_blocked_tracks(self):
        """Display blocked tracks section"""
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="🚫 Blocked Railway Tracks", 
                         font=("Arial", 20, "bold"), fg="#95a5a6", bg="#ecf0f1")
        header.pack(pady=20)
        
        columns = ("Track ID", "Route", "Blocking Reason", "Estimated Clearance")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=250, anchor=tk.CENTER)
        
        for track in self.tracks_data['blocked_tracks']:
            tree.insert("", tk.END, values=(
                track['track_id'], track['route'], track['reason'], 
                track['estimated_clearance']
            ))
        
        tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        emergency_btn = tk.Button(self.content_frame, text="🚨 Emergency Clear Protocol", 
                                 command=self.emergency_clear,
                                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                                 padx=20, pady=10, cursor="hand2")
        emergency_btn.pack(pady=10)

    def show_free_tracks(self):
        """Display free tracks section"""
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="✅ Free Railway Tracks", 
                         font=("Arial", 20, "bold"), fg="#27ae60", bg="#ecf0f1")
        header.pack(pady=20)
        
        columns = ("Track ID", "Route", "Capacity Available", "Next Scheduled Train")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=250, anchor=tk.CENTER)
        
        for track in self.tracks_data['free_tracks']:
            tree.insert("", tk.END, values=(
                track['track_id'], track['route'], track['capacity'], 
                track['next_scheduled']
            ))
        
        tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        schedule_btn = tk.Button(self.content_frame, text="🚂 Schedule New Train", 
                               command=self.schedule_train,
                               bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                               padx=20, pady=10, cursor="hand2")
        schedule_btn.pack(pady=10)

    def refresh_live_data(self):
        """Simulate refreshing live data"""
        for track in self.tracks_data['live_tracks']:
            track['speed'] = f"{random.randint(80, 130)} km/h"
            track['location'] = f"Kilometer {random.randint(100, 400)}"
        
        messagebox.showinfo("Data Refreshed", "Live track data has been updated!")
        self.show_live_tracks()

    def generate_ai_recommendations(self):
        """Generate new AI recommendations"""
        new_recommendations = [
            "Implement automated traffic control system for peak hours",
            "Use machine learning to predict congestion patterns",
            "Deploy additional signaling systems on high-traffic routes",
            "Consider alternative routing for freight trains during rush hours",
            "Upgrade infrastructure on frequently congested tracks",
            "Implement train platooning to reduce headway distances",
            "Use dynamic pricing to distribute passenger load across time slots"
        ]
        
        self.ai_recommendations = random.sample(new_recommendations, 4)
        messagebox.showinfo("AI Analysis Complete", "New recommendations generated based on current traffic patterns!")
        self.show_congested_tracks()

    def emergency_clear(self):
        """Simulate emergency clear protocol"""
        messagebox.showwarning("Emergency Protocol", 
                              "Emergency clear protocol initiated!\\n\\n"
                              "• All maintenance teams have been notified\\n"
                              "• Alternative routes are being prepared\\n"
                              "• Emergency services are on standby")

    def schedule_train(self):
        """Simulate scheduling a new train"""
        messagebox.showinfo("Schedule Train", 
                           "Opening train scheduling interface...\\n\\n"
                           "Available features:\\n"
                           "• Select departure and arrival stations\\n"
                           "• Choose optimal time slots\\n" 
                           "• Assign train and crew\\n"
                           "• Optimize route for minimal delays")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayTrackMonitoringApp(root)
    
    # Center the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()
'''

# Save Tkinter application
tkinter_path = os.path.join(project_dir, "railway_track_monitoring_tkinter.py")
with open(tkinter_path, "w") as f:
    f.write(tkinter_code)

print("✅ Created enhanced Tkinter application with highlighted tracks")
print(f"📄 File size: {len(tkinter_code)} characters")