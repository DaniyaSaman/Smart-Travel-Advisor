import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta
import calendar
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import base64
import os

# Page configuration
st.set_page_config(
    page_title="Travel Planner - Smart Travel Advisor",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - LIGHT BLUE BACKGROUND WITH BLACK FONT
# ============================================================
st.markdown("""
<style>
    /* ============ MAIN BACKGROUND: LIGHT BLUE ============ */
    .stApp {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 50%, #E1F5FE 100%);
    }
    
    .block-container {
        background: transparent;
    }
    
    /* ============ GLOBAL FONT COLOR: BLACK ============ */
    html, body, [class*="css"], p, span, div, label, li {
        color: #000000 !important;
    }
    
    /* Headers in dark blue for contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #0D47A1 !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #FFFFFF !important;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Sidebar - light blue */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E3F2FD 0%, #BBDEFB 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    /* ============ DESTINATION CARDS ============ */
    .destination-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        background-size: cover;
        background-position: center;
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        min-height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }
    
    .destination-card h3,
    .destination-card p,
    .destination-card span,
    .destination-card strong {
        color: #FFFFFF !important;
    }
    
    .destination-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .destination-card-content {
        background: rgba(0,0,0,0.8);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    /* ============ HOTEL CARDS ============ */
    .hotel-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #FF6B6B;
        transition: transform 0.2s;
        color: #000000 !important;
    }
    
    .hotel-card * {
        color: #000000 !important;
    }
    
    .hotel-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }
    
    .hotel-card.selected {
        border-left: 4px solid #4CAF50;
        background: #E8F5E9;
    }
    
    .cheap-hotel-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1rem;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 1rem;
        color: #000000 !important;
        box-shadow: 0 3px 8px rgba(76, 175, 80, 0.2);
    }
    
    .cheap-hotel-card * {
        color: #000000 !important;
    }
    
    /* ============ METRIC CARDS ============ */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #000000 !important;
    }
    
    .metric-card * {
        color: #000000 !important;
    }
    
    /* ============ WEATHER BADGES ============ */
    .weather-badge {
        padding: 0.5rem;
        border-radius: 5px;
        color: #FFFFFF !important;
        font-weight: bold;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .sunny { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }
    .cloudy { background: linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%); }
    .rainy { background: linear-gradient(135deg, #a8c0ff 0%, #3f2b96 100%); }
    .snow { background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); color: #000000 !important; }
    
    /* ============ FOLDER CARDS ============ */
    .folder-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: #FFFFFF !important;
        cursor: pointer;
        transition: transform 0.3s;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 2px solid transparent;
        margin-bottom: 1rem;
    }
    
    .folder-card * {
        color: #FFFFFF !important;
    }
    
    .folder-card:hover {
        transform: scale(1.05);
        border: 2px solid gold;
    }
    
    /* ============ BADGES ============ */
    .safety-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
        font-size: 0.9rem;
        color: #FFFFFF !important;
    }
    
    .safety-high { background: #4CAF50; }
    .safety-medium { background: #FFC107; color: #000000 !important; }
    .safety-low { background: #F44336; }
    
    .interest-badge {
        background: #FF6B6B;
        color: #FFFFFF !important;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.1rem;
        display: inline-block;
    }
    
    .group-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
        font-size: 0.9rem;
        color: #FFFFFF !important;
    }
    
    .group-solo { background: #9C27B0; }
    .group-family { background: #FF9800; }
    .group-couple { background: #E91E63; }
    .group-friends { background: #2196F3; }
    
    /* ============ DETAIL CARDS ============ */
    .detail-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        color: #000000 !important;
    }
    
    .detail-card * {
        color: #000000 !important;
    }
    
    /* ============ TRIP ITEMS ============ */
    .trip-destination-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        color: #000000 !important;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .trip-destination-item * {
        color: #000000 !important;
    }
    
    /* ============ EMPTY ALBUM ============ */
    .empty-album {
        background: white;
        padding: 4rem;
        border-radius: 20px;
        text-align: center;
        color: #000000 !important;
        border: 3px dashed #999;
        margin: 2rem 0;
    }
    
    /* ============ STAR RATING ============ */
    .star-rating {
        color: #FFD700 !important;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    
    /* ============ CHEAPEST HIGHLIGHT ============ */
    .cheapest-highlight {
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
        color: #FFFFFF !important;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(76, 175, 80, 0.3);
    }
    
    .cheapest-highlight * {
        color: #FFFFFF !important;
    }
    
    .cost-summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: #FFFFFF !important;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .cost-summary-card * {
        color: #FFFFFF !important;
    }
    
    .reminder-card {
        background: linear-gradient(135deg, #FFE5B4 0%, #FFCCCB 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: #000000 !important;
        border-left: 5px solid #FF6B6B;
        margin-bottom: 1rem;
    }
    
    .reminder-card * {
        color: #000000 !important;
    }
    
    .auth-container {
        max-width: 500px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        color: #000000 !important;
    }
    
    .auth-container * {
        color: #000000 !important;
    }
    
    .auth-header {
        text-align: center;
        color: #667eea !important;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []
if 'current_trip' not in st.session_state:
    st.session_state.current_trip = None
if 'saved_destinations' not in st.session_state:
    st.session_state.saved_destinations = []
if 'photo_albums' not in st.session_state:
    st.session_state.photo_albums = {}
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None
if 'view_photos_country' not in st.session_state:
    st.session_state.view_photos_country = None
if 'show_place_details' not in st.session_state:
    st.session_state.show_place_details = None
if 'safety_ratings' not in st.session_state:
    st.session_state.safety_ratings = {}

# ============================================================
# HOTEL DATABASE - REAL NAMES WITH EXACT LOCATIONS
# ============================================================
HOTEL_DATABASE = {
    'Japan': [
        {'name': "K's House Kyoto", 'location': 'Kyoto - Near Kyoto Station, Shimogyo Ward', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 1200, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'AC', 'Shared Kitchen', 'Lounge']},
        {'name': 'Nui. Hostel & Bar Lounge', 'location': 'Tokyo - Kuramae, Taito City (Near Asakusa)', 'category': 'Budget', 'stars': 3, 'rating': 4.6, 'reviews': 890, 'nightly_rate_inr': 4200, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Cafe']},
        {'name': 'Piece Hostel Kyoto', 'location': 'Kyoto - Near Kyoto Tower, Shimogyo Ward', 'category': 'Standard', 'stars': 3, 'rating': 4.7, 'reviews': 1500, 'nightly_rate_inr': 5500, 'amenities': ['Free WiFi', 'AC', 'Breakfast', 'Lounge']},
        {'name': 'Sotetsu Fresa Inn', 'location': 'Tokyo - Ginza District, Chuo City', 'category': 'Standard', 'stars': 3, 'rating': 4.4, 'reviews': 2100, 'nightly_rate_inr': 7200, 'amenities': ['Free WiFi', 'AC', 'Breakfast', '24hr Reception']},
        {'name': 'Hotel Gracery Shinjuku', 'location': 'Tokyo - Shinjuku, Kabukicho', 'category': 'Premium', 'stars': 4, 'rating': 4.5, 'reviews': 3400, 'nightly_rate_inr': 12500, 'amenities': ['Free WiFi', 'AC', 'Breakfast', 'Restaurant']},
        {'name': 'Park Hyatt Tokyo', 'location': 'Tokyo - Shinjuku, Nishi-Shinjuku', 'category': 'Luxury', 'stars': 5, 'rating': 4.8, 'reviews': 2200, 'nightly_rate_inr': 35000, 'amenities': ['Free WiFi', 'Spa', 'Pool', 'Fine Dining']}
    ],
    'Singapore': [
        {'name': 'The Pod @ Beach Road', 'location': 'Singapore - Beach Road, Bugis', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 1800, 'nightly_rate_inr': 3800, 'amenities': ['Free WiFi', 'AC', 'Pod Beds', 'Lounge']},
        {'name': 'Wink Hostel', 'location': 'Singapore - Chinatown, Pagoda Street', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 1200, 'nightly_rate_inr': 4200, 'amenities': ['Free WiFi', 'AC', 'Breakfast', 'Lounge']},
        {'name': 'Dream Lodge', 'location': 'Singapore - Little India, Serangoon Road', 'category': 'Standard', 'stars': 3, 'rating': 4.3, 'reviews': 950, 'nightly_rate_inr': 5500, 'amenities': ['Free WiFi', 'AC', 'Breakfast', 'Rooftop']},
        {'name': 'Hotel G Singapore', 'location': 'Singapore - Middle Road, Bugis', 'category': 'Standard', 'stars': 4, 'rating': 4.4, 'reviews': 2500, 'nightly_rate_inr': 8500, 'amenities': ['Free WiFi', 'AC', 'Gym', 'Restaurant']},
        {'name': 'Marina Bay Sands', 'location': 'Singapore - Bayfront Avenue, Marina Bay', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 15000, 'nightly_rate_inr': 45000, 'amenities': ['Infinity Pool', 'Spa', 'Casino', 'SkyPark']}
    ],
    'Indonesia': [
        {'name': 'Puri Garden Hotel', 'location': 'Bali - Ubud, Monkey Forest Road', 'category': 'Budget', 'stars': 3, 'rating': 4.6, 'reviews': 1500, 'nightly_rate_inr': 2200, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Yoga']},
        {'name': 'M Boutique Hostel', 'location': 'Bali - Seminyak, Kuta', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 800, 'nightly_rate_inr': 1800, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Bar']},
        {'name': 'The Farm Hostel', 'location': 'Bali - Canggu, Batu Bolong', 'category': 'Standard', 'stars': 3, 'rating': 4.5, 'reviews': 1100, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Restaurant']},
        {'name': 'Alaya Resort Ubud', 'location': 'Bali - Ubud Center, Jalan Hanoman', 'category': 'Premium', 'stars': 4, 'rating': 4.7, 'reviews': 2000, 'nightly_rate_inr': 8500, 'amenities': ['Free WiFi', 'AC', 'Spa', 'Pool']},
        {'name': 'Four Seasons Sayan', 'location': 'Bali - Sayan, Ubud (Near Ayung River)', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 1800, 'nightly_rate_inr': 42000, 'amenities': ['Private Pool', 'Spa', 'Fine Dining', 'River View']}
    ],
    'Thailand': [
        {'name': 'Slumber Party Hostel', 'location': 'Phuket - Patong Beach, Soi Bangla', 'category': 'Budget', 'stars': 3, 'rating': 4.3, 'reviews': 2000, 'nightly_rate_inr': 1200, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Bar']},
        {'name': 'The Yard Hostel', 'location': 'Bangkok - Ari, Phahon Yothin Soi 4', 'category': 'Budget', 'stars': 3, 'rating': 4.7, 'reviews': 1600, 'nightly_rate_inr': 1500, 'amenities': ['Free WiFi', 'AC', 'Garden', 'Cafe']},
        {'name': 'Pai Village Boutique', 'location': 'Pai - Walking Street, Mae Hong Son', 'category': 'Standard', 'stars': 3, 'rating': 4.5, 'reviews': 900, 'nightly_rate_inr': 2800, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Restaurant']},
        {'name': 'Hotel Indigo Phuket', 'location': 'Phuket - Patong, Rat-U-Thit Road', 'category': 'Premium', 'stars': 4, 'rating': 4.6, 'reviews': 1500, 'nightly_rate_inr': 7500, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Spa']},
        {'name': 'Mandarin Oriental Bangkok', 'location': 'Bangkok - Riverside, Charoen Krung Road', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 3500, 'nightly_rate_inr': 38000, 'amenities': ['Spa', 'Pool', 'Fine Dining', 'River View']}
    ],
    'India': [
        {'name': 'Zostel Jaipur', 'location': 'Jaipur - MI Road, Near Hawa Mahal', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 1200, 'nightly_rate_inr': 800, 'amenities': ['Free WiFi', 'AC', 'Common Room', 'Cafe']},
        {'name': 'Moustache Hostel', 'location': 'Jaipur - Bani Park, Near Railway Station', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 950, 'nightly_rate_inr': 1000, 'amenities': ['Free WiFi', 'AC', 'Rooftop', 'Cafe']},
        {'name': 'GoStops Agra', 'location': 'Agra - Taj Ganj, Near Taj Mahal East Gate', 'category': 'Standard', 'stars': 3, 'rating': 4.3, 'reviews': 800, 'nightly_rate_inr': 1500, 'amenities': ['Free WiFi', 'AC', 'Rooftop', 'Taj View']},
        {'name': 'Trident Agra', 'location': 'Agra - Fatehabad Road, Near Taj Mahal', 'category': 'Premium', 'stars': 5, 'rating': 4.7, 'reviews': 2200, 'nightly_rate_inr': 6500, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Spa']},
        {'name': 'The Oberoi Amarvilas', 'location': 'Agra - Taj East Gate Road (350m from Taj)', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 1800, 'nightly_rate_inr': 45000, 'amenities': ['Taj View', 'Pool', 'Spa', 'Fine Dining']}
    ],
    'France': [
        {'name': 'Generator Paris', 'location': 'Paris - 10th Arrondissement, Place du Colonel Fabien', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 3500, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Rooftop']},
        {'name': 'The People Hostel', 'location': 'Paris - Bercy Village, 12th Arrondissement', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 2200, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Kitchen']},
        {'name': 'Jo&Joe Paris', 'location': 'Paris - Gentilly, South of 13th Arrondissement', 'category': 'Standard', 'stars': 3, 'rating': 4.6, 'reviews': 1800, 'nightly_rate_inr': 4500, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Restaurant']},
        {'name': 'Hotel du Louvre', 'location': 'Paris - 1st Arrondissement, Rue de Rivoli (Near Louvre)', 'category': 'Premium', 'stars': 5, 'rating': 4.7, 'reviews': 2500, 'nightly_rate_inr': 22000, 'amenities': ['Free WiFi', 'Spa', 'Fine Dining', 'Concierge']},
        {'name': 'Ritz Paris', 'location': 'Paris - Place Vendôme, 1st Arrondissement', 'category': 'Ultra-Luxury', 'stars': 5, 'rating': 5.0, 'reviews': 1200, 'nightly_rate_inr': 85000, 'amenities': ['Spa', 'Pool', 'Michelin Dining', 'Butler']}
    ],
    'Italy': [
        {'name': 'YellowSquare Rome', 'location': 'Rome - Termini Area, Via Palestro', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 2500, 'nightly_rate_inr': 2800, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Rooftop']},
        {'name': 'Ostello Bello', 'location': 'Rome - Near Colosseum, Via dei Boschetto', 'category': 'Budget', 'stars': 3, 'rating': 4.7, 'reviews': 3000, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Terrace']},
        {'name': 'Plus Florence', 'location': 'Florence - Near Santa Maria Novella Station', 'category': 'Standard', 'stars': 3, 'rating': 4.4, 'reviews': 1800, 'nightly_rate_inr': 4200, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Rooftop']},
        {'name': 'Hotel Artemide', 'location': 'Rome - Via Nazionale, Near Termini', 'category': 'Premium', 'stars': 4, 'rating': 4.7, 'reviews': 3200, 'nightly_rate_inr': 12000, 'amenities': ['Free WiFi', 'Spa', 'Restaurant', 'Rooftop']},
        {'name': 'Hotel Danieli', 'location': 'Venice - Riva degli Schiavoni, Near St. Marks', 'category': 'Luxury', 'stars': 5, 'rating': 4.8, 'reviews': 2000, 'nightly_rate_inr': 45000, 'amenities': ['Water View', 'Fine Dining', 'Spa', 'Historic']}
    ],
    'United Kingdom': [
        {'name': 'Generator London', 'location': 'London - Russell Square, Bloomsbury', 'category': 'Budget', 'stars': 3, 'rating': 4.3, 'reviews': 4000, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'Bar', 'Lounge', 'Games Room']},
        {'name': 'YHA London Central', 'location': 'London - Oxford Street, Westminster', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 2800, 'nightly_rate_inr': 3800, 'amenities': ['Free WiFi', 'Kitchen', 'Lounge', 'Cafe']},
        {'name': 'Clink78 Hostel', 'location': "London - King's Cross, Near St Pancras", 'category': 'Standard', 'stars': 3, 'rating': 4.2, 'reviews': 2200, 'nightly_rate_inr': 4200, 'amenities': ['Free WiFi', 'Bar', 'Lounge', 'Historic']},
        {'name': 'The Hoxton Holborn', 'location': 'London - Holborn, High Holborn Street', 'category': 'Premium', 'stars': 4, 'rating': 4.6, 'reviews': 3200, 'nightly_rate_inr': 15000, 'amenities': ['Free WiFi', 'Restaurant', 'Bar', 'Co-working']},
        {'name': 'The Ritz London', 'location': 'London - Piccadilly, Near Green Park', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 2500, 'nightly_rate_inr': 65000, 'amenities': ['Fine Dining', 'Spa', 'Butler', 'Afternoon Tea']}
    ],
    'Switzerland': [
        {'name': 'Youth Hostel Interlaken', 'location': 'Interlaken - Near Interlaken Ost Train Station', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 1800, 'nightly_rate_inr': 3800, 'amenities': ['Free WiFi', 'Breakfast', 'Garden', 'Games Room']},
        {'name': 'The Yard Hostel', 'location': 'Geneva - City Center, Rue du Perron', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 1200, 'nightly_rate_inr': 4200, 'amenities': ['Free WiFi', 'Kitchen', 'Lounge', 'Bar']},
        {'name': 'City Backpacker Zurich', 'location': 'Zurich - Niederdorf, Old Town', 'category': 'Standard', 'stars': 3, 'rating': 4.3, 'reviews': 1000, 'nightly_rate_inr': 5200, 'amenities': ['Free WiFi', 'Kitchen', 'Lounge', 'Central']},
        {'name': 'Hotel Bellevue', 'location': 'Interlaken - Höheweg (Main Street)', 'category': 'Premium', 'stars': 4, 'rating': 4.7, 'reviews': 2200, 'nightly_rate_inr': 18000, 'amenities': ['Mountain View', 'Spa', 'Restaurant', 'Bar']},
        {'name': "Badrutt's Palace", 'location': 'St. Moritz - Center, Via Serlas', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 1500, 'nightly_rate_inr': 75000, 'amenities': ['Ski-in/Ski-out', 'Spa', 'Fine Dining', 'Butler']}
    ],
    'Greece': [
        {'name': 'Athens Backpackers', 'location': 'Athens - Makrigianni, Near Acropolis Museum', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 1500, 'nightly_rate_inr': 2500, 'amenities': ['Free WiFi', 'AC', 'Rooftop Bar', 'Acropolis View']},
        {'name': 'Santorini Hostel', 'location': 'Santorini - Fira, Main Town', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 800, 'nightly_rate_inr': 3000, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Caldera View']},
        {'name': 'Caveland', 'location': 'Santorini - Karterados Village', 'category': 'Standard', 'stars': 3, 'rating': 4.6, 'reviews': 600, 'nightly_rate_inr': 4500, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Cave Rooms']},
        {'name': 'Hotel Grande Bretagne', 'location': 'Athens - Syntagma Square, City Center', 'category': 'Luxury', 'stars': 5, 'rating': 4.8, 'reviews': 2500, 'nightly_rate_inr': 42000, 'amenities': ['Acropolis View', 'Spa', 'Fine Dining', 'Rooftop Pool']}
    ],
    'Spain': [
        {'name': 'Generator Barcelona', 'location': 'Barcelona - Gràcia, Carrer de Còrsega', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 3000, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Rooftop']},
        {'name': 'The Hat Madrid', 'location': 'Madrid - Plaza Mayor, City Center', 'category': 'Budget', 'stars': 3, 'rating': 4.6, 'reviews': 2500, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'AC', 'Rooftop Bar', 'Central']},
        {'name': 'Ostello Bello', 'location': 'Barcelona - Eixample, Carrer de Girona', 'category': 'Standard', 'stars': 3, 'rating': 4.5, 'reviews': 1800, 'nightly_rate_inr': 4200, 'amenities': ['Free WiFi', 'AC', 'Terrace', 'Bar']},
        {'name': 'Hotel Casa Fuster', 'location': 'Barcelona - Passeig de Gràcia, Eixample', 'category': 'Luxury', 'stars': 5, 'rating': 4.8, 'reviews': 2000, 'nightly_rate_inr': 35000, 'amenities': ['Spa', 'Rooftop Pool', 'Fine Dining', 'Modernist']}
    ],
    'USA': [
        {'name': 'HI New York Hostel', 'location': 'New York - Upper West Side, Amsterdam Ave', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 3500, 'nightly_rate_inr': 4500, 'amenities': ['Free WiFi', 'AC', 'Kitchen', 'Garden']},
        {'name': 'The Green Tortoise', 'location': 'San Francisco - North Beach, Columbus Ave', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 1500, 'nightly_rate_inr': 4000, 'amenities': ['Free WiFi', 'Breakfast', 'Kitchen', 'Lounge']},
        {'name': 'Freehand Los Angeles', 'location': 'Los Angeles - Downtown, S Olive Street', 'category': 'Standard', 'stars': 4, 'rating': 4.3, 'reviews': 2800, 'nightly_rate_inr': 8500, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Rooftop Bar']},
        {'name': 'The Standard High Line', 'location': 'New York - Meatpacking District, Washington St', 'category': 'Premium', 'stars': 4, 'rating': 4.5, 'reviews': 3200, 'nightly_rate_inr': 25000, 'amenities': ['Free WiFi', 'Rooftop Bar', 'Gym', 'City View']},
        {'name': 'The Plaza Hotel', 'location': 'New York - Central Park South, 5th Avenue', 'category': 'Luxury', 'stars': 5, 'rating': 4.7, 'reviews': 4500, 'nightly_rate_inr': 55000, 'amenities': ['Spa', 'Fine Dining', 'Butler', 'Central Park View']}
    ],
    'Canada': [
        {'name': 'Samesun Banff', 'location': 'Banff - Banff Avenue, Town Center', 'category': 'Budget', 'stars': 3, 'rating': 4.6, 'reviews': 1800, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'Kitchen', 'Bar', 'Lounge']},
        {'name': 'HI Vancouver', 'location': 'Vancouver - Downtown, Granville Street', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 2200, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'Kitchen', 'Lounge', 'Activities']},
        {'name': 'The Only Backpackers', 'location': 'Toronto - Downtown, King Street West', 'category': 'Standard', 'stars': 3, 'rating': 4.3, 'reviews': 1200, 'nightly_rate_inr': 4200, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Games Room']},
        {'name': 'Fairmont Banff Springs', 'location': 'Banff - Spray Avenue, Near Bow Falls', 'category': 'Luxury', 'stars': 5, 'rating': 4.8, 'reviews': 3500, 'nightly_rate_inr': 38000, 'amenities': ['Spa', 'Golf', 'Fine Dining', 'Mountain View']}
    ],
    'Peru': [
        {'name': 'Pariwana Hostel', 'location': 'Cusco - Plaza de Armas, City Center', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 1500, 'nightly_rate_inr': 1200, 'amenities': ['Free WiFi', 'Breakfast', 'Bar', 'Terrace']},
        {'name': 'Wild Rover Hostel', 'location': 'Cusco - Centro Histórico, Near Plaza', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 2000, 'nightly_rate_inr': 1000, 'amenities': ['Free WiFi', 'Bar', 'Restaurant', 'Activities']},
        {'name': 'Kokopelli Hostel', 'location': 'Lima - Miraflores, Near Larcomar', 'category': 'Standard', 'stars': 3, 'rating': 4.6, 'reviews': 1800, 'nightly_rate_inr': 1800, 'amenities': ['Free WiFi', 'Breakfast', 'Bar', 'Ocean View']},
        {'name': 'Belmond Sanctuary Lodge', 'location': 'Machu Picchu - Entrance Gate, Citadel', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 800, 'nightly_rate_inr': 85000, 'amenities': ['Machu Picchu View', 'Fine Dining', 'Spa', 'Exclusive']}
    ],
    'Australia': [
        {'name': 'YHA Sydney Harbour', 'location': 'Sydney - The Rocks, Near Circular Quay', 'category': 'Budget', 'stars': 4, 'rating': 4.7, 'reviews': 2500, 'nightly_rate_inr': 3800, 'amenities': ['Free WiFi', 'AC', 'Rooftop', 'Harbour View']},
        {'name': 'Base Backpackers', 'location': 'Sydney - CBD, Kent Street', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 3000, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Lounge']},
        {'name': 'Nomads Melbourne', 'location': 'Melbourne - CBD, Little Collins Street', 'category': 'Standard', 'stars': 3, 'rating': 4.3, 'reviews': 2200, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'AC', 'Bar', 'Kitchen']},
        {'name': 'Park Hyatt Sydney', 'location': 'Sydney - The Rocks, Dawes Point', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 1800, 'nightly_rate_inr': 58000, 'amenities': ['Opera House View', 'Spa', 'Fine Dining', 'Butler']}
    ],
    'New Zealand': [
        {'name': 'Nomads Queenstown', 'location': 'Queenstown - City Center, Shotover Street', 'category': 'Budget', 'stars': 3, 'rating': 4.5, 'reviews': 2000, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'Bar', 'Lounge', 'Activities']},
        {'name': 'YHA Auckland', 'location': 'Auckland - City Center, City Road', 'category': 'Budget', 'stars': 3, 'rating': 4.4, 'reviews': 1800, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'Kitchen', 'Lounge', 'Central']},
        {'name': 'Base Backpackers', 'location': 'Wellington - Courtenay Place, City Center', 'category': 'Standard', 'stars': 3, 'rating': 4.3, 'reviews': 1500, 'nightly_rate_inr': 3800, 'amenities': ['Free WiFi', 'Bar', 'Kitchen', 'Central']},
        {'name': 'Matakauri Lodge', 'location': 'Queenstown - Lake Wakatipu, Sunshine Bay', 'category': 'Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 900, 'nightly_rate_inr': 95000, 'amenities': ['Lake View', 'Spa', 'Fine Dining', 'Butler']}
    ],
    'UAE': [
        {'name': 'Dubai Youth Hostel', 'location': 'Dubai - Al Barsha, Near Mall of Emirates', 'category': 'Budget', 'stars': 3, 'rating': 4.2, 'reviews': 1200, 'nightly_rate_inr': 3500, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Restaurant']},
        {'name': 'At the Top Hostel', 'location': 'Dubai - Deira, Near Gold Souk', 'category': 'Budget', 'stars': 3, 'rating': 4.3, 'reviews': 900, 'nightly_rate_inr': 3200, 'amenities': ['Free WiFi', 'AC', 'Lounge', 'Central']},
        {'name': 'Rove Downtown', 'location': 'Dubai - Downtown, Near Burj Khalifa', 'category': 'Standard', 'stars': 3, 'rating': 4.6, 'reviews': 3500, 'nightly_rate_inr': 6500, 'amenities': ['Free WiFi', 'AC', 'Pool', 'Burj View']},
        {'name': 'Atlantis The Palm', 'location': 'Dubai - Palm Jumeirah, Crescent Road', 'category': 'Luxury', 'stars': 5, 'rating': 4.7, 'reviews': 12000, 'nightly_rate_inr': 45000, 'amenities': ['Water Park', 'Aquarium', 'Spa', 'Beach']},
        {'name': 'Burj Al Arab', 'location': 'Dubai - Jumeirah Beach, Umm Suqeim', 'category': 'Ultra-Luxury', 'stars': 5, 'rating': 4.9, 'reviews': 5000, 'nightly_rate_inr': 125000, 'amenities': ['Butler', 'Helipad', 'Private Beach', 'Michelin Dining']}
    ],
    'Maldives': [
        {'name': 'Hulhumale Inn', 'location': 'Maldives - Hulhumale Island, Near Airport', 'category': 'Budget', 'stars': 3, 'rating': 4.2, 'reviews': 800, 'nightly_rate_inr': 4500, 'amenities': ['Free WiFi', 'AC', 'Beach Access', 'Restaurant']},
        {'name': 'Maafushi Village', 'location': 'Maldives - Maafushi Island, South Male Atoll', 'category': 'Budget', 'stars': 3, 'rating': 4.3, 'reviews': 1200, 'nightly_rate_inr': 5000, 'amenities': ['Free WiFi', 'AC', 'Beach', 'Water Sports']},
        {'name': 'Island Budget Stay', 'location': 'Maldives - Male City, Near Ferry Terminal', 'category': 'Standard', 'stars': 3, 'rating': 4.1, 'reviews': 600, 'nightly_rate_inr': 6000, 'amenities': ['Free WiFi', 'AC', 'Restaurant', 'Ferry Access']},
        {'name': 'Soneva Jani', 'location': 'Maldives - Medhufaru Island, Noonu Atoll', 'category': 'Luxury', 'stars': 5, 'rating': 5.0, 'reviews': 400, 'nightly_rate_inr': 250000, 'amenities': ['Overwater Villa', 'Private Pool', 'Observatory', 'Butler']}
    ]
}

def get_hotels_for_destination(destination):
    country = destination['country']
    if country in HOTEL_DATABASE:
        return HOTEL_DATABASE[country]
    else:
        return [
            {'name': f'Budget Stay {country}', 'location': f'{country} - City Center', 'category': 'Budget', 'stars': 3, 'rating': 4.0, 'reviews': 500, 'nightly_rate_inr': 2500, 'amenities': ['Free WiFi', 'AC']},
            {'name': f'Comfort Hotel {country}', 'location': f'{country} - Downtown', 'category': 'Standard', 'stars': 3, 'rating': 4.3, 'reviews': 800, 'nightly_rate_inr': 5500, 'amenities': ['Free WiFi', 'AC', 'Breakfast']},
            {'name': f'Grand {country} Hotel', 'location': f'{country} - Prime Area', 'category': 'Luxury', 'stars': 5, 'rating': 4.7, 'reviews': 1500, 'nightly_rate_inr': 25000, 'amenities': ['Spa', 'Pool', 'Fine Dining']}
        ]

def get_cheapest_hotel(country):
    hotels = HOTEL_DATABASE.get(country, [])
    if hotels:
        return min(hotels, key=lambda x: x['nightly_rate_inr'])
    return None

# Famous landmarks database with background images
COUNTRY_BACKGROUNDS = {
    'France': {'flag': '🇫🇷', 'landmark': '🗼 Eiffel Tower', 'image': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800', 'description': 'City of Lights', 'capital': 'Paris'},
    'Japan': {'flag': '🇯🇵', 'landmark': '🗻 Mount Fuji', 'image': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800', 'description': 'Land of the Rising Sun', 'capital': 'Tokyo'},
    'UAE': {'flag': '🇦🇪', 'landmark': '🏙️ Burj Khalifa', 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800', 'description': 'City of Gold', 'capital': 'Abu Dhabi'},
    'Indonesia': {'flag': '🇮🇩', 'landmark': '🛕 Tanah Lot', 'image': 'https://images.unsplash.com/photo-1537996192471-5f26c3e1c7e6?w=800', 'description': 'Island of Gods', 'capital': 'Jakarta'},
    'USA': {'flag': '🇺🇸', 'landmark': '🗽 Statue of Liberty', 'image': 'https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?w=800', 'description': 'The Big Apple', 'capital': 'Washington D.C.'},
    'Italy': {'flag': '🇮🇹', 'landmark': '🏛️ Colosseum', 'image': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800', 'description': 'Eternal City', 'capital': 'Rome'},
    'United Kingdom': {'flag': '🇬🇧', 'landmark': '🕰️ Big Ben', 'image': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800', 'description': 'London Calling', 'capital': 'London'},
    'Australia': {'flag': '🇦🇺', 'landmark': '🏛️ Sydney Opera House', 'image': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800', 'description': 'Down Under', 'capital': 'Canberra'},
    'Thailand': {'flag': '🇹🇭', 'landmark': '🛕 Wat Arun', 'image': 'https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800', 'description': 'Land of Smiles', 'capital': 'Bangkok'},
    'India': {'flag': '🇮🇳', 'landmark': '🕌 Taj Mahal', 'image': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800', 'description': 'Incredible India', 'capital': 'New Delhi'},
    'Singapore': {'flag': '🇸🇬', 'landmark': '🏨 Marina Bay Sands', 'image': 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800', 'description': 'Lion City', 'capital': 'Singapore'},
    'Switzerland': {'flag': '🇨🇭', 'landmark': '⛰️ Matterhorn', 'image': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=800', 'description': 'Heaven on Earth', 'capital': 'Bern'},
    'Canada': {'flag': '🇨🇦', 'landmark': '🍁 CN Tower', 'image': 'https://images.unsplash.com/photo-1517935706615-2717063c2225?w=800', 'description': 'Great White North', 'capital': 'Ottawa'},
    'New Zealand': {'flag': '🇳🇿', 'landmark': '🏔️ Milford Sound', 'image': 'https://images.unsplash.com/photo-1469796466635-455e9406263f?w=800', 'description': 'Adventure Capital', 'capital': 'Wellington'},
    'Maldives': {'flag': '🇲🇻', 'landmark': '🏝️ Overwater Bungalows', 'image': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800', 'description': 'Tropical Paradise', 'capital': 'Male'},
    'Peru': {'flag': '🇵🇪', 'landmark': '🏔️ Machu Picchu', 'image': 'https://images.unsplash.com/photo-1526392064735-418b8c6f5c5b?w=800', 'description': 'Ancient Wonders', 'capital': 'Lima'},
    'Greece': {'flag': '🇬🇷', 'landmark': '🏛️ Parthenon', 'image': 'https://images.unsplash.com/photo-1533577116850-9cc66cad8a9b?w=800', 'description': 'Cradle of Civilization', 'capital': 'Athens'},
    'Spain': {'flag': '🇪🇸', 'landmark': '🏟️ Sagrada Familia', 'image': 'https://images.unsplash.com/photo-1543783207-ec64e4d95325?w=800', 'description': 'Vibrant Culture', 'capital': 'Madrid'}
}

# Currency conversion rates (INR as base)
CURRENCY_RATES = {
    'INR': 1.0, 'USD': 83.5, 'EUR': 90.2, 'GBP': 105.3, 'JPY': 0.55,
    'AUD': 54.8, 'AED': 22.7, 'SGD': 61.9, 'CAD': 61.2, 'CHF': 94.5,
    'NOK': 7.8, 'NZD': 51.2, 'MVR': 5.4, 'PEN': 22.3, 'THB': 2.3,
    'IDR': 0.0054, 'EGP': 1.7, 'TRY': 2.6
}

# ============================================================
# DESTINATION GENERATOR (Full list with all 19 destinations)
# ============================================================
def generate_destinations():
    destinations = [
        {'name': 'Tokyo, Japan', 'country': 'Japan', 'flag': '🇯🇵', 'landmark': 'Mount Fuji', 'landmark_emoji': '🗻', 'description': 'Futuristic metropolis with traditional temples and amazing food', 'long_description': 'Tokyo seamlessly blends the ultramodern with the traditional.', 'best_time': 'March-May', 'avg_cost_per_day': 25000, 'weather': random.choice(['Sunny', 'Cloudy']), 'temperature': random.randint(10, 25), 'safety_score': 9.5, 'solo_female_safety': 9.5, 'attractions': [{'name': 'Shibuya Crossing', 'description': 'Busiest crossing', 'best_time': 'Evening'}, {'name': 'Senso-ji Temple', 'description': 'Ancient temple', 'best_time': 'Morning'}], 'foods': ['Sushi', 'Ramen', 'Tempura'], 'local_tips': ['Get a Suica card', 'Learn basic Japanese'], 'group_friendly': ['Solo', 'Couple', 'Family with Kids', 'Friends Group'], 'interest_tags': ['Mountains', 'Food', 'Cultural'], 'language': 'Japanese', 'currency': 'JPY', 'safe_areas': ['Shibuya', 'Shinjuku'], 'unsafe_areas': ['Kabukicho at night'], 'emergency_numbers': {'Police': '110', 'Ambulance': '119'}},
        {'name': 'Singapore', 'country': 'Singapore', 'flag': '🇸🇬', 'landmark': 'Marina Bay Sands', 'landmark_emoji': '🏨', 'description': 'Clean, safe, and modern city-state', 'long_description': 'A futuristic city-state.', 'best_time': 'February-April', 'avg_cost_per_day': 22000, 'weather': random.choice(['Sunny', 'Rainy']), 'temperature': random.randint(26, 32), 'safety_score': 9.3, 'solo_female_safety': 9.3, 'attractions': [{'name': 'Marina Bay Sands', 'description': 'Iconic hotel', 'best_time': 'Sunset'}, {'name': 'Gardens by the Bay', 'description': 'Supertree Grove', 'best_time': 'Evening'}], 'foods': ['Chicken Rice', 'Chili Crab', 'Laksa'], 'local_tips': ['Don\'t litter', 'Use Grab'], 'group_friendly': ['Solo', 'Couple', 'Family with Kids'], 'interest_tags': ['Food', 'Modern', 'Shopping'], 'language': 'English', 'currency': 'SGD', 'safe_areas': ['Marina Bay', 'Orchard'], 'unsafe_areas': ['Geylang at night'], 'emergency_numbers': {'Police': '999', 'Ambulance': '995'}},
        {'name': 'Bali, Indonesia', 'country': 'Indonesia', 'flag': '🇮🇩', 'landmark': 'Tanah Lot Temple', 'landmark_emoji': '🛕', 'description': 'Tropical paradise with beautiful beaches', 'long_description': 'Island of the Gods.', 'best_time': 'May-September', 'avg_cost_per_day': 12000, 'weather': random.choice(['Sunny', 'Rainy']), 'temperature': random.randint(25, 32), 'safety_score': 7.2, 'solo_female_safety': 6.8, 'attractions': [{'name': 'Tanah Lot', 'description': 'Temple on rock', 'best_time': 'Sunset'}, {'name': 'Uluwatu', 'description': 'Clifftop temple', 'best_time': 'Sunset'}], 'foods': ['Nasi Goreng', 'Babi Guling', 'Satay'], 'local_tips': ['Rent scooter', 'Respect temples'], 'group_friendly': ['Couple', 'Friends Group', 'Solo'], 'interest_tags': ['Beaches', 'Mountains', 'Cultural'], 'language': 'Indonesian', 'currency': 'IDR', 'safe_areas': ['Ubud', 'Seminyak'], 'unsafe_areas': ['Remote beaches'], 'emergency_numbers': {'Police': '110', 'Ambulance': '118'}},
        {'name': 'Phuket, Thailand', 'country': 'Thailand', 'flag': '🇹🇭', 'landmark': 'Phi Phi Islands', 'landmark_emoji': '🏝️', 'description': 'Stunning beaches and vibrant nightlife', 'long_description': 'Thailand\'s largest island.', 'best_time': 'November-April', 'avg_cost_per_day': 10000, 'weather': random.choice(['Sunny', 'Rainy']), 'temperature': random.randint(28, 34), 'safety_score': 7.0, 'solo_female_safety': 6.5, 'attractions': [{'name': 'Phi Phi Islands', 'description': 'Archipelago', 'best_time': 'Morning'}, {'name': 'Patong Beach', 'description': 'Main beach', 'best_time': 'Evening'}], 'foods': ['Pad Thai', 'Tom Yum', 'Green Curry'], 'local_tips': ['Bargain at markets', 'Cover up at temples'], 'group_friendly': ['Friends Group', 'Couple'], 'interest_tags': ['Beaches', 'Food', 'Adventure'], 'language': 'Thai', 'currency': 'THB', 'safe_areas': ['Patong', 'Kata'], 'unsafe_areas': ['Remote beaches'], 'emergency_numbers': {'Police': '191', 'Ambulance': '1669'}},
        {'name': 'Jaipur, India', 'country': 'India', 'flag': '🇮🇳', 'landmark': 'Hawa Mahal', 'landmark_emoji': '🏰', 'description': 'The Pink City with magnificent palaces', 'long_description': 'Capital of Rajasthan.', 'best_time': 'October-March', 'avg_cost_per_day': 5000, 'weather': random.choice(['Sunny', 'Clear']), 'temperature': random.randint(22, 32), 'safety_score': 7.0, 'solo_female_safety': 6.5, 'attractions': [{'name': 'Hawa Mahal', 'description': 'Palace of Winds', 'best_time': 'Morning'}, {'name': 'Amber Fort', 'description': 'Hilltop fort', 'best_time': 'Morning'}], 'foods': ['Dal Baati', 'Laal Maas'], 'local_tips': ['Hire guide', 'Drink bottled water'], 'group_friendly': ['Family with Kids', 'Couple'], 'interest_tags': ['Historical', 'Cultural', 'Food'], 'language': 'Hindi', 'currency': 'INR', 'safe_areas': ['MI Road', 'C-Scheme'], 'unsafe_areas': ['Isolated areas'], 'emergency_numbers': {'Police': '100', 'Ambulance': '102'}},
        {'name': 'Agra, India', 'country': 'India', 'flag': '🇮🇳', 'landmark': 'Taj Mahal', 'landmark_emoji': '🕌', 'description': 'Home to the iconic Taj Mahal', 'long_description': 'One of the Seven Wonders.', 'best_time': 'October-March', 'avg_cost_per_day': 4500, 'weather': random.choice(['Sunny', 'Clear']), 'temperature': random.randint(20, 35), 'safety_score': 6.5, 'solo_female_safety': 6.0, 'attractions': [{'name': 'Taj Mahal', 'description': 'White marble mausoleum', 'best_time': 'Sunrise'}, {'name': 'Agra Fort', 'description': 'Red sandstone fort', 'best_time': 'Afternoon'}], 'foods': ['Petha', 'Mughlai'], 'local_tips': ['Visit Taj at sunrise', 'Avoid touts'], 'group_friendly': ['Family with Kids', 'Couple'], 'interest_tags': ['Historical', 'Cultural'], 'language': 'Hindi', 'currency': 'INR', 'safe_areas': ['Taj Ganj'], 'unsafe_areas': ['Outskirts'], 'emergency_numbers': {'Police': '100', 'Ambulance': '102'}},
        {'name': 'Paris, France', 'country': 'France', 'flag': '🇫🇷', 'landmark': 'Eiffel Tower', 'landmark_emoji': '🗼', 'description': 'City of Love', 'long_description': 'The City of Light.', 'best_time': 'April-June', 'avg_cost_per_day': 21000, 'weather': random.choice(['Sunny', 'Cloudy']), 'temperature': random.randint(15, 28), 'safety_score': 7.5, 'solo_female_safety': 7.0, 'attractions': [{'name': 'Eiffel Tower', 'description': 'Iconic tower', 'best_time': 'Sunset'}, {'name': 'Louvre', 'description': 'Art museum', 'best_time': 'Morning'}], 'foods': ['Croissant', 'Baguette', 'Macarons'], 'local_tips': ['Learn French', 'Watch pickpockets'], 'group_friendly': ['Couple', 'Family with Kids'], 'interest_tags': ['Historical', 'Food', 'Romantic'], 'language': 'French', 'currency': 'EUR', 'safe_areas': ['Le Marais'], 'unsafe_areas': ['Northern suburbs'], 'emergency_numbers': {'Police': '17', 'Ambulance': '15'}},
        {'name': 'Rome, Italy', 'country': 'Italy', 'flag': '🇮🇹', 'landmark': 'Colosseum', 'landmark_emoji': '🏛️', 'description': 'Ancient history and incredible food', 'long_description': 'The Eternal City.', 'best_time': 'April-June', 'avg_cost_per_day': 18000, 'weather': random.choice(['Sunny', 'Cloudy']), 'temperature': random.randint(15, 28), 'safety_score': 7.8, 'solo_female_safety': 7.2, 'attractions': [{'name': 'Colosseum', 'description': 'Amphitheater', 'best_time': 'Morning'}, {'name': 'Vatican', 'description': 'Smallest country', 'best_time': 'Morning'}], 'foods': ['Carbonara', 'Pizza', 'Gelato'], 'local_tips': ['Book in advance', 'Cover up in churches'], 'group_friendly': ['Family with Kids', 'Couple'], 'interest_tags': ['Historical', 'Food'], 'language': 'Italian', 'currency': 'EUR', 'safe_areas': ['Trastevere'], 'unsafe_areas': ['Termini at night'], 'emergency_numbers': {'Police': '112', 'Ambulance': '118'}},
        {'name': 'London, UK', 'country': 'United Kingdom', 'flag': '🇬🇧', 'landmark': 'Big Ben', 'landmark_emoji': '🕰️', 'description': 'Historic city with royal palaces', 'long_description': 'A global city.', 'best_time': 'May-September', 'avg_cost_per_day': 23000, 'weather': random.choice(['Cloudy', 'Rainy']), 'temperature': random.randint(10, 22), 'safety_score': 8.0, 'solo_female_safety': 7.8, 'attractions': [{'name': 'Big Ben', 'description': 'Clock tower', 'best_time': 'Day'}, {'name': 'London Eye', 'description': 'Observation wheel', 'best_time': 'Sunset'}], 'foods': ['Fish and Chips', 'Tea'], 'local_tips': ['Get Oyster card'], 'group_friendly': ['Family with Kids', 'Couple'], 'interest_tags': ['Historical', 'Cultural'], 'language': 'English', 'currency': 'GBP', 'safe_areas': ['Kensington'], 'unsafe_areas': ['Some Hackney areas'], 'emergency_numbers': {'Police': '999', 'Ambulance': '999'}},
        {'name': 'Swiss Alps, Switzerland', 'country': 'Switzerland', 'flag': '🇨🇭', 'landmark': 'Matterhorn', 'landmark_emoji': '⛰️', 'description': 'Stunning Alps', 'long_description': 'Picture-perfect alpine scenery.', 'best_time': 'June-September', 'avg_cost_per_day': 28000, 'weather': random.choice(['Sunny', 'Snow']), 'temperature': random.randint(0, 22), 'safety_score': 9.0, 'solo_female_safety': 9.0, 'attractions': [{'name': 'Matterhorn', 'description': 'Iconic mountain', 'best_time': 'Sunrise'}, {'name': 'Jungfraujoch', 'description': 'Top of Europe', 'best_time': 'Morning'}], 'foods': ['Fondue', 'Chocolate'], 'local_tips': ['Get Travel Pass'], 'group_friendly': ['Family with Kids', 'Couple', 'Solo'], 'interest_tags': ['Mountains', 'Snow'], 'language': 'German', 'currency': 'CHF', 'safe_areas': ['Zurich', 'Geneva'], 'unsafe_areas': ['Isolated trails'], 'emergency_numbers': {'Police': '117', 'Ambulance': '144'}},
        {'name': 'Santorini, Greece', 'country': 'Greece', 'flag': '🇬🇷', 'landmark': 'Caldera View', 'landmark_emoji': '🏝️', 'description': 'Stunning sunsets', 'long_description': 'The most romantic Greek Island.', 'best_time': 'May-October', 'avg_cost_per_day': 20000, 'weather': random.choice(['Sunny', 'Clear']), 'temperature': random.randint(20, 30), 'safety_score': 8.5, 'solo_female_safety': 8.2, 'attractions': [{'name': 'Oia Sunset', 'description': 'Famous sunset', 'best_time': 'Sunset'}, {'name': 'Red Beach', 'description': 'Red sand beach', 'best_time': 'Morning'}], 'foods': ['Seafood', 'Greek Salad'], 'local_tips': ['Book sunset dinner'], 'group_friendly': ['Couple', 'Friends Group'], 'interest_tags': ['Beaches', 'Romantic'], 'language': 'Greek', 'currency': 'EUR', 'safe_areas': ['Fira', 'Oia'], 'unsafe_areas': ['Very safe'], 'emergency_numbers': {'Police': '100', 'Ambulance': '166'}},
        {'name': 'Barcelona, Spain', 'country': 'Spain', 'flag': '🇪🇸', 'landmark': 'Sagrada Familia', 'landmark_emoji': '🏟️', 'description': 'Gaudí architecture', 'long_description': 'A Mediterranean gem.', 'best_time': 'May-June', 'avg_cost_per_day': 19000, 'weather': random.choice(['Sunny', 'Clear']), 'temperature': random.randint(18, 28), 'safety_score': 7.5, 'solo_female_safety': 7.2, 'attractions': [{'name': 'Sagrada Familia', 'description': 'Gaudí masterpiece', 'best_time': 'Morning'}, {'name': 'Park Güell', 'description': 'Colorful park', 'best_time': 'Afternoon'}], 'foods': ['Paella', 'Tapas'], 'local_tips': ['Book Gaudí sites'], 'group_friendly': ['Friends Group', 'Couple'], 'interest_tags': ['Cultural', 'Food', 'Beaches'], 'language': 'Spanish', 'currency': 'EUR', 'safe_areas': ['Eixample'], 'unsafe_areas': ['La Rambla at night'], 'emergency_numbers': {'Police': '112', 'Ambulance': '061'}},
        {'name': 'New York, USA', 'country': 'USA', 'flag': '🇺🇸', 'landmark': 'Statue of Liberty', 'landmark_emoji': '🗽', 'description': 'The city that never sleeps', 'long_description': 'The Big Apple.', 'best_time': 'September-November', 'avg_cost_per_day': 26000, 'weather': random.choice(['Sunny', 'Cloudy']), 'temperature': random.randint(5, 30), 'safety_score': 7.0, 'solo_female_safety': 6.5, 'attractions': [{'name': 'Statue of Liberty', 'description': 'Symbol of freedom', 'best_time': 'Morning'}, {'name': 'Times Square', 'description': 'Bright lights', 'best_time': 'Evening'}], 'foods': ['Pizza', 'Bagels'], 'local_tips': ['Get MetroCard'], 'group_friendly': ['Family with Kids', 'Friends Group'], 'interest_tags': ['Modern', 'Cultural'], 'language': 'English', 'currency': 'USD', 'safe_areas': ['Upper East Side'], 'unsafe_areas': ['Some Bronx areas'], 'emergency_numbers': {'Police': '911', 'Ambulance': '911'}},
        {'name': 'Banff, Canada', 'country': 'Canada', 'flag': '🇨🇦', 'landmark': 'Lake Louise', 'landmark_emoji': '🏞️', 'description': 'Spectacular mountains', 'long_description': 'Jewel of the Rockies.', 'best_time': 'June-September', 'avg_cost_per_day': 24000, 'weather': random.choice(['Sunny', 'Snow']), 'temperature': random.randint(-5, 22), 'safety_score': 8.8, 'solo_female_safety': 8.8, 'attractions': [{'name': 'Lake Louise', 'description': 'Turquoise lake', 'best_time': 'Sunrise'}, {'name': 'Moraine Lake', 'description': 'Spectacular lake', 'best_time': 'Morning'}], 'foods': ['Poutine', 'Maple Syrup'], 'local_tips': ['Book early'], 'group_friendly': ['Family with Kids', 'Couple'], 'interest_tags': ['Mountains', 'Snow'], 'language': 'English', 'currency': 'CAD', 'safe_areas': ['Banff Town'], 'unsafe_areas': ['Very safe'], 'emergency_numbers': {'Police': '911', 'Ambulance': '911'}},
        {'name': 'Machu Picchu, Peru', 'country': 'Peru', 'flag': '🇵🇪', 'landmark': 'Machu Picchu', 'landmark_emoji': '🏔️', 'description': 'Ancient Incan citadel', 'long_description': 'New Seven Wonder.', 'best_time': 'May-September', 'avg_cost_per_day': 15000, 'weather': random.choice(['Sunny', 'Rainy']), 'temperature': random.randint(10, 22), 'safety_score': 6.8, 'solo_female_safety': 6.2, 'attractions': [{'name': 'Machu Picchu', 'description': 'Incan citadel', 'best_time': 'Sunrise'}, {'name': 'Inca Trail', 'description': 'Famous trek', 'best_time': 'May-Sep'}], 'foods': ['Ceviche', 'Lomo Saltado'], 'local_tips': ['Book early', 'Acclimatize'], 'group_friendly': ['Adventure', 'Couple'], 'interest_tags': ['Historical', 'Mountains'], 'language': 'Spanish', 'currency': 'PEN', 'safe_areas': ['Cusco'], 'unsafe_areas': ['Remote areas'], 'emergency_numbers': {'Police': '105', 'Ambulance': '106'}},
        {'name': 'Sydney, Australia', 'country': 'Australia', 'flag': '🇦🇺', 'landmark': 'Sydney Opera House', 'landmark_emoji': '🏛️', 'description': 'Stunning harbor', 'long_description': 'Australia\'s largest city.', 'best_time': 'September-November', 'avg_cost_per_day': 20000, 'weather': random.choice(['Sunny', 'Cloudy']), 'temperature': random.randint(18, 26), 'safety_score': 8.8, 'solo_female_safety': 8.5, 'attractions': [{'name': 'Opera House', 'description': 'Performing arts', 'best_time': 'Day'}, {'name': 'Bondi Beach', 'description': 'Famous beach', 'best_time': 'Morning'}], 'foods': ['Meat Pie', 'Lamington'], 'local_tips': ['Use Opal card'], 'group_friendly': ['Family with Kids', 'Couple'], 'interest_tags': ['Beaches', 'Nature'], 'language': 'English', 'currency': 'AUD', 'safe_areas': ['CBD', 'Bondi'], 'unsafe_areas': ['Kings Cross late night'], 'emergency_numbers': {'Police': '000', 'Ambulance': '000'}},
        {'name': 'Queenstown, New Zealand', 'country': 'New Zealand', 'flag': '🇳🇿', 'landmark': 'Milford Sound', 'landmark_emoji': '🏔️', 'description': 'Adventure capital', 'long_description': 'Adventure capital of the world.', 'best_time': 'December-February', 'avg_cost_per_day': 22000, 'weather': random.choice(['Sunny', 'Rainy']), 'temperature': random.randint(15, 25), 'safety_score': 9.0, 'solo_female_safety': 9.0, 'attractions': [{'name': 'Milford Sound', 'description': 'Fjord', 'best_time': 'Morning'}, {'name': 'Skyline Gondola', 'description': 'Panoramic views', 'best_time': 'Sunset'}], 'foods': ['Lamb', 'Pavlova'], 'local_tips': ['Book in advance'], 'group_friendly': ['Adventure', 'Couple'], 'interest_tags': ['Mountains', 'Adventure'], 'language': 'English', 'currency': 'NZD', 'safe_areas': ['Queenstown CBD'], 'unsafe_areas': ['Very safe'], 'emergency_numbers': {'Police': '111', 'Ambulance': '111'}},
        {'name': 'Dubai, UAE', 'country': 'UAE', 'flag': '🇦🇪', 'landmark': 'Burj Khalifa', 'landmark_emoji': '🏙️', 'description': 'Luxury destination', 'long_description': 'City of superlatives.', 'best_time': 'November-March', 'avg_cost_per_day': 30000, 'weather': random.choice(['Sunny', 'Clear']), 'temperature': random.randint(20, 35), 'safety_score': 8.5, 'solo_female_safety': 7.5, 'attractions': [{'name': 'Burj Khalifa', 'description': 'Tallest building', 'best_time': 'Sunset'}, {'name': 'Dubai Mall', 'description': 'Largest mall', 'best_time': 'Evening'}], 'foods': ['Shawarma', 'Hummus'], 'local_tips': ['Dress modestly'], 'group_friendly': ['Family with Kids', 'Couple'], 'interest_tags': ['Luxury', 'Modern'], 'language': 'Arabic', 'currency': 'AED', 'safe_areas': ['Marina'], 'unsafe_areas': ['Deira at night'], 'emergency_numbers': {'Police': '999', 'Ambulance': '998'}},
        {'name': 'Maldives', 'country': 'Maldives', 'flag': '🇲🇻', 'landmark': 'Overwater Bungalows', 'landmark_emoji': '🏝️', 'description': 'Tropical paradise', 'long_description': 'The ultimate tropical paradise.', 'best_time': 'November-April', 'avg_cost_per_day': 35000, 'weather': random.choice(['Sunny', 'Clear']), 'temperature': random.randint(27, 32), 'safety_score': 8.5, 'solo_female_safety': 7.8, 'attractions': [{'name': 'Overwater Bungalows', 'description': 'Iconic accommodation', 'best_time': 'All day'}, {'name': 'Male Atoll', 'description': 'Capital', 'best_time': 'Day'}], 'foods': ['Seafood', 'Mas Huni'], 'local_tips': ['Choose resort carefully'], 'group_friendly': ['Couple', 'Family with Kids'], 'interest_tags': ['Beaches', 'Romantic'], 'language': 'Dhivehi', 'currency': 'MVR', 'safe_areas': ['Resort Islands'], 'unsafe_areas': ['Very safe'], 'emergency_numbers': {'Police': '119', 'Ambulance': '102'}},
    ]
    return destinations

# ============================================================
# RATING FUNCTIONS
# ============================================================
def calculate_dynamic_rating(dest, travel_group, selected_interests):
    base_score = 3.0
    group_weights = {
        "Solo": {"Japan": +1.5, "Singapore": +1.5, "Switzerland": +1.0, "New Zealand": +1.0, "default": 0.0},
        "Couple": {"France": +1.5, "Italy": +1.5, "Maldives": +2.0, "Switzerland": +1.5, "default": 0.0},
        "Family with Kids": {"Singapore": +1.5, "Japan": +1.5, "USA": +1.0, "Australia": +1.5, "default": 0.0},
        "Friends Group": {"Thailand": +1.5, "Indonesia": +1.5, "USA": +1.0, "default": 0.0}
    }
    interest_weights = {
        "Mountains": {"Switzerland": +1.5, "Canada": +1.5, "New Zealand": +1.5, "default": 0.0},
        "Beaches": {"Maldives": +2.0, "Thailand": +1.5, "Indonesia": +1.5, "default": 0.0},
        "Historical": {"Italy": +1.5, "Greece": +1.5, "India": +1.5, "default": 0.0},
        "Snow": {"Switzerland": +1.5, "Canada": +1.5, "default": 0.0},
        "Food": {"Italy": +1.5, "France": +1.5, "Japan": +1.5, "default": 0.0}
    }
    country_name = dest['country']
    group_adjust = group_weights.get(travel_group, {}).get(country_name, 0)
    interest_adjust = 0
    for interest in selected_interests:
        if interest in interest_weights:
            interest_adjust += interest_weights[interest].get(country_name, 0)
    if selected_interests:
        interest_adjust /= len(selected_interests)
    safety_adjust = 0
    if travel_group == "Solo":
        current_trip = st.session_state.get('current_trip')
        if current_trip is not None and current_trip.get('is_solo_female', False):
            if dest['solo_female_safety'] >= 9.0: safety_adjust = +0.5
            elif dest['solo_female_safety'] >= 8.0: safety_adjust = +0.3
            elif dest['solo_female_safety'] < 7.0: safety_adjust = -0.3
    final_score = base_score + group_adjust + interest_adjust + safety_adjust
    return round(max(1, min(5, final_score)), 1)

def get_star_rating(rating):
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)
    return "★" * full_stars + ("½" if half_star else "") + "☆" * empty_stars

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">✈️ AI Travel Planner - Smart Travel Advisor</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🎯 Plan Your Journey")
    
    trip_name = st.text_input("Trip Name", "My Dream Vacation")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() + timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now() + timedelta(days=37))
    
    trip_duration = max(1, (end_date - start_date).days)
    nights = max(1, trip_duration - 1)
    st.info(f"📅 Duration: {trip_duration} days ({nights} nights)")
    
    st.markdown("### 👥 Travel Group")
    travel_group = st.radio("Who are you traveling with?", ["Solo", "Couple", "Family with Kids", "Friends Group"], horizontal=True)
    
    group_class = {"Solo": "group-solo", "Couple": "group-couple", "Family with Kids": "group-family", "Friends Group": "group-friends"}
    
    st.markdown("### 🎯 Your Interests")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        mountains = st.checkbox("🏔️ Mountains", value=True)
        beaches = st.checkbox("🏖️ Beaches", value=True)
        historical = st.checkbox("🏛️ Historical", value=True)
        waterfalls = st.checkbox("💦 Waterfalls", value=False)
    with col_i2:
        snow = st.checkbox("❄️ Snow", value=False)
        food = st.checkbox("🍜 Food", value=True)
        adventure = st.checkbox("🧗 Adventure", value=False)
        wildlife = st.checkbox("🦁 Wildlife", value=False)
    
    selected_interests = []
    if mountains: selected_interests.append("Mountains")
    if beaches: selected_interests.append("Beaches")
    if historical: selected_interests.append("Historical")
    if waterfalls: selected_interests.append("Waterfalls")
    if snow: selected_interests.append("Snow")
    if food: selected_interests.append("Food")
    if adventure: selected_interests.append("Adventure")
    if wildlife: selected_interests.append("Wildlife")
    
    st.markdown("### 💰 Budget Settings")
    currency = st.selectbox("Currency", list(CURRENCY_RATES.keys()))
    
    if currency == 'INR':
        budget_placeholder, min_budget, max_budget, step = 500000, 5000, 5000000, 5000
    else:
        budget_placeholder, min_budget, max_budget, step = 5000, 100, 50000, 100
    
    total_budget = st.number_input(f"Total Budget ({currency})", min_value=min_budget, max_value=max_budget, value=budget_placeholder, step=step)
    
    if currency != 'INR':
        st.caption(f"≈ ₹{total_budget * CURRENCY_RATES[currency]:,.0f} INR")
    
    st.markdown("### 👩 Solo Traveler Safety")
    is_solo_female = st.checkbox("I'm a solo female traveler", value=True)
    
    if st.button("🎯 Generate Recommendations", use_container_width=True):
        st.session_state.current_trip = {
            'name': trip_name,
            'start_date': start_date,
            'end_date': end_date,
            'duration': trip_duration,
            'nights': nights,
            'budget': total_budget,
            'currency': currency,
            'travel_group': travel_group,
            'interests': selected_interests,
            'is_solo_female': is_solo_female,
            'destinations': [],
            'selected_hotels': {},
            'created_at': datetime.now()
        }
        st.success("✅ Recommendations generated!")
        st.rerun()

# ============================================================
# MAIN TABS
# ============================================================
tab_main1, tab_main2, tab_main3, tab_main4, tab_main5 = st.tabs([
    "🌍 Destinations", "🏨 Hotels & Booking", "📸 Photo Blog",
    "👩 Solo Travel Safety", "🗺️ Trip Planner"
])

# ----- TAB 1: DESTINATIONS -----
with tab_main1:
    st.markdown("### 🗺️ Personalized Destinations")
    
    if travel_group and selected_interests:
        group_class_display = group_class.get(travel_group, "group-solo")
        st.markdown(f"""
        <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; padding: 1rem; background: white; border-radius: 10px;">
            <span class="group-badge {group_class_display}">👥 {travel_group}</span>
            {"".join([f'<span class="interest-badge">{"🏔️" if i=="Mountains" else "🏖️" if i=="Beaches" else "🏛️" if i=="Historical" else "💦" if i=="Waterfalls" else "❄️" if i=="Snow" else "🍜" if i=="Food" else "🧗" if i=="Adventure" else "🦁"} {i}</span>' for i in selected_interests])}
        </div>
        """, unsafe_allow_html=True)
    
    destinations = generate_destinations()
    for dest in destinations:
        dest['dynamic_rating'] = calculate_dynamic_rating(dest, travel_group, selected_interests)
        dest['stars'] = get_star_rating(dest['dynamic_rating'])
    destinations = sorted(destinations, key=lambda x: x['dynamic_rating'], reverse=True)
    
    for i in range(0, len(destinations), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(destinations):
                dest = destinations[i + j]
                with cols[j]:
                    bg = COUNTRY_BACKGROUNDS.get(dest['country'], COUNTRY_BACKGROUNDS['France'])
                    weather_class = dest['weather'].lower()
                    if dest['weather'] == 'Snow': weather_class = 'snow'
                    safety_class = 'safety-high' if dest['solo_female_safety'] >= 8 else 'safety-medium' if dest['solo_female_safety'] >= 6.5 else 'safety-low'
                    cost_in_currency = dest['avg_cost_per_day'] / CURRENCY_RATES[currency] if currency != 'INR' else dest['avg_cost_per_day']
                    
                    st.markdown(f"""
                    <div class="destination-card" style="background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url('{bg['image']}');">
                        <div class="destination-card-content">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                                <h3>{dest['flag']} {dest['name']} {dest['landmark_emoji']}</h3>
                                <span class="weather-badge {weather_class}">{dest['weather']} {dest['temperature']}°C</span>
                            </div>
                            <p><strong>Famous Landmark:</strong> {dest['landmark']}</p>
                            <p>{dest['description'][:100]}...</p>
                            <div style="display: flex; gap: 1rem; margin: 0.5rem 0; flex-wrap: wrap;">
                                <span>💰 {currency} {cost_in_currency:,.0f}/day</span>
                                <span class="{safety_class} safety-badge">👩 Safety: {dest['solo_female_safety']}/10</span>
                            </div>
                            <div style="margin: 0.5rem 0;">
                                <span class="star-rating">{dest['stars']}</span>
                                <span style="margin-left: 0.5rem; font-weight: bold;">({dest['dynamic_rating']}/5)</span>
                            </div>
                            <div style="margin-top: 0.5rem; display: flex; gap: 0.3rem; flex-wrap: wrap;">
                                {"".join([f'<span class="interest-badge">{tag}</span>' for tag in dest['interest_tags'][:3]])}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show cheapest hotel info
                    cheapest = get_cheapest_hotel(dest['country'])
                    if cheapest:
                        st.markdown(f"""
                        <div class="cheap-hotel-card">
                            <strong>💰 Cheapest Stay:</strong> {cheapest['name']}<br>
                            <small>📍 {cheapest['location']}</small><br>
                            <small>💵 ₹{cheapest['nightly_rate_inr']:,}/night • ⭐ {cheapest['rating']}/5</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        if st.button(f"➕ Add", key=f"add_{i+j}_{dest['country']}"):
                            if st.session_state.current_trip:
                                if not any(d['country'] == dest['country'] for d in st.session_state.current_trip['destinations']):
                                    st.session_state.current_trip['destinations'].append(dest)
                                    if dest['country'] not in st.session_state.photo_albums:
                                        st.session_state.photo_albums[dest['country']] = []
                                    st.success(f"✅ Added {dest['name']}!")
                                    st.rerun()
                                else:
                                    st.warning("Already added!")
                            else:
                                st.warning("Generate a trip plan first!")
                    with col_b:
                        if st.button(f"📸 Photos", key=f"photo_{i+j}_{dest['country']}"):
                            st.session_state.view_photos_country = dest['country']
                            st.session_state.selected_country = dest['country']
                            st.rerun()
                    with col_c:
                        if st.button(f"ℹ️ Details", key=f"details_{i+j}_{dest['country']}"):
                            st.session_state.show_place_details = dest['country']
                            st.rerun()
                    with col_d:
                        if st.button(f"⭐ Rate", key=f"rate_{i+j}_{dest['country']}"):
                            st.info(f"Rating: {dest['dynamic_rating']}/5 {dest['stars']}")

# ----- TAB 2: HOTELS & BOOKING -----
with tab_main2:
    st.markdown("### 🏨 Hotel Selection & Booking")
    
    if not st.session_state.current_trip:
        st.warning("⚠️ Please generate a trip plan first!")
    elif not st.session_state.current_trip['destinations']:
        st.info("👈 Add destinations first!")
    else:
        trip = st.session_state.current_trip
        nights_per_dest = max(1, trip['nights'] // len(trip['destinations']))
        
        # CHEAPEST TRIP SUMMARY
        st.markdown("### 💰 Cheapest Trip Cost Summary")
        
        cheapest_total = 0
        cheapest_details = []
        
        for dest in trip['destinations']:
            cheapest_hotel = get_cheapest_hotel(dest['country'])
            dest_nights = max(1, trip['nights'] // len(trip['destinations']))
            
            if cheapest_hotel:
                hotel_cost = cheapest_hotel['nightly_rate_inr'] * dest_nights
                activities_cost = dest['avg_cost_per_day'] * dest_nights
                total_dest = hotel_cost + activities_cost
                cheapest_total += total_dest
                cheapest_details.append({
                    'destination': dest['name'],
                    'flag': dest['flag'],
                    'hotel': cheapest_hotel['name'],
                    'location': cheapest_hotel['location'],
                    'hotel_cost': hotel_cost,
                    'activities_cost': activities_cost,
                    'total': total_dest,
                    'nights': dest_nights
                })
        
        st.markdown(f"""
        <div class="cheapest-highlight">
            <h2>💰 MINIMUM TRIP COST: ₹{cheapest_total:,.0f}</h2>
            <p>Using budget-friendly hotels for all destinations</p>
        </div>
        """, unsafe_allow_html=True)
        
        for detail in cheapest_details:
            st.markdown(f"""
            <div class="cheap-hotel-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h4>{detail['flag']} {detail['destination']}</h4>
                        <p><strong>🏨 Cheapest Hotel:</strong> {detail['hotel']}</p>
                        <p><strong>📍 Location:</strong> {detail['location']}</p>
                        <p><strong>🌙 Nights:</strong> {detail['nights']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p>🏨 Hotel: ₹{detail['hotel_cost']:,}</p>
                        <p>🎯 Activities: ₹{detail['activities_cost']:,}</p>
                        <p style="font-size: 1.3rem; font-weight: bold; color: #1B5E20;">Total: ₹{detail['total']:,}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🏨 All Available Hotels")
        
        for dest in trip['destinations']:
            dest_country = dest['country']
            
            with st.expander(f"🏨 {dest['flag']} {dest['name']} - Select Your Hotel", expanded=False):
                hotels = get_hotels_for_destination(dest)
                categories = list(set([h['category'] for h in hotels]))
                selected_categories = st.multiselect("Filter by Category", categories, default=categories, key=f"filter_{dest_country}")
                filtered_hotels = [h for h in hotels if h['category'] in selected_categories]
                
                sort_by = st.radio("Sort by", ["Price (Low to High)", "Price (High to Low)", "Rating"], horizontal=True, key=f"sort_{dest_country}")
                if sort_by == "Price (Low to High)":
                    filtered_hotels = sorted(filtered_hotels, key=lambda x: x['nightly_rate_inr'])
                elif sort_by == "Price (High to Low)":
                    filtered_hotels = sorted(filtered_hotels, key=lambda x: x['nightly_rate_inr'], reverse=True)
                else:
                    filtered_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)
                
                for hotel in filtered_hotels:
                    is_selected = trip.get('selected_hotels', {}).get(dest_country, {}).get('name') == hotel['name']
                    card_class = "hotel-card selected" if is_selected else "hotel-card"
                    
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap;">
                            <div style="flex: 1;">
                                <h4 style="margin: 0;">🏨 {hotel['name']}</h4>
                                <p style="margin: 0.3rem 0;">
                                    <span class="star-rating">{'★' * hotel['stars']}</span> 
                                    | ⭐ {hotel['rating']}/5 ({hotel['reviews']:,} reviews)
                                </p>
                                <p style="margin: 0.3rem 0;"><strong>📍 Location:</strong> {hotel['location']}</p>
                                <p style="margin: 0.3rem 0;"><strong>Category:</strong> {hotel['category']}</p>
                                <p style="margin: 0.3rem 0; font-size: 0.85rem;">
                                    <strong>Amenities:</strong> {', '.join(hotel['amenities'][:5])}
                                </p>
                            </div>
                            <div style="text-align: right; min-width: 180px;">
                                <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #667eea;">
                                    ₹{hotel['nightly_rate_inr']:,}
                                </p>
                                <p style="margin: 0; font-size: 0.8rem;">per night</p>
                                <p style="margin: 0.5rem 0; font-weight: bold; color: #4CAF50;">
                                    Total ({nights_per_dest} nights): ₹{hotel['nightly_rate_inr'] * nights_per_dest:,}
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if is_selected:
                        st.success(f"✅ Selected: {hotel['name']}")
                        if st.button(f"❌ Remove", key=f"remove_hotel_{dest_country}_{hotel['name']}"):
                            del trip['selected_hotels'][dest_country]
                            st.rerun()
                    else:
                        if st.button(f"✅ Select This Hotel", key=f"select_{dest_country}_{hotel['name']}"):
                            if 'selected_hotels' not in trip:
                                trip['selected_hotels'] = {}
                            trip['selected_hotels'][dest_country] = {
                                **hotel,
                                'nights': nights_per_dest,
                                'total_cost_inr': hotel['nightly_rate_inr'] * nights_per_dest
                            }
                            st.success(f"✅ Selected: {hotel['name']}")
                            st.rerun()

# ----- TAB 3: PHOTO BLOG -----
with tab_main3:
    st.markdown("### 📸 Country Photo Albums")
    
    col_blog1, col_blog2 = st.columns([1, 3])
    
    with col_blog1:
        st.markdown("#### 📂 Countries")
        all_destinations = generate_destinations()
        available_countries = sorted(list(set([dest['country'] for dest in all_destinations])))
        
        new_country = st.selectbox("Select Country", [""] + available_countries, key="new_album_country")
        if new_country and new_country != "":
            if new_country not in st.session_state.photo_albums:
                st.session_state.photo_albums[new_country] = []
                st.success(f"Created album for {new_country}!")
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.photo_albums:
            for country in sorted(st.session_state.photo_albums.keys()):
                bg = COUNTRY_BACKGROUNDS.get(country, {'flag': '🏳️'})
                photo_count = len(st.session_state.photo_albums[country])
                if st.button(f"{bg['flag']} {country} ({photo_count})", key=f"folder_{country}", use_container_width=True):
                    st.session_state.selected_country = country
                    st.rerun()
        else:
            st.info("No albums yet.")
    
    with col_blog2:
        if st.session_state.selected_country or st.session_state.view_photos_country:
            country = st.session_state.view_photos_country or st.session_state.selected_country
            bg = COUNTRY_BACKGROUNDS.get(country, {'flag': '🏳️'})
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 1.5rem;">
                <h2 style="color: white !important;">{bg['flag']} {country} Photo Album</h2>
                <p style="color: white !important;">📸 {len(st.session_state.photo_albums.get(country, []))} photos</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📤 Upload New Photo", expanded=True):
                uploaded_file = st.file_uploader("Choose a photo", type=['jpg', 'jpeg', 'png'], key=f"upload_{country}")
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Preview", use_container_width=True)
                    
                    col_t, col_d = st.columns(2)
                    with col_t:
                        photo_title = st.text_input("Title", "My Memory", key=f"title_{country}")
                    with col_d:
                        photo_date = st.date_input("Date", datetime.now(), key=f"date_{country}")
                    
                    photo_desc = st.text_area("Description", "", key=f"desc_{country}")
                    photo_loc = st.text_input("Location", "", key=f"loc_{country}")
                    
                    if st.button("💾 Save", use_container_width=True, key=f"save_{country}"):
                        if country not in st.session_state.photo_albums:
                            st.session_state.photo_albums[country] = []
                        new_photo = {
                            'id': f"photo_{country}_{len(st.session_state.photo_albums[country])}_{random.randint(1000, 9999)}",
                            'title': photo_title, 'description': photo_desc,
                            'location': photo_loc, 'date': photo_date.strftime('%Y-%m-%d'),
                            'country': country, 'image_data': image,
                            'uploaded_at': datetime.now(), 'likes': 0
                        }
                        st.session_state.photo_albums[country].append(new_photo)
                        st.success("✅ Photo saved!")
                        st.rerun()
            
            if country in st.session_state.photo_albums and st.session_state.photo_albums[country]:
                for i in range(0, len(st.session_state.photo_albums[country]), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(st.session_state.photo_albums[country]):
                            photo = st.session_state.photo_albums[country][i + j]
                            with cols[j]:
                                if 'image_data' in photo:
                                    st.image(photo['image_data'], use_container_width=True)
                                st.markdown(f"**{photo['title']}**<br><small>📍 {photo.get('location', '')} | 📅 {photo['date']}</small>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-album"><h2>📷</h2><h3>No photos yet</h3></div>', unsafe_allow_html=True)

# ----- TAB 4: SOLO SAFETY -----
with tab_main4:
    st.markdown("### 👩 Solo Female Traveler Safety Guide")
    
    col_safe1, col_safe2 = st.columns([1, 1])
    
    with col_safe1:
        st.markdown("#### 🛡️ Safety Ratings")
        safety_destinations = sorted(generate_destinations(), key=lambda x: x['solo_female_safety'], reverse=True)
        safety_data = [{'Country': f"{d['flag']} {d['country']}", 'Safety': d['solo_female_safety']} for d in safety_destinations[:10]]
        safety_df = pd.DataFrame(safety_data)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=safety_df['Country'], y=safety_df['Safety'],
            marker_color=['#4CAF50' if x >= 8 else '#FFC107' if x >= 6.5 else '#F44336' for x in safety_df['Safety']],
            text=safety_df['Safety'], textposition='outside'
        ))
        fig.update_layout(
            title="Top Safest Countries", height=500, yaxis=dict(range=[0, 10]),
            plot_bgcolor='#E3F2FD', paper_bgcolor='#E3F2FD',
            font=dict(color='#000000')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        rank_data = []
        for dest in safety_destinations[:15]:
            rank_data.append({
                'Country': f"{dest['flag']} {dest['country']}",
                'Safety': f"{dest['solo_female_safety']}/10",
                'Rating': get_star_rating(dest['solo_female_safety']/2)
            })
        st.dataframe(pd.DataFrame(rank_data), use_container_width=True)
    
    with col_safe2:
        st.markdown("#### 💡 Safety Tips")
        safety_destinations = generate_destinations()
        selected_dest_safety = st.selectbox("Select Country", [f"{d['flag']} {d['country']}" for d in safety_destinations])
        
        for dest in safety_destinations:
            if dest['country'] in selected_dest_safety:
                st.markdown(f"""
                <div class="detail-card">
                    <h4>{dest['flag']} {dest['country']}</h4>
                    <p><span class="star-rating">{get_star_rating(dest['solo_female_safety']/2)}</span> ({dest['solo_female_safety']}/10)</p>
                    <p><strong>Safe Areas:</strong> {', '.join(dest['safe_areas'])}</p>
                    <p><strong>Areas to Avoid:</strong> {', '.join(dest.get('unsafe_areas', ['None']))}</p>
                    <p><strong>Emergency:</strong></p>
                    <ul>
                """, unsafe_allow_html=True)
                for service, number in dest['emergency_numbers'].items():
                    st.markdown(f"<li>{service}: {number}</li>", unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)

# ----- TAB 5: TRIP PLANNER -----
with tab_main5:
    st.markdown("### 🗺️ Your Trip Planner")
    
    if st.session_state.current_trip:
        trip = st.session_state.current_trip
        
        st.markdown(f"""
        <div class="cost-summary-card">
            <h2>📋 {trip['name']}</h2>
            <p>📅 {trip['start_date'].strftime('%d %b %Y')} - {trip['end_date'].strftime('%d %b %Y')}</p>
            <p>⏱️ {trip['duration']} days | 🌙 {trip['nights']} nights</p>
            <p>👥 {trip['travel_group']} | 💰 {trip['currency']} {trip['budget']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if trip['destinations']:
            st.markdown("### 📍 Selected Destinations & Hotels")
            
            total_destination_cost = 0
            total_hotel_cost = 0
            
            for idx, dest in enumerate(trip['destinations']):
                dest_country = dest['country']
                selected_hotel = trip.get('selected_hotels', {}).get(dest_country)
                dest_nights = max(1, trip['nights'] // len(trip['destinations']))
                
                dest_cost_inr = dest['avg_cost_per_day'] * dest_nights
                total_destination_cost += dest_cost_inr
                
                if selected_hotel:
                    hotel_cost_inr = selected_hotel.get('total_cost_inr', 0)
                    total_hotel_cost += hotel_cost_inr
                    hotel_display = f"""
                    <div style="background: #E8F5E9; padding: 0.8rem; border-radius: 8px; margin-top: 0.5rem;">
                        <strong>🏨 Hotel:</strong> {selected_hotel['name']}<br>
                        <strong>📍 Location:</strong> {selected_hotel.get('location', 'N/A')}<br>
                        <small>{dest_nights} nights × ₹{selected_hotel['nightly_rate_inr']:,}/night</small><br>
                        <strong>Hotel Total:</strong> ₹{hotel_cost_inr:,}
                    </div>
                    """
                else:
                    cheapest = get_cheapest_hotel(dest_country)
                    if cheapest:
                        cheapest_cost = cheapest['nightly_rate_inr'] * dest_nights
                        hotel_display = f"""
                        <div style="background: #FFF3CD; padding: 0.8rem; border-radius: 8px; margin-top: 0.5rem;">
                            <strong>💰 Cheapest Option:</strong> {cheapest['name']}<br>
                            <strong>📍 Location:</strong> {cheapest['location']}<br>
                            <small>{dest_nights} nights × ₹{cheapest['nightly_rate_inr']:,}/night</small><br>
                            <strong>Est. Cost:</strong> ₹{cheapest_cost:,}
                        </div>
                        """
                    else:
                        hotel_display = ""
                
                st.markdown(f"""
                <div class="trip-destination-item">
                    <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap;">
                        <div>
                            <strong>{dest['flag']} {dest['name']}</strong><br>
                            <span>⭐ {dest['stars']} | 👩 Safety: {dest['solo_female_safety']}/10</span><br>
                            <span>🌙 {dest_nights} nights</span>
                        </div>
                        <div style="text-align: right;">
                            <span>Activities: ₹{dest_cost_inr:,}</span>
                        </div>
                    </div>
                    {hotel_display}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"❌ Remove {dest['name']}", key=f"remove_trip_{idx}"):
                    trip['destinations'].pop(idx)
                    if dest_country in trip.get('selected_hotels', {}):
                        del trip['selected_hotels'][dest_country]
                    st.rerun()
            
            # CHEAPEST TRIP OPTION
            st.markdown("---")
            st.markdown("### 💰 Cheapest Trip Option")
            
            cheapest_total = 0
            for dest in trip['destinations']:
                cheapest = get_cheapest_hotel(dest['country'])
                dest_nights = max(1, trip['nights'] // len(trip['destinations']))
                if cheapest:
                    cheapest_total += (cheapest['nightly_rate_inr'] + dest['avg_cost_per_day']) * dest_nights
            
            st.markdown(f"""
            <div class="cheapest-highlight">
                <h2>💰 MINIMUM TRIP COST: ₹{cheapest_total:,}</h2>
                <p>If you choose the cheapest hotels and activities for all destinations</p>
            </div>
            """, unsafe_allow_html=True)
            
            # TOTAL COST BREAKDOWN
            st.markdown("### 💵 Your Current Cost Breakdown")
            
            total_cost_inr = total_destination_cost + total_hotel_cost
            budget_inr = trip['budget'] if trip['currency'] == 'INR' else trip['budget'] * CURRENCY_RATES[trip['currency']]
            remaining_inr = budget_inr - total_cost_inr
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                st.markdown(f'<div class="metric-card"><h4>🎯 Activities</h4><p style="font-size: 1.3rem; font-weight: bold;">₹{total_destination_cost:,}</p></div>', unsafe_allow_html=True)
            with col_b2:
                st.markdown(f'<div class="metric-card"><h4>🏨 Hotels</h4><p style="font-size: 1.3rem; font-weight: bold;">₹{total_hotel_cost:,}</p></div>', unsafe_allow_html=True)
            with col_b3:
                st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;"><h4 style="color: white !important;">💰 Total</h4><p style="font-size: 1.3rem; font-weight: bold; color: white !important;">₹{total_cost_inr:,}</p></div>', unsafe_allow_html=True)
            with col_b4:
                color = "#4CAF50" if remaining_inr >= 0 else "#F44336"
                st.markdown(f'<div class="metric-card" style="border-left: 4px solid {color};"><h4>💵 Remaining</h4><p style="font-size: 1.3rem; font-weight: bold; color: {color};">₹{remaining_inr:,}</p></div>', unsafe_allow_html=True)
            
            # Save trip
            if st.button("💾 Save This Trip", use_container_width=True):
                trip_copy = trip.copy()
                trip_copy['total_cost_inr'] = total_cost_inr
                st.session_state.trip_history.append(trip_copy)
                st.success("Trip saved to history!")
        else:
            st.info("📍 Add destinations to build your trip plan.")
    else:
        st.info("👈 Generate a trip plan using the sidebar first!")

# ============================================================
# PLACE DETAILS MODAL
# ============================================================
if st.session_state.get('show_place_details'):
    country = st.session_state.show_place_details
    destinations = generate_destinations()
    
    for dest in destinations:
        if dest['country'] == country:
            with st.expander(f"📋 Details: {dest['flag']} {dest['name']}", expanded=True):
                st.markdown(f"""
                <div class="detail-card">
                    <h2>{dest['flag']} {dest['name']}</h2>
                    <p><strong>Landmark:</strong> {dest['landmark']} {dest['landmark_emoji']}</p>
                    <p><strong>Description:</strong> {dest['long_description']}</p>
                    <p><strong>Best Time:</strong> {dest['best_time']}</p>
                    <p><strong>Language:</strong> {dest['language']} | <strong>Currency:</strong> {dest['currency']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 🏨 Available Hotels")
                hotels = get_hotels_for_destination(dest)
                for hotel in hotels:
                    st.markdown(f"""
                    <div class="hotel-card">
                        <strong>🏨 {hotel['name']}</strong> ({'★' * hotel['stars']})<br>
                        📍 {hotel['location']}<br>
                        💰 ₹{hotel['nightly_rate_inr']:,}/night • ⭐ {hotel['rating']}/5
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("Close Details", key="close_details"):
                    st.session_state.show_place_details = None
                    st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #000000; padding: 1rem;">
        ✈️ AI Travel Planner - Smart Travel Advisor<br>
        Star ratings change dynamically based on your travel group and interests<br>
        Destinations remain fixed until you generate new recommendations
    </div>
    """,
    unsafe_allow_html=True
)