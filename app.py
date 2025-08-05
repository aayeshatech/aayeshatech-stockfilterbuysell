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

# Simple but effective CSS
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
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        color: #2e7d32;
        font-size: 1.5rem;
        font-weight: bold;
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
    
    .timeline-card {
        background: rgba(255,255,255,0.1);
        border: 1px solid #e94560;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
    }
    
    .current-hora {
        background: linear-gradient(135deg, #e94560, #f06292) !important;
        border: 2px solid white !important;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(233, 69, 96, 0.5); }
        50% { box-shadow: 0 0 20px rgba(233, 69, 96, 0.8); }
        100% { box-shadow: 0 0 5px rgba(233, 69, 96, 0.5); }
    }
    
    .planet-card {
        background: rgba(255,255,255,0.08);
        border-left: 4px solid #e94560;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        color: white;
    }
    
    .aspect-card {
        background: linear-gradient(90deg, #1a237e, #283593);
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #e94560;
    }
    
    .strategy-card {
        background: linear-gradient(135deg, #1a237e, #3949ab);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .entry-signal {
        background: rgba(76, 175, 80, 0.2);
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: white;
    }
    
    .exit-signal {
        background: rgba(244, 67, 54, 0.2);
        border: 1px solid #f44336;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: white;
    }
    
    .forecast-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        color: #333;
    }
    
    .forecast-today {
        border: 3px solid #e94560;
        background: #fff3f4;
    }
    
    .live-time {
        font-family: monospace;
        font-size: 1.2rem;
        color: #e94560;
        text-align: center;
        background: rgba(0,0,0,0.2);
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
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

# Calculate aspects and timeline
aspects = calculate_dynamic_aspects(st.session_state.planetary_degrees)
timeline_data = generate_dynamic_timeline(symbol, date, st.session_state.planetary_degrees, aspects)

# Calculate market sentiment
sentiment, sentiment_class, sentiment_score, sentiment_factors = calculate_market_sentiment_dynamic(
    st.session_state.planetary_data, aspects, date
)

# Display market sentiment using Streamlit components
st.markdown(f'<div class="sentiment-card {sentiment_class}">{sentiment}<br><small>Score: {sentiment_score:.1f}</small></div>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🕐 Transit Timeline", "🪐 Planetary Positions", "⚡ Strategy", "🔮 Forecast"])

with tab1:
    st.header("🕐 Critical Transit Timeline")
    
    # Find current hora
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
        
        if is_current:
            current_hora = item
        
        # Create timeline item using columns
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if is_current:
                st.markdown(f'<div class="timeline-card current-hora">🔥 <strong>{time_str} - {hora_lord} Hora (CURRENT)</strong><br>{influence}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="timeline-card"><strong>{time_str} - {hora_lord} Hora</strong><br>{influence}</div>', unsafe_allow_html=True)
        
        with col2:
            # Sentiment badge
            if sentiment_item == "Very Bullish" or sentiment_item == "Bullish":
                st.success(sentiment_item)
            elif sentiment_item == "Very Bearish" or sentiment_item == "Bearish":
                st.error(sentiment_item)
            else:
                st.warning(sentiment_item)
    
    # Current hora alert
    if current_hora:
        st.success(f"🔥 CURRENT HORA: {current_hora['HoraLord']} - {current_hora['Sentiment']} (Score: {current_hora['SentimentScore']:.1f})")
        
        action_text = "LONG POSITIONS" if current_hora['SentimentScore'] > 0 else "SHORT POSITIONS" if current_hora['SentimentScore'] < -1 else "CAUTIOUS TRADING"
        st.info(f"**Recommended Action:** {action_text}")

with tab2:
    st.header("🪐 Planetary Positions & Strengths")
    
    # Display planetary data in a clean format
    for planet in st.session_state.planetary_data:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div class="planet-card"><strong>{planet["Planet"]}</strong> - {planet["Degree"]} in <strong>{planet["Sign"]}</strong> ({planet["Nakshatra"]})</div>', unsafe_allow_html=True)
        
        with col2:
            strength = planet["Strength"]
            if strength == "Exalted":
                st.success(strength)
            elif strength == "Own Sign":
                st.info(strength)
            elif strength == "Debilitated":
                st.error(strength)
            else:
                st.warning(strength)
    
    # Display aspects
    st.subheader("⚡ Active Planetary Aspects")
    
    if aspects:
        for aspect in aspects[:10]:  # Show top 10
            st.markdown(f'<div class="aspect-card"><strong>{aspect["planet1"]} {aspect["type"]} {aspect["planet2"]}</strong> - {aspect["strength"]} (Orb: {aspect["orb"]:.1f}°)</div>', unsafe_allow_html=True)
    else:
        st.info("No significant aspects found for this date.")

with tab3:
    st.header("⚡ Dynamic Trading Strategy")
    
    # Strategy content using Streamlit components
    date_str = date.strftime("%d %B %Y (%A)")
    
    st.markdown(f'<div class="strategy-card"><h2>🎯 Strategy for {symbol} on {date_str}</h2></div>', unsafe_allow_html=True)
    
    # Sentiment breakdown
    st.subheader("📊 Sentiment Analysis Breakdown")
    for factor in sentiment_factors[:8]:
        st.write(f"• {factor}")
    
    # Trading windows
    st.subheader("⏰ Hora-based Trading Windows")
    
    # Find best entries and avoid periods
    best_entries = []
    avoid_periods = []
    
    for timeline_item in timeline_data:
        hora_score = timeline_item["SentimentScore"]
        if hora_score >= 1.5:
            best_entries.append(timeline_item)
        elif hora_score <= -1.5:
            avoid_periods.append(timeline_item)
    
    # Display best entries
    if best_entries:
        st.subheader("🚀 Best Entry Opportunities")
        for entry in best_entries[:3]:
            target = f"{1.2 + entry['SentimentScore'] * 0.3:.1f}%"
            st.markdown(f'<div class="entry-signal"><strong>{entry["Time"]} - {entry["HoraLord"]} Hora</strong><br>Action: Strong Buy | Target: {target} | Stop: 0.5%<br>Reason: {entry["Influence"][:100]}...</div>', unsafe_allow_html=True)
    else:
        st.info("No strong bullish signals detected today.")
    
    # Display avoid periods
    if avoid_periods:
        st.subheader("⚠️ Periods to Avoid/Short")
        for avoid in avoid_periods[:3]:
            st.markdown(f'<div class="exit-signal"><strong>{avoid["Time"]} - {avoid["HoraLord"]} Hora</strong><br>Action: Avoid/Short<br>Reason: {avoid["Influence"][:100]}...</div>', unsafe_allow_html=True)
    else:
        st.info("No major bearish signals detected today.")
    
    # Symbol-specific strategy
    st.subheader(f"📈 {symbol}-Specific Strategy")
    
    if symbol.upper() == "NIFTY":
        jupiter_degree = st.session_state.planetary_degrees.get('Jupiter', 0)
        saturn_degree = st.session_state.planetary_degrees.get('Saturn', 0)
        st.write(f"• **Support Levels:** Jupiter at {jupiter_degree:.0f}° provides support")
        st.write(f"• **Resistance:** Saturn at {saturn_degree:.0f}° may create resistance")
        st.write(f"• **Breakout Potential:** {'High' if sentiment_score > 2 else 'Moderate' if sentiment_score > 0 else 'Low'}")
        
    elif symbol.upper() == "BANKNIFTY":
        mars_degree = st.session_state.planetary_degrees.get("Mars", 0)
        mars_sign = get_sign_from_degree(mars_degree)
        mars_strength = get_planet_strength("Mars", mars_sign)
        st.write(f"• **Mars Influence:** Mars at {mars_degree:.0f}° in {mars_sign} - {mars_strength}")
        st.write(f"• **Banking Sentiment:** {'Positive' if sentiment_score > 1 else 'Negative' if sentiment_score < -1 else 'Mixed'}")
        st.write(f"• **Volatility Expected:** {'High' if abs(sentiment_score) > 2 else 'Moderate'}")
    
    # Risk management
    st.subheader("🛡️ Risk Management")
    st.write(f"• **Position Size:** {'Conservative (10-15%)' if abs(sentiment_score) > 3 else 'Moderate (15-20%)' if abs(sentiment_score) > 1 else 'Normal (20-25%)'}")
    st.write("• **Stop-Loss:** 0.5% for intraday, 1% for swing trades")
    st.write(f"• **Profit Booking:** {'Aggressive' if sentiment == 'Extremely Bullish' else 'Gradual'} - book 50% at 1st target")
    st.write("• **Max Daily Loss:** 2% of capital")
    
    # Key insight
    insight_text = "Focus on long positions during favorable horas." if sentiment_score > 0 else "Exercise caution and consider short strategies." if sentiment_score < -1 else "Mixed signals suggest smaller position sizes."
    st.info(f"**Today's Key Insight:** {date_str} shows {sentiment.lower()} energy. {insight_text}")

with tab4:
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
        
        # Create forecast card
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if i == 0:  # Today
                st.markdown(f'<div class="forecast-card forecast-today"><h3>🎯 {forecast_date.strftime("%d %B %Y")} ({forecast_date.strftime("%A")}) - TODAY</h3><strong>Key Influences:</strong> {len(forecast_aspects)} active aspects | Score: {forecast_score:.1f}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="forecast-card"><h3>{forecast_date.strftime("%d %B %Y")} ({forecast_date.strftime("%A")})</h3><strong>Key Influences:</strong> {len(forecast_aspects)} active aspects | Score: {forecast_score:.1f}</div>', unsafe_allow_html=True)
        
        with col2:
            if forecast_sentiment in ["Very Bullish", "Bullish"]:
                st.success(forecast_sentiment)
            elif forecast_sentiment in ["Very Bearish", "Bearish"]:
                st.error(forecast_sentiment)
            else:
                st.warning(forecast_sentiment)
            
            # Recommendation
            recommendation = "Long bias" if forecast_score > 1 else "Short bias" if forecast_score < -1 else "Neutral"
            st.caption(f"**Rec:** {recommendation}")

# Footer
st.markdown("---")
st.markdown("🌟 **Dynamic Planetary Trading Dashboard** | Real-time Astro-Financial Intelligence")
st.caption("Powered by Advanced Astrological Calculations & Market Analysis")
