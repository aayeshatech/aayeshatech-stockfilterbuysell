import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import math
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="Planetary Trading Dashboard",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #e94560;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #f5f5f5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .bearish {
        color: #d32f2f;
        font-weight: bold;
    }
    .bullish {
        color: #388e3c;
        font-weight: bold;
    }
    .volatile {
        color: #f57c00;
        font-weight: bold;
    }
    .dataframe {
        width: 100%;
    }
    .status-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #16213e;
        color: white;
        padding: 10px;
        text-align: center;
    }
    .live-action {
        background-color: #0f3460;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .countdown {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .strategy-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        color: #333333;
        border-left: 5px solid #e94560;
    }
    .strategy-box h3 {
        color: #e94560;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 10px;
        margin-top: 0;
    }
    .strategy-box h4 {
        color: #495057;
        margin-top: 20px;
    }
    .strategy-box ul {
        padding-left: 20px;
    }
    .strategy-box li {
        margin-bottom: 8px;
    }
    .strategy-box strong {
        color: #495057;
    }
    .report-header {
        background-color: #e94560;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .market-type {
        background-color: #0f3460;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .sentiment-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .highly-bullish {
        background-color: rgba(56, 142, 60, 0.2);
        border: 2px solid #388e3c;
        color: #388e3c;
    }
    .highly-bearish {
        background-color: rgba(211, 47, 47, 0.2);
        border: 2px solid #d32f2f;
        color: #d32f2f;
    }
    .neutral {
        background-color: rgba(245, 124, 0, 0.2);
        border: 2px solid #f57c00;
        color: #f57c00;
    }
    .current-time {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .refresh-btn {
        background-color: #e94560;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }
    .refresh-btn:hover {
        background-color: #d63450;
    }
    .aspect-legend {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .aspect-item {
        display: flex;
        align-items: center;
        margin: 0 10px;
    }
    .aspect-color {
        width: 20px;
        height: 3px;
        margin-right: 5px;
    }
    .auto-update {
        color: #388e3c;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .update-indicator {
        background-color: #e94560;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.9rem;
        margin-bottom: 10px;
        display: inline-block;
    }
    .forecast-day {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #e94560;
    }
    .forecast-day-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .forecast-day-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333333;
    }
    .forecast-day-sentiment {
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .forecast-content {
        margin-top: 10px;
    }
    .forecast-section {
        margin-bottom: 15px;
    }
    .forecast-section-title {
        font-weight: bold;
        color: #495057;
        margin-bottom: 5px;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'planetary_data' not in st.session_state:
    st.session_state.planetary_data = None
if 'timeline_data' not in st.session_state:
    st.session_state.timeline_data = None
if 'trade_strategy' not in st.session_state:
    st.session_state.trade_strategy = None
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "NIFTY"
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.date(2025, 8, 4)
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'planetary_degrees' not in st.session_state:
    # Initialize planetary degrees for the default date (4th August 2025)
    st.session_state.planetary_degrees = {
        "Sun": 117.5, "Moon": 230.0, "Mercury": 130.0, 
        "Venus": 125.0, "Mars": 110.0, "Jupiter": 40.0, 
        "Saturn": 335.0, "Rahu": 350.0, "Ketu": 170.0
    }
if 'last_date' not in st.session_state:
    st.session_state.last_date = st.session_state.current_date
if 'last_symbol' not in st.session_state:
    st.session_state.last_symbol = st.session_state.current_symbol
if 'auto_update' not in st.session_state:
    st.session_state.auto_update = True
if 'update_count' not in st.session_state:
    st.session_state.update_count = 0

# Function to determine market type
def get_market_type(symbol):
    indian_symbols = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]
    international_symbols = ["GOLD", "SILVER", "CRUDE", "BTC", "BITCOIN", "DOWJONES", "DOW", "DJIA", "SPX", "NASDAQ"]
    
    symbol_upper = symbol.upper()
    
    if symbol_upper in indian_symbols:
        return "Indian"
    elif symbol_upper in international_symbols:
        return "International"
    else:
        # Default to International for unknown symbols
        return "International"

# Function to calculate planetary positions based on date
def calculate_planetary_positions(date):
    # Reference date (4th August 2025)
    reference_date = datetime.date(2025, 8, 4)
    
    # Calculate days difference
    days_diff = (date - reference_date).days
    
    # Daily movement for each planet (simplified)
    daily_movements = {
        "Sun": 0.9856,      # Approximately 1 degree per day
        "Moon": 13.1764,    # Approximately 13 degrees per day
        "Mercury": 1.5,     # Varies, but average around 1.5 degrees
        "Venus": 1.2,       # Approximately 1.2 degrees per day
        "Mars": 0.5,        # Approximately 0.5 degrees per day
        "Jupiter": 0.08,    # Approximately 0.08 degrees per day
        "Saturn": 0.03,     # Approximately 0.03 degrees per day
        "Rahu": 0.05,       # Approximately 0.05 degrees per day (retrograde)
        "Ketu": 0.05       # Same as Rahu (retrograde)
    }
    
    # Base positions for reference date
    base_positions = {
        "Sun": 117.5, "Moon": 230.0, "Mercury": 130.0, 
        "Venus": 125.0, "Mars": 110.0, "Jupiter": 40.0, 
        "Saturn": 335.0, "Rahu": 350.0, "Ketu": 170.0
    }
    
    # Calculate new positions
    new_positions = {}
    for planet, base_pos in base_positions.items():
        movement = daily_movements[planet] * days_diff
        new_pos = (base_pos + movement) % 360
        new_positions[planet] = new_pos
    
    return new_positions

# Function to calculate overall market sentiment
def calculate_market_sentiment(planetary_data, aspects):
    bullish_count = 0
    bearish_count = 0
    
    # Simple sentiment calculation based on planetary positions
    for planet in planetary_data:
        if planet["Planet"] in ["Jupiter", "Venus"]:
            bullish_count += 1
        elif planet["Planet"] in ["Saturn", "Mars", "Rahu", "Ketu"]:
            bearish_count += 1
    
    # Calculate aspects
    for aspect in aspects:
        if aspect["type"] in ["Trine", "Sextile"]:
            bullish_count += 1
        elif aspect["type"] in ["Square", "Opposition"]:
            bearish_count += 1
    
    # Determine overall sentiment
    if bullish_count > bearish_count * 1.5:
        return "Highly Bullish", "highly-bullish"
    elif bearish_count > bullish_count * 1.5:
        return "Highly Bearish", "highly-bearish"
    elif bullish_count > bearish_count:
        return "Bullish", "bullish"
    elif bearish_count > bullish_count:
        return "Bearish", "bearish"
    else:
        return "Neutral", "neutral"

# Function to calculate aspects between planets
def calculate_aspects(degrees):
    aspects = []
    planets = list(degrees.keys())
    
    # Define aspect types and their orbs
    aspect_types = {
        "Conjunction": {"angle": 0, "orb": 8},
        "Sextile": {"angle": 60, "orb": 8},
        "Square": {"angle": 90, "orb": 8},
        "Trine": {"angle": 120, "orb": 8},
        "Opposition": {"angle": 180, "orb": 8}
    }
    
    # Check all pairs of planets
    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            planet1 = planets[i]
            planet2 = planets[j]
            
            # Calculate angular distance
            angle1 = degrees[planet1]
            angle2 = degrees[planet2]
            
            # Find the smallest angle between the two planets
            diff = abs(angle1 - angle2) % 360
            if diff > 180:
                diff = 360 - diff
            
            # Check for aspects
            for aspect_name, aspect_data in aspect_types.items():
                aspect_angle = aspect_data["angle"]
                orb = aspect_data["orb"]
                
                if abs(diff - aspect_angle) <= orb:
                    aspects.append({
                        "planet1": planet1,
                        "planet2": planet2,
                        "type": aspect_name,
                        "angle": diff,
                        "orb": abs(diff - aspect_angle)
                    })
    
    return aspects

# Function to update planetary degrees (simulate movement)
def update_planetary_degrees():
    # Simulate planetary movement by adding small random changes
    for planet in st.session_state.planetary_degrees:
        # Different planets move at different speeds
        if planet == "Moon":
            movement = np.random.uniform(0.3, 0.5)  # Moon moves fastest
        elif planet == "Sun":
            movement = np.random.uniform(0.05, 0.1)  # Sun moves slower
        elif planet in ["Mercury", "Venus"]:
            movement = np.random.uniform(0.1, 0.2)
        elif planet == "Mars":
            movement = np.random.uniform(0.05, 0.08)
        elif planet == "Jupiter":
            movement = np.random.uniform(0.02, 0.04)
        elif planet == "Saturn":
            movement = np.random.uniform(0.01, 0.02)
        else:  # Rahu/Ketu
            movement = np.random.uniform(0.03, 0.05)
        
        # Update degree
        st.session_state.planetary_degrees[planet] = (st.session_state.planetary_degrees[planet] + movement) % 360

# Function to get sign from degree
def get_sign_from_degree(degree):
    signs = [
        ("Aries", 0, 30), ("Taurus", 30, 60), ("Gemini", 60, 90),
        ("Cancer", 90, 120), ("Leo", 120, 150), ("Virgo", 150, 180),
        ("Libra", 180, 210), ("Scorpio", 210, 240), ("Sagittarius", 240, 270),
        ("Capricorn", 270, 300), ("Aquarius", 300, 330), ("Pisces", 330, 360)
    ]
    
    for sign, start, end in signs:
        if start <= degree < end:
            return sign
    
    return "Aries"  # Default

# Function to get nakshatra from degree
def get_nakshatra_from_degree(degree):
    nakshatras = [
        ("Ashwini", 0, 13.2), ("Bharani", 13.2, 26.4), ("Krittika", 26.4, 40),
        ("Rohini", 40, 53.2), ("Mrigashira", 53.2, 66.4), ("Ardra", 66.4, 80),
        ("Punarvasu", 80, 93.2), ("Pushya", 93.2, 106.4), ("Ashlesha", 106.4, 120),
        ("Magha", 120, 133.2), ("Purva Phalguni", 133.2, 146.4), ("Uttara Phalguni", 146.4, 160),
        ("Hasta", 160, 173.2), ("Chitra", 173.2, 186.4), ("Swati", 186.4, 200),
        ("Vishakha", 200, 213.2), ("Anuradha", 213.2, 226.4), ("Jyeshtha", 226.4, 240),
        ("Mula", 240, 253.2), ("Purva Ashadha", 253.2, 266.4), ("Uttara Ashadha", 266.4, 280),
        ("Shravana", 280, 293.2), ("Dhanishta", 293.2, 306.4), ("Shatabhisha", 306.4, 320),
        ("Purva Bhadrapada", 320, 333.2), ("Uttara Bhadrapada", 333.2, 346.4), ("Revati", 346.4, 360)
    ]
    
    for nakshatra, start, end in nakshatras:
        if start <= degree < end:
            return nakshatra
    
    return "Ashwini"  # Default

# Function to get lord of sign
def get_sign_lord(sign):
    sign_lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
        "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
        "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    return sign_lords.get(sign, "Unknown")

# Function to get lord of nakshatra
def get_nakshatra_lord(nakshatra):
    nakshatra_lords = {
        "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun",
        "Rohini": "Moon", "Mrigashira": "Mars", "Ardra": "Rahu",
        "Punarvasu": "Jupiter", "Pushya": "Saturn", "Ashlesha": "Mercury",
        "Magha": "Ketu", "Purva Phalguni": "Venus", "Uttara Phalguni": "Sun",
        "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu",
        "Vishakha": "Jupiter", "Anuradha": "Saturn", "Jyeshtha": "Mercury",
        "Mula": "Ketu", "Purva Ashadha": "Venus", "Uttara Ashadha": "Sun",
        "Shravana": "Moon", "Dhanishta": "Mars", "Shatabhisha": "Rahu",
        "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn", "Revati": "Mercury"
    }
    return nakshatra_lords.get(nakshatra, "Unknown")

# Function to generate planetary data based on current degrees
def generate_planetary_data(degrees):
    planetary_data = []
    
    for planet, degree in degrees.items():
        sign = get_sign_from_degree(degree)
        nakshatra = get_nakshatra_from_degree(degree)
        sign_lord = get_sign_lord(sign)
        nakshatra_lord = get_nakshatra_lord(nakshatra)
        
        # Format degree
        deg = int(degree)
        min = int((degree - deg) * 60)
        degree_str = f"{deg}° {min}'"
        
        # Determine house (simplified)
        house = (int(degree) // 30) + 1
        
        planetary_data.append({
            "Planet": planet,
            "Sign": sign,
            "Degree": degree_str,
            "Nakshatra": nakshatra,
            "Lord": sign_lord,
            "Sublord": nakshatra_lord,
            "House": house
        })
    
    return planetary_data

# Function to create zodiac wheel visualization with aspects
def create_zodiac_wheel_with_aspects(planetary_data, aspects):
    # Create a blank image
    img = Image.new('RGB', (800, 800), color='#0f3460')
    draw = ImageDraw.Draw(img)
    
    # Define parameters
    center_x, center_y = 400, 400
    radius = 300
    
    # Draw zodiac circle
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline='#e94560', width=2)
    
    # Draw zodiac signs
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        small_font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    for i, sign in enumerate(signs):
        angle = i * 30  # 30 degrees per sign
        rad = math.radians(angle)
        x = center_x + (radius - 40) * math.cos(rad)
        y = center_y + (radius - 40) * math.sin(rad)
        draw.text((x, y), sign, fill='white', font=font)
    
    # Draw aspects
    aspect_colors = {
        "Conjunction": "#ffcc00",  # Yellow
        "Sextile": "#00ccff",     # Light Blue
        "Square": "#ff3366",      # Pink
        "Trine": "#33cc33",       # Green
        "Opposition": "#ff6633"   # Orange
    }
    
    # Get planet positions
    planet_positions = {}
    for planet in planetary_data:
        sign = planet["Sign"]
        if sign in signs:
            angle = signs.index(sign) * 30
            # Add degree offset within sign
            degree_str = planet["Degree"]
            deg = int(degree_str.split("°")[0])
            min = int(degree_str.split("'")[0].split(" ")[1])
            angle += (deg % 30) + (min / 60)
            
            rad = math.radians(angle)
            x = center_x + (radius - 80) * math.cos(rad)
            y = center_y + (radius - 80) * math.sin(rad)
            planet_positions[planet["Planet"]] = (x, y, angle)
    
    # Draw aspect lines
    for aspect in aspects:
        planet1 = aspect["planet1"]
        planet2 = aspect["planet2"]
        aspect_type = aspect["type"]
        
        if planet1 in planet_positions and planet2 in planet_positions:
            x1, y1, _ = planet_positions[planet1]
            x2, y2, _ = planet_positions[planet2]
            
            # Draw line with aspect color
            draw.line([(x1, y1), (x2, y2)], fill=aspect_colors[aspect_type], width=2)
    
    # Draw planets
    planet_colors = {
        "Sun": "#ffcc00", "Moon": "#cccccc", "Mercury": "#b0b0b0", 
        "Venus": "#e39e1c", "Mars": "#ff0000", "Jupiter": "#ff9900", 
        "Saturn": "#ffcc99", "Rahu": "#4b0082", "Ketu": "#8b008b"
    }
    
    for planet, (x, y, angle) in planet_positions.items():
        # Draw planet
        color = planet_colors.get(planet, "#ffffff")
        draw.ellipse((x-12, y-12, x+12, y+12), fill=color, outline='white')
        
        # Draw planet label and degree
        degree_str = f"{planet}\n{angle:.1f}°"
        draw.text((x-20, y-40), degree_str, fill='white', font=small_font, anchor='mm')
    
    # Draw aspect legend
    legend_y = 20
    for aspect_type, color in aspect_colors.items():
        draw.line([(20, legend_y), (50, legend_y)], fill=color, width=2)
        draw.text((60, legend_y-5), aspect_type, fill='white', font=small_font)
        legend_y += 20
    
    # Convert to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Function to generate timeline data based on market type and date
def generate_timeline_data(symbol, date):
    market_type = get_market_type(symbol)
    
    # Get day of week
    day_of_week = date.strftime("%A")
    
    if market_type == "Indian":
        # Indian market timeline (9:15 AM to 3:30 PM)
        return [
            {"Time": "9:15 AM", "Event": f"Market Open - {day_of_week}", 
             "Influence": "Rahu aspects Moon (exact trine). Saturn-Rahu conjunction creates volatility.", 
             "Sentiment": "Bearish"},
            {"Time": "10:15 AM", "Event": "Mercury Hora starts", 
             "Influence": "Mercury in Leo (Magha) aspected by Rahu. Technical breakdown likely.", 
             "Sentiment": "Bearish"},
            {"Time": "11:15 AM", "Event": "Sun Hora starts", 
             "Influence": "Sun in Cancer (Ashlesha) aspected by Rahu, but Jupiter's 7th aspect provides support.", 
             "Sentiment": "Bullish"},
            {"Time": "12:15 PM", "Event": "Venus Hora starts", 
             "Influence": "Venus in Leo (Magha) under Rahu's 5th aspect. Profit-booking likely.", 
             "Sentiment": "Volatile"},
            {"Time": "1:15 PM", "Event": "Moon Hora starts", 
             "Influence": "Moon debilitated in Scorpio. Ketu sublord intensifies reversals.", 
             "Sentiment": "Bearish"},
            {"Time": "2:15 PM", "Event": "Mars Hora starts", 
             "Influence": "Mars in Cancer (Pushya) aspected by Rahu. Banking sector pressure.", 
             "Sentiment": "Bearish"},
            {"Time": "3:15 PM", "Event": "Jupiter Hora starts", 
             "Influence": "Jupiter in Taurus (Krittika) aspected by Saturn. Mild recovery attempt.", 
             "Sentiment": "Mildly Bullish"},
            {"Time": "3:30 PM", "Event": "Market Close", 
             "Influence": "Moon at 23° Scorpio. Rahu influence dominates.", 
             "Sentiment": "Bearish Close"}
        ]
    else:
        # International market timeline (5:00 AM to 11:55 PM)
        return [
            {"Time": "5:00 AM", "Event": f"Market Open - {day_of_week}", 
             "Influence": "Rahu aspects Moon (exact trine). Saturn-Rahu conjunction creates volatility.", 
             "Sentiment": "Bearish"},
            {"Time": "7:00 AM", "Event": "Mercury Hora starts", 
             "Influence": "Mercury in Leo (Magha) aspected by Rahu. Technical breakdown likely.", 
             "Sentiment": "Bearish"},
            {"Time": "9:00 AM", "Event": "Sun Hora starts", 
             "Influence": "Sun in Cancer (Ashlesha) aspected by Rahu, but Jupiter's 7th aspect provides support.", 
             "Sentiment": "Bullish"},
            {"Time": "11:00 AM", "Event": "Venus Hora starts", 
             "Influence": "Venus in Leo (Magha) under Rahu's 5th aspect. Profit-booking likely.", 
             "Sentiment": "Volatile"},
            {"Time": "1:00 PM", "Event": "Moon Hora starts", 
             "Influence": "Moon debilitated in Scorpio. Ketu sublord intensifies reversals.", 
             "Sentiment": "Bearish"},
            {"Time": "3:00 PM", "Event": "Mars Hora starts", 
             "Influence": "Mars in Cancer (Pushya) aspected by Rahu. Banking sector pressure.", 
             "Sentiment": "Bearish"},
            {"Time": "5:00 PM", "Event": "Jupiter Hora starts", 
             "Influence": "Jupiter in Taurus (Krittika) aspected by Saturn. Mild recovery attempt.", 
             "Sentiment": "Mildly Bullish"},
            {"Time": "7:00 PM", "Event": "Saturn Hora starts", 
             "Influence": "Saturn in Pisces (Uttara Bhadrapada) aspected by Jupiter. Consolidation phase.", 
             "Sentiment": "Neutral"},
            {"Time": "9:00 PM", "Event": "Venus Hora starts", 
             "Influence": "Venus in Leo (Magha) under Ketu's aspect. Trend reversal possible.", 
             "Sentiment": "Volatile"},
            {"Time": "11:00 PM", "Event": "Moon Hora starts", 
             "Influence": "Moon in Scorpio (Jyeshtha) aspected by Mars. Late session volatility.", 
             "Sentiment": "Bearish"},
            {"Time": "11:55 PM", "Event": "Market Close", 
             "Influence": "Moon at 23° Scorpio. Rahu influence dominates.", 
             "Sentiment": "Bearish Close"}
        ]

# Function to generate trade strategy
def generate_trade_strategy(symbol, date):
    # Format date for display
    date_str = date.strftime("%d %B %Y")
    market_type = get_market_type(symbol)
    
    if market_type == "Indian":
        market_hours = "9:15 AM - 3:30 PM"
    else:
        market_hours = "5:00 AM - 11:55 PM"
    
    if symbol.upper() == "NIFTY":
        return f"""
### Nifty (Index) Trading Strategy
<div class="report-header">Report for NIFTY on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">Indian Market</div>

#### 1. Bearish Strategy (9:15 AM – 10:15 AM)
- **Entry**: Short at open (9:15 AM) with stop-loss at 0.5% above entry.
- **Target**: 0.8-1% decline by 10:15 AM.
- **Rationale**: Moon-Rahu trine + Saturn-Rahu conjunction triggers panic selling.

#### 2. Bullish Strategy (11:15 AM – 12:15 PM)
- **Entry**: Long at 11:15 AM reversal (if technical indicators align).
- **Target**: 0.6% rise by 12:15 PM.
- **Rationale**: Jupiter's aspect counters Rahu; Sun hora supports optimism.

#### 3. Bearish Re-entry (1:15 PM – 2:15 PM)
- **Entry**: Short on breakdown below 1:15 PM low.
- **Target**: 0.7% decline by 2:15 PM.
- **Rationale**: Moon debilitation + Mars hora intensifies selling.

### Risk Management
- **Stop-Loss**: 0.5% for intraday trades.
- **Avoid**: Trades during Moon hora (1:15 PM – 2:15 PM) due to extreme volatility.
- **Focus**: Technical confirmation (e.g., support/resistance, RSI divergence) alongside astro signals.
"""
    elif symbol.upper() == "BANKNIFTY":
        return f"""
### Bank Nifty (Banking Index) Trading Strategy
<div class="report-header">Report for BANKNIFTY on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">Indian Market</div>

#### 1. Bearish Open (9:15 AM – 10:15 AM)
- **Entry**: Short at open.
- **Target**: 1.2% decline by 10:15 AM.
- **Rationale**: Mars (ruler of banking) in Cancer aspected by Rahu; Saturn-Rahu conjunction disrupts financials.

#### 2. Avoid Longs (12:15 PM – 1:15 PM)
- **Action**: Exit longs; no fresh entries.
- **Rationale**: Venus-Rahu aspect triggers volatility in banking stocks.

#### 3. Mild Recovery (3:15 PM – 3:30 PM)
- **Entry**: Long if Bank Nifty rebounds above 3:15 PM high.
- **Target**: 0.4% rise by close.
- **Rationale**: Jupiter hora supports late-session bounce.

### Risk Management
- **Stop-Loss**: 0.5% for intraday trades.
- **Avoid**: Trades during Moon hora (1:15 PM – 2:15 PM) due to extreme volatility.
- **Focus**: Technical confirmation (e.g., support/resistance, RSI divergence) alongside astro signals.
"""
    elif symbol.upper() in ["GOLD", "XAUUSD"]:
        return f"""
### Gold Trading Strategy
<div class="report-header">Report for GOLD on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">International Market</div>

#### 1. Early Morning Reversal (5:00 AM – 7:00 AM)
- **Entry**: Long on dip below 5:30 AM low.
- **Target**: 0.5% rise by 7:00 AM.
- **Rationale**: Jupiter's aspect on gold-friendly signs supports early buying.

#### 2. Morning Session (9:00 AM – 11:00 AM)
- **Action**: Range-bound trading expected.
- **Strategy**: Buy at support, sell at resistance.
- **Rationale**: Venus influences create sideways movement.

#### 3. Afternoon Breakout (1:00 PM – 3:00 PM)
- **Entry**: Breakout above 1:00 PM high.
- **Target**: 0.7% rise by 3:00 PM.
- **Rationale**: Sun hora strengthens precious metals.

#### 4. Evening Session (7:00 PM – 9:00 PM)
- **Entry**: Follow the 7:00 PM reversal direction.
- **Target**: 0.6% move by 9:00 PM.
- **Rationale**: Saturn hora creates trend continuation.

### Risk Management
- **Stop-Loss**: 0.3% for intraday trades.
- **Position Size**: Limit to 15% of trading capital.
- **Focus**: USD index movements alongside astro signals.
"""
    elif symbol.upper() in ["SILVER", "XAGUSD"]:
        return f"""
### Silver Trading Strategy
<div class="report-header">Report for SILVER on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">International Market</div>

#### 1. Early Morning Volatility (5:00 AM – 7:00 AM)
- **Entry**: Short on rejection at 5:30 AM high.
- **Target**: 0.8% decline by 7:00 AM.
- **Rationale**: Rahu influence creates sharp reversals.

#### 2. Mid-morning Recovery (9:00 AM – 11:00 AM)
- **Entry**: Long on bounce from 9:30 AM low.
- **Target**: 0.7% rise by 11:00 AM.
- **Rationale**: Mercury hora supports industrial metals.

#### 3. Afternoon Trend (1:00 PM – 3:00 PM)
- **Entry**: Follow the 1:00 PM breakout direction.
- **Target**: 0.9% move by 3:00 PM.
- **Rationale**: Sun hora strengthens precious metals.

#### 4. Evening Session (7:00 PM – 9:00 PM)
- **Entry**: Short on rejection at 7:30 PM high.
- **Target**: 0.6% decline by 9:00 PM.
- **Rationale**: Saturn hora creates selling pressure.

### Risk Management
- **Stop-Loss**: 0.4% for intraday trades.
- **Position Size**: Limit to 15% of trading capital.
- **Focus**: Gold price movements alongside astro signals.
"""
    elif symbol.upper() in ["CRUDE", "CL", "WTI"]:
        return f"""
### Crude Oil Trading Strategy
<div class="report-header">Report for CRUDE on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">International Market</div>

#### 1. Early Morning Breakout (5:00 AM – 7:00 AM)
- **Entry**: Long on breakout above 5:30 AM high.
- **Target**: 1.0% rise by 7:00 AM.
- **Rationale**: Mars hora supports energy commodities.

#### 2. Mid-morning Reversal (9:00 AM – 11:00 AM)
- **Entry**: Short on rejection at 9:30 AM high.
- **Target**: 0.8% decline by 11:00 AM.
- **Rationale**: Mercury hora creates profit-taking.

#### 3. Afternoon Volatility (1:00 PM – 3:00 PM)
- **Entry**: Follow the 1:00 PM breakout direction.
- **Target**: 1.2% move by 3:00 PM.
- **Rationale**: Sun hora influences energy markets.

#### 4. Evening Session (7:00 PM – 9:00 PM)
- **Entry**: Short on breakdown below 7:30 PM low.
- **Target**: 0.9% decline by 9:00 PM.
- **Rationale**: Saturn hora creates selling pressure.

### Risk Management
- **Stop-Loss**: 0.5% for intraday trades.
- **Position Size**: Limit to 15% of trading capital.
- **Focus**: Inventory reports alongside astro signals.
"""
    elif symbol.upper() in ["BTC", "BITCOIN"]:
        return f"""
### Bitcoin Trading Strategy
<div class="report-header">Report for BITCOIN on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">International Market</div>

#### 1. Early Morning Volatility (5:00 AM – 7:00 AM)
- **Entry**: Short on rejection at 5:30 AM high.
- **Target**: 1.5% decline by 7:00 AM.
- **Rationale**: Rahu influence creates sharp reversals.

#### 2. Mid-morning Recovery (9:00 AM – 11:00 AM)
- **Entry**: Long on bounce from 9:30 AM low.
- **Target**: 1.2% rise by 11:00 AM.
- **Rationale**: Mercury hora supports tech/crypto assets.

#### 3. Afternoon Trend (1:00 PM – 3:00 PM)
- **Entry**: Follow the 1:00 PM breakout direction.
- **Target**: 1.0% move by 3:00 PM.
- **Rationale**: Ketu influence creates sustained trends.

#### 4. Evening Session (7:00 PM – 9:00 PM)
- **Entry**: Long on breakout above 7:30 PM high.
- **Target**: 1.3% rise by 9:00 PM.
- **Rationale**: Venus hora supports speculative assets.

#### 5. Late Session (11:00 PM – 11:55 PM)
- **Entry**: Short on rejection at 11:30 PM high.
- **Target**: 0.8% decline by close.
- **Rationale**: Moon hora creates late session volatility.

### Risk Management
- **Stop-Loss**: 0.8% for intraday trades.
- **Position Size**: Limit to 10% of trading capital due to volatility.
- **Focus**: Crypto market sentiment alongside astro signals.
"""
    elif symbol.upper() in ["DOWJONES", "DOW", "DJIA"]:
        return f"""
### Dow Jones Trading Strategy
<div class="report-header">Report for DOWJONES on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">International Market</div>

#### 1. Early Morning Drive (5:00 AM – 7:00 AM)
- **Entry**: Short at open with 0.3% stop-loss.
- **Target**: 0.6% decline by 7:00 AM.
- **Rationale**: Saturn-Rahu conjunction pressures equities.

#### 2. Mid-morning Reversal (9:00 AM – 11:00 AM)
- **Entry**: Long on bounce from 9:30 AM low.
- **Target**: 0.5% rise by 11:00 AM.
- **Rationale**: Jupiter's aspect provides temporary support.

#### 3. Afternoon Trend (1:00 PM – 3:00 PM)
- **Entry**: Follow the 1:00 PM breakout direction.
- **Target**: 0.4% move by 3:00 PM.
- **Rationale**: Sun hora influences market direction.

#### 4. Evening Session (7:00 PM – 9:00 PM)
- **Entry**: Short on rejection at 7:30 PM high.
- **Target**: 0.5% decline by 9:00 PM.
- **Rationale**: Saturn hora creates selling pressure.

### Risk Management
- **Stop-Loss**: 0.3% for intraday trades.
- **Position Size**: Limit to 20% of trading capital.
- **Focus**: VIX index alongside astro signals.
"""
    else:
        return f"""
### {symbol} Trading Strategy
<div class="report-header">Report for {symbol} on {date_str} | Market Hours: {market_hours}</div>
<div class="market-type">{market_type} Market</div>

#### General Approach
Based on the planetary positions and transit timeline for today, the following strategy is recommended for {symbol}:

1. **Morning Session (5:00 AM - 12:00 PM)**: 
   - Bearish sentiment dominates in the first hour. Consider short positions with tight stop-loss.
   - Mid-morning may see a brief bullish reversal around 9:00 AM.

2. **Afternoon Session (12:00 PM - 7:00 PM)**:
   - Volatility expected during Moon hora (1:00 PM - 2:00 PM). Avoid new positions.
   - Late afternoon may see trend development.

3. **Evening Session (7:00 PM - 11:55 PM)**:
   - Saturn hora influences may create trend reversals.
   - Late session volatility expected during Moon hora.

### Risk Management
- **Stop-Loss**: 0.5% for intraday trades.
- **Position Sizing**: Limit exposure to 20% of trading capital per trade.
- **Confirmation**: Always use technical indicators to confirm astrological signals.
"""

# Function to generate forecast data
def generate_forecast_data(symbol, center_date):
    forecast_data = []
    
    # Generate dates for 3 days before and 3 days after the selected date
    for i in range(-3, 4):
        date = center_date + datetime.timedelta(days=i)
        
        # Calculate planetary positions for this date
        planetary_degrees = calculate_planetary_positions(date)
        
        # Generate planetary data
        planetary_data = generate_planetary_data(planetary_degrees)
        
        # Calculate aspects
        aspects = calculate_aspects(planetary_degrees)
        
        # Filter moon aspects
        moon_aspects = [aspect for aspect in aspects if aspect["planet1"] == "Moon" or aspect["planet2"] == "Moon"]
        
        # Generate timeline data for this date
        timeline_data = generate_timeline_data(symbol, date)
        
        # Calculate sentiment
        sentiment, sentiment_class = calculate_market_sentiment(planetary_data, aspects)
        
        # Format date for display
        date_str = date.strftime("%d %B %Y")
        day_name = date.strftime("%A")
        
        # Add to forecast data
        forecast_data.append({
            "date": date,
            "date_str": date_str,
            "day_name": day_name,
            "sentiment": sentiment,
            "sentiment_class": sentiment_class,
            "planetary_data": planetary_data,
            "aspects": aspects,
            "moon_aspects": moon_aspects,
            "timeline_data": timeline_data
        })
    
    return forecast_data

# Function to update all data based on current inputs
def update_all_data(date, symbol):
    # Calculate new planetary positions based on date
    st.session_state.planetary_degrees = calculate_planetary_positions(date)
    
    # Update session state
    st.session_state.last_date = date
    st.session_state.last_symbol = symbol
    st.session_state.current_date = date
    st.session_state.current_symbol = symbol
    st.session_state.update_count += 1
    
    # Generate new data
    st.session_state.planetary_data = generate_planetary_data(st.session_state.planetary_degrees)
    st.session_state.timeline_data = generate_timeline_data(symbol, date)
    st.session_state.trade_strategy = generate_trade_strategy(symbol, date)
    st.session_state.forecast_data = generate_forecast_data(symbol, date)

# Header
st.markdown('<div class="main-header">INTRADAY PLANETARY TRANSIT TRADING DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Astrowise & Gann Wise Trading System</div>', unsafe_allow_html=True)

# Current time display
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f'<div class="current-time">Current Time: {current_time}</div>', unsafe_allow_html=True)

# Update indicator
if st.session_state.update_count > 0:
    st.markdown(f'<div class="update-indicator">✅ Data updated {st.session_state.update_count} time(s)</div>', unsafe_allow_html=True)

# Auto-update indicator
if st.session_state.auto_update:
    st.markdown('<div class="auto-update">✅ Auto-update enabled - Data refreshes automatically when date or symbol changes</div>', unsafe_allow_html=True)

# Refresh button
if st.button("Refresh Planetary Positions", key="refresh_btn"):
    update_planetary_degrees()
    # Regenerate all data with updated degrees
    st.session_state.planetary_data = generate_planetary_data(st.session_state.planetary_degrees)
    st.session_state.timeline_data = generate_timeline_data(st.session_state.current_symbol, st.session_state.current_date)
    st.session_state.trade_strategy = generate_trade_strategy(st.session_state.current_symbol, st.session_state.current_date)
    st.session_state.forecast_data = generate_forecast_data(st.session_state.current_symbol, st.session_state.current_date)
    st.rerun()

# Market sentiment display
if st.session_state.planetary_data:
    sentiment, sentiment_class = calculate_market_sentiment(st.session_state.planetary_data, calculate_aspects(st.session_state.planetary_degrees))
    st.markdown(f'<div class="sentiment-box {sentiment_class}"><h2>{sentiment}</h2></div>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Date input
date = st.sidebar.date_input("Date", value=st.session_state.current_date)

# Symbol input - Changed to text input for any symbol
symbol = st.sidebar.text_input("Symbol", value=st.session_state.current_symbol, 
                              help="Enter any symbol like NIFTY, BANKNIFTY, GOLD, BTC, DOWJONES, etc.")

# City input
city = st.sidebar.text_input("City", value="Mumbai")

# Time input
time_input = st.sidebar.time_input("Time", value=datetime.time(9, 15))

# Auto-update toggle
auto_update = st.sidebar.checkbox("Auto-update data when parameters change", value=st.session_state.auto_update)
st.session_state.auto_update = auto_update

# Generate button
generate_btn = st.sidebar.button("Generate Report")

# Auto-update data if date or symbol changed and auto-update is enabled
if st.session_state.auto_update and (date != st.session_state.last_date or symbol != st.session_state.last_symbol):
    update_all_data(date, symbol)

# Generate report when button is clicked
if generate_btn:
    # Update session state
    st.session_state.current_date = date
    st.session_state.current_symbol = symbol
    
    # Create datetime object
    datetime_obj = datetime.datetime.combine(date, time_input)
    
    # Generate data
    update_all_data(date, symbol)
    
    # Show success message
    st.sidebar.success("Report generated successfully!")

# Generate planetary data if not already generated
if not st.session_state.planetary_data:
    update_all_data(st.session_state.current_date, st.session_state.current_symbol)

# Calculate aspects
aspects = calculate_aspects(st.session_state.planetary_degrees)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Transit Timeline", "Planetary Positions", "Trade Execution Strategy", "Forecast"])

# Tab 1: Transit Timeline
with tab1:
    st.header("Critical Transit Timeline")
    
    if st.session_state.timeline_data:
        # Display market type
        market_type = get_market_type(st.session_state.current_symbol)
        st.markdown(f'<div class="market-type">{market_type} Market</div>', unsafe_allow_html=True)
        
        # Create DataFrame
        df = pd.DataFrame(st.session_state.timeline_data)
        
        # Add color formatting
        def highlight_sentiment(val):
            if "Bullish" in val:
                return 'color: #388e3c'
            elif "Bearish" in val:
                return 'color: #d32f2f'
            else:
                return 'color: #f57c00'
        
        # Display table with color formatting
        st.dataframe(
            df.style.applymap(highlight_sentiment, subset=['Sentiment']),
            use_container_width=True
        )
        
        # Live trading guidance
        st.markdown('<div class="live-action">', unsafe_allow_html=True)
        st.subheader("Live Trading Guidance")
        
        # Get current time
        now = datetime.datetime.now()
        current_time_str = now.strftime("%H:%M:%S")
        
        # Find next action
        next_action = None
        for item in st.session_state.timeline_data:
            time_str = item["Time"]
            try:
                action_time = datetime.datetime.strptime(time_str, "%I:%M %p")
                action_time = action_time.replace(year=now.year, month=now.month, day=now.day)
                
                # Check if action time is in the future
                if action_time > now:
                    next_action = item
                    break
            except:
                pass
        
        # Display current time
        st.write(f"**Current Time:** {current_time_str}")
        
        if next_action:
            # Display next action
            sentiment_class = "bullish" if "Bullish" in next_action['Sentiment'] else "bearish" if "Bearish" in next_action['Sentiment'] else "volatile"
            st.markdown(f"**Next Action:** <span class='{sentiment_class}'>{next_action['Time']} - {next_action['Sentiment']}</span>", unsafe_allow_html=True)
            
            # Calculate time remaining
            action_time = datetime.datetime.strptime(next_action['Time'], "%I:%M %p")
            action_time = action_time.replace(year=now.year, month=now.month, day=now.day)
            time_remaining = action_time - now
            
            # Display countdown
            hours, remainder = divmod(time_remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.markdown(f"<div class='countdown'>Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)
        else:
            st.markdown("**Next Action:** <span class='bearish'>Market Closed</span>", unsafe_allow_html=True)
            st.markdown("<div class='countdown'>Time Remaining: --:--:--</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Generate a report to see the transit timeline.")

# Tab 2: Planetary Positions
with tab2:
    st.header("Planetary Positions")
    
    if st.session_state.planetary_data:
        # Create DataFrame
        df = pd.DataFrame(st.session_state.planetary_data)
        
        # Display table
        st.dataframe(df, use_container_width=True)
        
        # Display aspects
        st.subheader("Planetary Aspects")
        aspects_df = pd.DataFrame(aspects)
        if not aspects_df.empty:
            st.dataframe(aspects_df, use_container_width=True)
        else:
            st.write("No significant aspects at this time.")
        
        # Display zodiac wheel
        st.subheader("Planetary Positions Visualization")
        zodiac_image = create_zodiac_wheel_with_aspects(st.session_state.planetary_data, aspects)
        st.image(zodiac_image, width=700)
        
        # Display aspect legend
        st.markdown("""
        <div class="aspect-legend">
            <div class="aspect-item">
                <div class="aspect-color" style="background-color: #ffcc00;"></div>
                <span>Conjunction (0°)</span>
            </div>
            <div class="aspect-item">
                <div class="aspect-color" style="background-color: #00ccff;"></div>
                <span>Sextile (60°)</span>
            </div>
            <div class="aspect-item">
                <div class="aspect-color" style="background-color: #ff3366;"></div>
                <span>Square (90°)</span>
            </div>
            <div class="aspect-item">
                <div class="aspect-color" style="background-color: #33cc33;"></div>
                <span>Trine (120°)</span>
            </div>
            <div class="aspect-item">
                <div class="aspect-color" style="background-color: #ff6633;"></div>
                <span>Opposition (180°)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Generate a report to see planetary positions.")

# Tab 3: Trade Execution Strategy
with tab3:
    st.header("Trade Execution Strategy")
    
    if st.session_state.trade_strategy:
        st.markdown(f'<div class="strategy-box">{st.session_state.trade_strategy}</div>', unsafe_allow_html=True)
    else:
        st.info("Generate a report to see trade execution strategy.")

# Tab 4: Forecast
with tab4:
    st.header("6-Day Forecast")
    
    if st.session_state.forecast_data:
        # Display market type
        market_type = get_market_type(st.session_state.current_symbol)
        st.markdown(f'<div class="market-type">{market_type} Market</div>', unsafe_allow_html=True)
        
        # Display forecast summary
        st.subheader("Forecast Summary")
        
        # Create summary DataFrame
        summary_data = []
        for day_data in st.session_state.forecast_data:
            summary_data.append({
                "Date": day_data["date_str"],
                "Day": day_data["day_name"],
                "Sentiment": day_data["sentiment"]
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Add color formatting
        def highlight_sentiment(val):
            if "Bullish" in val:
                return 'color: #388e3c'
            elif "Bearish" in val:
                return 'color: #d32f2f'
            else:
                return 'color: #f57c00'
        
        # Display table with color formatting
        st.dataframe(
            summary_df.style.applymap(highlight_sentiment, subset=['Sentiment']),
            use_container_width=True
        )
        
        # Display detailed forecast for each day
        st.subheader("Detailed Forecast")
        
        for day_data in st.session_state.forecast_data:
            # Create expander for each day
            with st.expander(f"{day_data['date_str']} - {day_data['sentiment']}"):
                # Display day header with sentiment
                st.markdown(f"""
                <div class="forecast-day-header">
                    <div class="forecast-day-title">{day_data['date_str']} ({day_data['day_name']})</div>
                    <div class="forecast-day-sentiment {day_data['sentiment_class']}">{day_data['sentiment']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display planetary positions
                st.markdown('<div class="forecast-section-title">Planetary Positions</div>', unsafe_allow_html=True)
                planet_df = pd.DataFrame(day_data["planetary_data"])
                st.dataframe(planet_df, use_container_width=True)
                
                # Display aspects
                st.markdown('<div class="forecast-section-title">Astro Aspects</div>', unsafe_allow_html=True)
                if day_data["aspects"]:
                    aspects_df = pd.DataFrame(day_data["aspects"])
                    st.dataframe(aspects_df, use_container_width=True)
                else:
                    st.write("No significant aspects on this day.")
                
                # Display moon aspects
                st.markdown('<div class="forecast-section-title">Moon Aspects</div>', unsafe_allow_html=True)
                if day_data["moon_aspects"]:
                    moon_aspects_df = pd.DataFrame(day_data["moon_aspects"])
                    st.dataframe(moon_aspects_df, use_container_width=True)
                else:
                    st.write("No significant Moon aspects on this day.")
                
                # Display timeline
                st.markdown('<div class="forecast-section-title">Planetary Transit Timeline</div>', unsafe_allow_html=True)
                timeline_df = pd.DataFrame(day_data["timeline_data"])
                
                # Add color formatting
                def highlight_timeline_sentiment(val):
                    if "Bullish" in val:
                        return 'color: #388e3c'
                    elif "Bearish" in val:
                        return 'color: #d32f2f'
                    else:
                        return 'color: #f57c00'
                
                st.dataframe(
                    timeline_df.style.applymap(highlight_timeline_sentiment, subset=['Sentiment']),
                    use_container_width=True
                )
    else:
        st.info("Generate a report to see the forecast.")

# Status bar
st.markdown('<div class="status-bar">© 2025 Planetary Trading Dashboard | Status: Ready</div>', unsafe_allow_html=True)

# Auto-refresh every minute
if time.time() - st.session_state.last_update > 60:
    st.session_state.last_update = time.time()
    update_planetary_degrees()
    st.rerun()
