import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import plotly.graph_objects as go
import plotly.express as px
import math

# Set page configuration
st.set_page_config(
    page_title="Dynamic Planetary Trading Dashboard",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better alignment
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        color: #e94560;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .sub-title {
        font-size: 1.3rem;
        color: #f5f5f5;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .sentiment-card {
        background: linear-gradient(135deg, #81c784, #a5d6a7);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        color: #2e7d32;
        font-size: 1.8rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .sentiment-bullish {
        background: linear-gradient(135deg, #4caf50, #66bb6a);
        color: white;
    }
    
    .sentiment-bearish {
        background: linear-gradient(135deg, #f44336, #ef5350);
        color: white;
    }
    
    .sentiment-neutral {
        background: linear-gradient(135deg, #ff9800, #ffb74d);
        color: white;
    }
    
    .timeline-container {
        background: rgba(255,255,255,0.05);
        border: 2px solid #e94560;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        color: white;
    }
    
    .timeline-current {
        background: linear-gradient(135deg, #e94560, #f06292) !important;
        border: 3px solid #ffffff !important;
        animation: glow 2s infinite;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.6);
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 20px rgba(233, 69, 96, 0.6); }
        50% { box-shadow: 0 0 30px rgba(233, 69, 96, 0.9); }
        100% { box-shadow: 0 0 20px rgba(233, 69, 96, 0.6); }
    }
    
    .timeline-bullish {
        border-color: #4caf50;
        background: rgba(76, 175, 80, 0.1);
    }
    
    .timeline-bearish {
        border-color: #f44336;
        background: rgba(244, 67, 54, 0.1);
    }
    
    .timeline-neutral {
        border-color: #ff9800;
        background: rgba(255, 152, 0, 0.1);
    }
    
    .planet-container {
        background: rgba(255,255,255,0.08);
        border-left: 5px solid #e94560;
        padding: 20px;
        margin: 12px 0;
        border-radius: 10px;
        color: white;
    }
    
    .aspect-container {
        background: linear-gradient(90deg, #1a237e, #283593);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #e94560;
    }
    
    .strategy-section {
        background: linear-gradient(135deg, #1a237e, #3949ab);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .entry-opportunity {
        background: rgba(76, 175, 80, 0.15);
        border: 2px solid #4caf50;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        color: white;
    }
    
    .exit-warning {
        background: rgba(244, 67, 54, 0.15);
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        color: white;
    }
    
    .forecast-container {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 25px;
        margin: 18px 0;
        color: #333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .forecast-today {
        border: 4px solid #e94560;
        background: linear-gradient(135deg, #fff3f4, #fce4ec);
        animation: pulse-today 3s infinite;
    }
    
    @keyframes pulse-today {
        0% { border-color: #e94560; }
        50% { border-color: #f06292; }
        100% { border-color: #e94560; }
    }
    
    .live-time {
        font-family: 'Courier New', monospace;
        font-size: 1.3rem;
        font-weight: bold;
        color: #e94560;
        text-align: center;
        background: rgba(0,0,0,0.2);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border: 2px solid #e94560;
    }
    
    .current-hora-alert {
        background: linear-gradient(135deg, #e94560, #f06292);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.4);
        animation: pulse-alert 2s infinite;
    }
    
    @keyframes pulse-alert {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .data-table {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
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
if 'timeline_data' not in st.session_state:
    st.session_state.timeline_data = []
if 'aspects' not in st.session_state:
    st.session_state.aspects = []
if 'sentiment_data' not in st.session_state:
    st.session_state.sentiment_data = {}

# Enhanced planetary calculations
def calculate_dynamic_planetary_positions(date):
    """Calculate actual planetary positions based on date"""
    reference_date = datetime.date(2025, 1, 1)
    days_diff = (date - reference_date).days
    
    daily_movements = {
        "Sun": 0.9856, "Moon": 13.1764, "Mercury": 1.383, 
        "Venus": 1.202, "Mars": 0.524, "Jupiter": 0.083, 
        "Saturn": 0.034, "Rahu": -0.053, "Ketu": -0.053
    }
    
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
    
    # Aspect influence (limit to top 6)
    for aspect in aspects[:6]:
        aspect_type = aspect["type"]
        strength = aspect["strength"]
        
        multiplier = {"Exact": 1.0, "Close": 0.8, "Wide": 0.5}[strength]
        
        if aspect_type in ["Trine", "Sextile"]:
            sentiment_score += 1 * multiplier
            sentiment_factors.append(f"🔺 {aspect['planet1']}-{aspect['planet2']} {aspect_type} (+{1*multiplier:.1f})")
        elif aspect_type in ["Square", "Opposition"]:
            sentiment_score -= 1 * multiplier
            sentiment_factors.append(f"🔻 {aspect['planet1']}-{aspect['planet2']} {aspect_type} (-{1*multiplier:.1f})")
    
    # Day of week influence
    weekday = date.weekday()
    if weekday == 0:  # Monday
        sentiment_score -= 0.5
        sentiment_factors.append("🌙 Monday (Moon day) - emotional volatility (-0.5)")
    elif weekday == 1:  # Tuesday
        sentiment_score -= 1
        sentiment_factors.append("⚔️ Tuesday (Mars day) - aggressive trading (-1)")
    elif weekday == 3:  # Thursday
        sentiment_score += 1
        sentiment_factors.append("🎯 Thursday (Jupiter day) - optimistic trading (+1)")
    elif weekday == 4:  # Friday
        sentiment_score += 0.5
        sentiment_factors.append("💎 Friday (Venus day) - favorable for gains (+0.5)")
    
    # Determine sentiment level
    if sentiment_score >= 4:
        return "Extremely Bullish", "sentiment-bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= 2:
        return "Very Bullish", "sentiment-bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= 0.5:
        return "Bullish", "sentiment-bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= -0.5:
        return "Neutral", "sentiment-neutral", sentiment_score, sentiment_factors
    elif sentiment_score >= -2:
        return "Bearish", "sentiment-bearish", sentiment_score, sentiment_factors
    elif sentiment_score >= -4:
        return "Very Bearish", "sentiment-bearish", sentiment_score, sentiment_factors
    else:
        return "Extremely Bearish", "sentiment-bearish", sentiment_score, sentiment_factors

def generate_dynamic_timeline(symbol, date, planetary_degrees, aspects):
    """Generate dynamic timeline based on actual planetary positions"""
    market_type = "Indian" if symbol.upper() in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"] else "International"
    
    hora_sequence = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    
    if market_type == "Indian":
        start_hour, start_minute = 9, 15
        end_hour, end_minute = 15, 30
        hora_duration = 1
    else:
        start_hour, start_minute = 5, 0
        end_hour, end_minute = 23, 55
        hora_duration = 2
    
    current_time = datetime.datetime.combine(date, datetime.time(start_hour, start_minute))
    end_time = datetime.datetime.combine(date, datetime.time(end_hour, end_minute))
    
    timeline_data = []
    hora_index = (date.weekday() * 24 + start_hour) % 7
    
    while current_time <= end_time:
        hora_lord = hora_sequence[hora_index % 7]
        
        hora_degree = planetary_degrees.get(hora_lord, 0)
        hora_sign = get_sign_from_degree(hora_degree)
        hora_nakshatra = get_nakshatra_from_degree(hora_degree)
        hora_strength = get_planet_strength(hora_lord, hora_sign)
        
        relevant_aspects = [asp for asp in aspects if asp["planet1"] == hora_lord or asp["planet2"] == hora_lord]
        
        influence_parts = []
        influence_parts.append(f"{hora_lord} at {hora_degree:.1f}° in {hora_sign} ({hora_nakshatra})")
        
        if hora_strength != "Neutral":
            influence_parts.append(f"{hora_lord} is {hora_strength}")
        
        sentiment_score = 0
        for aspect in relevant_aspects[:2]:
            other_planet = aspect["planet2"] if aspect["planet1"] == hora_lord else aspect["planet1"]
            aspect_type = aspect["type"]
            strength = aspect["strength"]
            
            influence_parts.append(f"{aspect_type} with {other_planet} ({strength})")
            
            if aspect_type in ["Trine", "Sextile"]:
                sentiment_score += {"Exact": 2, "Close": 1.5, "Wide": 1}[strength]
            elif aspect_type in ["Square", "Opposition"]:
                sentiment_score -= {"Exact": 2, "Close": 1.5, "Wide": 1}[strength]
        
        if hora_lord in ["Jupiter", "Venus"]:
            sentiment_score += {"Exalted": 2, "Own Sign": 1, "Debilitated": -2}.get(hora_strength, 0)
        elif hora_lord in ["Mars", "Saturn", "Rahu", "Ketu"]:
            sentiment_score += {"Exalted": 1, "Own Sign": 0.5, "Debilitated": -2}.get(hora_strength, -0.5)
        else:
            sentiment_score += {"Exalted": 1.5, "Own Sign": 1, "Debilitated": -1.5}.get(hora_strength, 0)
        
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
        
        timeline_data.append({
            "Time": current_time.strftime("%I:%M %p"),
            "Event": f"{hora_lord} Hora - {current_time.strftime('%A')}",
            "Influence": ". ".join(influence_parts),
            "Sentiment": sentiment,
            "SentimentScore": sentiment_score,
            "HoraLord": hora_lord,
            "DateTime": current_time
        })
        
        current_time += datetime.timedelta(hours=hora_duration)
        hora_index += 1
    
    return timeline_data

def update_all_data(date, symbol):
    """Update all data when date or symbol changes"""
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
    
    # Calculate aspects
    st.session_state.aspects = calculate_dynamic_aspects(st.session_state.planetary_degrees)
    
    # Generate timeline
    st.session_state.timeline_data = generate_dynamic_timeline(symbol, date, st.session_state.planetary_degrees, st.session_state.aspects)
    
    # Calculate sentiment
    sentiment, sentiment_class, sentiment_score, sentiment_factors = calculate_market_sentiment_dynamic(
        st.session_state.planetary_data, st.session_state.aspects, date
    )
    
    st.session_state.sentiment_data = {
        "sentiment": sentiment,
        "sentiment_class": sentiment_class,
        "sentiment_score": sentiment_score,
        "sentiment_factors": sentiment_factors
    }

# Header
st.markdown('<div class="main-title">🌟 DYNAMIC PLANETARY TRADING DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time Astro-Financial Intelligence System</div>', unsafe_allow_html=True)

# Live time display
current_time = datetime.datetime.now()
market_status = "OPEN" if 9 <= current_time.hour <= 15 and current_time.weekday() < 5 else "CLOSED"
st.markdown(f'<div class="live-time">🕐 Live Time: {current_time.strftime("%Y-%m-%d %H:%M:%S")} | Market Status: {market_status}</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📊 Trading Parameters")
date = st.sidebar.date_input("📅 Select Date", value=st.session_state.current_date)
symbol = st.sidebar.text_input("💹 Trading Symbol", value=st.session_state.current_symbol)
city = st.sidebar.text_input("🌍 Location", value="Mumbai")

# Auto-update when inputs change
if date != st.session_state.current_date or symbol != st.session_state.current_symbol:
    st.session_state.current_date = date
    st.session_state.current_symbol = symbol
    update_all_data(date, symbol)

# Initialize data if not exists
if not st.session_state.planetary_data:
    update_all_data(date, symbol)

# Display market sentiment
sentiment_data = st.session_state.sentiment_data
st.markdown(f'<div class="sentiment-card {sentiment_data["sentiment_class"]}">{sentiment_data["sentiment"]}<br><small>Score: {sentiment_data["sentiment_score"]:.1f}</small></div>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🕐 Transit Timeline", "🪐 Planetary Positions", "⚡ Strategy", "🔮 Forecast"])

with tab1:
    st.header("🕐 Critical Transit Timeline")
    
    # Find current hora
    now = datetime.datetime.now()
    current_hora = None
    
    for i, item in enumerate(st.session_state.timeline_data):
        time_str = item["Time"]
        sentiment_item = item["Sentiment"]
        hora_lord = item["HoraLord"]
        influence = item["Influence"]
        
        # Check if this is current hora
        try:
            item_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
            is_current = False
            if i < len(st.session_state.timeline_data) - 1:
                next_time = datetime.datetime.strptime(st.session_state.timeline_data[i+1]["Time"], "%I:%M %p").time()
                is_current = item_time <= now.time() < next_time
            else:
                is_current = item_time <= now.time()
        except:
            is_current = False
        
        if is_current:
            current_hora = item
        
        # Create timeline item with proper alignment
        col1, col2, col3 = st.columns([6, 2, 1])
        
        with col1:
            # Determine timeline class
            timeline_class = "timeline-container"
            if is_current:
                timeline_class += " timeline-current"
            elif sentiment_item in ["Very Bullish", "Bullish"]:
                timeline_class += " timeline-bullish"
            elif sentiment_item in ["Very Bearish", "Bearish"]:
                timeline_class += " timeline-bearish"
            else:
                timeline_class += " timeline-neutral"
            
            timeline_content = f"""
            <div class="{timeline_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h4 style="margin: 0; color: white;">⏰ {time_str} - {hora_lord} Hora</h4>
                    {"<span style='color: #ffff00; font-weight: bold;'>🔥 CURRENT</span>" if is_current else ""}
                </div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.95rem;">
                    <strong>Influence:</strong> {influence}
                </div>
                <div style="margin-top: 10px; color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                    <strong>Score:</strong> {item['SentimentScore']:.1f}
                </div>
            </div>
            """
            st.markdown(timeline_content, unsafe_allow_html=True)
        
        with col2:
            # Sentiment indicator
            if sentiment_item == "Very Bullish":
                st.success(f"🚀 {sentiment_item}")
            elif sentiment_item == "Bullish":
                st.success(f"📈 {sentiment_item}")
            elif sentiment_item == "Very Bearish":
                st.error(f"📉 {sentiment_item}")
            elif sentiment_item == "Bearish":
                st.error(f"🔻 {sentiment_item}")
            else:
                st.warning(f"⚖️ {sentiment_item}")
        
        with col3:
            # Action recommendation
            if item['SentimentScore'] > 1:
                st.success("BUY")
            elif item['SentimentScore'] < -1:
                st.error("SELL")
            else:
                st.warning("HOLD")
    
    # Current hora alert
    if current_hora:
        action_text = "LONG POSITIONS" if current_hora['SentimentScore'] > 0 else "SHORT POSITIONS" if current_hora['SentimentScore'] < -1 else "CAUTIOUS TRADING"
        st.markdown(f'''
        <div class="current-hora-alert">
            <h2>🔥 CURRENT HORA ACTIVE</h2>
            <h3>{current_hora['HoraLord']} Hora - {current_hora['Sentiment']}</h3>
            <p><strong>Recommended Action:</strong> {action_text}</p>
            <p><strong>Sentiment Score:</strong> {current_hora['SentimentScore']:.1f}</p>
        </div>
        ''', unsafe_allow_html=True)

with tab2:
    st.header("🪐 Planetary Positions & Strengths")
    
    # Display planetary data in organized layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌟 Planetary Positions")
        for i, planet in enumerate(st.session_state.planetary_data):
            if i % 2 == 0:  # Show every other planet in left column
                planet_content = f"""
                <div class="planet-container">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: white;">{planet["Planet"]}</h4>
                            <p style="margin: 5px 0; color: #e94560; font-weight: bold;">{planet["Degree"]} in {planet["Sign"]}</p>
                            <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">{planet["Nakshatra"]}</p>
                        </div>
                    </div>
                </div>
                """
                st.markdown(planet_content, unsafe_allow_html=True)
                
                # Strength indicator
                strength = planet["Strength"]
                if strength == "Exalted":
                    st.success(f"✨ {strength}")
                elif strength == "Own Sign":
                    st.info(f"🏠 {strength}")
                elif strength == "Debilitated":
                    st.error(f"⚠️ {strength}")
                else:
                    st.warning(f"⚖️ {strength}")
    
    with col2:
        st.subheader("🌟 Planetary Positions")
        for i, planet in enumerate(st.session_state.planetary_data):
            if i % 2 == 1:  # Show every other planet in right column
                planet_content = f"""
                <div class="planet-container">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: white;">{planet["Planet"]}</h4>
                            <p style="margin: 5px 0; color: #e94560; font-weight: bold;">{planet["Degree"]} in {planet["Sign"]}</p>
                            <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">{planet["Nakshatra"]}</p>
                        </div>
                    </div>
                </div>
                """
                st.markdown(planet_content, unsafe_allow_html=True)
                
                # Strength indicator
                strength = planet["Strength"]
                if strength == "Exalted":
                    st.success(f"✨ {strength}")
                elif strength == "Own Sign":
                    st.info(f"🏠 {strength}")
                elif strength == "Debilitated":
                    st.error(f"⚠️ {strength}")
                else:
                    st.warning(f"⚖️ {strength}")
    
    # Display aspects in organized layout
    st.subheader("⚡ Active Planetary Aspects")
    
    if st.session_state.aspects:
        # Create aspects table
        aspects_data = []
        for aspect in st.session_state.aspects[:12]:  # Show top 12
            aspects_data.append({
                "Aspect": f"{aspect['planet1']} {aspect['type']} {aspect['planet2']}",
                "Strength": aspect['strength'],
                "Orb": f"{aspect['orb']:.1f}°",
                "Angle": f"{aspect['angle']:.1f}°"
            })
        
        aspects_df = pd.DataFrame(aspects_data)
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(aspects_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No significant aspects found for this date.")

with tab3:
    st.header("⚡ Dynamic Trading Strategy")
    
    # Strategy content
    date_str = date.strftime("%d %B %Y (%A)")
    sentiment_data = st.session_state.sentiment_data
    
    st.markdown(f'''
    <div class="strategy-section">
        <h2>🎯 Trading Strategy for {symbol} on {date_str}</h2>
        <div style="text-align: center; margin: 20px 0;">
            <div class="sentiment-card {sentiment_data["sentiment_class"]}">
                Market Sentiment: {sentiment_data["sentiment"]}<br>
                <small>Score: {sentiment_data["sentiment_score"]:.1f}</small>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sentiment breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Sentiment Analysis Breakdown")
        for factor in sentiment_data["sentiment_factors"][:8]:
            st.write(f"• {factor}")
    
    with col2:
        st.subheader("⏰ Hora-based Trading Windows")
        
        # Find best entries and avoid periods
        best_entries = []
        avoid_periods = []
        
        for timeline_item in st.session_state.timeline_data:
            hora_score = timeline_item["SentimentScore"]
            if hora_score >= 1.5:
                best_entries.append(timeline_item)
            elif hora_score <= -1.5:
                avoid_periods.append(timeline_item)
        
        st.write(f"**Best Entry Opportunities:** {len(best_entries)}")
        st.write(f"**Periods to Avoid:** {len(avoid_periods)}")
    
    # Display best entries
    if best_entries:
        st.subheader("🚀 Best Entry Opportunities")
        for entry in best_entries[:3]:
            target = f"{1.2 + entry['SentimentScore'] * 0.3:.1f}%"
            entry_content = f"""
            <div class="entry-opportunity">
                <h4>⏰ {entry["Time"]} - {entry["HoraLord"]} Hora</h4>
                <p><strong>Action:</strong> Strong Buy | <strong>Target:</strong> {target} | <strong>Stop:</strong> 0.5%</p>
                <p><strong>Reason:</strong> {entry["Influence"][:120]}...</p>
                <p><strong>Score:</strong> {entry['SentimentScore']:.1f}</p>
            </div>
            """
            st.markdown(entry_content, unsafe_allow_html=True)
    else:
        st.info("No strong bullish signals detected today.")
    
    # Display avoid periods
    if avoid_periods:
        st.subheader("⚠️ Periods to Avoid/Short")
        for avoid in avoid_periods[:3]:
            avoid_content = f"""
            <div class="exit-warning">
                <h4>⏰ {avoid["Time"]} - {avoid["HoraLord"]} Hora</h4>
                <p><strong>Action:</strong> Avoid/Short</p>
                <p><strong>Reason:</strong> {avoid["Influence"][:120]}...</p>
                <p><strong>Score:</strong> {avoid['SentimentScore']:.1f}</p>
            </div>
            """
            st.markdown(avoid_content, unsafe_allow_html=True)
    else:
        st.info("No major bearish signals detected today.")
    
    # Symbol-specific strategy
    st.subheader(f"📈 {symbol}-Specific Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if symbol.upper() == "NIFTY":
            jupiter_degree = st.session_state.planetary_degrees.get('Jupiter', 0)
            saturn_degree = st.session_state.planetary_degrees.get('Saturn', 0)
            st.write(f"• **Support Levels:** Jupiter at {jupiter_degree:.0f}°")
            st.write(f"• **Resistance:** Saturn at {saturn_degree:.0f}°")
            st.write(f"• **Breakout Potential:** {'High' if sentiment_data['sentiment_score'] > 2 else 'Moderate' if sentiment_data['sentiment_score'] > 0 else 'Low'}")
            
        elif symbol.upper() == "BANKNIFTY":
            mars_degree = st.session_state.planetary_degrees.get("Mars", 0)
            mars_sign = get_sign_from_degree(mars_degree)
            mars_strength = get_planet_strength("Mars", mars_sign)
            st.write(f"• **Mars Influence:** {mars_degree:.0f}° in {mars_sign} - {mars_strength}")
            st.write(f"• **Banking Sentiment:** {'Positive' if sentiment_data['sentiment_score'] > 1 else 'Negative' if sentiment_data['sentiment_score'] < -1 else 'Mixed'}")
            st.write(f"• **Volatility:** {'High' if abs(sentiment_data['sentiment_score']) > 2 else 'Moderate'}")
    
    with col2:
        st.subheader("🛡️ Risk Management")
        st.write(f"• **Position Size:** {'Conservative (10-15%)' if abs(sentiment_data['sentiment_score']) > 3 else 'Moderate (15-20%)' if abs(sentiment_data['sentiment_score']) > 1 else 'Normal (20-25%)'}")
        st.write("• **Stop-Loss:** 0.5% for intraday, 1% for swing")
        st.write(f"• **Profit Booking:** {'Aggressive' if sentiment_data['sentiment'] == 'Extremely Bullish' else 'Gradual'}")
        st.write("• **Max Daily Loss:** 2% of capital")
    
    # Key insight
    insight_text = "Focus on long positions during favorable horas." if sentiment_data['sentiment_score'] > 0 else "Exercise caution and consider short strategies." if sentiment_data['sentiment_score'] < -1 else "Mixed signals suggest smaller position sizes."
    st.info(f"**Today's Key Insight:** {date_str} shows {sentiment_data['sentiment'].lower()} energy. {insight_text}")

with tab4:
    st.header("🔮 Multi-day Forecast")
    
    # Generate 7-day forecast
    forecast_dates = []
    for i in range(-3, 4):
        forecast_date = date + datetime.timedelta(days=i)
        forecast_dates.append((forecast_date, i))
    
    col1, col2 = st.columns(2)
    
    for idx, (forecast_date, day_offset) in enumerate(forecast_dates):
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
        
        # Alternate between columns
        current_col = col1 if idx % 2 == 0 else col2
        
        with current_col:
            # Create forecast card
            card_class = "forecast-container forecast-today" if day_offset == 0 else "forecast-container"
            
            forecast_content = f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div>
                        <h3 style="margin: 0; color: #333;">
                            {forecast_date.strftime("%d %B %Y")} ({forecast_date.strftime("%A")})
                            {"🎯 TODAY" if day_offset == 0 else ""}
                        </h3>
                    </div>
                </div>
                <div style="color: #666; margin-bottom: 10px;">
                    <strong>Sentiment:</strong> {forecast_sentiment} (Score: {forecast_score:.1f})<br>
                    <strong>Active Aspects:</strong> {len(forecast_aspects)}<br>
                    <strong>Recommendation:</strong> {"Long bias" if forecast_score > 1 else "Short bias" if forecast_score < -1 else "Neutral approach"}
                </div>
            </div>
            """
            st.markdown(forecast_content, unsafe_allow_html=True)
            
            # Sentiment indicator
            if forecast_sentiment in ["Very Bullish", "Extremely Bullish"]:
                st.success(f"🚀 {forecast_sentiment}")
            elif forecast_sentiment == "Bullish":
                st.success(f"📈 {forecast_sentiment}")
            elif forecast_sentiment in ["Very Bearish", "Extremely Bearish"]:
                st.error(f"📉 {forecast_sentiment}")
            elif forecast_sentiment == "Bearish":
                st.error(f"🔻 {forecast_sentiment}")
            else:
                st.warning(f"⚖️ {forecast_sentiment}")

# Footer
st.markdown("---")
st.markdown("🌟 **Dynamic Planetary Trading Dashboard** | Real-time Astro-Financial Intelligence")
st.caption("Powered by Advanced Astrological Calculations & Market Analysis")
st.caption(f"Last Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S')} | Data for: {date.strftime('%d %B %Y')} | Symbol: {symbol}")
