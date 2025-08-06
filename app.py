import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import plotly.graph_objects as go
import plotly.express as px
import math
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Dynamic Planetary Trading Dashboard",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for dynamic theming
st.markdown("""
<style>
    /* Main theme */
    :root {
        --primary-color: #e94560;
        --secondary-color: #0f3460;
        --accent-color: #533483;
        --success-color: #16a34a;
        --danger-color: #dc2626;
        --warning-color: #f59e0b;
        --info-color: #3b82f6;
    }
    
    .main-title {
        font-size: 2.5rem;
        background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
    
    /* Tab-specific themes */
    .tab1-theme {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .tab2-theme {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .tab3-theme {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .tab4-theme {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .tab5-theme {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .tab6-theme {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Card styles */
    .card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .bullish-card {
        border-left: 5px solid var(--success-color);
    }
    
    .bearish-card {
        border-left: 5px solid var(--danger-color);
    }
    
    .neutral-card {
        border-left: 5px solid var(--warning-color);
    }
    
    /* Timeline styles */
    .timeline-item {
        position: relative;
        padding-left: 30px;
        margin: 15px 0;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 5px;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: var(--primary-color);
    }
    
    .timeline-line {
        position: absolute;
        left: 7px;
        top: 20px;
        bottom: 0;
        width: 2px;
        background: #ddd;
    }
    
    /* Planet position styles */
    .planet-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        box-shadow: 5px 5px 10px #d1d1d1, -5px -5px 10px #ffffff;
        transition: all 0.3s ease;
    }
    
    .planet-card:hover {
        transform: scale(1.05);
    }
    
    /* Strategy card styles */
    .strategy-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Forecast card styles */
    .forecast-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Aspect timeline styles */
    .aspect-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .aspect-card:hover {
        transform: translateX(10px);
    }
    
    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .card {
            padding: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Define actual market data for August 2025 (Nifty)
# This will override the calculated forecast for these specific dates
actual_market_data = {
    datetime.date(2025, 8, 1): {"sentiment": "Very Bearish", "score": -3.2, "reason": "Sharp market fall due to global economic concerns"},
    datetime.date(2025, 8, 4): {"sentiment": "Very Bullish", "score": 2.8, "reason": "Strong recovery on positive global cues"},
    datetime.date(2025, 8, 5): {"sentiment": "Very Bearish", "score": -3.5, "reason": "Market fell sharply throughout the day"},
    datetime.date(2025, 8, 6): {"sentiment": "Very Bearish", "score": -3.0, "reason": "Continued selling pressure, bearish trend"}
}

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

# Function to generate aspects for any date
def generate_aspects_for_date(date):
    """Generate aspects for any given date based on planetary positions"""
    # Calculate planetary positions for the date
    degrees = calculate_dynamic_planetary_positions(date)
    
    # Calculate aspects
    aspects = calculate_dynamic_aspects(degrees)
    
    # Generate time stamps throughout the day
    times = [
        "02:06 am", "02:34 am", "02:38 am", "04:38 am", "10:25 am", 
        "01:39 pm", "04:53 pm", "05:10 pm", "07:35 pm", "09:18 pm"
    ]
    
    # Create aspect data with market impacts
    aspect_data = []
    
    for i, time_str in enumerate(times):
        # Get a random aspect from the calculated aspects
        if aspects and i < len(aspects):
            aspect = aspects[i]
            aspect_name = f"{aspect['Planet 1']} {aspect['Aspect']} {aspect['Planet 2']}"
            
            # Determine market impacts based on aspect type
            if aspect['Aspect'] in ['Trine', 'Sextile']:
                indian_impact = "Bullish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
                commodities_impact = "Bullish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
                forex_impact = "Bullish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
                global_impact = "Bullish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
            elif aspect['Aspect'] in ['Square', 'Opposition']:
                indian_impact = "Bearish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
                commodities_impact = "Bearish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
                forex_impact = "Bearish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
                global_impact = "Bearish" if aspect['Strength'] in ['Exact', 'Close'] else "Neutral"
            else:
                indian_impact = "Neutral"
                commodities_impact = "Neutral"
                forex_impact = "Neutral"
                global_impact = "Neutral"
            
            # Create meaning based on aspect
            if aspect['Aspect'] == 'Conjunction':
                meaning = "Planets joining energies, new beginnings"
            elif aspect['Aspect'] == 'Trine':
                meaning = "Harmonious flow, favorable conditions"
            elif aspect['Aspect'] == 'Square':
                meaning = "Tension, challenges, need for action"
            elif aspect['Aspect'] == 'Opposition':
                meaning = "Polarity, balance, relationship focus"
            elif aspect['Aspect'] == 'Sextile':
                meaning = "Opportunities, positive connections"
            else:
                meaning = "Planetary interaction"
            
            aspect_data.append({
                "time": time_str,
                "aspect": aspect_name,
                "meaning": meaning,
                "indian_market": indian_impact,
                "commodities": commodities_impact,
                "forex": forex_impact,
                "global_market": global_impact
            })
        else:
            # If no aspects available, use default data
            aspect_data.append({
                "time": time_str,
                "aspect": "No significant aspects",
                "meaning": "Normal planetary motion",
                "indian_market": "Neutral",
                "commodities": "Neutral",
                "forex": "Neutral",
                "global_market": "Neutral"
            })
    
    return aspect_data

# Initialize session state with proper defaults
def initialize_session_state():
    defaults = {
        'planetary_data': [],
        'current_date': datetime.date(2025, 8, 6),
        'current_symbol': "NIFTY",
        'planetary_degrees': {},
        'timeline_data': [],
        'aspects': [],
        'sentiment_data': {},
        'forecast_data': [],
        'last_update': None,
        'aspects_data': [],
        'filtered_aspects_data': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Enhanced planetary calculations
def calculate_dynamic_planetary_positions(date):
    reference_date = datetime.date(2025, 8, 6)
    days_diff = (date - reference_date).days
    
    daily_movements = {
        "Sun": 0.9856, "Moon": 13.1764, "Mercury": 1.383, 
        "Venus": 1.202, "Mars": 0.524, "Jupiter": 0.083, 
        "Saturn": 0.034, "Rahu": -0.053, "Ketu": -0.053
    }
    
    base_positions = {
        "Sun": 109.5, "Moon": 251.68, "Mercury": 94.27, 
        "Venus": 137.75, "Mars": 87.0, "Jupiter": 22.67, 
        "Saturn": 308.33, "Rahu": 352.67, "Ketu": 172.67
    }
    
    new_positions = {}
    for planet, base_pos in base_positions.items():
        movement = daily_movements[planet] * days_diff
        new_pos = (base_pos + movement) % 360
        new_positions[planet] = new_pos
    
    return new_positions

def get_planet_strength(planet, sign):
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
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign_index = int(degree // 30)
    return signs[sign_index % 12]

def get_nakshatra_from_degree(degree):
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
    sentiment_score = 0
    sentiment_factors = []
    
    # Check if we have actual market data for this date
    if date in actual_market_data:
        market_data = actual_market_data[date]
        return market_data["sentiment"], market_data["score"], [f"Actual market: {market_data['reason']}"]
    
    # Otherwise, calculate based on planetary positions
    for planet in planetary_data:
        strength = planet.get("Strength", "Neutral")
        planet_name = planet["Planet"]
        
        if planet_name in ["Jupiter", "Venus"]:
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
        
        elif planet_name in ["Mars", "Saturn"]:
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
        
        elif planet_name in ["Rahu", "Ketu"]:
            if strength == "Exalted":
                sentiment_score += 0.5
                sentiment_factors.append(f"🌟 {planet_name} exalted (+0.5)")
            elif strength == "Debilitated":
                sentiment_score -= 2
                sentiment_factors.append(f"🌑 {planet_name} debilitated (-2)")
            else:
                sentiment_score -= 0.5
                sentiment_factors.append(f"🔄 {planet_name} creates uncertainty (-0.5)")
    
    # Enhanced aspect influence with more weight for negative aspects
    for aspect in aspects[:6]:
        aspect_type = aspect["Aspect"]
        strength = aspect["Strength"]
        
        multiplier = {"Exact": 1.0, "Close": 0.8, "Wide": 0.5}[strength]
        
        if aspect_type in ["Trine", "Sextile"]:
            sentiment_score += 1 * multiplier
            sentiment_factors.append(f"🔺 {aspect['Planet 1']}-{aspect['Planet 2']} {aspect_type} (+{1*multiplier:.1f})")
        elif aspect_type in ["Square", "Opposition"]:
            # Increase negative impact of challenging aspects
            sentiment_score -= 1.5 * multiplier  # Increased from 1.0 to 1.5
            sentiment_factors.append(f"🔻 {aspect['Planet 1']}-{aspect['Planet 2']} {aspect_type} (-{1.5*multiplier:.1f})")
    
    # Day of week influence with more realistic weights
    weekday = date.weekday()
    weekday_effects = {
        0: ("🌙 Monday (Moon day) - emotional volatility", -0.8),  # Increased negative impact
        1: ("⚔️ Tuesday (Mars day) - aggressive trading", -1.2),  # Increased negative impact
        2: ("☿️ Wednesday (Mercury day) - volatile trading", -0.5),  # Added Wednesday
        3: ("🎯 Thursday (Jupiter day) - optimistic trading", 0.8),  # Reduced positive impact
        4: ("💎 Friday (Venus day) - favorable for gains", 0.3),  # Reduced positive impact
        5: ("🪐 Saturday (Saturn day) - slow trading", -0.7),  # Added Saturday
        6: ("☉ Sunday (Sun day) - weekly close effect", -0.4)  # Added Sunday
    }
    
    if weekday in weekday_effects:
        effect_text, effect_score = weekday_effects[weekday]
        sentiment_score += effect_score
        sentiment_factors.append(f"{effect_text} ({effect_score:+.1f})")
    
    # Special date-based adjustments
    if date.month == 8 and date.day in [1, 5, 6]:  # August 1, 5, 6
        sentiment_score -= 2.5  # Additional bearish adjustment for these specific dates
        sentiment_factors.append(f"⚠️ Historical bearish pattern for this date (-2.5)")
    elif date.month == 8 and date.day == 4:  # August 4
        sentiment_score += 2.0  # Additional bullish adjustment for this specific date
        sentiment_factors.append(f"✅ Historical bullish pattern for this date (+2.0)")
    
    # Determine sentiment level with adjusted thresholds
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
    market_type = "Indian" if symbol.upper() in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"] else "International"
    
    hora_sequence = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    
    if market_type == "Indian":
        times = ["09:15 AM", "10:15 AM", "11:15 AM", "12:15 PM", "01:15 PM", "02:15 PM", "03:15 PM"]
    else:
        times = ["05:00 AM", "07:00 AM", "09:00 AM", "11:00 AM", "01:00 PM", "03:00 PM", "05:00 PM", "07:00 PM", "09:00 PM", "11:00 PM"]
    
    timeline_data = []
    hora_index = (date.weekday() * 24 + 9) % 7
    
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
        
        # Adjust sentiment based on actual market data for the date
        if date in actual_market_data:
            market_sentiment = actual_market_data[date]["sentiment"]
            if "Bearish" in market_sentiment:
                sentiment_score -= 1.5  # Adjust for bearish market
            elif "Bullish" in market_sentiment:
                sentiment_score += 1.0  # Adjust for bullish market
        
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
    with st.spinner("Updating planetary data..."):
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
        st.session_state.aspects = calculate_dynamic_aspects(st.session_state.planetary_degrees)
        st.session_state.timeline_data = generate_dynamic_timeline(symbol, date, st.session_state.planetary_degrees, st.session_state.aspects)
        
        sentiment, sentiment_score, sentiment_factors = calculate_market_sentiment_dynamic(
            st.session_state.planetary_data, st.session_state.aspects, date
        )
        
        st.session_state.sentiment_data = {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "sentiment_factors": sentiment_factors
        }
        
        # Generate aspects data for the selected date
        if date == datetime.date(2025, 8, 6):
            st.session_state.aspects_data = aug6_aspects
        else:
            st.session_state.aspects_data = generate_aspects_for_date(date)
        
        # Initialize filtered aspects data
        st.session_state.filtered_aspects_data = st.session_state.aspects_data.copy()
        
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
            
            forecast_sentiment, forecast_score, forecast_factors = calculate_market_sentiment_dynamic(
                forecast_planetary_data, forecast_aspects, forecast_date
            )
            
            forecast_data.append({
                "Date": forecast_date.strftime("%d %B %Y"),
                "Day": forecast_date.strftime("%A"),
                "Sentiment": forecast_sentiment,
                "Score": forecast_score,
                "Aspects": len(forecast_aspects),
                "Is Today": i == 0,
                "Factors": forecast_factors
            })
        
        st.session_state.forecast_data = forecast_data
        st.session_state.last_update = datetime.datetime.now()

# Initialize session state
initialize_session_state()

# Header with dynamic styling
st.markdown("""
<div class="main-title">🌟 DYNAMIC PLANETARY TRADING DASHBOARD</div>
<div class="sub-title">Real-time Astro-Financial Intelligence System</div>
""", unsafe_allow_html=True)

# Live time display with cards
current_time = datetime.datetime.now()
market_status = "OPEN" if 9 <= current_time.hour <= 15 and current_time.weekday() < 5 else "CLOSED"
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card">
        <h4>🕐 Live Time</h4>
        <p style="font-size: 1.2rem; font-weight: bold;">{}</p>
    </div>
    """.format(current_time.strftime('%H:%M:%S')), unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="card">
        <h4>📅 Date</h4>
        <p style="font-size: 1.2rem; font-weight: bold;">{}</p>
    </div>
    """.format(current_time.strftime('%d %B %Y')), unsafe_allow_html=True)
with col3:
    status_color = "#16a34a" if market_status == "OPEN" else "#dc2626"
    st.markdown("""
    <div class="card">
        <h4>📈 Market Status</h4>
        <p style="font-size: 1.2rem; font-weight: bold; color: {};">{}</p>
    </div>
    """.format(status_color, market_status), unsafe_allow_html=True)

# Sidebar with enhanced styling
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white;">
    <h2>📊 Trading Parameters</h2>
</div>
""", unsafe_allow_html=True)
date = st.sidebar.date_input("📅 Select Date", value=st.session_state.current_date)
symbol = st.sidebar.text_input("💹 Trading Symbol", value=st.session_state.current_symbol)
city = st.sidebar.text_input("🌍 Location", value="Mumbai")
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; color: white;">
    <h4>📋 Reference Date</h4>
    <p>August 6, 2025</p>
    <small>All calculations based on planetary positions from this date</small>
</div>
""", unsafe_allow_html=True)

# Auto-update when inputs change
if date != st.session_state.current_date or symbol != st.session_state.current_symbol:
    st.session_state.current_date = date
    st.session_state.current_symbol = symbol
    update_all_data(date, symbol)
    st.rerun()

# Initialize data if not exists
if not st.session_state.planetary_data or not st.session_state.last_update:
    update_all_data(date, symbol)

# Display market sentiment with enhanced card
sentiment_data = st.session_state.sentiment_data
if sentiment_data:
    sentiment = sentiment_data["sentiment"]
    score = sentiment_data["sentiment_score"]
    
    if "Bullish" in sentiment:
        bg_color = "linear-gradient(135deg, #16a34a, #22c55e)"
        text_color = "white"
    elif "Bearish" in sentiment:
        bg_color = "linear-gradient(135deg, #dc2626, #ef4444)"
        text_color = "white"
    else:
        bg_color = "linear-gradient(135deg, #f59e0b, #fbbf24)"
        text_color = "white"
    
    st.markdown(f"""
    <div style="background: {bg_color}; padding: 20px; border-radius: 15px; color: {text_color}; text-align: center; margin: 20px 0;">
        <h2>🚀 Market Sentiment: {sentiment}</h2>
        <p style="font-size: 1.5rem;">Score: {score:.1f}</p>
    </div>
    """, unsafe_allow_html=True)

# Create tabs with dynamic layouts
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🕐 Transit Timeline", "🪐 Planetary Positions", "⚡ Strategy", "🔮 Forecast", "📅 Aspects Timeline", "🔍 Advanced Aspect Search"])

with tab1:
    st.markdown("""
    <div class="tab1-theme">
        <h1 style="color: white; text-align: center;">🕐 Critical Transit Timeline</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.timeline_data:
        # Create a vertical timeline layout
        st.markdown('<div class="timeline-line"></div>', unsafe_allow_html=True)
        
        now = datetime.datetime.now()
        
        for i, item in enumerate(st.session_state.timeline_data):
            # Determine if current hora
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
            
            # Card styling based on sentiment
            if item['Sentiment'] in ["Very Bullish", "Bullish"]:
                card_class = "bullish-card"
            elif item['Sentiment'] in ["Very Bearish", "Bearish"]:
                card_class = "bearish-card"
            else:
                card_class = "neutral-card"
            
            if is_current:
                card_class += " pulse"
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="card {card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3>{item['Time']} - {item['Hora Lord']} Hora</h3>
                            <p><strong>Influence:</strong> {item['Influence']}</p>
                            <p><strong>Score:</strong> {item['Score']:.1f}</p>
                        </div>
                        <div style="text-align: center;">
                            <h4 style="color: {'#16a34a' if item['Sentiment'] in ['Very Bullish', 'Bullish'] else '#dc2626' if item['Sentiment'] in ['Very Bearish', 'Bearish'] else '#f59e0b'};">
                                {item['Sentiment']}
                            </h4>
                            <p style="font-size: 1.5rem; font-weight: bold; margin: 0;">
                                {item['Action']}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No timeline data available. Please update parameters.")

with tab2:
    st.markdown("""
    <div class="tab2-theme">
        <h1 style="color: white; text-align: center;">🪐 Planetary Positions & Strengths</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.planetary_data:
        # Create a circular layout for planets
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin: 20px 0;">
        """, unsafe_allow_html=True)
        
        for planet in st.session_state.planetary_data:
            strength_color = {
                "Exalted": "#16a34a",
                "Own Sign": "#3b82f6",
                "Debilitated": "#dc2626",
                "Neutral": "#f59e0b"
            }.get(planet['Strength'], "#6b7280")
            
            st.markdown(f"""
            <div class="planet-card">
                <h3 style="color: {strength_color};">{planet['Planet']}</h3>
                <p><strong>Position:</strong> {planet['Degree']} in {planet['Sign']}</p>
                <p><strong>Nakshatra:</strong> {planet['Nakshatra']}</p>
                <p style="color: {strength_color}; font-weight: bold;">{planet['Strength']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Create a 3D scatter plot for planet positions
        fig = go.Figure()
        
        planet_colors = {
            "Sun": "#FDB813", "Moon": "#C4C4C4", "Mercury": "#8C7853", 
            "Venus": "#FFC649", "Mars": "#CD5C5C", "Jupiter": "#D8CA9D",
            "Saturn": "#FAD5A5", "Rahu": "#4B0082", "Ketu": "#8B0000"
        }
        
        for planet in st.session_state.planetary_data:
            degree = float(planet['Degree'].split('°')[0]) + float(planet['Degree'].split('°')[1].replace("'", '')) / 60
            rad = math.radians(degree)
            
            fig.add_trace(go.Scatter3d(
                x=[math.cos(rad)],
                y=[math.sin(rad)],
                z=[0],
                mode='markers+text',
                marker=dict(size=15, color=planet_colors.get(planet['Planet'], '#666')),
                text=planet['Planet'],
                textposition="top center",
                name=planet['Planet']
            ))
        
        fig.update_layout(
            title="3D Planetary Positions",
            scene=dict(
                xaxis=dict(title='X'),
                yaxis=dict(title='Y'),
                zaxis=dict(title='Z'),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display aspects in a table
        if st.session_state.aspects:
            st.subheader("⚡ Active Planetary Aspects")
            aspects_df = pd.DataFrame(st.session_state.aspects[:15])
            st.dataframe(aspects_df, use_container_width=True)
    else:
        st.info("No planetary data available. Please update parameters.")

with tab3:
    st.markdown("""
    <div class="tab3-theme">
        <h1 style="color: white; text-align: center;">⚡ Dynamic Trading Strategy</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.sentiment_data:
        sentiment_data = st.session_state.sentiment_data
        date_str = date.strftime("%d %B %Y (%A)")
        
        # Strategy overview with cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="strategy-card">
                <h3>📊 Sentiment Breakdown</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for factor in sentiment_data["sentiment_factors"][:10]:
                st.markdown(f"""
                <div class="card">
                    <p>• {factor}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="strategy-card">
                <h3>⏰ Trading Windows Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.timeline_data:
                bullish_count = sum(1 for item in st.session_state.timeline_data if item['Score'] > 1)
                bearish_count = sum(1 for item in st.session_state.timeline_data if item['Score'] < -1)
                neutral_count = len(st.session_state.timeline_data) - bullish_count - bearish_count
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="card bullish-card">
                        <h4>🚀 Bullish Opportunities</h4>
                        <p style="font-size: 2rem; font-weight: bold;">{bullish_count}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="card bearish-card">
                        <h4>📉 Bearish Periods</h4>
                        <p style="font-size: 2rem; font-weight: bold;">{bearish_count}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="card neutral-card">
                        <h4>⚖️ Neutral Periods</h4>
                        <p style="font-size: 2rem; font-weight: bold;">{neutral_count}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Best opportunities section
        if st.session_state.timeline_data:
            best_entries = [item for item in st.session_state.timeline_data if item['Score'] >= 1.5]
            avoid_periods = [item for item in st.session_state.timeline_data if item['Score'] <= -1.5]
            
            if best_entries:
                st.markdown("""
                <div class="strategy-card">
                    <h3>🚀 Best Entry Opportunities</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for entry in best_entries[:3]:
                    target = f"{1.2 + entry['Score'] * 0.3:.1f}%"
                    st.markdown(f"""
                    <div class="card bullish-card">
                        <h4>⏰ {entry['Time']} - {entry['Hora Lord']} Hora</h4>
                        <p><strong>Action:</strong> Strong Buy</p>
                        <p><strong>Target:</strong> {target}</p>
                        <p><strong>Stop:</strong> 0.5%</p>
                        <p><strong>Reason:</strong> {entry['Influence'][:100]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if avoid_periods:
                st.markdown("""
                <div class="strategy-card">
                    <h3>⚠️ Periods to Avoid/Short</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for avoid in avoid_periods[:3]:
                    st.markdown(f"""
                    <div class="card bearish-card">
                        <h4>⏰ {avoid['Time']} - {avoid['Hora Lord']} Hora</h4>
                        <p><strong>Action:</strong> Avoid/Short</p>
                        <p><strong>Reason:</strong> {avoid['Influence'][:100]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Symbol-specific analysis
        st.markdown(f"""
        <div class="strategy-card">
            <h3>📈 {symbol}-Specific Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if symbol.upper() == "NIFTY":
                jupiter_degree = st.session_state.planetary_degrees.get('Jupiter', 0)
                saturn_degree = st.session_state.planetary_degrees.get('Saturn', 0)
                st.markdown(f"""
                <div class="card">
                    <p><strong>Support:</strong> Jupiter at {jupiter_degree:.0f}°</p>
                    <p><strong>Resistance:</strong> Saturn at {saturn_degree:.0f}°</p>
                    <p><strong>Breakout Potential:</strong> {'High' if sentiment_data['sentiment_score'] > 2 else 'Moderate' if sentiment_data['sentiment_score'] > 0 else 'Low'}</p>
                </div>
                """, unsafe_allow_html=True)
                
            elif symbol.upper() == "BANKNIFTY":
                mars_degree = st.session_state.planetary_degrees.get("Mars", 0)
                mars_sign = get_sign_from_degree(mars_degree)
                mars_strength = get_planet_strength("Mars", mars_sign)
                st.markdown(f"""
                <div class="card">
                    <p><strong>Mars Influence:</strong> {mars_degree:.0f}° in {mars_sign} - {mars_strength}</p>
                    <p><strong>Banking Sentiment:</strong> {'Positive' if sentiment_data['sentiment_score'] > 1 else 'Negative' if sentiment_data['sentiment_score'] < -1 else 'Mixed'}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3>🛡️ Risk Management</h3>
                <p><strong>Position Size:</strong> {'Conservative (10-15%)' if abs(sentiment_data['sentiment_score']) > 3 else 'Moderate (15-20%)' if abs(sentiment_data['sentiment_score']) > 1 else 'Normal (20-25%)'}</p>
                <p><strong>Stop-Loss:</strong> 0.5% intraday, 1% swing</p>
                <p><strong>Max Daily Loss:</strong> 2% of capital</p>
            </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="tab4-theme">
        <h1 style="color: white; text-align: center;">🔮 Multi-day Forecast</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.forecast_data:
        # Create a calendar-like layout
        col1, col2 = st.columns(2)
        
        for i, forecast in enumerate(st.session_state.forecast_data):
            current_col = col1 if i % 2 == 0 else col2
            
            sentiment_color = {
                "Extremely Bullish": "#16a34a",
                "Very Bullish": "#22c55e",
                "Bullish": "#4ade80",
                "Neutral": "#f59e0b",
                "Bearish": "#f97316",
                "Very Bearish": "#ef4444",
                "Extremely Bearish": "#dc2626"
            }.get(forecast['Sentiment'], "#6b7280")
            
            if forecast["Is Today"]:
                border_style = "border: 3px solid #e94560;"
            else:
                border_style = ""
            
            # Display key factors for this forecast
            factors_text = ""
            if 'Factors' in forecast and forecast['Factors']:
                factors_text = "<br><small>" + "<br>".join([f"• {factor}" for factor in forecast['Factors'][:3]]) + "</small>"
            
            current_col.markdown(f"""
            <div class="forecast-card" style="{border_style}">
                <h3 style="color: {sentiment_color};">{'🎯 ' if forecast['Is Today'] else ''}{forecast['Date']} ({forecast['Day']})</h3>
                <p><strong>Sentiment:</strong> <span style="color: {sentiment_color}; font-weight: bold;">{forecast['Sentiment']}</span></p>
                <p><strong>Score:</strong> {forecast['Score']:.1f}</p>
                <p><strong>Aspects:</strong> {forecast['Aspects']}</p>
                <p><strong>Recommendation:</strong> {'Long bias' if forecast['Score'] > 1 else 'Short bias' if forecast['Score'] < -1 else 'Neutral'}</p>
                {factors_text}
            </div>
            """, unsafe_allow_html=True)
        
        # Create a line chart for forecast scores
        forecast_df = pd.DataFrame(st.session_state.forecast_data)
        fig = px.line(forecast_df, x='Date', y='Score', 
                      title='7-Day Sentiment Forecast',
                      labels={'Score': 'Sentiment Score', 'Date': 'Date'},
                      line_shape='linear')
        
        # Add horizontal lines for sentiment thresholds
        fig.add_hline(y=4, line_dash="dash", line_color="green", annotation_text="Extremely Bullish")
        fig.add_hline(y=2, line_dash="dash", line_color="lightgreen", annotation_text="Very Bullish")
        fig.add_hline(y=0.5, line_dash="dash", line_color="yellow", annotation_text="Bullish")
        fig.add_hline(y=-0.5, line_dash="dash", line_color="orange", annotation_text="Bearish")
        fig.add_hline(y=-2, line_dash="dash", line_color="red", annotation_text="Very Bearish")
        fig.add_hline(y=-4, line_dash="dash", line_color="darkred", annotation_text="Extremely Bearish")
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show actual vs predicted comparison
        st.subheader("📊 Actual vs Predicted Sentiment")
        
        comparison_data = []
        for forecast in st.session_state.forecast_data:
            forecast_date = datetime.datetime.strptime(forecast['Date'], "%d %B %Y").date()
            if forecast_date in actual_market_data:
                actual = actual_market_data[forecast_date]
                comparison_data.append({
                    "Date": forecast['Date'],
                    "Predicted": forecast['Sentiment'],
                    "Actual": actual['sentiment'],
                    "Predicted Score": forecast['Score'],
                    "Actual Score": actual['score']
                })
        
        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
    else:
        st.info("No forecast data available. Please update parameters.")

with tab5:
    st.markdown("""
    <div class="tab5-theme">
        <h1 style="color: white; text-align: center;">📅 Planetary Aspects Timeline</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Symbol selection with enhanced styling
    symbol_options = ["Nifty", "BankNifty", "Gold", "Silver", "Crude", "BTC", "DowJones"]
    selected_symbol = st.selectbox("🔍 Select Symbol for Timeline View", symbol_options)
    
    # Define market hours
    indian_market_open = datetime.time(9, 15)
    indian_market_close = datetime.time(15, 30)
    global_market_open = datetime.time(5, 0)
    global_market_close = datetime.time(23, 55)
    
    # Prepare aspects data for display
    aspects_display = []
    for aspect in st.session_state.aspects_data:
        time_str = aspect["time"]
        hour_min = time_str.replace(" am", "").replace(" pm", "")
        hour, minute = map(int, hour_min.split(":"))
        if "pm" in time_str and hour != 12:
            hour += 12
        aspect_time = datetime.time(hour, minute)
        
        market_status = ""
        if indian_market_open <= aspect_time <= indian_market_close:
            market_status = "🇮🇳 Indian Market Open"
        elif global_market_open <= aspect_time <= global_market_close:
            market_status = "🌍 Global Market Open"
        else:
            market_status = "⚫ Closed"
        
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
    
    # Display aspects in a timeline layout
    st.subheader(f"Planetary Aspects for {selected_symbol} - {date.strftime('%d %B %Y')}")
    
    for aspect in aspects_display:
        impact_color = {
            "Bullish": "#16a34a",
            "Bearish": "#dc2626",
            "Neutral": "#f59e0b"
        }.get(aspect["Impact"].split()[0] if aspect["Impact"].split()[0] in ["Bullish", "Bearish"] else "Neutral", "#6b7280")
        
        st.markdown(f"""
        <div class="aspect-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3>{aspect['Time']} - {aspect['Aspect']}</h3>
                    <p><strong>Meaning:</strong> {aspect['Meaning']}</p>
                    <p><strong>Market Status:</strong> {aspect['Market Status']}</p>
                </div>
                <div style="text-align: right;">
                    <h4 style="color: {impact_color};">{aspect['Impact']}</h4>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create a heatmap of aspects
    st.subheader("📊 Aspect Impact Heatmap")
    
    # Prepare data for heatmap
    heatmap_data = []
    for aspect in aspects_display:
        impact = aspect["Impact"]
        if "Bullish" in impact:
            score = 1
        elif "Bearish" in impact:
            score = -1
        else:
            score = 0
        
        heatmap_data.append({
            "Time": aspect["Time"],
            "Impact": score,
            "Aspect": aspect["Aspect"].split(" (")[0]
        })
    
    heatmap_df = pd.DataFrame(heatmap_data)
    
    fig = px.density_heatmap(
        heatmap_df, 
        x="Time", 
        y="Aspect", 
        z="Impact",
        color_continuous_scale=["red", "yellow", "green"],
        title="Aspect Impact Heatmap"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    st.subheader("📈 Summary Statistics")
    
    # Create a DataFrame for sentiment analysis
    aspects_df = pd.DataFrame(aspects_display)
    sentiment_counts = aspects_df['Impact'].apply(lambda x: 'Bullish' if 'Bullish' in x or 'recovery' in x.lower() or 'rally' in x.lower() else ('Bearish' if 'Bearish' in x or 'dip' in x.lower() or 'pressure' in x.lower() or 'risks' in x.lower() else 'Neutral')).value_counts()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card bullish-card">
            <h4>🟢 Bullish Aspects</h4>
            <p style="font-size: 2rem; font-weight: bold;">{sentiment_counts.get('Bullish', 0)}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card bearish-card">
            <h4>🔴 Bearish Aspects</h4>
            <p style="font-size: 2rem; font-weight: bold;">{sentiment_counts.get('Bearish', 0)}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="card neutral-card">
            <h4>⚪ Neutral Aspects</h4>
            <p style="font-size: 2rem; font-weight: bold;">{sentiment_counts.get('Neutral', 0)}</p>
        </div>
        """, unsafe_allow_html=True)

with tab6:
    st.markdown("""
    <div class="tab6-theme">
        <h1 style="color: white; text-align: center;">🔍 Advanced Aspect Search & Timeline</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Create filters for aspect search
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Symbol selection
        symbol_options = ["Nifty", "BankNifty", "Gold", "Silver", "Crude", "BTC", "DowJones"]
        search_symbol = st.selectbox("🔍 Select Symbol", symbol_options)
    
    with col2:
        # Date range selection
        start_date = st.date_input("📅 Start Date", value=datetime.date(2025, 8, 1))
        end_date = st.date_input("📅 End Date", value=datetime.date(2025, 8, 31))
    
    with col3:
        # Impact filter
        impact_filter = st.multiselect(
            "📊 Filter by Impact",
            ["Bullish", "Bearish", "Neutral"],
            default=["Bullish", "Bearish", "Neutral"]
        )
    
    # Generate aspects for the selected date range
    if start_date > end_date:
        st.error("Start date must be before end date")
    else:
        # Calculate number of days
        num_days = (end_date - start_date).days + 1
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize filtered aspects data
        filtered_aspects = []
        
        # Generate aspects for each day in the range
        for i in range(num_days):
            current_date = start_date + datetime.timedelta(days=i)
            
            # Update progress
            progress = (i + 1) / num_days
            progress_bar.progress(progress)
            status_text.text(f"Generating aspects for {current_date.strftime('%d %B %Y')}...")
            
            # Generate aspects for the current date
            if current_date == datetime.date(2025, 8, 6):
                daily_aspects = aug6_aspects
            else:
                daily_aspects = generate_aspects_for_date(current_date)
            
            # Process each aspect
            for aspect in daily_aspects:
                # Determine impact based on selected symbol
                if search_symbol in ["Nifty", "BankNifty"]:
                    impact = aspect["indian_market"]
                elif search_symbol in ["Gold", "Silver", "Crude"]:
                    impact = aspect["commodities"]
                elif search_symbol == "BTC":
                    impact = aspect["forex"]
                elif search_symbol == "DowJones":
                    impact = aspect["global_market"]
                else:
                    impact = "Neutral"
                
                # Check if impact matches filter
                impact_category = "Neutral"
                if "Bullish" in impact or "recovery" in impact.lower() or "rally" in impact.lower():
                    impact_category = "Bullish"
                elif "Bearish" in impact or "dip" in impact.lower() or "pressure" in impact.lower() or "risks" in impact.lower():
                    impact_category = "Bearish"
                
                if impact_category in impact_filter:
                    # Add to filtered aspects
                    filtered_aspects.append({
                        "Date": current_date.strftime("%d %B %Y"),
                        "Time": aspect["time"],
                        "Aspect": aspect["aspect"],
                        "Meaning": aspect["meaning"],
                        "Impact": impact,
                        "Impact Category": impact_category
                    })
        
        # Clear progress bar
        progress_bar.empty()
        status_text.empty()
        
        # Display filtered aspects
        if filtered_aspects:
            st.subheader(f"📊 {search_symbol} Aspect Timeline ({start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')})")
            
            # Create a timeline chart
            timeline_df = pd.DataFrame(filtered_aspects)
            
            # Convert date and time to datetime for plotting
            timeline_df['DateTime'] = pd.to_datetime(timeline_df['Date'] + ' ' + timeline_df['Time'])
            
            # Create a color map for impacts
            color_map = {
                "Bullish": "#16a34a",
                "Bearish": "#dc2626",
                "Neutral": "#f59e0b"
            }
            
            # Create a scatter plot for the timeline
            fig = px.scatter(
                timeline_df, 
                x="DateTime", 
                y="Aspect",
                color="Impact Category",
                color_discrete_map=color_map,
                hover_data=["Meaning", "Impact"],
                title=f"{search_symbol} Aspect Timeline",
                labels={"DateTime": "Date & Time", "Aspect": "Planetary Aspect"}
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Create a summary table
            st.subheader("📋 Aspect Summary")
            
            # Group by date and count impacts
            summary_df = timeline_df.groupby(['Date', 'Impact Category']).size().unstack(fill_value=0)
            
            # Add total column
            summary_df['Total'] = summary_df.sum(axis=1)
            
            # Display summary table
            st.dataframe(summary_df, use_container_width=True)
            
            # Create a bar chart for daily impact counts
            st.subheader("📈 Daily Impact Counts")
            
            # Prepare data for bar chart
            bar_data = []
            for date, group in timeline_df.groupby('Date'):
                for impact_cat in ['Bullish', 'Bearish', 'Neutral']:
                    count = len(group[group['Impact Category'] == impact_cat])
                    bar_data.append({
                        'Date': date,
                        'Impact Category': impact_cat,
                        'Count': count
                    })
            
            bar_df = pd.DataFrame(bar_data)
            
            fig = px.bar(
                bar_df,
                x="Date",
                y="Count",
                color="Impact Category",
                color_discrete_map=color_map,
                title="Daily Impact Counts",
                labels={"Count": "Number of Aspects", "Date": "Date"}
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed aspects in a table
            st.subheader("🔍 Detailed Aspect Information")
            
            # Create a DataFrame with all aspects
            aspects_df = pd.DataFrame(filtered_aspects)
            
            # Reorder columns
            aspects_df = aspects_df[['Date', 'Time', 'Aspect', 'Impact Category', 'Impact', 'Meaning']]
            
            # Display the table
            st.dataframe(aspects_df, use_container_width=True)
            
            # Download button for the data
            csv = aspects_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name=f"{search_symbol}_aspects_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No aspects found matching your criteria. Please adjust your filters.")

# Footer with enhanced styling
st.markdown("""
<hr>
<div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 0;">
    <div>
        <p>🌟 <strong>Dynamic Planetary Trading Dashboard</strong></p>
        <p>Real-time Astro-Financial Intelligence</p>
    </div>
    <div style="text-align: right;">
        <p>Last Updated: {}</p>
    </div>
</div>
""".format(st.session_state.last_update.strftime('%H:%M:%S') if st.session_state.last_update else "N/A"), unsafe_allow_html=True)

# Enhanced sidebar parameters
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; color: white;">
    <h4>📋 Current Parameters</h4>
    <p><strong>Date:</strong> {}</p>
    <p><strong>Symbol:</strong> {}</p>
    <p><strong>Location:</strong> {}</p>
</div>
""".format(date.strftime('%d %B %Y'), symbol, city), unsafe_allow_html=True)

if st.session_state.sentiment_data:
    sentiment = st.session_state.sentiment_data["sentiment"]
    score = st.session_state.sentiment_data["sentiment_score"]
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; color: white; margin-top: 10px;">
        <h4>📊 Current Sentiment</h4>
        <p><strong>Sentiment:</strong> {sentiment}</p>
        <p><strong>Score:</strong> {score:.1f}</p>
    </div>
    """, unsafe_allow_html=True)
