import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import pandas as pd
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math
import threading
import time

class PlanetaryTradingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("INTRADAY PLANETARY TRANSIT TRADING DASHBOARD")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Create main frames
        self.create_header()
        self.create_input_section()
        self.create_output_section()
        self.create_status_bar()
        
        # Initialize data
        self.planetary_data = None
        self.timeline_data = None
        self.trade_strategy = None
        self.current_time = None
        self.next_action = None
        
        # Start live update thread
        self.update_thread_running = True
        self.update_thread = threading.Thread(target=self.update_live_time)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#16213e', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title = tk.Label(header_frame, text="INTRADAY PLANETARY TRANSIT TRADING DASHBOARD", 
                         font=('Arial', 20, 'bold'), bg='#16213e', fg='#e94560')
        title.pack(pady=15)
        
        subtitle = tk.Label(header_frame, text="Astrowise & Gann Wise Trading System", 
                            font=('Arial', 12), bg='#16213e', fg='#f5f5f5')
        subtitle.pack()
    
    def create_input_section(self):
        input_frame = tk.LabelFrame(self.root, text="Input Parameters", bg='#0f3460', fg='white', 
                                   font=('Arial', 12, 'bold'))
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Date input
        date_frame = tk.Frame(input_frame, bg='#0f3460')
        date_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(date_frame, text="Date:", bg='#0f3460', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        self.date_entry = tk.Entry(date_frame, width=12, font=('Arial', 10))
        self.date_entry.pack(side=tk.LEFT)
        self.date_entry.insert(0, "04/08/2025")
        
        # Symbol input
        symbol_frame = tk.Frame(input_frame, bg='#0f3460')
        symbol_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(symbol_frame, text="Symbol:", bg='#0f3460', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        self.symbol_entry = tk.Entry(symbol_frame, width=10, font=('Arial', 10))
        self.symbol_entry.pack(side=tk.LEFT)
        self.symbol_entry.insert(0, "NIFTY")
        
        # City input
        city_frame = tk.Frame(input_frame, bg='#0f3460')
        city_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(city_frame, text="City:", bg='#0f3460', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        self.city_entry = tk.Entry(city_frame, width=10, font=('Arial', 10))
        self.city_entry.pack(side=tk.LEFT)
        self.city_entry.insert(0, "Mumbai")
        
        # Time input
        time_frame = tk.Frame(input_frame, bg='#0f3460')
        time_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(time_frame, text="Time:", bg='#0f3460', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        self.time_entry = tk.Entry(time_frame, width=8, font=('Arial', 10))
        self.time_entry.pack(side=tk.LEFT)
        self.time_entry.insert(0, "09:15")
        
        # Generate button
        self.generate_btn = tk.Button(input_frame, text="Generate Report", command=self.generate_report,
                                     bg='#e94560', fg='white', font=('Arial', 10, 'bold'))
        self.generate_btn.pack(side=tk.LEFT, padx=20, pady=10)
    
    def create_output_section(self):
        output_frame = tk.Frame(self.root, bg='#1a1a2e')
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(output_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Timeline tab
        self.timeline_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(self.timeline_frame, text="Transit Timeline")
        
        # Planetary positions tab
        self.planetary_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(self.planetary_frame, text="Planetary Positions")
        
        # Trade strategy tab
        self.strategy_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(self.strategy_frame, text="Trade Execution Strategy")
        
        # Create content for each tab
        self.create_timeline_tab()
        self.create_planetary_tab()
        self.create_strategy_tab()
    
    def create_timeline_tab(self):
        # Title
        title = tk.Label(self.timeline_frame, text="Critical Transit Timeline", 
                        font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#e94560')
        title.pack(pady=10)
        
        # Timeline table
        self.timeline_table = ttk.Treeview(self.timeline_frame, columns=('Time', 'Event', 'Influence', 'Sentiment'), 
                                          show='headings', height=15)
        
        # Define headings
        self.timeline_table.heading('Time', text='Time (IST)')
        self.timeline_table.heading('Event', text='Event')
        self.timeline_table.heading('Influence', text='Influence on Nifty/Bank Nifty')
        self.timeline_table.heading('Sentiment', text='Sentiment')
        
        # Define columns
        self.timeline_table.column('Time', width=100, anchor='center')
        self.timeline_table.column('Event', width=150, anchor='center')
        self.timeline_table.column('Influence', width=400, anchor='w')
        self.timeline_table.column('Sentiment', width=100, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.timeline_frame, orient="vertical", command=self.timeline_table.yview)
        self.timeline_table.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.timeline_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure style for color coding
        style = ttk.Style()
        style.configure("Treeview", background="#0f3460", foreground="white", fieldbackground="#0f3460")
        style.map('Treeview', background=[('selected', '#e94560')])
        
        # Live action section
        live_frame = tk.LabelFrame(self.timeline_frame, text="Live Trading Guidance", 
                                  bg='#16213e', fg='white', font=('Arial', 12, 'bold'))
        live_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Current time
        self.current_time_label = tk.Label(live_frame, text="Current Time: --:--:--", 
                                          font=('Arial', 12), bg='#16213e', fg='#f5f5f5')
        self.current_time_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Next action
        self.next_action_label = tk.Label(live_frame, text="Next Action: --", 
                                         font=('Arial', 12, 'bold'), bg='#16213e', fg='#e94560')
        self.next_action_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Action countdown
        self.countdown_label = tk.Label(live_frame, text="Time Remaining: --:--", 
                                       font=('Arial', 12), bg='#16213e', fg='#f5f5f5')
        self.countdown_label.pack(side=tk.LEFT, padx=20, pady=10)
    
    def create_planetary_tab(self):
        # Title
        title = tk.Label(self.planetary_frame, text="Planetary Positions", 
                        font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#e94560')
        title.pack(pady=10)
        
        # Planetary table
        self.planetary_table = ttk.Treeview(self.planetary_frame, 
                                           columns=('Planet', 'Sign', 'Degree', 'Nakshatra', 'Lord', 'Sublord', 'House'), 
                                           show='headings', height=15)
        
        # Define headings
        self.planetary_table.heading('Planet', text='Planet')
        self.planetary_table.heading('Sign', text='Sign')
        self.planetary_table.heading('Degree', text='Degree')
        self.planetary_table.heading('Nakshatra', text='Nakshatra')
        self.planetary_table.heading('Lord', text='Lord')
        self.planetary_table.heading('Sublord', text='Sublord')
        self.planetary_table.heading('House', text='House')
        
        # Define columns
        self.planetary_table.column('Planet', width=100, anchor='center')
        self.planetary_table.column('Sign', width=100, anchor='center')
        self.planetary_table.column('Degree', width=100, anchor='center')
        self.planetary_table.column('Nakshatra', width=120, anchor='center')
        self.planetary_table.column('Lord', width=100, anchor='center')
        self.planetary_table.column('Sublord', width=100, anchor='center')
        self.planetary_table.column('House', width=80, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.planetary_frame, orient="vertical", command=self.planetary_table.yview)
        self.planetary_table.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.planetary_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", background="#0f3460", foreground="white", fieldbackground="#0f3460")
        style.map('Treeview', background=[('selected', '#e94560')])
        
        # Planet visualization
        self.planet_canvas = tk.Canvas(self.planetary_frame, width=600, height=300, bg='#0f3460', highlightthickness=0)
        self.planet_canvas.pack(fill=tk.X, padx=10, pady=10)
    
    def create_strategy_tab(self):
        # Title
        title = tk.Label(self.strategy_frame, text="Trade Execution Strategy", 
                        font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#e94560')
        title.pack(pady=10)
        
        # Strategy text
        self.strategy_text = tk.Text(self.strategy_frame, wrap=tk.WORD, height=20, width=80, 
                                    bg='#0f3460', fg='white', font=('Arial', 10))
        self.strategy_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbar
        strategy_scrollbar = ttk.Scrollbar(self.strategy_text, command=self.strategy_text.yview)
        self.strategy_text.configure(yscrollcommand=strategy_scrollbar.set)
        strategy_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg='#16213e', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="Ready", bg='#16213e', fg='white', 
                                    font=('Arial', 10), anchor='w')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.copyright_label = tk.Label(status_frame, text="© 2025 Planetary Trading Dashboard", 
                                      bg='#16213e', fg='white', font=('Arial', 10), anchor='e')
        self.copyright_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def generate_report(self):
        try:
            # Get input values
            date_str = self.date_entry.get()
            symbol = self.symbol_entry.get().upper()
            city = self.city_entry.get()
            time_str = self.time_entry.get()
            
            # Parse date and time
            date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
            time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
            datetime_obj = datetime.datetime.combine(date_obj, time_obj)
            
            # Update status
            self.status_label.config(text=f"Generating report for {symbol} on {date_str} at {time_str} in {city}...")
            
            # Generate planetary data (mock data for demonstration)
            self.generate_planetary_data(datetime_obj, city)
            
            # Generate timeline data
            self.generate_timeline_data(symbol)
            
            # Generate trade strategy
            self.generate_trade_strategy(symbol)
            
            # Update UI
            self.update_timeline_table()
            self.update_planetary_table()
            self.update_planet_visualization()
            self.update_strategy_text()
            
            # Update status
            self.status_label.config(text="Report generated successfully")
            messagebox.showinfo("Success", "Report generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_label.config(text="Error generating report")
    
    def generate_planetary_data(self, datetime_obj, city):
        # Mock planetary data for demonstration
        # In a real implementation, this would use astronomical calculations
        
        # Define planetary data structure
        self.planetary_data = [
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
    
    def generate_timeline_data(self, symbol):
        # Mock timeline data for demonstration
        # In a real implementation, this would use astrological calculations
        
        # Define timeline data structure
        self.timeline_data = [
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
    
    def generate_trade_strategy(self, symbol):
        # Mock trade strategy for demonstration
        # In a real implementation, this would use astrological and technical analysis
        
        if symbol == "NIFTY":
            self.trade_strategy = """
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
            self.trade_strategy = """
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
            self.trade_strategy = f"""
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
    
    def update_timeline_table(self):
        # Clear existing data
        for item in self.timeline_table.get_children():
            self.timeline_table.delete(item)
        
        # Add new data with color coding
        for item in self.timeline_data:
            # Determine tag for color coding
            if "Bullish" in item["Sentiment"]:
                tags = ('bullish',)
            elif "Bearish" in item["Sentiment"]:
                tags = ('bearish',)
            else:
                tags = ('volatile',)
            
            # Insert item
            self.timeline_table.insert('', 'end', values=(
                item["Time"], 
                item["Event"], 
                item["Influence"], 
                item["Sentiment"]
            ), tags=tags)
        
        # Configure tags for color coding
        self.timeline_table.tag_configure('bullish', background='#2d8a2f', foreground='white')
        self.timeline_table.tag_configure('bearish', background='#b22222', foreground='white')
        self.timeline_table.tag_configure('volatile', background='#ff8c00', foreground='white')
    
    def update_planetary_table(self):
        # Clear existing data
        for item in self.planetary_table.get_children():
            self.planetary_table.delete(item)
        
        # Add new data
        for item in self.planetary_data:
            self.planetary_table.insert('', 'end', values=(
                item["Planet"], 
                item["Sign"], 
                item["Degree"], 
                item["Nakshatra"], 
                item["Lord"], 
                item["Sublord"], 
                item["House"]
            ))
    
    def update_planet_visualization(self):
        # Clear canvas
        self.planet_canvas.delete("all")
        
        # Draw zodiac wheel
        width = 600
        height = 300
        center_x = width // 2
        center_y = height // 2
        radius = 120
        
        # Draw zodiac circle
        self.planet_canvas.create_oval(center_x - radius, center_y - radius, 
                                      center_x + radius, center_y + radius, 
                                      outline='#e94560', width=2)
        
        # Draw zodiac signs
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        for i, sign in enumerate(signs):
            angle = i * 30  # 30 degrees per sign
            rad = math.radians(angle)
            x = center_x + (radius - 20) * math.cos(rad)
            y = center_y + (radius - 20) * math.sin(rad)
            self.planet_canvas.create_text(x, y, text=sign, fill='white', font=('Arial', 8))
        
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
        
        for planet in self.planetary_data:
            sign = planet["Sign"]
            if sign in sign_angles:
                angle = sign_angles[sign]
                # Add some randomness for visualization
                angle += np.random.randint(-10, 10)
                rad = math.radians(angle)
                
                # Position planet
                planet_radius = radius - 40
                x = center_x + planet_radius * math.cos(rad)
                y = center_y + planet_radius * math.sin(rad)
                
                # Draw planet
                color = planet_colors.get(planet["Planet"], "#ffffff")
                self.planet_canvas.create_oval(x-8, y-8, x+8, y+8, fill=color, outline='white')
                
                # Draw planet label
                self.planet_canvas.create_text(x, y-15, text=planet["Planet"], fill='white', font=('Arial', 8))
        
        # Draw legend
        legend_x = 20
        legend_y = 20
        self.planet_canvas.create_text(legend_x, legend_y, text="Planetary Positions", 
                                      fill='white', font=('Arial', 10, 'bold'), anchor='w')
        
        # Draw planet color legend
        for i, (planet, color) in enumerate(planet_colors.items()):
            y_pos = legend_y + 20 + i * 15
            self.planet_canvas.create_oval(legend_x, y_pos, legend_x+10, y_pos+10, fill=color, outline='white')
            self.planet_canvas.create_text(legend_x+15, y_pos+5, text=planet, fill='white', 
                                          font=('Arial', 8), anchor='w')
    
    def update_strategy_text(self):
        # Clear existing text
        self.strategy_text.delete(1.0, tk.END)
        
        # Add new text
        self.strategy_text.insert(tk.END, self.trade_strategy)
        
        # Configure text tags for color coding
        self.strategy_text.tag_configure("header", foreground="#e94560", font=('Arial', 12, 'bold'))
        self.strategy_text.tag_configure("subheader", foreground="#f5f5f5", font=('Arial', 10, 'bold'))
        self.strategy_text.tag_configure("bullish", foreground="#2d8a2f", font=('Arial', 10))
        self.strategy_text.tag_configure("bearish", foreground="#b22222", font=('Arial', 10))
        self.strategy_text.tag_configure("neutral", foreground="#f5f5f5", font=('Arial', 10))
        
        # Apply tags to text
        lines = self.strategy_text.get(1.0, tk.END).split('\n')
        for i, line in enumerate(lines):
            if line.startswith("###"):
                self.strategy_text.tag_add(f"header", f"{i+1}.0", f"{i+1}.end")
            elif line.startswith("####"):
                self.strategy_text.tag_add(f"subheader", f"{i+1}.0", f"{i+1}.end")
            elif "Bullish" in line:
                self.strategy_text.tag_add(f"bullish", f"{i+1}.0", f"{i+1}.end")
            elif "Bearish" in line:
                self.strategy_text.tag_add(f"bearish", f"{i+1}.0", f"{i+1}.end")
            else:
                self.strategy_text.tag_add(f"neutral", f"{i+1}.0", f"{i+1}.end")
    
    def update_live_time(self):
        while self.update_thread_running:
            try:
                # Get current time
                now = datetime.datetime.now()
                current_time_str = now.strftime("%H:%M:%S")
                
                # Update current time label
                self.current_time_label.config(text=f"Current Time: {current_time_str}")
                
                # Check if we have timeline data
                if self.timeline_data:
                    # Find next action
                    next_action = None
                    for item in self.timeline_data:
                        time_str = item["Time"]
                        # Parse time
                        try:
                            action_time = datetime.datetime.strptime(time_str, "%I:%M %p")
                            action_time = action_time.replace(year=now.year, month=now.month, day=now.day)
                            
                            # Check if action time is in the future
                            if action_time > now:
                                next_action = item
                                break
                        except:
                            pass
                    
                    if next_action:
                        # Update next action label
                        self.next_action_label.config(text=f"Next Action: {next_action['Time']} - {next_action['Sentiment']}")
                        
                        # Calculate time remaining
                        action_time = datetime.datetime.strptime(next_action['Time'], "%I:%M %p")
                        action_time = action_time.replace(year=now.year, month=now.month, day=now.day)
                        time_remaining = action_time - now
                        
                        # Update countdown label
                        hours, remainder = divmod(time_remaining.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        self.countdown_label.config(text=f"Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d}")
                        
                        # Color code based on sentiment
                        if "Bullish" in next_action['Sentiment']:
                            self.next_action_label.config(fg="#2d8a2f")
                        elif "Bearish" in next_action['Sentiment']:
                            self.next_action_label.config(fg="#b22222")
                        else:
                            self.next_action_label.config(fg="#ff8c00")
                    else:
                        self.next_action_label.config(text="Next Action: Market Closed")
                        self.countdown_label.config(text="Time Remaining: --:--:--")
                
                # Sleep for 1 second
                time.sleep(1)
            except Exception as e:
                print(f"Error updating live time: {e}")
                time.sleep(5)
    
    def on_closing(self):
        self.update_thread_running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanetaryTradingDashboard(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
