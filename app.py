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
# Simple CSS for basic styling only
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #e94560;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 20px;
    }
    .stAlert > div {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .bullish {
        color: #16a34a;
        font-weight: bold;
    }
    .bearish {
        color: #dc2626;
        font-weight: bold;
    }
    .neutral {
        color: #6b7280;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Define planetary aspects data for August 6, 2025
aug6_aspects = [
    {
        "time": "02:06 am",
        "aspect": "Moon Quintile Node (☽ ⬠ ☊)",
        "meaning": "Unusual opportunities, karmic shifts",
        "indian_market": "Neutral",
        "commodities": "Neutral",
        "forex": "Sudden trend change",
        "global_market": "Neutral"
    },
    {
        "time": "02:34 am",
        "aspect": "Moon BiQuintile Uranus (☽ bQ ♅)",
        "meaning": "Innovative but erratic energy",
        "indian_market": "Tech stocks volatile",
        "commodities": "Neutral",
        "forex": "Bullish",
        "global_market": "Neutral"
    },
    {
        "time": "02:38 am",
        "aspect": "Moon Opposition Venus (☽ ☍ ♀)",
        "meaning": "Emotional vs. financial balance",
        "indian_market": "Neutral",
        "commodities": "Short-term dip",
        "forex": "Neutral",
        "global_market": "Neutral"
    },
    {
        "time": "04:38 am",
        "aspect": "Sun BiQuintile Moon (☉ bQ ☽)",
        "meaning": "Creative problem-solving",
        "indian_market": "BankNifty recovery",
        "commodities": "Neutral",
        "forex": "Neutral",
        "global_market": "Neutral"
    },
    {
        "time": "10:25 am",
        "aspect": "Mars SemiSquare Lilith (♂ ∠ ⚸)",
        "meaning": "Aggressive speculation",
        "indian_market": "Midcaps/Smallcaps risks",
        "commodities": "Neutral",
        "forex": "Neutral",
        "global_market": "Neutral"
    },
    {
        "time": "01:39 pm",
        "aspect": "Moon Opposition Jupiter (☽ ☍ ♃)",
        "meaning": "Overconfidence vs. reality check",
        "indian_market": "Rally then profit-booking",
        "commodities": "Neutral",
        "forex": "Neutral",
        "global_market": "Temporary rally then profit-booking"
    },
    {
        "time": "04:53 pm",
        "aspect": "Sun Quincunx Moon (☉ ⚻ ☽)",
        "meaning": "Adjustments needed",
        "indian_market": "Neutral",
        "commodities": "Bearish pressure",
        "forex": "Neutral",
        "global_market": "Neutral"
    },
    {
        "time": "05:10 pm",
        "aspect": "Moon Sextile Lilith (☽ ⚹ ⚸)",
        "meaning": "Hidden opportunities",
        "indian_market": "Neutral",
        "commodities": "Neutral",
        "forex": "Altcoins rally",
        "global_market": "Neutral"
    },
    {
        "time": "07:35 pm",
        "aspect": "Moon Sesquiquadrate Uranus (☽ ⚼ ♅)",
        "meaning": "Sudden disruptions",
        "indian_market": "Neutral",
        "commodities": "Neutral",
        "forex": "Neutral",
        "global_market": "After-hours volatility"
    },
    {
        "time": "09:18 pm",
        "aspect": "Sun Square Lilith (☉ ☐ ⚸)",
        "meaning": "Power struggles, manipulation",
        "indian_market": "Neutral",
        "commodities": "Institutional manipulation",
        "forex": "Neutral",
        "global_market": "Neutral"
    }
]

# Initialize session state with proper defaults
def initialize_session_state():
    defaults = {
        'planetary_data': [],
        'current_date': datetime.date(2025, 8, 6),  # Set default to Aug 6, 2025
        'current_symbol': "NIFTY",
        'planetary_degrees': {},
        'timeline_data': [],
        'aspects': [],
        'sentiment_data': {},
        'forecast_data': [],
        'last_update': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
# Enhanced planetary calculations
def calculate_dynamic_planetary_positions(date):
    """Calculate actual planetary positions based on date"""
    # Updated reference date to August 6, 2025
    reference_date = datetime.date(2025, 8, 6)
    days_diff = (date - reference_date).days
    
    daily_movements = {
        "Sun": 0.9856, "Moon": 13.1764, "Mercury": 1.383, 
        "Venus": 1.202, "Mars": 0.524, "Jupiter": 0.083, 
        "Saturn": 0.034, "Rahu": -0.053, "Ketu": -0.053
    }
    
    # Updated base positions for August 6, 2025 (as per your requirements)
    base_positions = {
        "Sun": 109.5,      # Cancer 19°30' = 90 + 19.5
        "Moon": 251.68,    # Sagittarius 11°41' = 240 + 11.6833
        "Mercury": 94.27,  # Cancer 4°16' = 90 + 4.2667
        "Venus": 137.75,   # Leo 17°45' = 120 + 17.75
        "Mars": 87.0,      # Gemini 27°00' = 60 + 27
        "Jupiter": 22.67,  # Aries 22°40' = 0 + 22.6667
        "Saturn": 308.33,  # Aquarius 8°20' = 300 + 8.3333
        "Rahu": 352.67,    # Pisces 22°40' = 330 + 22.6667
        "Ketu": 172.67     # Virgo 22°40' = 150 + 22.6667
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
                        "Planet 1": planet1,
                        "Aspect": aspect_name,
                        "Planet 2": planet2,
                        "Strength": strength,
                        "Orb": f"{orb_difference:.1f}°"
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
        aspect_type = aspect["Aspect"]
        strength = aspect["Strength"]
        
        multiplier = {"Exact": 1.0, "Close": 0.8, "Wide": 0.5}[strength]
        
        if aspect_type in ["Trine", "Sextile"]:
            sentiment_score += 1 * multiplier
            sentiment_factors.append(f"🔺 {aspect['Planet 1']}-{aspect['Planet 2']} {aspect_type} (+{1*multiplier:.1f})")
        elif aspect_type in ["Square", "Opposition"]:
            sentiment_score -= 1 * multiplier
            sentiment_factors.append(f"🔻 {aspect['Planet 1']}-{aspect['Planet 2']} {aspect_type} (-{1*multiplier:.1f})")
    
    # Day of week influence
    weekday = date.weekday()
    weekday_effects = {
        0: ("🌙 Monday (Moon day) - emotional volatility", -0.5),
        1: ("⚔️ Tuesday (Mars day) - aggressive trading", -1),
        3: ("🎯 Thursday (Jupiter day) - optimistic trading", 1),
        4: ("💎 Friday (Venus day) - favorable for gains", 0.5)
    }
    
    if weekday in weekday_effects:
        effect_text, effect_score = weekday_effects[weekday]
        sentiment_score += effect_score
        sentiment_factors.append(f"{effect_text} ({effect_score:+.1f})")
    
    # Determine sentiment level
    if sentiment_score >= 4:
        return "Extremely Bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= 2:
        return "Very Bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= 0.5:
        return "Bullish", sentiment_score, sentiment_factors
    elif sentiment_score >= -0.5:
        return "Neutral", sentiment_score, sentiment_factors
    elif sentiment_score >= -2:
        return "Bearish", sentiment_score, sentiment_factors
    elif sentiment_score >= -4:
        return "Very Bearish", sentiment_score, sentiment_factors
    else:
        return "Extremely Bearish", sentiment_score, sentiment_factors
def generate_dynamic_timeline(symbol, date, planetary_degrees, aspects):
    """Generate dynamic timeline based on actual planetary positions"""
    market_type = "Indian" if symbol.upper() in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"] else "International"
    
    hora_sequence = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    
    if market_type == "Indian":
        times = ["09:15 AM", "10:15 AM", "11:15 AM", "12:15 PM", "01:15 PM", "02:15 PM", "03:15 PM"]
    else:
        times = ["05:00 AM", "07:00 AM", "09:00 AM", "11:00 AM", "01:00 PM", "03:00 PM", "05:00 PM", "07:00 PM", "09:00 PM", "11:00 PM"]
    
    timeline_data = []
    hora_index = (date.weekday() * 24 + 9) % 7  # Start with appropriate hora
    
    for i, time_str in enumerate(times):
        hora_lord = hora_sequence[hora_index % 7]
        
        hora_degree = planetary_degrees.get(hora_lord, 0)
        hora_sign = get_sign_from_degree(hora_degree)
        hora_nakshatra = get_nakshatra_from_degree(hora_degree)
        hora_strength = get_planet_strength(hora_lord, hora_sign)
        
        relevant_aspects = [asp for asp in aspects if asp["Planet 1"] == hora_lord or asp["Planet 2"] == hora_lord]
        
        influence_parts = []
        influence_parts.append(f"{hora_lord} at {hora_degree:.1f}° in {hora_sign} ({hora_nakshatra})")
        
        if hora_strength != "Neutral":
            influence_parts.append(f"{hora_lord} is {hora_strength}")
        
        sentiment_score = 0
        for aspect in relevant_aspects[:2]:
            other_planet = aspect["Planet 2"] if aspect["Planet 1"] == hora_lord else aspect["Planet 1"]
            aspect_type = aspect["Aspect"]
            strength = aspect["Strength"]
            
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
            "Time": time_str,
            "Hora Lord": hora_lord,
            "Influence": ". ".join(influence_parts),
            "Sentiment": sentiment,
            "Score": sentiment_score,
            "Action": "BUY" if sentiment_score > 1 else "SELL" if sentiment_score < -1 else "HOLD"
        })
        
        hora_index += 1
    
    return timeline_data
def update_all_data(date, symbol):
    """Update all data when date or symbol changes"""
    with st.spinner("Updating planetary data..."):
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
        sentiment, sentiment_score, sentiment_factors = calculate_market_sentiment_dynamic(
            st.session_state.planetary_data, st.session_state.aspects, date
        )
        
        st.session_state.sentiment_data = {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "sentiment_factors": sentiment_factors
        }
        
        # Generate forecast
        forecast_data = []
        for i in range(-3, 4):
            forecast_date = date + datetime.timedelta(days=i)
            forecast_degrees = calculate_dynamic_planetary_positions(forecast_date)
            forecast_aspects = calculate_dynamic_aspects(forecast_degrees)
            
            forecast_planetary_data = []
            for planet, degree in forecast_degrees.items():
                sign = get_sign_from_degree(degree)
                strength = get_planet_strength(planet, sign)
                forecast_planetary_data.append({
                    "Planet": planet,
                    "Sign": sign,
                    "Strength": strength
                })
            
            forecast_sentiment, forecast_score, _ = calculate_market_sentiment_dynamic(
                forecast_planetary_data, forecast_aspects, forecast_date
            )
            
            forecast_data.append({
                "Date": forecast_date.strftime("%d %B %Y"),
                "Day": forecast_date.strftime("%A"),
                "Sentiment": forecast_sentiment,
                "Score": forecast_score,
                "Aspects": len(forecast_aspects),
                "Is Today": i == 0
            })
        
        st.session_state.forecast_data = forecast_data
        st.session_state.last_update = datetime.datetime.now()
# Initialize session state
initialize_session_state()
# Header
st.markdown('<div class="main-title">🌟 DYNAMIC PLANETARY TRADING DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time Astro-Financial Intelligence System</div>', unsafe_allow_html=True)
# Live time display
current_time = datetime.datetime.now()
market_status = "OPEN" if 9 <= current_time.hour <= 15 and current_time.weekday() < 5 else "CLOSED"
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"🕐 **Live Time:** {current_time.strftime('%H:%M:%S')}")
with col2:
    st.info(f"📅 **Date:** {current_time.strftime('%d %B %Y')}")
with col3:
    st.info(f"📈 **Market Status:** {market_status}")
# Sidebar
st.sidebar.header("📊 Trading Parameters")
date = st.sidebar.date_input("📅 Select Date", value=st.session_state.current_date)
symbol = st.sidebar.text_input("💹 Trading Symbol", value=st.session_state.current_symbol)
city = st.sidebar.text_input("🌍 Location", value="Mumbai")
# Display reference date info
st.sidebar.markdown("---")
st.sidebar.info(f"**Reference Date:** August 6, 2025\n*All calculations based on planetary positions from this date*")
# Auto-update when inputs change
if date != st.session_state.current_date or symbol != st.session_state.current_symbol:
    st.session_state.current_date = date
    st.session_state.current_symbol = symbol
    update_all_data(date, symbol)
    st.rerun()
# Initialize data if not exists
if not st.session_state.planetary_data or not st.session_state.last_update:
    update_all_data(date, symbol)
# Display market sentiment
sentiment_data = st.session_state.sentiment_data
if sentiment_data:
    sentiment = sentiment_data["sentiment"]
    score = sentiment_data["sentiment_score"]
    
    if "Bullish" in sentiment:
        st.success(f"🚀 **Market Sentiment: {sentiment}** | Score: {score:.1f}")
    elif "Bearish" in sentiment:
        st.error(f"📉 **Market Sentiment: {sentiment}** | Score: {score:.1f}")
    else:
        st.warning(f"⚖️ **Market Sentiment: {sentiment}** | Score: {score:.1f}")
# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🕐 Transit Timeline", "🪐 Planetary Positions", "⚡ Strategy", "🔮 Forecast", "📅 Aspects Timeline"])
with tab1:
    st.header("🕐 Critical Transit Timeline")
    
    if st.session_state.timeline_data:
        # Find current hora
        now = datetime.datetime.now()
        current_time_str = now.strftime("%I:%M %p").upper().replace(" ", "")
        
        # Display timeline in organized format
        for i, item in enumerate(st.session_state.timeline_data):
            # Create container for each timeline item
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    # Check if current hora
                    item_time_str = item["Time"].replace(" ", "").upper()
                    is_current = False
                    
                    try:
                        item_time = datetime.datetime.strptime(item["Time"], "%I:%M %p").time()
                        if i < len(st.session_state.timeline_data) - 1:
                            next_time = datetime.datetime.strptime(st.session_state.timeline_data[i+1]["Time"], "%I:%M %p").time()
                            is_current = item_time <= now.time() < next_time
                        else:
                            is_current = item_time <= now.time()
                    except:
                        pass
                    
                    if is_current:
                        st.error(f"🔥 **{item['Time']} - {item['Hora Lord']} Hora (CURRENT)**")
                    else:
                        st.write(f"**{item['Time']} - {item['Hora Lord']} Hora**")
                    
                    st.caption(f"**Influence:** {item['Influence']}")
                    st.caption(f"**Score:** {item['Score']:.1f}")
                
                with col2:
                    sentiment = item['Sentiment']
                    if sentiment == "Very Bullish":
                        st.success(f"🚀 {sentiment}")
                    elif sentiment == "Bullish":
                        st.success(f"📈 {sentiment}")
                    elif sentiment == "Very Bearish":
                        st.error(f"📉 {sentiment}")
                    elif sentiment == "Bearish":
                        st.error(f"🔻 {sentiment}")
                    else:
                        st.warning(f"⚖️ {sentiment}")
                
                with col3:
                    action = item['Action']
                    if action == "BUY":
                        st.success(f"✅ {action}")
                    elif action == "SELL":
                        st.error(f"❌ {action}")
                    else:
                        st.warning(f"⏸️ {action}")
                
                with col4:
                    if item['Score'] > 1:
                        st.success("LONG")
                    elif item['Score'] < -1:
                        st.error("SHORT")
                    else:
                        st.warning("WAIT")
                
                st.divider()
    else:
        st.warning("No timeline data available. Please update parameters.")
with tab2:
    st.header("🪐 Planetary Positions & Strengths")
    
    if st.session_state.planetary_data:
        # Display planetary positions
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌟 Planetary Positions")
            for planet in st.session_state.planetary_data[:5]:  # First 5 planets
                with st.container():
                    st.write(f"**{planet['Planet']}** - {planet['Degree']} in **{planet['Sign']}**")
                    st.caption(f"Nakshatra: {planet['Nakshatra']}")
                    
                    strength = planet['Strength']
                    if strength == "Exalted":
                        st.success(f"✨ {strength}")
                    elif strength == "Own Sign":
                        st.info(f"🏠 {strength}")
                    elif strength == "Debilitated":
                        st.error(f"⚠️ {strength}")
                    else:
                        st.warning(f"⚖️ {strength}")
                    st.divider()
        
        with col2:
            st.subheader("🌟 Planetary Positions")
            for planet in st.session_state.planetary_data[5:]:  # Remaining planets
                with st.container():
                    st.write(f"**{planet['Planet']}** - {planet['Degree']} in **{planet['Sign']}**")
                    st.caption(f"Nakshatra: {planet['Nakshatra']}")
                    
                    strength = planet['Strength']
                    if strength == "Exalted":
                        st.success(f"✨ {strength}")
                    elif strength == "Own Sign":
                        st.info(f"🏠 {strength}")
                    elif strength == "Debilitated":
                        st.error(f"⚠️ {strength}")
                    else:
                        st.warning(f"⚖️ {strength}")
                    st.divider()
    
    # Display aspects
    if st.session_state.aspects:
        st.subheader("⚡ Active Planetary Aspects")
        aspects_df = pd.DataFrame(st.session_state.aspects[:15])  # Show top 15
        st.dataframe(aspects_df, use_container_width=True)
    else:
        st.info("No significant aspects found for this date.")
with tab3:
    st.header("⚡ Dynamic Trading Strategy")
    
    if st.session_state.sentiment_data:
        sentiment_data = st.session_state.sentiment_data
        date_str = date.strftime("%d %B %Y (%A)")
        
        # Strategy overview
        st.subheader(f"🎯 Strategy for {symbol} on {date_str}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Sentiment Breakdown")
            for factor in sentiment_data["sentiment_factors"][:10]:
                st.write(f"• {factor}")
        
        with col2:
            st.subheader("⏰ Trading Windows Summary")
            
            if st.session_state.timeline_data:
                bullish_count = sum(1 for item in st.session_state.timeline_data if item['Score'] > 1)
                bearish_count = sum(1 for item in st.session_state.timeline_data if item['Score'] < -1)
                neutral_count = len(st.session_state.timeline_data) - bullish_count - bearish_count
                
                st.metric("🚀 Bullish Opportunities", bullish_count)
                st.metric("📉 Bearish Periods", bearish_count)
                st.metric("⚖️ Neutral Periods", neutral_count)
        
        # Best opportunities
        if st.session_state.timeline_data:
            best_entries = [item for item in st.session_state.timeline_data if item['Score'] >= 1.5]
            avoid_periods = [item for item in st.session_state.timeline_data if item['Score'] <= -1.5]
            
            if best_entries:
                st.subheader("🚀 Best Entry Opportunities")
                for entry in best_entries[:3]:
                    target = f"{1.2 + entry['Score'] * 0.3:.1f}%"
                    st.success(f"**⏰ {entry['Time']} - {entry['Hora Lord']} Hora**")
                    st.write(f"Action: Strong Buy | Target: {target} | Stop: 0.5%")
                    st.caption(f"Reason: {entry['Influence'][:100]}...")
                    st.divider()
            
            if avoid_periods:
                st.subheader("⚠️ Periods to Avoid/Short")
                for avoid in avoid_periods[:3]:
                    st.error(f"**⏰ {avoid['Time']} - {avoid['Hora Lord']} Hora**")
                    st.write("Action: Avoid/Short")
                    st.caption(f"Reason: {avoid['Influence'][:100]}...")
                    st.divider()
        
        # Symbol-specific analysis
        st.subheader(f"📈 {symbol}-Specific Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if symbol.upper() == "NIFTY":
                jupiter_degree = st.session_state.planetary_degrees.get('Jupiter', 0)
                saturn_degree = st.session_state.planetary_degrees.get('Saturn', 0)
                st.write(f"• **Support:** Jupiter at {jupiter_degree:.0f}°")
                st.write(f"• **Resistance:** Saturn at {saturn_degree:.0f}°")
                st.write(f"• **Breakout Potential:** {'High' if sentiment_data['sentiment_score'] > 2 else 'Moderate' if sentiment_data['sentiment_score'] > 0 else 'Low'}")
                
            elif symbol.upper() == "BANKNIFTY":
                mars_degree = st.session_state.planetary_degrees.get("Mars", 0)
                mars_sign = get_sign_from_degree(mars_degree)
                mars_strength = get_planet_strength("Mars", mars_sign)
                st.write(f"• **Mars Influence:** {mars_degree:.0f}° in {mars_sign} - {mars_strength}")
                st.write(f"• **Banking Sentiment:** {'Positive' if sentiment_data['sentiment_score'] > 1 else 'Negative' if sentiment_data['sentiment_score'] < -1 else 'Mixed'}")
        
        with col2:
            st.subheader("🛡️ Risk Management")
            st.write(f"• **Position Size:** {'Conservative (10-15%)' if abs(sentiment_data['sentiment_score']) > 3 else 'Moderate (15-20%)' if abs(sentiment_data['sentiment_score']) > 1 else 'Normal (20-25%)'}")
            st.write("• **Stop-Loss:** 0.5% intraday, 1% swing")
            st.write("• **Max Daily Loss:** 2% of capital")
with tab4:
    st.header("🔮 Multi-day Forecast")
    
    if st.session_state.forecast_data:
        # Display forecast in organized format
        col1, col2 = st.columns(2)
        
        for i, forecast in enumerate(st.session_state.forecast_data):
            current_col = col1 if i % 2 == 0 else col2
            
            with current_col:
                with st.container():
                    if forecast["Is Today"]:
                        st.error(f"🎯 **{forecast['Date']} ({forecast['Day']}) - TODAY**")
                    else:
                        st.write(f"**{forecast['Date']} ({forecast['Day']})**")
                    
                    sentiment = forecast['Sentiment']
                    if "Bullish" in sentiment:
                        st.success(f"📈 {sentiment}")
                    elif "Bearish" in sentiment:
                        st.error(f"📉 {sentiment}")
                    else:
                        st.warning(f"⚖️ {sentiment}")
                    
                    st.caption(f"Score: {forecast['Score']:.1f} | Aspects: {forecast['Aspects']}")
                    
                    recommendation = "Long bias" if forecast['Score'] > 1 else "Short bias" if forecast['Score'] < -1 else "Neutral"
                    st.caption(f"**Recommendation:** {recommendation}")
                    
                    st.divider()
with tab5:
    st.header("📅 Planetary Aspects Timeline")
    
    # Check if date is August 6, 2025
    if date != datetime.date(2025, 8, 6):
        st.warning("⚠️ Detailed aspects timeline is only available for August 6, 2025. Please select this date to view the complete timeline.")
    else:
        # Symbol selection
        symbol_options = ["Nifty", "BankNifty", "Gold", "Silver", "Crude", "BTC", "DowJones"]
        selected_symbol = st.selectbox("🔍 Select Symbol for Timeline View", symbol_options)
        
        # Define market hours
        indian_market_open = datetime.time(9, 15)
        indian_market_close = datetime.time(15, 30)
        global_market_open = datetime.time(5, 0)
        global_market_close = datetime.time(23, 55)
        
        # Prepare aspects data for display
        aspects_display = []
        for aspect in aug6_aspects:
            # Parse time
            time_str = aspect["time"]
            hour_min = time_str.replace(" am", "").replace(" pm", "")
            hour, minute = map(int, hour_min.split(":"))
            if "pm" in time_str and hour != 12:
                hour += 12
            aspect_time = datetime.time(hour, minute)
            
            # Determine market status
            market_status = ""
            if indian_market_open <= aspect_time <= indian_market_close:
                market_status = "🇮🇳 Indian Market Open"
            elif global_market_open <= aspect_time <= global_market_close:
                market_status = "🌍 Global Market Open"
            else:
                market_status = "⚫ Closed"
            
            # Get impact for selected symbol
            if selected_symbol in ["Nifty", "BankNifty"]:
                impact = aspect["indian_market"]
            elif selected_symbol in ["Gold", "Silver", "Crude"]:
                impact = aspect["commodities"]
            elif selected_symbol == "BTC":
                impact = aspect["forex"]
            elif selected_symbol == "DowJones":
                impact = aspect["global_market"]
            else:
                impact = "Neutral"
            
            aspects_display.append({
                "Time": aspect["time"],
                "Aspect": aspect["aspect"],
                "Meaning": aspect["meaning"],
                "Impact": impact,
                "Market Status": market_status
            })
        
        # Display aspects table
        st.subheader(f"Planetary Aspects for {selected_symbol} - August 6, 2025")
        
        # Create DataFrame with styling
        df = pd.DataFrame(aspects_display)
        
        # Style the DataFrame
        def highlight_impact(val):
            color = ''
            if "Bullish" in val or "recovery" in val.lower() or "rally" in val.lower():
                color = 'background-color: #d4edda; color: #155724'
            elif "Bearish" in val or "dip" in val.lower() or "pressure" in val.lower() or "risks" in val.lower():
                color = 'background-color: #f8d7da; color: #721c24'
            else:
                color = 'background-color: #fff3cd; color: #856404'
            return color
        
        styled_df = df.style.applymap(highlight_impact, subset=['Impact'])
        
        # Display the styled table
        st.dataframe(styled_df, use_container_width=True)
        
        # Create a visual timeline
        st.subheader("📊 Visual Timeline")
        
        # Prepare data for timeline visualization
        timeline_viz = []
        for aspect in aspects_display:
            impact = aspect["Impact"]
            
            # Determine sentiment
            if "Bullish" in impact or "recovery" in impact.lower() or "rally" in impact.lower():
                sentiment = "Bullish"
            elif "Bearish" in impact or "dip" in impact.lower() or "pressure" in impact.lower() or "risks" in impact.lower():
                sentiment = "Bearish"
            else:
                sentiment = "Neutral"
            
            timeline_viz.append({
                "Time": aspect_time.strftime("%H:%M"),
                "Aspect": aspect["Aspect"].split(" (")[0],
                "Sentiment": sentiment,
                "Impact": impact
            })
        
        # Sort by time
        timeline_viz.sort(key=lambda x: x["Time"])
        
        # Create timeline chart
        fig = go.Figure()
        
        # Add Indian market hours background
        fig.add_vrect(
            x0="9:15", x1="15:30",
            fillcolor="LightGreen", opacity=0.2,
            layer="below", line_width=0,
            annotation_text="Indian Market Hours"
        )
        
        # Add global market hours background
        fig.add_vrect(
            x0="5:00", x1="23:55",
            fillcolor="LightBlue", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="Global Market Hours"
        )
        
        # Add aspects as scatter points
        colors = {"Bullish": "green", "Bearish": "red", "Neutral": "orange"}
        
        for item in timeline_viz:
            fig.add_trace(go.Scatter(
                x=[item["Time"]],
                y=[1],
                mode="markers+text",
                marker=dict(size=15, color=colors[item["Sentiment"]]),
                text=item["Aspect"],
                textposition="top center",
                name=item["Aspect"],
                hovertext=f"<b>{item['Aspect']}</b><br>Sentiment: {item['Sentiment']}<br>Impact: {item['Impact']}",
                hoverinfo="text"
            ))
        
        fig.update_layout(
            title=f"Planetary Aspects Timeline for {selected_symbol}",
            xaxis_title="Time",
            yaxis=dict(visible=False),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("📈 Summary Statistics")
        
        sentiment_counts = df['Impact'].apply(lambda x: 'Bullish' if 'Bullish' in x or 'recovery' in x.lower() or 'rally' in x.lower() else ('Bearish' if 'Bearish' in x or 'dip' in x.lower() or 'pressure' in x.lower() or 'risks' in x.lower() else 'Neutral')).value_counts()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🟢 Bullish Aspects", sentiment_counts.get('Bullish', 0))
        with col2:
            st.metric("🔴 Bearish Aspects", sentiment_counts.get('Bearish', 0))
        with col3:
            st.metric("⚪ Neutral Aspects", sentiment_counts.get('Neutral', 0))
        
        # Key insights
        st.subheader("💡 Key Insights for " + selected_symbol)
        
        # Get all aspects for the selected symbol
        symbol_aspects = [aspect for aspect in aspects_display if aspect["Impact"] != "Neutral"]
        
        if symbol_aspects:
            for aspect in symbol_aspects:
                impact = aspect["Impact"]
                if "Bullish" in impact or "recovery" in impact.lower() or "rally" in impact.lower():
                    st.success(f"🟢 **{aspect['Time']} - {aspect['Aspect'].split(' (')[0]}**")
                    st.write(f"   {impact}")
                elif "Bearish" in impact or "dip" in impact.lower() or "pressure" in impact.lower() or "risks" in impact.lower():
                    st.error(f"🔴 **{aspect['Time']} - {aspect['Aspect'].split(' (')[0]}**")
                    st.write(f"   {impact}")
        else:
            st.info("No significant planetary aspects directly affecting this symbol on this date.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🌟 **Dynamic Planetary Trading Dashboard**")
with col2:
    st.caption("Real-time Astro-Financial Intelligence")
with col3:
    if st.session_state.last_update:
        st.caption(f"Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
# Display current parameters
st.sidebar.markdown("---")
st.sidebar.subheader("📋 Current Parameters")
st.sidebar.write(f"**Date:** {date.strftime('%d %B %Y')}")
st.sidebar.write(f"**Symbol:** {symbol}")
st.sidebar.write(f"**Location:** {city}")
if st.session_state.sentiment_data:
    sentiment = st.session_state.sentiment_data["sentiment"]
    score = st.session_state.sentiment_data["sentiment_score"]
    st.sidebar.write(f"**Current Sentiment:** {sentiment}")
    st.sidebar.write(f"**Sentiment Score:** {score:.1f}")
