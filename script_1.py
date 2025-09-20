# Create the Streamlit application with highlighted tracks
streamlit_code = '''import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time

# Try to import folium for maps
try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

class RailwayTrackMonitoringStreamlit:
    def __init__(self):
        self.initialize_mock_data()
    
    def initialize_mock_data(self):
        """Initialize mock data for the railway system with route coordinates"""
        self.tracks_data = {
            'live_tracks': [
                {
                    'Track ID': 'T001', 'Route': 'Delhi-Mumbai', 'Train': 'Rajdhani Express', 
                    'Status': '🟢 Running', 'Speed': '110 km/h', 'Current Location': 'Kilometer 250',
                    'route_coords': [[28.7041, 77.1025], [21.7679, 78.8718], [19.0760, 72.8777]]
                },
                {
                    'Track ID': 'T002', 'Route': 'Chennai-Kolkata', 'Train': 'Coromandel Express', 
                    'Status': '🟢 Running', 'Speed': '95 km/h', 'Current Location': 'Kilometer 180',
                    'route_coords': [[13.0827, 80.2707], [17.3850, 78.4867], [22.5726, 88.3639]]
                },
                {
                    'Track ID': 'T003', 'Route': 'Bangalore-Delhi', 'Train': 'Karnataka Express', 
                    'Status': '🟢 Running', 'Speed': '120 km/h', 'Current Location': 'Kilometer 320',
                    'route_coords': [[12.9716, 77.5946], [17.3850, 78.4867], [28.7041, 77.1025]]
                },
                {
                    'Track ID': 'T005', 'Route': 'Mumbai-Chennai', 'Train': 'Chennai Express', 
                    'Status': '🟢 Running', 'Speed': '105 km/h', 'Current Location': 'Kilometer 145',
                    'route_coords': [[19.0760, 72.8777], [15.2993, 74.1240], [13.0827, 80.2707]]
                }
            ],
            'congested_tracks': [
                {
                    'Track ID': 'T004', 'Route': 'Mumbai-Pune', 'Congestion Level': '🔴 High', 
                    'Trains Count': 8, 'Average Delay': '45 min', 'severity': 'high',
                    'route_coords': [[19.0760, 72.8777], [18.5204, 73.8567]]
                },
                {
                    'Track ID': 'T007', 'Route': 'Delhi-Jaipur', 'Congestion Level': '🟡 Medium', 
                    'Trains Count': 5, 'Average Delay': '20 min', 'severity': 'medium',
                    'route_coords': [[28.7041, 77.1025], [26.9124, 75.7873]]
                },
                {
                    'Track ID': 'T012', 'Route': 'Kolkata-Bhubaneswar', 'Congestion Level': '🔴 High', 
                    'Trains Count': 7, 'Average Delay': '35 min', 'severity': 'high',
                    'route_coords': [[22.5726, 88.3639], [20.2961, 85.8245]]
                },
                {
                    'Track ID': 'T018', 'Route': 'Bangalore-Mysore', 'Congestion Level': '🟡 Medium', 
                    'Trains Count': 4, 'Average Delay': '15 min', 'severity': 'medium',
                    'route_coords': [[12.9716, 77.5946], [12.2958, 76.6394]]
                }
            ],
            'blocked_tracks': [
                {
                    'Track ID': 'T008', 'Route': 'Hyderabad-Vijayawada', 'Blocking Reason': '🔧 Maintenance Work', 
                    'Estimated Clearance': '2 hours',
                    'route_coords': [[17.3850, 78.4867], [16.5062, 80.6480]]
                },
                {
                    'Track ID': 'T015', 'Route': 'Ahmedabad-Rajkot', 'Blocking Reason': '🚨 Signal Failure', 
                    'Estimated Clearance': '30 min',
                    'route_coords': [[23.0225, 72.5714], [22.3039, 70.8022]]
                },
                {
                    'Track ID': 'T022', 'Route': 'Pune-Nashik', 'Blocking Reason': '🛠️ Track Repair', 
                    'Estimated Clearance': '4 hours',
                    'route_coords': [[18.5204, 73.8567], [19.9975, 73.7898]]
                }
            ],
            'free_tracks': [
                {
                    'Track ID': 'T020', 'Route': 'Lucknow-Kanpur', 'Capacity Available': '100%', 
                    'Next Scheduled Train': '14:30',
                    'route_coords': [[26.8467, 80.9462], [26.4499, 80.3319]]
                },
                {
                    'Track ID': 'T025', 'Route': 'Surat-Vadodara', 'Capacity Available': '100%', 
                    'Next Scheduled Train': '16:45',
                    'route_coords': [[21.1702, 72.8311], [22.3072, 73.1812]]
                },
                {
                    'Track ID': 'T030', 'Route': 'Indore-Bhopal', 'Capacity Available': '100%', 
                    'Next Scheduled Train': '18:20',
                    'route_coords': [[22.7196, 75.8577], [23.2599, 77.4126]]
                },
                {
                    'Track ID': 'T035', 'Route': 'Jaipur-Udaipur', 'Capacity Available': '100%', 
                    'Next Scheduled Train': '19:15',
                    'route_coords': [[26.9124, 75.7873], [24.5854, 73.7125]]
                }
            ]
        }
        
        self.ai_recommendations = [
            "Reroute 2 trains from T004 to alternate tracks T021 and T022 for optimal flow",
            "Implement dynamic scheduling to reduce peak hour congestion by 30%",
            "Use predictive maintenance algorithms to prevent signal failures",
            "Optimize train speeds during congested periods to improve overall efficiency"
        ]

def main():
    # Page configuration
    st.set_page_config(
        page_title="Railway Track Monitoring System - Enhanced Track Visualization",
        page_icon="🚄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize the app
    if 'app' not in st.session_state:
        st.session_state.app = RailwayTrackMonitoringStreamlit()
    
    app = st.session_state.app
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #34495e;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .ai-recommendation {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .track-legend {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #dee2e6;
        margin-top: 1rem;
    }
    .track-status-high { color: #dc3545; font-weight: bold; }
    .track-status-medium { color: #fd7e14; font-weight: bold; }
    .track-status-normal { color: #28a745; font-weight: bold; }
    .track-status-blocked { color: #6c757d; font-weight: bold; }
    .track-status-free { color: #007bff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title
    st.markdown('<h1 class="main-header">🚄 Railway Track Monitoring System - Enhanced Track Visualization</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🚉 Navigation Dashboard")
    section = st.sidebar.radio(
        "Select Section:",
        ["🚄 Live Railway Tracks", "⚠️ Congested Tracks", "🗺️ Railway Map", "🚫 Blocked Tracks", "✅ Free Tracks"],
        index=0
    )
    
    # Display current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.sidebar.markdown(f"**📅 Current Time:** `{current_time}`")
    
    # Track statistics in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Overview")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("🚄 Live", len(app.tracks_data['live_tracks']), "0")
        st.metric("🚫 Blocked", len(app.tracks_data['blocked_tracks']), "+1")
    with col2:
        st.metric("⚠️ Congested", len(app.tracks_data['congested_tracks']), "+1")  
        st.metric("✅ Free", len(app.tracks_data['free_tracks']), "-1")
    
    # Enhanced system status
    st.sidebar.markdown("### 🎯 System Status")
    st.sidebar.success("🟢 Track Visualization Active")
    st.sidebar.info("📡 Real-time Monitoring Active")
    st.sidebar.warning("🗺️ Enhanced Maps Available")
    
    # Track visualization settings
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Visualization Settings")
    show_track_labels = st.sidebar.checkbox("🏷️ Show Track Labels", value=True)
    highlight_congestion = st.sidebar.checkbox("🔍 Highlight Congestion", value=True)
    show_animations = st.sidebar.checkbox("🎬 Animated Tracks", value=False)
    
    # Auto-refresh option
    st.sidebar.markdown("---")
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False)
    if auto_refresh:
        time.sleep(30)
        st.experimental_rerun()
    
    # Main content area
    if section == "🚄 Live Railway Tracks":
        show_live_tracks(app)
    elif section == "⚠️ Congested Tracks":
        show_congested_tracks(app)
    elif section == "🗺️ Railway Map":
        show_railway_map(app, show_track_labels, highlight_congestion, show_animations)
    elif section == "🚫 Blocked Tracks":
        show_blocked_tracks(app)
    elif section == "✅ Free Tracks":
        show_free_tracks(app)

def show_railway_map(app, show_labels=True, highlight_congestion=True, show_animations=False):
    """Display railway map section with highlighted track visualization"""
    st.markdown('<h2 class="section-header">🗺️ Railway Network Map - Highlighted Track Visualization</h2>', unsafe_allow_html=True)
    
    # Map controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.info("🗺️ Interactive railway network map with highlighted track visualization showing congestion status")
    with col2:
        map_style = st.selectbox("🎨 Map Style", ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark_Matter"], index=0)
    with col3:
        track_width = st.selectbox("📏 Track Width", ["Thin", "Medium", "Thick"], index=1)
    with col4:
        if st.button("🔄 Refresh Tracks", type="primary"):
            st.success("🎯 Track visualization refreshed!")
            st.experimental_rerun()
    
    st.markdown("---")
    
    if MAP_AVAILABLE:
        # Create interactive map with highlighted tracks
        create_interactive_track_map(app, map_style, track_width, show_labels, highlight_congestion, show_animations)
    else:
        # Show installation instructions and fallback
        create_fallback_track_map(app)
    
    # Track analysis dashboard
    st.markdown("---")
    st.markdown("### 📊 Track Network Analysis Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔥 Congestion Hotspots")
        high_congestion = [track for track in app.tracks_data['congested_tracks'] if track['severity'] == 'high']
        medium_congestion = [track for track in app.tracks_data['congested_tracks'] if track['severity'] == 'medium']
        
        for track in high_congestion:
            st.error(f"**🔴 {track['Track ID']}** - {track['Route']}\\n🚄 {track['Trains Count']} trains | ⏰ {track['Average Delay']} delay")
        
        for track in medium_congestion:
            st.warning(f"**🟡 {track['Track ID']}** - {track['Route']}\\n🚄 {track['Trains Count']} trains | ⏰ {track['Average Delay']} delay")
    
    with col2:
        st.markdown("#### 🚫 Service Disruptions")
        for track in app.tracks_data['blocked_tracks']:
            st.info(f"**{track['Track ID']}** - {track['Route']}\\n{track['Blocking Reason']} | ⏳ {track['Estimated Clearance']}")
    
    with col3:
        st.markdown("#### ✅ Available Capacity")
        for track in app.tracks_data['free_tracks']:
            st.success(f"**{track['Track ID']}** - {track['Route']}\\n{track['Capacity Available']} capacity | 🚄 Next: {track['Next Scheduled Train']}")

def create_interactive_track_map(app, map_style, track_width, show_labels, highlight_congestion, show_animations):
    """Create interactive folium map with highlighted tracks"""
    
    # Map tile selection
    tile_map = {
        "OpenStreetMap": "OpenStreetMap",
        "CartoDB Positron": "CartoDB Positron", 
        "CartoDB Dark_Matter": "CartoDB Dark_Matter"
    }
    
    # Track width mapping
    width_map = {"Thin": 4, "Medium": 6, "Thick": 8}
    base_width = width_map[track_width]
    
    # Create base map centered on India
    m = folium.Map(
        location=[20.5937, 78.9629],  # Center of India
        zoom_start=5,
        tiles=tile_map.get(map_style, "OpenStreetMap")
    )
    
    # Add highlighted tracks using PolyLine (NO MARKERS)
    
    # 1. Congested tracks with RED/ORANGE lines
    for track in app.tracks_data['congested_tracks']:
        if 'route_coords' in track and len(track['route_coords']) >= 2:
            # Color based on severity
            if track['severity'] == 'high':
                color = "#dc3545"  # Red for high congestion
                weight = base_width + 3
                opacity = 0.9
            else:
                color = "#fd7e14"  # Orange for medium congestion
                weight = base_width + 1
                opacity = 0.8
            
            # Create PolyLine for track
            folium.PolyLine(
                locations=track['route_coords'],
                color=color,
                weight=weight,
                opacity=opacity,
                popup=f"⚠️ CONGESTED: {track['Track ID']} - {track['Route']}\\nLevel: {track['Congestion Level']}\\nTrains: {track['Trains Count']} | Delay: {track['Average Delay']}",
                tooltip=f"{track['Track ID']} - {track['Route']} (CONGESTED)" if show_labels else None
            ).add_to(m)
            
            # Add pulsating effect for high congestion if animations enabled
            if show_animations and track['severity'] == 'high':
                folium.plugins.AntPath(
                    locations=track['route_coords'],
                    color=color,
                    weight=weight-2,
                    opacity=0.6,
                    delay=1000,
                    dashArray="10,20"
                ).add_to(m)
    
    # 2. Live tracks with GREEN lines
    for track in app.tracks_data['live_tracks']:
        if 'route_coords' in track and len(track['route_coords']) >= 2:
            color = "#28a745"  # Green for live tracks
            weight = base_width
            
            folium.PolyLine(
                locations=track['route_coords'],
                color=color,
                weight=weight,
                opacity=0.8,
                popup=f"🚄 LIVE: {track['Track ID']} - {track['Route']}\\nTrain: {track['Train']}\\nSpeed: {track['Speed']} | Status: {track['Status']}",
                tooltip=f"{track['Track ID']} - {track['Train']}" if show_labels else None
            ).add_to(m)
            
            # Add moving effect for live trains if animations enabled
            if show_animations:
                folium.plugins.AntPath(
                    locations=track['route_coords'],
                    color=color,
                    weight=weight-1,
                    opacity=0.5,
                    delay=2000,
                    dashArray="5,10"
                ).add_to(m)
    
    # 3. Blocked tracks with GRAY dashed lines
    for track in app.tracks_data['blocked_tracks']:
        if 'route_coords' in track and len(track['route_coords']) >= 2:
            color = "#6c757d"  # Gray for blocked tracks
            weight = base_width + 2
            
            folium.PolyLine(
                locations=track['route_coords'],
                color=color,
                weight=weight,
                opacity=0.7,
                dashArray="15,10",  # Dashed line
                popup=f"🚫 BLOCKED: {track['Track ID']} - {track['Route']}\\nReason: {track['Blocking Reason']}\\nClearance: {track['Estimated Clearance']}",
                tooltip=f"{track['Track ID']} - BLOCKED" if show_labels else None
            ).add_to(m)
    
    # 4. Free tracks with BLUE semi-transparent lines
    for track in app.tracks_data['free_tracks']:
        if 'route_coords' in track and len(track['route_coords']) >= 2:
            color = "#007bff"  # Blue for free tracks
            weight = base_width - 1
            
            folium.PolyLine(
                locations=track['route_coords'],
                color=color,
                weight=weight,
                opacity=0.6,
                popup=f"✅ FREE: {track['Track ID']} - {track['Route']}\\nCapacity: {track['Capacity Available']}\\nNext Train: {track['Next Scheduled Train']}",
                tooltip=f"{track['Track ID']} - Available" if show_labels else None
            ).add_to(m)
    
    # Add layer control for different track types
    if highlight_congestion:
        # Create feature groups for layer control
        congested_group = folium.FeatureGroup(name="Congested Tracks")
        live_group = folium.FeatureGroup(name="Live Tracks")
        blocked_group = folium.FeatureGroup(name="Blocked Tracks")
        free_group = folium.FeatureGroup(name="Free Tracks")
        
        # Add groups to map
        congested_group.add_to(m)
        live_group.add_to(m)
        blocked_group.add_to(m)
        free_group.add_to(m)
        
        # Add layer control
        folium.LayerControl(collapsed=False).add_to(m)
    
    # Add scale bar and measurement tools
    folium.plugins.MeasureControl().add_to(m)
    
    # Display the map
    map_data = st_folium(m, width=1200, height=600, returned_objects=["last_clicked", "last_object_clicked"])
    
    # Show clicked information
    if map_data and map_data.get('last_object_clicked'):
        clicked_info = map_data['last_object_clicked']
        if clicked_info:
            st.info(f"📍 **Track Clicked** - Displaying detailed information for selected railway track")
    
    # Enhanced track legend
    create_enhanced_track_legend()

def create_fallback_track_map(app):
    """Create fallback track visualization when folium is not available"""
    # Installation notice
    st.error("📦 **Enhanced Track Visualization Not Available**")
    st.markdown("Install required packages for full interactive track maps:")
    st.code("pip install folium streamlit-folium", language="bash")
    
    # Alternative text-based track visualization
    st.markdown("### 🗺️ Text-Based Railway Track Network")
    
    # Create tabs for different track status views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Network Overview", "🔥 Congestion Analysis", "🚫 Service Status", "📈 Capacity Planning"])
    
    with tab1:
        st.markdown("#### 🗺️ Railway Network Schematic")
        st.markdown("""
        ```
        🗺️ INDIAN RAILWAY NETWORK - TRACK STATUS VISUALIZATION
        ═══════════════════════════════════════════════════════════════════════
        
        🔴━━━━━━━ Mumbai ←→ Pune (HIGH CONGESTION)
              ┃   ┃  • 8 trains active  • 45 min delay
              ┃   ┗━━━━━━━ 🟢 Mumbai-Chennai (LIVE)
              ┃
        Delhi ●━━━━●━━━━● Jaipur
              ┃ 🟡MED ┃  (Medium Congestion - 5 trains, 20 min delay)
              ┃      ┃
              ┃      ┗━━━━● Udaipur (🔵 FREE TRACK)
              ┃
        🟢━━━━┗━━━━━━━━━━● Mumbai
        (Delhi-Mumbai LIVE - Rajdhani Express)
              
        🔴━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Kolkata ←→ Bhubaneswar
        (HIGH CONGESTION - 7 trains, 35 min delay)
                    
        🟢━━━━━━━━━━━━━━━━━━━━━━━ Chennai ←→ Kolkata
        (LIVE - Coromandel Express)
        
        🚫┅┅┅┅┅┅┅ Hyderabad ←→ Vijayawada (BLOCKED - Maintenance)
        🚫┅┅┅┅┅┅┅ Ahmedabad ←→ Rajkot (BLOCKED - Signal Failure)
        
        🔵━━━━━━━ Lucknow ←→ Kanpur (FREE - Next: 14:30)
        🔵━━━━━━━ Surat ←→ Vadodara (FREE - Next: 16:45)
        
        Legend: 🔴 High Congestion | 🟡 Medium | 🟢 Live | 🚫 Blocked | 🔵 Free
        ```
        """)
    
    with tab2:
        st.markdown("#### 🌡️ Real-Time Congestion Heat Analysis")
        
        # Create congestion visualization
        congestion_data = []
        for track in app.tracks_data['congested_tracks']:
            severity_emoji = "🔴" if track['severity'] == 'high' else "🟡"
            congestion_data.append({
                "Track": f"{severity_emoji} {track['Track ID']}",
                "Route": track['Route'],
                "Intensity": track['Congestion Level'],
                "Active Trains": track['Trains Count'],
                "Avg Delay": track['Average Delay'],
                "Priority": "CRITICAL" if track['severity'] == 'high' else "MONITOR"
            })
        
        congestion_df = pd.DataFrame(congestion_data)
        st.dataframe(congestion_df, use_container_width=True)
        
        # Congestion metrics
        high_count = len([t for t in app.tracks_data['congested_tracks'] if t['severity'] == 'high'])
        medium_count = len([t for t in app.tracks_data['congested_tracks'] if t['severity'] == 'medium'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Critical Congestion", high_count, "+1")
        with col2:
            st.metric("🟡 Moderate Congestion", medium_count, "0")
        with col3:
            st.metric("⚡ System Efficiency", "72%", "-8%")
    
    with tab3:
        st.markdown("#### 🚫 Service Disruption Analysis")
        
        blocked_data = []
        for track in app.tracks_data['blocked_tracks']:
            blocked_data.append({
                "Track ID": f"🚫 {track['Track ID']}",
                "Route": track['Route'],
                "Issue": track['Blocking Reason'],
                "ETA": track['Estimated Clearance'],
                "Impact": "High" if "Maintenance" in track['Blocking Reason'] else "Medium"
            })
        
        blocked_df = pd.DataFrame(blocked_data)
        st.dataframe(blocked_df, use_container_width=True)
    
    with tab4:
        st.markdown("#### 📈 Track Capacity & Availability")
        
        capacity_data = []
        for track in app.tracks_data['free_tracks']:
            capacity_data.append({
                "Track ID": f"✅ {track['Track ID']}",
                "Route": track['Route'],
                "Available Capacity": track['Capacity Available'],
                "Next Slot": track['Next Scheduled Train'],
                "Utilization": f"{random.randint(15, 35)}%"
            })
        
        capacity_df = pd.DataFrame(capacity_data)
        st.dataframe(capacity_df, use_container_width=True)

def create_enhanced_track_legend():
    """Create enhanced legend for track visualization"""
    st.markdown("""
    <div class="track-legend">
        <h4>🗺️ Enhanced Track Visualization Legend</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 20px;">
            <div><span style="color: #dc3545; font-size: 18px;">━━━</span> High Congestion Tracks (Critical - Thick Red Lines)</div>
            <div><span style="color: #fd7e14; font-size: 18px;">━━━</span> Medium Congestion Tracks (Moderate - Orange Lines)</div>
            <div><span style="color: #28a745; font-size: 18px;">━━━</span> Live Tracks (Normal Operations - Green Lines)</div>
            <div><span style="color: #6c757d; font-size: 18px;">┅┅┅</span> Blocked Tracks (Maintenance/Issues - Dashed Gray)</div>
            <div><span style="color: #007bff; font-size: 18px;">━━━</span> Free Tracks (Available Capacity - Blue Lines)</div>
        </div>
        <p><strong>🎨 Track Width:</strong> Indicates priority and traffic density<br>
        <strong>🔄 Animations:</strong> Moving patterns show live train movement<br>
        <strong>📍 Interactive:</strong> Click on tracks for detailed information</p>
    </div>
    """, unsafe_allow_html=True)

# Include all other show functions (show_live_tracks, show_congested_tracks, etc.)
def show_live_tracks(app):
    st.markdown('<h2 class="section-header">🚄 Live Railway Tracks</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.info("🔴 Real-time monitoring of active railway tracks with live status updates")
    with col2:
        if st.button("🔄 Refresh Data", key="refresh_live", type="primary"):
            for track in app.tracks_data['live_tracks']:
                track['Speed'] = f"{random.randint(80, 130)} km/h"
                track['Current Location'] = f"Kilometer {random.randint(100, 400)}"
            st.success("✅ Live data refreshed!")
            st.experimental_rerun()
    with col3:
        st.button("📊 Analytics", key="analytics")
    with col4:
        st.button("🚨 Alerts", key="alerts")
    
    st.markdown("---")
    
    df_live = pd.DataFrame(app.tracks_data['live_tracks'])
    st.dataframe(
        df_live.drop(columns=['route_coords'], errors='ignore'),
        use_container_width=True,
        height=400,
        column_config={
            "Track ID": st.column_config.TextColumn("Track ID", width="small"),
            "Route": st.column_config.TextColumn("Route", width="medium"),
            "Train": st.column_config.TextColumn("Train", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Speed": st.column_config.TextColumn("Speed", width="small"),
            "Current Location": st.column_config.TextColumn("Current Location", width="medium")
        }
    )
    
    st.markdown("### 📈 Live Performance Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Avg Speed", "108 km/h", "+5 km/h")
    with col2:
        st.metric("On-Time", "94%", "+2%")
    with col3:
        st.metric("Active Trains", "12", "+1")
    with col4:
        st.metric("Efficiency", "97%", "+1%")
    with col5:
        st.metric("Alerts", "2", "-1")

def show_congested_tracks(app):
    st.markdown('<h2 class="section-header">⚠️ Congested Railway Tracks</h2>', unsafe_allow_html=True)
    
    st.warning("⚠️ These tracks are experiencing high traffic volumes and potential delays")
    
    df_congested = pd.DataFrame(app.tracks_data['congested_tracks'])
    st.dataframe(
        df_congested.drop(columns=['route_coords', 'severity'], errors='ignore'), 
        use_container_width=True,
        height=300
    )
    
    st.markdown("### 📊 Congestion Analysis")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("High Congestion", "2 tracks", "+1")
    with col2:
        st.metric("Avg Delay", "29 min", "+8 min")
    with col3:
        st.metric("Peak Impact", "67%", "+12%")
    with col4:
        st.metric("Efficiency Loss", "15%", "+3%")
    
    # AI Recommendations Subsection
    st.markdown("---")
    st.markdown('<h3 style="color: #8e44ad;">🤖 AI-Powered Recommendations to Reduce Congestion</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("🧠 Advanced AI analysis provides intelligent solutions for traffic optimization")
    with col2:
        if st.button("📊 Generate New Analysis", key="generate_ai", type="primary"):
            new_recommendations = [
                "Implement automated traffic control for peak hours to reduce delays by 25%",
                "Use machine learning to predict congestion patterns 2 hours in advance",
                "Deploy additional signaling on high-traffic routes (T004, T012)",
                "Alternative routing for freight trains during rush hours",
                "Upgrade infrastructure using predictive maintenance",
                "Implement train platooning to reduce headway by 40%",
                "Dynamic pricing to distribute passenger load"
            ]
            app.ai_recommendations = random.sample(new_recommendations, 4)
            st.success("🎯 New AI recommendations generated!")
            st.experimental_rerun()
    
    st.markdown("#### 💡 Current AI Recommendations:")
    for i, recommendation in enumerate(app.ai_recommendations, 1):
        st.markdown(f"""
        <div class="ai-recommendation">
            <strong>🎯 Recommendation #{i}:</strong><br>
            {recommendation}
        </div>
        """, unsafe_allow_html=True)

def show_blocked_tracks(app):
    st.markdown('<h2 class="section-header">🚫 Blocked Railway Tracks</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.error("🚨 These tracks are currently unavailable due to maintenance, repairs, or technical issues")
    with col2:
        if st.button("🚨 Emergency Protocol", key="emergency_clear", type="secondary"):
            st.warning("🚨 Emergency clear protocol initiated!")
            st.balloons()
    
    df_blocked = pd.DataFrame(app.tracks_data['blocked_tracks'])
    st.dataframe(
        df_blocked.drop(columns=['route_coords'], errors='ignore'), 
        use_container_width=True,
        height=300
    )
    
    st.markdown("### 🔧 Maintenance Progress Tracking")
    maintenance_data = [
        {"Track": "T008", "Work": "Track Replacement", "Progress": 60, "ETA": "1.2 hours"},
        {"Track": "T015", "Work": "Signal Repair", "Progress": 85, "ETA": "25 min"},
        {"Track": "T022", "Work": "Infrastructure Upgrade", "Progress": 25, "ETA": "3.2 hours"}
    ]
    
    for item in maintenance_data:
        st.markdown(f"**🔧 {item['Track']} - {item['Work']}**")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(item['Progress'] / 100, text=f"Progress: {item['Progress']}%")
        with col2:
            st.metric("ETA", item['ETA'])

def show_free_tracks(app):
    st.markdown('<h2 class="section-header">✅ Free Railway Tracks</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success("✅ These tracks are currently available and ready for train scheduling")
    with col2:
        if st.button("🚂 Schedule Train", key="schedule_train", type="primary"):
            st.info("🚂 Opening advanced train scheduling interface...")
    
    df_free = pd.DataFrame(app.tracks_data['free_tracks'])
    st.dataframe(
        df_free.drop(columns=['route_coords'], errors='ignore'), 
        use_container_width=True,
        height=350
    )
    
    st.markdown("### 📊 Capacity Utilization & Efficiency")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Available Tracks", "4", "0")
    with col2:
        st.metric("Total Capacity", "100%", "0%")
    with col3:
        st.metric("Scheduling Efficiency", "92%", "+3%")
    with col4:
        st.metric("Next Slot", "14:30", "")
    with col5:
        st.metric("Utilization Rate", "78%", "+5%")

# Run the app
if __name__ == "__main__":
    main()
'''

# Save Streamlit application
streamlit_path = os.path.join(project_dir, "railway_track_monitoring_streamlit.py")
with open(streamlit_path, "w") as f:
    f.write(streamlit_code)

print("✅ Created enhanced Streamlit application with highlighted tracks")
print(f"📄 File size: {len(streamlit_code)} characters")