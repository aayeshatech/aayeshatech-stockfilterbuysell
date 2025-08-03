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
        color: #ff4b4b;
        font-weight: bold;
    }
    .bullish {
        color: #4fff4b;
        font-weight: bold;
    }
    .volatile {
        color: #ffb84d;
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
        background-color: #0f3460;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
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
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "NIFTY"
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.date(2025, 8, 4)
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Header
st.markdown('<div class="main-header">INTRADAY PLANETARY TRANSIT TRADING DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Astrowise & Gann Wise Trading System</div>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Date input
date = st.sidebar.date_input("Date", value=st.session_state.current_date)

# Symbol input
symbol = st.sidebar.selectbox("Symbol", ["NIFTY", "BANKNIFTY", "RELIANCE", "TCS", "INFY"])

# City input
city = st.sidebar.text_input("City", value="Mumbai")

# Time input
time_input = st.sidebar.time_input("Time", value=datetime.time(9, 15))

# Generate button
generate_btn = st.sidebar.button("Generate Report")

# Function to generate planetary data
def generate_planetary_data(datetime_obj, city):
    # Mock planetary data for demonstration
    return [
        {"Planet": "Sun", "Sign": "Cancer", "Degree": "17° 30'", "Nakshatra": "Ashlesha", 
         "Lord": "Moon", "Sublord": "Mercury", "House": "2"},
        {"Planet": "Moon", "Sign": "Scorpio", "Degree": "20° 00'", "Nakshatra": "Jyeshtha", 
         "Lord": "Mercury", "Sublord": "Ketu", "House": "6"},
        {"Planet": "Mercury", "Sign": "Leo", "Degree": "10° 00'", "Nakshatra": "Magha", 
         "Lord": "Sun", "Sublord": "Ketu", "House": "3"},
        {"Planet": "Venus", "Sign": "Leo", "Degree": "5° 00'", "Nakshatra": "Magha", 
         "Lord": "Sun", "Sublord": "Ketu", "House": "3"},
        {"Planet": "Mars", "Sign": "Cancer", "Degree": "10° 00'", "Nakshatra": "Pushya", 
         "Lord": "Saturn", "Sublord": "Mercury", "House": "2"},
        {"Planet": "Jupiter", "Sign": "Taurus", "Degree": "10° 00'", "Nakshatra": "Krittika", 
         "Lord": "Sun", "Sublord": "Venus", "House": "12"},
        {"Planet": "Saturn", "Sign": "Pisces", "Degree": "5° 00'", "Nakshatra": "Uttara Bhadrapada", 
         "Lord": "Saturn", "Sublord": "Jupiter", "House": "10"},
        {"Planet": "Rahu", "Sign": "Pisces", "Degree": "20° 00'", "Nakshatra": "Revati", 
         "Lord": "Mercury", "Sublord": "Sun", "House": "10"},
        {"Planet": "Ketu", "Sign": "Virgo", "Degree": "20° 00'", "Nakshatra": "Chitra", 
         "Lord": "Mars", "Sublord": "Venus", "House": "4"}
    ]

# Function to generate timeline data
def generate_timeline_data(symbol):
    # Mock timeline data for demonstration
    return [
        {"Time": "9:15 AM", "Event": "Moon in Jyeshtha (Scorpio)", 
         "Influence": "Rahu aspects Moon (exact trine). Saturn-Rahu conjunction in Pisces creates volatility.", 
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

# Function to generate trade strategy
def generate_trade_strategy(symbol):
    if symbol == "NIFTY":
        return """
### Nifty (Index) Trading Strategy

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
    elif symbol == "BANKNIFTY":
        return """
### Bank Nifty (Banking Index) Trading Strategy

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
    else:
        return f"""
### {symbol} Trading Strategy

#### General Approach
Based on the planetary positions and transit timeline for today, the following strategy is recommended:

1. **Morning Session (9:15 AM - 12:00 PM)**: 
   - Bearish sentiment dominates in the first hour. Consider short positions with tight stop-loss.
   - Mid-morning may see a brief bullish reversal around 11:15 AM.

2. **Afternoon Session (12:00 PM - 3:30 PM)**:
   - Volatility expected during Moon hora (1:15 PM - 2:15 PM). Avoid new positions.
   - Late session may see mild recovery attempts.

### Risk Management
- **Stop-Loss**: 0.5% for intraday trades.
- **Position Sizing**: Limit exposure to 20% of trading capital per trade.
- **Confirmation**: Always use technical indicators to confirm astrological signals.
"""

# Function to create zodiac wheel visualization
def create_zodiac_wheel(planetary_data):
    # Create a blank image
    img = Image.new('RGB', (600, 600), color='#0f3460')
    draw = ImageDraw.Draw(img)
    
    # Define parameters
    center_x, center_y = 300, 300
    radius = 250
    
    # Draw zodiac circle
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline='#e94560', width=2)
    
    # Draw zodiac signs
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    for i, sign in enumerate(signs):
        angle = i * 30  # 30 degrees per sign
        rad = math.radians(angle)
        x = center_x + (radius - 30) * math.cos(rad)
        y = center_y + (radius - 30) * math.sin(rad)
        draw.text((x, y), sign, fill='white', font=font)
    
    # Draw planets
    planet_colors = {
        "Sun": "#ffcc00", "Moon": "#cccccc", "Mercury": "#b0b0b0", 
        "Venus": "#e39e1c", "Mars": "#ff0000", "Jupiter": "#ff9900", 
        "Saturn": "#ffcc99", "Rahu": "#4b0082", "Ketu": "#8b008b"
    }
    
    # Map signs to angles (simplified)
    sign_angles = {
        "Aries": 0, "Taurus": 30, "Gemini": 60, "Cancer": 90, 
        "Leo": 120, "Virgo": 150, "Libra": 180, "Scorpio": 210, 
        "Sagittarius": 240, "Capricorn": 270, "Aquarius": 300, "Pisces": 330
    }
    
    for planet in planetary_data:
        sign = planet["Sign"]
        if sign in sign_angles:
            angle = sign_angles[sign]
            # Add some randomness for visualization
            angle += np.random.randint(-10, 10)
            rad = math.radians(angle)
            
            # Position planet
            planet_radius = radius - 60
            x = center_x + planet_radius * math.cos(rad)
            y = center_y + planet_radius * math.sin(rad)
            
            # Draw planet
            color = planet_colors.get(planet["Planet"], "#ffffff")
            draw.ellipse((x-10, y-10, x+10, y+10), fill=color, outline='white')
            
            # Draw planet label
            draw.text((x-15, y-25), planet["Planet"], fill='white', font=font)
    
    # Convert to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Generate report when button is clicked
if generate_btn:
    # Update session state
    st.session_state.current_date = date
    st.session_state.current_symbol = symbol
    
    # Create datetime object
    datetime_obj = datetime.datetime.combine(date, time_input)
    
    # Generate data
    st.session_state.planetary_data = generate_planetary_data(datetime_obj, city)
    st.session_state.timeline_data = generate_timeline_data(symbol)
    st.session_state.trade_strategy = generate_trade_strategy(symbol)
    
    # Show success message
    st.sidebar.success("Report generated successfully!")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Transit Timeline", "Planetary Positions", "Trade Execution Strategy"])

# Tab 1: Transit Timeline
with tab1:
    st.header("Critical Transit Timeline")
    
    if st.session_state.timeline_data:
        # Create DataFrame
        df = pd.DataFrame(st.session_state.timeline_data)
        
        # Add color formatting
        def highlight_sentiment(val):
            if "Bullish" in val:
                return 'color: #4fff4b'
            elif "Bearish" in val:
                return 'color: #ff4b4b'
            else:
                return 'color: #ffb84d'
        
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
        
        # Display zodiac wheel
        st.subheader("Planetary Positions Visualization")
        zodiac_image = create_zodiac_wheel(st.session_state.planetary_data)
        st.image(zodiac_image, width=600)
    else:
        st.info("Generate a report to see planetary positions.")

# Tab 3: Trade Execution Strategy
with tab3:
    st.header("Trade Execution Strategy")
    
    if st.session_state.trade_strategy:
        st.markdown(f'<div class="strategy-box">{st.session_state.trade_strategy}</div>', unsafe_allow_html=True)
    else:
        st.info("Generate a report to see trade execution strategy.")

# Status bar
st.markdown('<div class="status-bar">© 2025 Planetary Trading Dashboard | Status: Ready</div>', unsafe_allow_html=True)

# Auto-refresh every minute
if time.time() - st.session_state.last_update > 60:
    st.session_state.last_update = time.time()
    st.experimental_rerun()
