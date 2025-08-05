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
    page_title="Dynamic Planetary Trading Dashboard",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for better styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        color: #e94560;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(233, 69, 96, 0.5); }
        to { text-shadow: 0 0 30px rgba(233, 69, 96, 0.8), 0 0 40px rgba(233, 69, 96, 0.6); }
    }
    
    .sub-header {
        font-family: 'Roboto', sans-serif;
        font-size: 1.4rem;
        color: #f5f5f5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .dynamic-card {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        border: 1px solid rgba(233, 69, 96, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        color: white;
    }
    
    .dynamic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(233, 69, 96, 0.2);
        border-color: rgba(233, 69, 96, 0.6);
    }
    
    .planet-strength {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 2px;
    }
    
    .strength-exalted { background-color: #4caf50; color: white; }
    .strength-own { background-color: #2196f3; color: white; }
    .strength-friend { background-color: #ff9800; color: white; }
    .strength-neutral { background-color: #9e9e9e; color: white; }
    .strength-enemy { background-color: #f44336; color: white; }
    .strength-debilitated { background-color: #e91e63; color: white; }
    
    .aspect-badge {
        background-color: #ff8800;
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 10px;
    }
    
    .aspect-exact { background-color: #ff4444; }
    .aspect-close { background-color: #ff8800; }
    .aspect-wide { background-color: #ffaa00; }
    
    .transit-card {
        background: linear-gradient(90deg, #1a237e 0%, #283593 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 5px solid #e94560;
    }
    
    .market-sentiment-display {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .extremely-bullish {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        color: white;
        animation: bounce 2s ease-in-out infinite;
    }
    
    .very-bullish {
        background: linear-gradient(135deg, #66bb6a 0%, #81c784 100%);
        color: white;
    }
    
    .bullish {
        background: linear-gradient(135deg, #81c784 0%, #a5d6a7 100%);
        color: #2e7d32;
    }
    
    .neutral {
        background: linear-gradient(135deg, #ff9800 0%, #ffb74d 100%);
        color: white;
    }
    
    .bearish {
        background: linear-gradient(135deg, #ef5350 0%, #e57373 100%);
        color: white;
    }
    
    .very-bearish {
        background: linear-gradient(135deg, #f44336 0%, #ef5350 100%);
        color: white;
    }
    
    .extremely-bearish {
        background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
        color: white;
        animation: shake 1.5s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .timeline-item {
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 18px;
        margin: 10px 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
        color: white;
    }
    
    .timeline-item:hover {
        transform: translateX(8px);
        background: rgba(255,255,255,0.12);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .timeline-bullish { border-color: #4caf50; }
    .timeline-bearish { border-color: #f44336; }
    .timeline-volatile { border-color: #ff9800; }
    .timeline-neutral { border-color: #9e9e9e; }
    
    .current-hora {
        background: linear-gradient(135deg, #e94560 0%, #f06292 100%) !important;
        color: white !important;
        font-weight: bold;
        border: 2px solid #ffffff !important;
        animation: glow-border 2s ease-in-out infinite alternate;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
    }
    
    @keyframes glow-border {
        from { border-color: #ffffff; box-shadow: 0 0 20px rgba(233, 69, 96, 0.5); }
        to { border-color: #e94560; box-shadow: 0 0 30px rgba(233, 69, 96, 0.8); }
    }
    
    .strategy-container {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .strategy-entry {
        background: rgba(76, 175, 80, 0.2);
        border: 1px solid #4caf50;
        border-radius: 10px;
        padding: 15px;
        margin: 12px 0;
        color: white;
    }
    
    .strategy-exit {
        background: rgba(244, 67, 54, 0.2);
        border: 1px solid #f44336;
        border-radius: 10px;
        padding: 15px;
        margin: 12px 0;
        color: white;
    }
    
    .live-time-display {
        font-family: 'Orbitron', monospace;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        color: #e94560;
        background: rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .planetary-degree {
        font-family: 'Orbitron', monospace;
        font-weight: bold;
        color: #e94560;
    }
    
    .forecast-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #333;
    }
    
    .forecast-today {
        border: 3px solid #e94560;
        background: linear-gradient(135deg, #fff3f4 0%, #fce4ec 100%);
        animation: pulse-border 2s ease-in-out infinite;
    }
    
    @keyframes pulse-border {
        0%, 100% { border-color: #e94560; }
        50% { border-color: #f06292; }
    }
    
    .sentiment-list {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        color: white;
    }
    
    .sentiment-list ul {
        list-style-type: none;
        padding-left: 0;
        margin: 0;
    }
    
    .sentiment-list li {
        padding: 5px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .sentiment-list li:last-child {
        border-bottom: none;
    }
    
    .current-hora-alert {
        background: linear-gradient(135deg, #e94560 0%, #f06292 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3);
    }
    
    .planet-card {
        background: rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 4px solid #e94560;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'planetary_data' not in st.session_state:
    st.session_state.planetary_data = None
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.date.today()
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "NIFTY"
if 'planetary_degrees' not in st.session_state:
    st.session_state.planetary_degrees = {}

# Enhanced planetary calculations with proper astronomy
def calculate_dynamic_planetary_positions(date):
    """Calculate actual planetary positions based on date with realistic movement"""
    reference_date = datetime.date(2025, 1, 1)
    days_diff = (date - reference_date).days
    
    # More accurate daily movements (degrees per day)
    daily_movements = {
        "Sun": 0.9856,      # 360° in 365.25 days
        "Moon": 13.1764,    # 360° in 27.3 days
        "Mercury": 1.383,   # Average, varies due to retrograde
        "Venus": 1.202,     # Average, varies due to retrograde
        "Mars": 0.524,      # 360° in 687 days
        "Jupiter": 0.083,   # 360° in 4333 days (11.86 years)
        "Saturn": 0.034,    # 360° in 10759 days (29.46 years)
        "Rahu": -0.053,     # Retrograde motion
        "Ketu": -0.053      # Same as Rahu but opposite
    }
    
    # Base positions for reference date (Jan 1, 2025)
    base_positions = {
        "Sun": 279.5, "Moon": 145.2, "Mercury": 285.1, 
        "Venus": 320.7, "Mars": 295.3, "Jupiter": 42.8, 
        "Saturn": 332.1, "Rahu": 15.4, "Ketu": 195.4
    }
    
    new_positions = {}
    for planet, base_pos in base_positions.items():
        movement = daily_movements[planet] * days_diff
        new_pos = (base_pos + movement) % 360
        new_positions[planet] = new_pos
    
    return new_positions

def get_planet_strength(planet, sign):
    """Calculate planet strength in sign"""
    planet_rulerships = {
        "Sun": {"exalted": "Aries", "own": ["Leo"], "debilitated": "Libra"},
        "Moon": {"exalted": "Taurus", "own": ["Cancer"], "debilitated": "Scorpio"},
        "Mercury": {"exalted": "Virgo", "own": ["Gemini", "Virgo"], "debilitated": "Pisces"},
        "Venus": {"exalted": "Pisces", "own": ["Taurus", "Libra"], "debilitated": "Virgo"},
        "Mars": {"exalted": "Capricorn", "own": ["Aries", "Scorpio"], "debilitated": "Cancer"},
        "Jupiter": {"exalted": "Cancer", "own": ["Sagittarius", "Pisces"], "debilitated": "Capricorn"},
        "Saturn": {"exalted": "Libra", "own": ["Capricorn", "Aquarius"], "debilitated": "Aries"},
        "Rahu": {"exalted": "Gemini", "own": [], "debilitated": "Sagittarius"},
        "Ketu": {"exalted": "Sagittarius", "own": [], "debilitated": "Gemini"}
    }
    
    if planet in planet_rulerships:
        rulership = planet_rulerships[planet]
        if sign == rulership.get("exalted"):
            return "Exalted"
        elif sign in rulership.get("own", []):
            return "Own Sign"
        elif sign == rulership.get("debilitated"):
            return "Debilitated"
        else:
            return "Neutral"
    return "Neutral"

def get_sign_from_degree(degree):
    """Get zodiac sign from degree"""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sign_index = int(degree // 30)
    return signs[sign_index % 12]

def get_nakshatra_from_degree(degree):
    """Get nakshatra from degree"""
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    nakshatra_index = int(degree // 13.333333)
    return nakshatras[nakshatra_index % 27]

def calculate_dynamic_aspects(degrees):
    """Calculate aspects with orb strength"""
    aspects = []
    planets = list(degrees.keys())
    
    aspect_types = {
        "Conjunction": {"angle": 0, "orb": 8},
        "Sextile": {"angle": 60, "orb": 6},
        "Square": {"angle": 90, "orb": 8},
        "Trine": {"angle": 120, "orb": 8},
        "Opposition": {"angle": 180, "orb": 8}
    }
    
    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            planet1, planet2 = planets[i], planets[j]
            angle1, angle2 = degrees[planet1], degrees[planet2]
            
            diff = abs(angle1 - angle2) % 360
            if diff > 180:
                diff = 360 - diff
            
            for aspect_name, aspect_data in aspect_types.items():
                aspect_angle = aspect_data["angle"]
                orb = aspect_data["orb"]
                
                if abs(diff - aspect_angle) <= orb:
                    orb_difference = abs(diff - aspect_angle)
                    if orb_difference <= 2:
                        strength = "Exact"
                    elif orb_difference <= 4:
                        strength = "Close"
                    else:
                        strength = "Wide"
                    
                    aspects.append({
                        "planet1": planet1,
                        "planet2": planet2,
                        "type": aspect_name,
                        "angle": diff,
                        "orb": orb_difference,
                        "strength": strength
                    })
    
    return aspects

def calculate_market_sentiment_dynamic(planetary_data, aspects, date):
    """Dynamic market sentiment calculation"""
    sentiment_score = 0
    sentiment_factors = []
    
    # Planetary strength influence
    for planet in planetary_data:
        strength = planet.get("Strength", "Neutral")
        planet_name = planet["Planet"]
        
        if planet_name in ["Jupiter", "Venus"]:  # Natural benefics
            if strength == "Exalted":
                sentiment_score += 3
                sentiment_factors.append(f"✅ {planet_name} exalted (+3)")
            elif strength == "Own Sign":
                sentiment_score += 2
                sentiment_factors.append(f"✅ {planet_name} in own sign (+2)")
            elif strength == "Debilitated":
                sentiment_score -= 2
                sentiment_factors.append(f"❌ {planet_name} debilitated (-2)")
            else:
                sentiment_score += 1
                sentiment_factors.append(f"⚪ {planet_name} neutral (+1)")
        
        elif planet_name in ["Mars", "Saturn"]:  # Natural malefics
            if strength == "Exalted":
                sentiment_score += 1
                sentiment_factors.append(f"⚡ {planet_name} exalted (+1)")
            elif strength == "Own Sign":
                sentiment_score += 0.5
                sentiment_factors.append(f"⚡ {planet_name} in own sign (+0.5)")
            elif strength == "Debilitated":
                sentiment_score -= 3
                sentiment_factors.append(f"💥 {planet_name} debilitated (-3)")
            else:
                sentiment_score -= 1
                sentiment_factors.append(f"⚠️ {planet_name} neutral (-1)")
        
        elif planet_name in ["Rahu", "Ketu"]:  # Shadow planets
            if strength == "Exalted":
                sentiment_score += 0.5
                sentiment_factors.append(f"🌟 {planet_name} exalted (+0.5)")
            elif strength == "Debilitated":
                sentiment_score -= 2
                sentiment_factors.append(f"🌑 {planet_name} debilitated (-2)")
            else:
                sentiment_score -= 0.5
                sentiment_factors.append(f"🔄 {planet_name} creates uncertainty (-0.5)")
    
    # Aspect influence
    for aspect in aspects[:8]:  # Limit to top 8 aspects
        aspect_type = aspect["type"]
        strength = aspect["strength"]
        
        multiplier = {"Exact": 1.0, "Close": 0.8, "Wide": 0.5}[strength]
        
        if aspect_type in ["Trine", "Sextile"]:
            sentiment_score += 1 * multiplier
            sentiment_factors.append(f"🔺 {aspect['planet1']}-{aspect['planet2']} {aspect_type} (+{1*multiplier:.1f})")
        elif aspect_type in ["Square", "Opposition"]:
            sentiment_score -= 1 * multiplier
            sentiment_factors.append(f"🔻 {aspect['planet1']}-{aspect['planet2']} {aspect_type} (-{1*multiplier:.1f})")
        elif aspect_type == "Conjunction":
            # Conjunction effect depends on planets involved
            if set([aspect["planet1"], aspect["planet2"]]) & {"Jupiter", "Venus"}:
                sentiment_score += 0.5 * multiplier
                sentiment_factors.append(f"✨ {aspect['planet1']}-{aspect['planet2']} conjunction (+{0.5*multiplier:.1f})")
            else:
                sentiment_score -= 0.5 * multiplier
                sentiment_factors.append(f"⚡ {aspect['planet1']}-{aspect['planet2']} conjunction (-{0.5*multiplier:.1f})")
    
    # Day of week influence
    weekday = date.weekday()
    if weekday == 0:  # Monday - Moon day
        sentiment_score -= 0.5
        sentiment_factors.append("🌙 Monday (Moon day) - emotional volatility (-0.5)")
    elif weekday == 1:  # Tuesday - Mars day
        sentiment_score -= 1
        sentiment_factors.append("⚔️ Tuesday (Mars day) - aggressive trading (-1)")
    elif weekday == 3:  # Thursday - Jupiter day
        sentiment_score += 1
        sentiment_factors.append("🎯 Thursday (Jupiter day) - optimistic trading (+1)")
    elif weekday == 4:  # Friday - Venus day
        sentiment_score += 0.5
        sentiment_factors.append("💎 Friday (Venus day) - favorable for gains (+0.5)")
    
    # Determine sentiment level
    if sentiment_score >= 4:
        return "Extremely Bullish", "extremely-bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= 2:
        return "Very Bullish", "very-bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= 0.5:
        return "Bullish", "bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= -0.5:
        return "Neutral", "neutral", sentiment_score, sentiment_factors
    elif sentiment_score >= -2:
        return "Bearish", "bearish", sentiment_score, sentiment_factors
    elif sentiment_score >= -4:
        return "Very Bearish", "very-bearish", sentiment_score, sentiment_factors
    else:
        return "Extremely Bearish", "extremely-bearish", sentiment_score, sentiment_factors

def generate_dynamic_timeline(symbol, date, planetary_degrees, aspects):
    """Generate dynamic timeline based on actual planetary positions"""
    market_type = "Indian" if symbol.upper() in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"] else "International"
    
    # Calculate hora lords based on actual planetary positions
    hora_sequence = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    
    if market_type == "Indian":
        start_hour = 9
        start_minute = 15
        end_hour = 15
        end_minute = 30
        hora_duration = 1  # 1 hour
    else:
        start_hour = 5
        start_minute = 0
        end_hour = 23
        end_minute = 55
        hora_duration = 2  # 2 hours
    
    current_time = datetime.datetime.combine(date, datetime.time(start_hour, start_minute))
    end_time = datetime.datetime.combine(date, datetime.time(end_hour, end_minute))
    
    timeline_data = []
    hora_index = (date.weekday() * 24 + start_hour) % 7  # Start with appropriate hora
    
    while current_time <= end_time:
        hora_lord = hora_sequence[hora_index % 7]
        
        # Get hora lord's position and strength
        hora_degree = planetary_degrees.get(hora_lord, 0)
        hora_sign = get_sign_from_degree(hora_degree)
        hora_nakshatra = get_nakshatra_from_degree(hora_degree)
        hora_strength = get_planet_strength(hora_lord, hora_sign)
        
        # Calculate dynamic influence based on aspects
        relevant_aspects = [asp for asp in aspects if asp["planet1"] == hora_lord or asp["planet2"] == hora_lord]
        
        # Generate dynamic influence text
        influence_parts = []
        influence_parts.append(f"{hora_lord} at {hora_degree:.1f}° in {hora_sign} ({hora_nakshatra})")
        
        if hora_strength != "Neutral":
            influence_parts.append(f"{hora_lord} is {hora_strength}")
        
        # Add aspect influences
        sentiment_score = 0
        for aspect in relevant_aspects[:2]:  # Limit to top 2 aspects
            other_planet = aspect["planet2"] if aspect["planet1"] == hora_lord else aspect["planet1"]
            aspect_type = aspect["type"]
            strength = aspect["strength"]
            
            influence_parts.append(f"{aspect_type} with {other_planet} ({strength})")
            
            # Calculate sentiment impact
            if aspect_type in ["Trine", "Sextile"]:
                sentiment_score += {"Exact": 2, "Close": 1.5, "Wide": 1}[strength]
            elif aspect_type in ["Square", "Opposition"]:
                sentiment_score -= {"Exact": 2, "Close": 1.5, "Wide": 1}[strength]
        
        # Adjust sentiment based on planet nature and strength
        if hora_lord in ["Jupiter", "Venus"]:
            sentiment_score += {"Exalted": 2, "Own Sign": 1, "Debilitated": -2}.get(hora_strength, 0)
        elif hora_lord in ["Mars", "Saturn", "Rahu", "Ketu"]:
            sentiment_score += {"Exalted": 1, "Own Sign": 0.5, "Debilitated": -2}.get(hora_strength, -0.5)
        else:  # Sun, Moon, Mercury
            sentiment_score += {"Exalted": 1.5, "Own Sign": 1, "Debilitated": -1.5}.get(hora_strength, 0)
        
        # Determine sentiment
        if sentiment_score >= 2:
            sentiment = "Very Bullish"
        elif sentiment_score >= 1:
            sentiment = "Bullish"
        elif sentiment_score >= -1:
            sentiment = "Neutral"
        elif sentiment_score >= -2:
            sentiment = "Bearish"
        else:
            sentiment = "Very Bearish"
        
        # Add market-specific influences
        if hora_lord == "Mars" and symbol.upper() == "BANKNIFTY":
            influence_parts.append("Banking under Mars - volatility expected")
        elif hora_lord == "Jupiter" and "GOLD" in symbol.upper():
            influence_parts.append("Jupiter favorable for precious metals")
        elif hora_lord == "Mercury" and "BTC" in symbol.upper():
            influence_parts.append("Mercury enhances crypto momentum")
        
        timeline_data.append({
            "Time": current_time.strftime("%I:%M %p"),
            "Event": f"{hora_lord} Hora - {current_time.strftime('%A')}",
            "Influence": ". ".join(influence_parts),
            "Sentiment": sentiment,
            "SentimentScore": sentiment_score,
            "HoraLord": hora_lord,
            "DateTime": current_time
        })
        
        # Move to next hora
        current_time += datetime.timedelta(hours=hora_duration)
        hora_index += 1
    
    return timeline_data

# Header
st.markdown('<div class="main-header">🌟 DYNAMIC PLANETARY TRADING DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time Astro-Financial Intelligence System</div>', unsafe_allow_html=True)

# Live time display
current_time = datetime.datetime.now()
market_status = "OPEN" if 9 <= current_time.hour <= 15 and current_time.weekday() < 5 else "CLOSED"
st.markdown(f'<div class="live-time-display">🕐 Live Time: {current_time.strftime("%Y-%m-%d %H:%M:%S")} | Market Status: <strong>{market_status}</strong></div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📊 Trading Parameters")
date = st.sidebar.date_input("📅 Select Date", value=st.session_state.current_date)
symbol = st.sidebar.text_input("💹 Trading Symbol", value=st.session_state.current_symbol, 
                              help="Enter: NIFTY, BANKNIFTY, GOLD, BTC, DOWJONES, etc.")
city = st.sidebar.text_input("🌍 Location", value="Mumbai")

# Auto-update when inputs change
if date != st.session_state.current_date or symbol != st.session_state.current_symbol:
    st.session_state.current_date = date
    st.session_state.current_symbol = symbol
    
    # Calculate new planetary positions
    st.session_state.planetary_degrees = calculate_dynamic_planetary_positions(date)
    
    # Generate planetary data with strength
    planetary_data = []
    for planet, degree in st.session_state.planetary_degrees.items():
        sign = get_sign_from_degree(degree)
        nakshatra = get_nakshatra_from_degree(degree)
        strength = get_planet_strength(planet, sign)
        
        planetary_data.append({
            "Planet": planet,
            "Degree": f"{int(degree)}°{int((degree % 1) * 60)}'",
            "Sign": sign,
            "Nakshatra": nakshatra,
            "Strength": strength
        })
    
    st.session_state.planetary_data = planetary_data

# Generate data if not exists
if not st.session_state.planetary_data:
    st.session_state.planetary_degrees = calculate_dynamic_planetary_positions(date)
    planetary_data = []
    for planet, degree in st.session_state.planetary_degrees.items():
        sign = get_sign_from_degree(degree)
        nakshatra = get_nakshatra_from_degree(degree)
        strength = get_planet_strength(planet, sign)
        
        planetary_data.append({
            "Planet": planet,
            "Degree": f"{int(degree)}°{int((degree % 1) * 60)}'",
            "Sign": sign,
            "Nakshatra": nakshatra,
            "Strength": strength
        })
    
    st.session_state.planetary_data = planetary_data

# Calculate aspects
aspects = calculate_dynamic_aspects(st.session_state.planetary_degrees)

# Generate timeline
timeline_data = generate_dynamic_timeline(symbol, date, st.session_state.planetary_degrees, aspects)

# Calculate market sentiment
sentiment, sentiment_class, sentiment_score, sentiment_factors = calculate_market_sentiment_dynamic(
    st.session_state.planetary_data, aspects, date
)

# Display market sentiment
st.markdown(f'<div class="market-sentiment-display {sentiment_class}">{sentiment}<br><small>Sentiment Score: {sentiment_score:.1f}</small></div>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🕐 Transit Timeline", "🪐 Planetary Positions", "⚡ Strategy", "🔮 Forecast"])

with tab1:
    st.markdown('<div class="dynamic-card">', unsafe_allow_html=True)
    st.header("🕐 Critical Transit Timeline")
    
    # Current time highlighting
    now = datetime.datetime.now()
    current_hora = None
    
    for i, item in enumerate(timeline_data):
        time_str = item["Time"]
        sentiment_item = item["Sentiment"]
        hora_lord = item["HoraLord"]
        influence = item["Influence"]
        
        # Check if this is current hora
        try:
            item_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
            is_current = False
            if i < len(timeline_data) - 1:
                next_time = datetime.datetime.strptime(timeline_data[i+1]["Time"], "%I:%M %p").time()
                is_current = item_time <= now.time() < next_time
            else:
                is_current = item_time <= now.time()
        except:
            is_current = False
        
        # Style based on sentiment and current status
        if is_current:
            item_class = "timeline-item current-hora"
            current_hora = item
        else:
            sentiment_class_map = {
                "Very Bullish": "timeline-bullish",
                "Bullish": "timeline-bullish", 
                "Neutral": "timeline-neutral",
                "Bearish": "timeline-bearish",
                "Very Bearish": "timeline-bearish"
            }
            sentiment_timeline_class = sentiment_class_map.get(sentiment_item, "timeline-neutral")
            item_class = f"timeline-item {sentiment_timeline_class}"
        
        # Create timeline item
        timeline_item_html = f"""
        <div class="{item_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div>
                    <strong>⏰ {time_str} - {hora_lord} Hora</strong>
                    {"<span style='color: #ffff00; margin-left: 10px;'>🔥 CURRENT</span>" if is_current else ""}
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 15px; font-size: 0.9rem; font-weight: bold;">
                    {sentiment_item}
                </div>
            </div>
            <div style="font-size: 0.9rem; color: rgba(255,255,255,0.9);">
                <strong>Influence:</strong> {influence}
            </div>
        </div>
        """
        
        st.markdown(timeline_item_html, unsafe_allow_html=True)
    
    # Current hora info
    if current_hora:
        action_text = "LONG POSITIONS" if current_hora['SentimentScore'] > 0 else "SHORT POSITIONS" if current_hora['SentimentScore'] < -1 else "CAUTIOUS TRADING"
        current_hora_html = f"""
        <div class="current-hora-alert">
            <h3>🔥 CURRENT HORA ACTIVE</h3>
            <h2>{current_hora['HoraLord']} Hora - {current_hora['Sentiment']}</h2>
            <p><strong>Recommended Action:</strong> {action_text}</p>
            <p><strong>Score:</strong> {current_hora['SentimentScore']:.1f}</p>
        </div>
        """
        st.markdown(current_hora_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="dynamic-card">', unsafe_allow_html=True)
    st.header("🪐 Planetary Positions & Strengths")
    
    # Display planetary data with strength indicators
    for planet in st.session_state.planetary_data:
        strength = planet["Strength"]
        strength_class_map = {
            "Exalted": "strength-exalted",
            "Own Sign": "strength-own", 
            "Debilitated": "strength-debilitated",
            "Neutral": "strength-neutral"
        }
        strength_class = strength_class_map.get(strength, "strength-neutral")
        
        planet_html = f"""
        <div class="planet-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 1.1rem;">{planet['Planet']}</strong> - 
                    <span class="planetary-degree">{planet['Degree']}</span> in 
                    <strong>{planet['Sign']}</strong> ({planet['Nakshatra']})
                </div>
                <div class="planet-strength {strength_class}">{strength}</div>
            </div>
        </div>
        """
        st.markdown(planet_html, unsafe_allow_html=True)
    
    # Display aspects with strength
    st.subheader("⚡ Active Planetary Aspects")
    if aspects:
        for aspect in aspects[:12]:  # Show top 12 aspects
            aspect_class = f"aspect-{aspect['strength'].lower()}"
            aspect_html = f"""
            <div class="transit-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{aspect['planet1']} {aspect['type']} {aspect['planet2']}</strong>
                        <span class="aspect-badge {aspect_class}">{aspect['strength']}</span>
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">
                        Orb: {aspect['orb']:.1f}°
                    </div>
                </div>
            </div>
            """
            st.markdown(aspect_html, unsafe_allow_html=True)
    else:
        st.write("No significant aspects found for this date.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.header("⚡ Dynamic Trading Strategy")
    
    # Create strategy content
    date_str = date.strftime("%d %B %Y (%A)")
    market_type = "Indian" if symbol.upper() in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"] else "International"
    
    strategy_html = f"""
    <div class="strategy-container">
        <h2>🎯 Dynamic Trading Strategy for {symbol}</h2>
        <div style="text-align: center; margin: 20px 0;">
            <div class="market-sentiment-display {sentiment_class}">
                Overall Market Sentiment: {sentiment}<br>
                <small>Score: {sentiment_score:.1f}</small>
            </div>
        </div>
        
        <div class="sentiment-list">
            <h4>📊 Sentiment Analysis Breakdown:</h4>
            <ul>
    """
    
    for factor in sentiment_factors[:8]:  # Show top 8 factors
        strategy_html += f"<li>{factor}</li>"
    
    strategy_html += """
            </ul>
        </div>
        
        <h3>⏰ Hora-based Trading Windows</h3>
    """
    
    # Generate strategies for each significant hora
    best_entries = []
    avoid_periods = []
    
    for i, timeline_item in enumerate(timeline_data):
        hora_sentiment = timeline_item["Sentiment"]
        hora_score = timeline_item["SentimentScore"]
        hora_lord = timeline_item["HoraLord"]
        time_str = timeline_item["Time"]
        
        if hora_score >= 1.5:
            best_entries.append({
                "time": time_str,
                "hora": hora_lord,
                "action": "Strong Buy",
                "target": f"{1.2 + hora_score * 0.3:.1f}%",
                "stop": "0.5%",
                "reason": timeline_item["Influence"]
            })
        elif hora_score <= -1.5:
            avoid_periods.append({
                "time": time_str,
                "hora": hora_lord,
                "action": "Avoid/Short",
                "reason": timeline_item["Influence"]
            })
    
    # Display best entry opportunities
    if best_entries:
        strategy_html += "<h4>🚀 Best Entry Opportunities:</h4>"
        for entry in best_entries[:3]:  # Show top 3
            strategy_html += f"""
            <div class="strategy-entry">
                <strong>⏰ {entry['time']} - {entry['hora']} Hora</strong><br>
                <strong>Action:</strong> {entry['action']}<br>
                <strong>Target:</strong> {entry['target']} | <strong>Stop-Loss:</strong> {entry['stop']}<br>
                <strong>Reason:</strong> {entry['reason'][:100]}...
            </div>
            """
    else:
        strategy_html += "<h4>🚀 Best Entry Opportunities:</h4><p>No strong bullish signals detected today.</p>"
    
    # Display periods to avoid
    if avoid_periods:
        strategy_html += "<h4>⚠️ Periods to Avoid/Short:</h4>"
        for avoid in avoid_periods[:3]:  # Show top 3
            strategy_html += f"""
            <div class="strategy-exit">
                <strong>⏰ {avoid['time']} - {avoid['hora']} Hora</strong><br>
                <strong>Action:</strong> {avoid['action']}<br>
                <strong>Reason:</strong> {avoid['reason'][:100]}...
            </div>
            """
    else:
        strategy_html += "<h4>⚠️ Periods to Avoid/Short:</h4><p>No major bearish signals detected today.</p>"
    
    # Add symbol-specific strategies
    if symbol.upper() == "NIFTY":
        jupiter_degree = st.session_state.planetary_degrees.get('Jupiter', 0)
        saturn_degree = st.session_state.planetary_degrees.get('Saturn', 0)
        strategy_html += f"""
        <h4>📈 NIFTY-Specific Strategy:</h4>
        <ul>
            <li><strong>Support Levels:</strong> Jupiter at {jupiter_degree:.0f}° provides support</li>
            <li><strong>Resistance:</strong> Saturn at {saturn_degree:.0f}° may create resistance</li>
            <li><strong>Breakout Potential:</strong> {"High" if sentiment_score > 2 else "Moderate" if sentiment_score > 0 else "Low"}</li>
            <li><strong>Intraday Range:</strong> Expected {"expansion" if abs(sentiment_score) > 2 else "normal" if abs(sentiment_score) > 1 else "contraction"}</li>
        </ul>
        """
    elif symbol.upper() == "BANKNIFTY":
        mars_degree = st.session_state.planetary_degrees.get("Mars", 0)
        mars_sign = get_sign_from_degree(mars_degree)
        mars_strength = get_planet_strength("Mars", mars_sign)
        strategy_html += f"""
        <h4>🏦 BANKNIFTY-Specific Strategy:</h4>
        <ul>
            <li><strong>Mars Influence:</strong> Mars at {mars_degree:.0f}° in {mars_sign} - {mars_strength}</li>
            <li><strong>Banking Sentiment:</strong> {"Positive" if sentiment_score > 1 else "Negative" if sentiment_score < -1 else "Mixed"}</li>
            <li><strong>Volatility Expected:</strong> {"High" if abs(sentiment_score) > 2 else "Moderate"}</li>
            <li><strong>Sector Focus:</strong> {"Private banks" if mars_strength in ["Exalted", "Own Sign"] else "PSU banks" if sentiment_score > 0 else "Defensive approach"}</li>
        </ul>
        """
    elif "GOLD" in symbol.upper():
        venus_degree = st.session_state.planetary_degrees.get("Venus", 0)
        jupiter_degree = st.session_state.planetary_degrees.get("Jupiter", 0)
        strategy_html += f"""
        <h4>🥇 GOLD-Specific Strategy:</h4>
        <ul>
            <li><strong>Venus Influence:</strong> Venus at {venus_degree:.0f}° affects precious metals</li>
            <li><strong>Jupiter Support:</strong> Jupiter at {jupiter_degree:.0f}° provides {"strong" if sentiment_score > 1 else "weak"} support</li>
            <li><strong>USD Impact:</strong> Monitor currency movements alongside planetary transits</li>
            <li><strong>Safe Haven Status:</strong> {"Enhanced" if sentiment_score < -1 else "Normal"}</li>
        </ul>
        """
    
    strategy_html += f"""
        <h3>🛡️ Risk Management</h3>
        <ul>
            <li><strong>Position Size:</strong> {"Conservative (10-15%)" if abs(sentiment_score) > 3 else "Moderate (15-20%)" if abs(sentiment_score) > 1 else "Normal (20-25%)"}</li>
            <li><strong>Stop-Loss:</strong> 0.5% for intraday, 1% for swing trades</li>
            <li><strong>Profit Booking:</strong> {"Aggressive" if sentiment == "Extremely Bullish" else "Gradual"} - book 50% at 1st target</li>
            <li><strong>Max Daily Loss:</strong> 2% of capital</li>
            <li><strong>Volatility Adjustment:</strong> {"Reduce size" if abs(sentiment_score) > 3 else "Standard size"}</li>
        </ul>
        
        <div style="background: rgba(233, 69, 96, 0.1); border: 1px solid #e94560; border-radius: 10px; padding: 15px; margin: 20px 0;">
            <h4 style="color: #e94560;">⚡ Today's Key Insight:</h4>
            <p>{date_str} shows <strong>{sentiment.lower()}</strong> energy with primary influence from {timeline_data[0]['HoraLord'] if timeline_data else 'planetary'} transits. 
            {"Focus on long positions during favorable horas and use trailing stops." if sentiment_score > 0 else "Exercise caution and consider short strategies with tight risk management." if sentiment_score < -1 else "Mixed signals suggest smaller position sizes and quick scalping strategies."}</p>
        </div>
    </div>
    """
    
    st.markdown(strategy_html, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="dynamic-card">', unsafe_allow_html=True)
    st.header("🔮 Multi-day Forecast")
    
    # Generate 7-day forecast
    for i in range(-3, 4):
        forecast_date = date + datetime.timedelta(days=i)
        forecast_degrees = calculate_dynamic_planetary_positions(forecast_date)
        forecast_aspects = calculate_dynamic_aspects(forecast_degrees)
        
        # Generate forecast planetary data
        forecast_planetary_data = []
        for planet, degree in forecast_degrees.items():
            sign = get_sign_from_degree(degree)
            strength = get_planet_strength(planet, sign)
            forecast_planetary_data.append({
                "Planet": planet,
                "Sign": sign,
                "Strength": strength
            })
        
        forecast_sentiment, forecast_class, forecast_score, _ = calculate_market_sentiment_dynamic(
            forecast_planetary_data, forecast_aspects, forecast_date
        )
        
        # Highlight today
        card_class = "forecast-card forecast-today" if i == 0 else "forecast-card"
        
        forecast_html = f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div>
                    <h3 style="margin: 0;">{forecast_date.strftime("%d %B %Y")} ({forecast_date.strftime("%A")})</h3>
                    {"<span style='color: #e94560; font-weight: bold;'>🎯 TODAY</span>" if i == 0 else ""}
                </div>
                <div class="market-sentiment-display {forecast_class}" style="font-size: 1rem; padding: 8px 15px; margin: 0;">
                    {forecast_sentiment}
                </div>
            </div>
            <div style="color: #666;">
                <strong>Key Influences:</strong> {len(forecast_aspects)} active aspects | 
                <strong>Score:</strong> {forecast_score:.1f} | 
                <strong>Recommendation:</strong> {"Long bias" if forecast_score > 1 else "Short bias" if forecast_score < -1 else "Neutral approach"}
            </div>
        </div>
        """
        st.markdown(forecast_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 40px;">
    <p>🌟 Dynamic Planetary Trading Dashboard | Real-time Astro-Financial Intelligence</p>
    <p><small>Powered by Advanced Astrological Calculations & Market Analysis</small></p>
</div>
""", unsafe_allow_html=True)
