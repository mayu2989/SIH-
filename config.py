# Railway Track Monitoring System Configuration
# Enhanced Track Visualization Settings

# Map Configuration
MAP_DEFAULT_CENTER = [20.5937, 78.9629]  # Center of India
MAP_DEFAULT_ZOOM = 5
MAP_DEFAULT_STYLE = "OpenStreetMap"

# Track Visualization Settings
TRACK_COLORS = {
    "high_congestion": "#dc3545",    # Red
    "medium_congestion": "#fd7e14",  # Orange  
    "live_tracks": "#28a745",        # Green
    "blocked_tracks": "#6c757d",     # Gray
    "free_tracks": "#007bff"         # Blue
}

TRACK_WIDTHS = {
    "high_congestion": 8,
    "medium_congestion": 6,
    "live_tracks": 5,
    "blocked_tracks": 7,
    "free_tracks": 4
}

# Animation Settings
ENABLE_ANIMATIONS = False
ANIMATION_SPEED = 2000  # milliseconds
DASH_PATTERNS = {
    "blocked": "15,10",
    "maintenance": "10,5"
}

# System Settings
AUTO_REFRESH_INTERVAL = 30  # seconds
MAX_TRACKS_DISPLAY = 50
ENABLE_TOOLTIPS = True
SHOW_TRACK_LABELS = True

# AI Recommendations
AI_UPDATE_INTERVAL = 300  # seconds
MAX_RECOMMENDATIONS = 4
ENABLE_PREDICTIVE_ANALYSIS = True
