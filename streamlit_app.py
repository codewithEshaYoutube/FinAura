# 💸 FinAura: Your Gen Z CFO – Where Vibes Meet Value
# Enhanced Streamlit App with Financial Planning & Budget Structure

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import sqlite3
import asyncio
from enum import Enum
import hashlib
import math  # Added for debt calculations
import traceback
import logging

# =============================================================================
# ERROR HANDLING & DEBUGGING SYSTEM
# =============================================================================

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_execute(func, fallback=None, error_message="An error occurred"):
    """Safely execute a function with error handling"""
    try:
        return func()
    except Exception as e:
        logger.error(f"Error in {func.__name__ if hasattr(func, '__name__') else 'function'}: {str(e)}")
        if st.session_state.get('debug_mode', False):
            st.error(f"🐛 Debug Mode: {error_message}\n```\n{str(e)}\n```")
        return fallback

def handle_calculation_error(calculation_func, default_value=0):
    """Handle mathematical calculation errors"""
    try:
        result = calculation_func()
        if math.isnan(result) or math.isinf(result):
            return default_value
        return result
    except (ZeroDivisionError, ValueError, TypeError) as e:
        logger.warning(f"Calculation error: {str(e)}")
        return default_value

# Page config with Gen Z vibes
st.set_page_config(
    page_title="💸 FinAura - Your Gen Z CFO",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Gen Z aesthetic
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .vibe-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .money-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 0.5rem;
    }
    
    .budget-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem;
        color: #2d3748;
        text-align: center;
    }
    
    .investment-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem;
        color: #2d3748;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #2d3748;
    }
    
    .financial-goal-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .chat-bubble {
        background: #f7fafc;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 15px 15px 0;
        font-style: italic;
    }
    
    .progress-bar {
        background: #e2e8f0;
        border-radius: 10px;
        height: 20px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# ENHANCED DATA MODELS & CORE LOGIC
# =============================================================================

class VibeType(Enum):
    STRESSED = "😩"
    CONFIDENT = "😎"
    CONFUSED = "🤔"
    EXCITED = "🚀"
    CHILL = "😌"
    GUILTY = "😬"

class SpendingCategory(Enum):
    ESSENTIAL = "🏠 Essential"
    JOY = "✨ Joy"
    OOPS = "😅 Oops"
    INVESTMENT = "📈 Investment"

class FinancialGoal(Enum):
    EMERGENCY_FUND = "🚨 Emergency Fund"
    TRAVEL = "✈️ Travel Fund"
    HOUSE_DEPOSIT = "🏡 House Deposit"
    RETIREMENT = "👴 Future Me Fund"
    SIDE_HUSTLE = "💼 Side Hustle Capital"
    EDUCATION = "📚 Skill Up Fund"

@dataclass
class Transaction:
    date: datetime
    amount: float
    description: str
    category: SpendingCategory
    merchant: str = ""
    vibe_impact: float = 0.0

@dataclass
class VibeData:
    current_vibe: VibeType
    money_stress_level: int
    spending_guilt: int
    financial_confidence: int

@dataclass
class BudgetPlan:
    monthly_income: float
    needs_percentage: float = 50.0  # 50/30/20 rule adjusted for Gen Z
    wants_percentage: float = 30.0
    savings_percentage: float = 20.0
    
    @property
    def needs_amount(self) -> float:
        return self.monthly_income * (self.needs_percentage / 100)
    
    @property
    def wants_amount(self) -> float:
        return self.monthly_income * (self.wants_percentage / 100)
    
    @property
    def savings_amount(self) -> float:
        return self.monthly_income * (self.savings_percentage / 100)

class EnhancedFinAuraAgent:
    """The Gen Z AI Agent that gets your vibes AND your financial goals"""
    
    def __init__(self):
        self.vibe_responses = {
            VibeType.STRESSED: [
                "Hey bestie, I see you're feeling the money stress 😔 Let's break this down together",
                "Okay, deep breath! Your finances aren't as scary as they seem rn",
                "You're doing better than you think! Let me show you the receipts 📊"
            ],
            VibeType.CONFIDENT: [
                "YES QUEEN! 👑 Your money game is strong today",
                "Love this energy! You're absolutely crushing your financial goals",
                "Confidence looks good on you! Your budget is thriving ✨"
            ],
            VibeType.CONFUSED: [
                "No judgment here! Money stuff is confusing AF sometimes 🤷‍♀️",
                "Let's untangle this together! I'll make it make sense",
                "Confusion is valid! Your finances don't have to be perfect"
            ],
            VibeType.GUILTY: [
                "Stop! 🛑 Guilt spending happens to literally everyone",
                "That purchase doesn't define you, babe. Let's just adjust and move on",
                "Self-compassion > self-judgment. Your worth isn't your spending"
            ]
        }
        
        self.investment_suggestions = {
            "low_risk": [
                {"name": "High-Yield Savings", "desc": "Safe & steady growth 📈", "risk": "Low", "return": "2-4%"},
                {"name": "Government Bonds", "desc": "Boring but reliable 🏛️", "risk": "Low", "return": "3-5%"},
                {"name": "CDs (Certificates of Deposit)", "desc": "Lock it up, stack it up 🔒", "risk": "Low", "return": "3-5%"}
            ],
            "medium_risk": [
                {"name": "Index Funds (S&P 500)", "desc": "Diversified market vibes 📊", "risk": "Medium", "return": "7-10%"},
                {"name": "Target-Date Funds", "desc": "Set it and forget it ⏰", "risk": "Medium", "return": "6-9%"},
                {"name": "REITs", "desc": "Real estate without the drama 🏠", "risk": "Medium", "return": "5-8%"}
            ],
            "high_risk": [
                {"name": "Individual Stocks", "desc": "Pick your favorites 🎯", "risk": "High", "return": "Variable"},
                {"name": "Cryptocurrency", "desc": "Digital gold or digital chaos? 🪙", "risk": "High", "return": "Highly Variable"},
                {"name": "Growth Stocks", "desc": "Betting on the future 🚀", "risk": "High", "return": "Variable"}
            ]
        }
        
        self.gen_z_financial_tips = [
            "💡 Automate your savings - treat it like a subscription you can't cancel",
            "🎯 Use the 24-hour rule for purchases over $50",
            "📱 Try investment apps like Robinhood, Acorns, or Stash for micro-investing",
            "🏠 Aim for 6-month emergency fund (adulting is expensive!)",
            "✨ Invest in yourself - courses, certifications, side hustles",
            "🌱 Start investing early - compound interest is your bestie",
            "💳 Build credit responsibly - your future self will thank you",
            "🎉 Celebrate small wins - every dollar saved matters!"
        ]
    
    def get_vibe_response(self, vibe: VibeType) -> str:
        return random.choice(self.vibe_responses.get(vibe, ["You're doing great! 💜"]))
    
    def get_budget_suggestions(self, income: float, age: int = 25) -> Dict:
        """Generate Gen Z-specific budget suggestions"""
        if income < 2000:
            return {
                "needs": 60,  # Higher for survival mode
                "wants": 25,
                "savings": 15,
                "advice": "Survival mode activated! Focus on essentials and small savings wins 💪"
            }
        elif income < 4000:
            return {
                "needs": 55,
                "wants": 30,
                "savings": 15,
                "advice": "Building phase! You're doing great - balance is key 🌟"
            }
        elif income < 6000:
            return {
                "needs": 50,
                "wants": 30,
                "savings": 20,
                "advice": "Thriving mode! Classic 50/30/20 rule works perfectly 🔥"
            }
        else:
            return {
                "needs": 45,
                "wants": 35,
                "savings": 20,
                "advice": "High earner energy! More room for joy spending AND aggressive saving ✨"
            }
    
    def get_investment_roadmap(self, age: int, income: float, risk_tolerance: str) -> List[Dict]:
        """Create age-appropriate investment suggestions"""
        roadmap = []
        
        # Emergency fund first (always!)
        roadmap.append({
            "priority": 1,
            "goal": "Emergency Fund",
            "target": min(income * 6, 10000),  # 6 months expenses
            "description": "Your financial safety net - aim for 3-6 months expenses 🚨"
        })
        
        # Age-based suggestions
        if age < 30:
            roadmap.extend([
                {
                    "priority": 2,
                    "goal": "Retirement Start",
                    "target": income * 0.15,  # 15% of income
                    "description": "Start early = retire like royalty 👑"
                },
                {
                    "priority": 3,
                    "goal": "Skill Investment",
                    "target": income * 0.05,  # 5% for education
                    "description": "Invest in yourself - best ROI ever 📚"
                }
            ])
        
        return roadmap

# =============================================================================
# SESSION STATE INITIALIZATION WITH ERROR HANDLING
# =============================================================================

# Initialize debug mode and error tracking
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

if 'error_count' not in st.session_state:
    st.session_state.error_count = 0

if 'last_error' not in st.session_state:
    st.session_state.last_error = None

if 'transactions' not in st.session_state:
    sample_data = [
        Transaction(datetime.now() - timedelta(days=1), 4.50, "iced coffee emergency", SpendingCategory.JOY, "starbucks", 0.3),
        Transaction(datetime.now() - timedelta(days=2), 89.99, "skincare haul (self care!!)", SpendingCategory.JOY, "sephora", 0.2),
        Transaction(datetime.now() - timedelta(days=3), 1200.00, "rent (ugh)", SpendingCategory.ESSENTIAL, "landlord", -0.2),
        Transaction(datetime.now() - timedelta(days=4), 25.99, "tiktok made me buy it", SpendingCategory.OOPS, "amazon", -0.4),
        Transaction(datetime.now() - timedelta(days=5), 15.99, "spotify premium", SpendingCategory.JOY, "spotify", 0.1),
        Transaction(datetime.now() - timedelta(days=6), 67.43, "groceries (adult moment)", SpendingCategory.ESSENTIAL, "whole foods", 0.0),
        Transaction(datetime.now() - timedelta(days=7), 150.00, "therapy session", SpendingCategory.ESSENTIAL, "therapist", 0.5),
        Transaction(datetime.now() - timedelta(days=8), 39.99, "late night uber eats", SpendingCategory.OOPS, "uber eats", -0.2),
    ]
    st.session_state.transactions = sample_data

if 'current_vibe' not in st.session_state:
    st.session_state.current_vibe = VibeType.CHILL

if 'agent' not in st.session_state:
    st.session_state.agent = EnhancedFinAuraAgent()

if 'budget_plan' not in st.session_state:
    st.session_state.budget_plan = None

if 'financial_profile' not in st.session_state:
    st.session_state.financial_profile = {}

# =============================================================================
# GLOBAL CURRENCY SELECTION
# =============================================================================

# Add currency selection at the top of the sidebar
if 'currency' not in st.session_state:
    st.session_state.currency = 'USD'

currency_symbols = {'USD': '$', 'PKR': 'PKR', 'EUR': '€'}
currency_rates = {'USD': 1.0, 'PKR': 280.0, 'EUR': 0.92}  # Example rates, update as needed

with st.sidebar:
    st.markdown('### 🌍 Select Currency')
    st.session_state.currency = st.selectbox(
        'Currency',
        options=['USD', 'PKR', 'EUR'],
        format_func=lambda x: f"{currency_symbols[x]} {x}",
        index=['USD', 'PKR', 'EUR'].index(st.session_state.currency)
    )
    
    st.markdown('---')
    
    # Debug Panel
    st.markdown('### 🛠️ Developer Tools')
    st.session_state.debug_mode = st.checkbox('🐛 Debug Mode', value=st.session_state.debug_mode)
    
    if st.session_state.debug_mode:
        st.markdown('#### 📊 Debug Info')
        st.info(f"Errors: {st.session_state.error_count}")
        if st.session_state.last_error:
            st.error(f"Last Error: {st.session_state.last_error}")
        
        if st.button('🔄 Reset App Data'):
            for key in list(st.session_state.keys()):
                if key not in ['debug_mode', 'error_count']:
                    del st.session_state[key]
            st.success('App data reset!')
            st.rerun()
    
    st.markdown('---')
    
    # App Settings
    st.markdown('### ⚙️ App Settings')
    
    # Theme selector
    theme_mode = st.selectbox(
        '🎨 Interface Theme',
        options=['Auto', 'Dark', 'Light'],
        index=0
    )
    
    # Notification settings
    show_notifications = st.checkbox('🔔 Show Notifications', value=True)
    
    # Performance mode
    performance_mode = st.selectbox(
        '⚡ Performance Mode',
        options=['Standard', 'Fast', 'Detailed'],
        index=0,
        help='Fast: Fewer animations, Detailed: More calculations'
    )
    
    st.markdown('---')
    
    # Quick Actions
    st.markdown('### 🚀 Quick Actions')
    
    if st.button('💰 Add Quick Transaction', use_container_width=True):
        # Add a quick random transaction
        try:
            quick_transactions = [
                ("Coffee break ☕", 5.50, SpendingCategory.JOY),
                ("Lunch deal 🍕", 12.99, SpendingCategory.ESSENTIAL),
                ("Impulse buy 😅", 25.00, SpendingCategory.OOPS),
                ("Gas/Transport 🚗", 35.00, SpendingCategory.ESSENTIAL),
                ("Movie night 🎬", 18.50, SpendingCategory.JOY)
            ]
            desc, amount, category = random.choice(quick_transactions)
            new_transaction = Transaction(
                datetime.now(), 
                amount, 
                desc, 
                category, 
                "quick-add", 
                random.uniform(-0.2, 0.3)
            )
            st.session_state.transactions.append(new_transaction)
            st.success(f'Added: {desc} - {format_currency(amount)}')
            st.rerun()
        except Exception as e:
            st.error(f"Error adding transaction: {str(e)}")
    
    if st.button('📈 Generate Report', use_container_width=True):
        st.info('📊 Report generated! Check the dashboard below.')
    
    if st.button('🎯 Set Financial Goal', use_container_width=True):
        st.info('🎯 Goal setting panel activated!')

# Helper to convert and format currency with error handling

def format_currency(amount, decimals=2):
    """Safely format currency with error handling"""
    try:
        if amount is None or math.isnan(amount) or math.isinf(amount):
            amount = 0
        
        symbol = currency_symbols.get(st.session_state.currency, '$')
        rate = currency_rates.get(st.session_state.currency, 1.0)
        value = float(amount) * rate
        
        if symbol == 'PKR':
            return f"PKR {value:,.{decimals}f}"
        elif symbol == '€':
            return f"€{value:,.{decimals}f}"
        else:
            return f"${value:,.{decimals}f}"
    except (ValueError, TypeError, KeyError) as e:
        logger.warning(f"Currency formatting error: {str(e)}")
        return f"${float(amount or 0):,.{decimals}f}"

# Helper to get currency label for headings

def get_currency_label():
    symbol = currency_symbols[st.session_state.currency]
    code = st.session_state.currency
    return f"{symbol} ({code})"

# =============================================================================
# MAIN APP INTERFACE
# =============================================================================



# =============================================================================
# GLOBAL ERROR HANDLER & MAIN APP WRAPPER
# =============================================================================

try:
    # Header with Gen Z energy
    st.markdown("""
    <div class="main-header">
        <h1>💸 FinAura: Your Gen Z CFO</h1>
        <p><em>"Forget spreadsheets. Feel your finances."</em></p>
        <p>Where vibes meet value ✨ | Fully Debugged & Enhanced!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Error count display for admins
    if st.session_state.debug_mode and st.session_state.error_count > 0:
        st.warning(f"⚠️ Debug Mode: {st.session_state.error_count} errors detected this session")

except Exception as e:
    st.error("🚨 Critical Error in App Header")
    logger.critical(f"Header error: {str(e)}")
    st.session_state.error_count += 1
    st.session_state.last_error = str(e)

# =============================================================================
# FINANCIAL PROFILE SETUP
# =============================================================================

st.markdown("## 💼 Financial Profile Setup")

with st.expander("🚀 Set Up Your Financial Profile (Click to expand)", expanded=not st.session_state.financial_profile):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monthly_income = st.number_input(
            f"💰 Monthly Income/Allowance {get_currency_label()}",
            min_value=0.0,
            value=st.session_state.financial_profile.get('monthly_income', 50000.0),
            step=1000.0,
            help="Include salary, freelance, side hustles, everything!"
        )
        
        age = st.slider(
            "🎂 Age",
            min_value=18,
            max_value=35,
            value=st.session_state.financial_profile.get('age', 25)
        )
    
    with col2:
        employment_status = st.selectbox(
            "👔 Employment Status",
            ["Student", "Full-time Job", "Freelancer", "Part-time", "Unemployed", "Side Hustle King/Queen"],
            index=1
        )
        
        living_situation = st.selectbox(
            "🏠 Living Situation",
            ["With Parents (blessed!)", "Shared Apartment", "Solo Living", "Dorm Life"],
            index=0
        )
    
    with col3:
        risk_tolerance = st.selectbox(
            "📊 Investment Risk Tolerance",
            ["Conservative (play it safe)", "Moderate (balanced vibes)", "Aggressive (YOLO but smart)"],
            index=1
        )
        
        primary_goal = st.selectbox(
            "🎯 Primary Financial Goal",
            list(FinancialGoal),
            format_func=lambda x: x.value
        )
    
    if st.button("💾 Save My Financial Profile", type="primary"):
        st.session_state.financial_profile = {
            'monthly_income': monthly_income,
            'age': age,
            'employment_status': employment_status,
            'living_situation': living_situation,
            'risk_tolerance': risk_tolerance,
            'primary_goal': primary_goal
        }
        
        # Generate budget plan
        budget_suggestions = st.session_state.agent.get_budget_suggestions(monthly_income, age)
        st.session_state.budget_plan = BudgetPlan(
            monthly_income=monthly_income,
            needs_percentage=budget_suggestions['needs'],
            wants_percentage=budget_suggestions['wants'],
            savings_percentage=budget_suggestions['savings']
        )
        
        st.success("🎉 Profile saved! Your personalized financial plan is ready!")
        st.rerun()

# =============================================================================
# PERSONALIZED BUDGET BREAKDOWN
# =============================================================================

if st.session_state.budget_plan:
    st.markdown("## 💎 Your Personalized Gen Z Budget Structure")
    
    budget = st.session_state.budget_plan
    profile = st.session_state.financial_profile
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="budget-card">
            <h3>💰 Monthly Income</h3>
            <h2>{format_currency(budget.monthly_income, 0)}</h2>
            <p>Your total hustle</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="budget-card">
            <h3>🏠 Needs ({budget.needs_percentage}%)</h3>
            <h2>{format_currency(budget.needs_amount, 0)}</h2>
            <p>Rent, food, transport</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="budget-card">
            <h3>✨ Wants ({budget.wants_percentage}%)</h3>
            <h2>{format_currency(budget.wants_amount, 0)}</h2>
            <p>Fun, joy, self-care</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="budget-card">
            <h3>📈 Savings ({budget.savings_percentage}%)</h3>
            <h2>{format_currency(budget.savings_amount, 0)}</h2>
            <p>Future you fund</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Budget visualization
    st.markdown("### 📊 Your Budget Breakdown")
    
    budget_data = {
        'Category': ['🏠 Needs', '✨ Wants', '📈 Savings'],
        'Amount': [budget.needs_amount, budget.wants_amount, budget.savings_amount],
        'Percentage': [budget.needs_percentage, budget.wants_percentage, budget.savings_percentage]
    }
    
    fig_budget = px.pie(
        values=budget_data['Amount'],
        names=budget_data['Category'],
        title="💫 Your Money Allocation",
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
    fig_budget.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14)
    )
    st.plotly_chart(fig_budget, use_container_width=True)

# =============================================================================
# INVESTMENT SUGGESTIONS
# =============================================================================

if st.session_state.financial_profile:
    st.markdown("## 📈 Gen Z Investment Roadmap")
    
    profile = st.session_state.financial_profile
    risk_level = profile['risk_tolerance'].split(' ')[0].lower()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Recommended Investments")
        
        if risk_level == "conservative":
            investments = st.session_state.agent.investment_suggestions["low_risk"]
        elif risk_level == "moderate":
            investments = st.session_state.agent.investment_suggestions["medium_risk"]
        else:
            investments = st.session_state.agent.investment_suggestions["high_risk"]
        
        for inv in investments:
            st.markdown(f"""
            <div class="investment-card">
                <h4>{inv['name']}</h4>
                <p>{inv['desc']}</p>
                <p><strong>Risk:</strong> {inv['risk']} | <strong>Expected Return:</strong> {inv['return']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Your Financial Goals Roadmap")
        
        roadmap = st.session_state.agent.get_investment_roadmap(
            profile['age'], 
            profile['monthly_income'],
            risk_level
        )
        
        for item in roadmap:
            progress = min(100, random.randint(10, 80))  # Simulated progress
            st.markdown(f"""
            <div class="financial-goal-card">
                <h4>Priority {item['priority']}: {item['goal']}</h4>
                <p>{item['description']}</p>
                <p><strong>Target:</strong> {format_currency(item['target'], 0)}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
                <p><small>{progress}% Complete</small></p>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# GEN Z FINANCIAL SURVIVAL GUIDE
# =============================================================================

st.markdown("## 🔥 Gen Z Financial Survival Guide")

tab1, tab2, tab3, tab4 = st.tabs(["💰 Budgeting Hacks", "📈 Investment 101", "🚨 Emergency Fund", "💼 Side Hustle Tips"])

with tab1:
    st.markdown("### 💡 Budgeting That Actually Works")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 The 50/30/20 Rule (Gen Z Edition):**
        - 50% Needs: Rent, groceries, transport, phone
        - 30% Wants: Entertainment, dining out, shopping
        - 20% Savings: Emergency fund + investments
        
        **📱 Apps That Slay:**
        - Mint (free budgeting)
        - YNAB (You Need A Budget)
        - PocketGuard (spending limits)
        - Goodbudget (envelope method)
        """)
    
    with col2:
        st.markdown("""
        **💫 Budgeting Hacks:**
        - Automate savings (pay yourself first!)
        - Use the 24-hour rule for big purchases
        - Track spending with photos of receipts
        - Set up separate accounts for different goals
        - Use cash for discretionary spending
        - Review and adjust monthly (not daily!)
        """)

with tab2:
    st.markdown("### 📊 Investing Made Simple")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🚀 Start Here (Beginner-Friendly):**
        - High-yield savings account (2-4% return)
        - Index funds (S&P 500) - diversified & low fees
        - Target-date funds - set it & forget it
        - Employer 401(k) match - FREE MONEY!
        
        **📱 Investment Apps:**
        - Robinhood (commission-free trading)
        - Acorns (micro-investing with spare change)
        - Stash ($5 minimum investment)
        - M1 Finance (automated portfolios)
        """)
    
    with col2:
        st.markdown("""
        **⚡ Power Moves:**
        - Start with small amounts ($25-50/month)
        - Diversify (don't put all eggs in one basket)
        - Think long-term (10+ years)
        - Don't panic sell during market dips
        - Reinvest dividends automatically
        - Learn about compound interest - it's magic! ✨
        """)

with tab3:
    st.markdown("### 🚨 Emergency Fund Essentials")
    
    emergency_target = st.session_state.budget_plan.monthly_income * 6 if st.session_state.budget_plan else 30000
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **🎯 Your Emergency Fund Goal: {format_currency(emergency_target, 0)}**
        
        **Why You Need It:**
        - Job loss protection
        - Medical emergencies
        - Car repairs
        - Unexpected expenses
        - Mental peace (priceless!)
        
        **Where to Keep It:**
        - High-yield savings account
        - Money market account
        - Short-term CDs
        """)
    
    with col2:
        st.markdown("""
        **🔥 Building Strategy:**
        - Start with PKR 1,000 (any amount is better than zero!)
        - Automate transfers (PKR 2,000-5,000/month)
        - Use windfalls (tax refunds, bonuses)
        - Sell stuff you don't need
        - Side hustle specifically for emergency fund
        - Celebrate milestones! 🎉
        """)

with tab4:
    st.markdown("### 💼 Side Hustle Game Strong")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔥 Hot Side Hustles for 2024:**
        - Content creation (TikTok, YouTube, Instagram)
        - Freelance writing/graphic design
        - Online tutoring
        - Virtual assistant
        - Social media management
        - Photography/videography
        - Food delivery (Uber Eats, DoorDash)
        - Pet sitting/dog walking
        """)
    
    with col2:
        st.markdown("""
        **💡 Side Hustle Success Tips:**
        - Start with skills you already have
        - Set clear income goals
        - Track time vs. money earned
        - Separate business & personal finances
        - Save taxes (15-30% of earnings)
        - Scale what works, drop what doesn't
        - Network like crazy! 🤝
        """)

# =============================================================================
# HERO VIBE CHECK SECTION (Gen Z Hero Feature)
# =============================================================================

st.markdown("""
<div style='
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 1rem 2rem 1rem;
    border-radius: 25px;
    margin-bottom: 2.5rem;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(102,126,234,0.15);
'>
    <h1 style='font-size: 2.8rem; margin-bottom: 0.5rem;'>🌈 Daily Vibe Check</h1>
    <p style='font-size: 1.3rem; margin-bottom: 1.5rem; font-style: italic;'>How are you feeling about your money today?</p>
</div>
""", unsafe_allow_html=True)

# Large, central vibe selector and sliders
vibe_col, stress_col, conf_col = st.columns([2, 1, 1])

with vibe_col:
    # Ensure current_vibe is always a valid VibeType
    try:
        vibe_index = list(VibeType).index(st.session_state.current_vibe)
    except Exception:
        st.session_state.current_vibe = VibeType.CHILL
        vibe_index = list(VibeType).index(VibeType.CHILL)
    current_vibe = st.selectbox(
        "",
        options=list(VibeType),
        format_func=lambda x: f"{x.value} {x.name.title()}",
        index=vibe_index,
        key="hero_vibe_selectbox"
    )
    
    # Check if vibe changed and trigger emoji pop-out effect
    if 'previous_vibe' not in st.session_state:
        st.session_state.previous_vibe = current_vibe
    
    if current_vibe != st.session_state.previous_vibe:
        # Trigger emoji pop-out effect instead of balloons
        st.markdown(f"""
        <div id="emoji-popup" style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 8rem;
            z-index: 9999;
            animation: emojiPop 2s ease-out forwards;
            pointer-events: none;
        ">
            {current_vibe.value}
        </div>
        <style>
        @keyframes emojiPop {{
            0% {{ 
                opacity: 0; 
                transform: translate(-50%, -50%) scale(0.1); 
            }}
            50% {{ 
                opacity: 1; 
                transform: translate(-50%, -50%) scale(1.2); 
            }}
            100% {{ 
                opacity: 0; 
                transform: translate(-50%, -50%) scale(0.8) translateY(-100px); 
            }}
        }}
        </style>
        <script>
        setTimeout(function() {{
            var popup = document.getElementById('emoji-popup');
            if (popup) {{
                popup.remove();
            }}
        }}, 2000);
        </script>
        """, unsafe_allow_html=True)
        st.session_state.previous_vibe = current_vibe
    
    # =============================================================================
    # DYNAMIC AURA SYSTEM - CHANGES WEBSITE COLORS BASED ON MOOD
    # =============================================================================
    
    # Define mood-based color schemes and auras
    vibe_auras = {
        VibeType.STRESSED: {
            "primary": "#FF6B6B",
            "secondary": "#FF8E8E", 
            "accent": "#FFB3B3",
            "bg_start": "#FF4757",
            "bg_end": "#FF6B6B",
            "card_bg": "linear-gradient(135deg, #FF6B6B 0%, #FF4757 100%)",
            "text_glow": "#FF6B6B",
            "particle_color": "#FF8E8E",
            "aura_name": "Stress Relief Aura",
            "description": "Calming reds to acknowledge stress while promoting healing"
        },
        VibeType.CONFIDENT: {
            "primary": "#4ECDC4",
            "secondary": "#45B7D1",
            "accent": "#96CEB4",
            "bg_start": "#667eea",
            "bg_end": "#764ba2",
            "card_bg": "linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%)",
            "text_glow": "#4ECDC4",
            "particle_color": "#45B7D1",
            "aura_name": "Confidence Power Aura",
            "description": "Bold blues and teals radiating success energy"
        },
        VibeType.CONFUSED: {
            "primary": "#A8A8A8",
            "secondary": "#B8B8B8",
            "accent": "#D3D3D3",
            "bg_start": "#74b9ff",
            "bg_end": "#0984e3",
            "card_bg": "linear-gradient(135deg, #A8A8A8 0%, #74b9ff 100%)",
            "text_glow": "#74b9ff",
            "particle_color": "#B8B8B8",
            "aura_name": "Clarity Seeking Aura",
            "description": "Cool grays and blues to promote mental clarity"
        },
        VibeType.EXCITED: {
            "primary": "#FFD93D",
            "secondary": "#FF6B35",
            "accent": "#FF8B94",
            "bg_start": "#FFD93D",
            "bg_end": "#FF6B35",
            "card_bg": "linear-gradient(135deg, #FFD93D 0%, #FF6B35 100%)",
            "text_glow": "#FFD93D",
            "particle_color": "#FF8B94",
            "aura_name": "High Energy Excitement Aura",
            "description": "Vibrant yellows and oranges bursting with excitement"
        },
        VibeType.CHILL: {
            "primary": "#96CEB4",
            "secondary": "#FFEAA7",
            "accent": "#DDA0DD",
            "bg_start": "#96CEB4",
            "bg_end": "#FFEAA7",
            "card_bg": "linear-gradient(135deg, #96CEB4 0%, #FFEAA7 100%)",
            "text_glow": "#96CEB4",
            "particle_color": "#DDA0DD",
            "aura_name": "Zen Chill Aura",
            "description": "Peaceful greens and soft yellows for ultimate relaxation"
        },
        VibeType.GUILTY: {
            "primary": "#E17055",
            "secondary": "#FDCB6E",
            "accent": "#FD79A8",
            "bg_start": "#E17055",
            "bg_end": "#FDCB6E",
            "card_bg": "linear-gradient(135deg, #E17055 0%, #FDCB6E 100%)",
            "text_glow": "#E17055",
            "particle_color": "#FD79A8",
            "aura_name": "Self-Compassion Aura",
            "description": "Warm oranges and peaches promoting self-forgiveness"
        }
    }
    
    current_aura = vibe_auras[current_vibe]
    
    # Apply dynamic aura styling
    st.markdown(f"""
    <style>
    /* DYNAMIC AURA SYSTEM - MOOD-RESPONSIVE DESIGN */
    
    :root {{
        --aura-primary: {current_aura['primary']};
        --aura-secondary: {current_aura['secondary']};
        --aura-accent: {current_aura['accent']};
        --aura-glow: {current_aura['text_glow']};
    }}
    
    /* Animated background aura effect */
    .stApp {{
        background: linear-gradient(45deg, {current_aura['bg_start']}22, {current_aura['bg_end']}22);
        animation: auraShift 8s ease-in-out infinite alternate;
    }}
    
    @keyframes auraShift {{
        0% {{ background: linear-gradient(45deg, {current_aura['bg_start']}15, {current_aura['bg_end']}15); }}
        100% {{ background: linear-gradient(135deg, {current_aura['bg_end']}15, {current_aura['bg_start']}15); }}
    }}
    
    /* Dynamic card styling based on mood */
    .main-header {{
        background: {current_aura['card_bg']} !important;
        box-shadow: 0 10px 30px {current_aura['primary']}40 !important;
        animation: cardGlow 3s ease-in-out infinite alternate;
    }}
    
    @keyframes cardGlow {{
        0% {{ box-shadow: 0 10px 30px {current_aura['primary']}40; }}
        100% {{ box-shadow: 0 15px 40px {current_aura['primary']}60, 0 0 20px {current_aura['text_glow']}30; }}
    }}
    
    .vibe-card {{
        background: {current_aura['card_bg']} !important;
        box-shadow: 0 8px 25px {current_aura['primary']}35 !important;
    }}
    
    .money-card {{
        background: {current_aura['card_bg']} !important;
        border: 2px solid {current_aura['accent']}60;
        box-shadow: 0 5px 20px {current_aura['primary']}30;
    }}
    
    .budget-card {{
        background: linear-gradient(135deg, {current_aura['accent']}80, {current_aura['secondary']}60) !important;
        border: 1px solid {current_aura['primary']}40;
    }}
    
    .investment-card {{
        background: linear-gradient(135deg, {current_aura['secondary']}70, {current_aura['accent']}50) !important;
        border-left: 4px solid {current_aura['primary']};
    }}
    
    .financial-goal-card {{
        background: {current_aura['card_bg']} !important;
        box-shadow: 0 6px 20px {current_aura['primary']}35;
    }}
    
    /* Mood-responsive text effects */
    h1, h2, h3 {{
        text-shadow: 0 0 10px {current_aura['text_glow']}50 !important;
        animation: textGlow 2s ease-in-out infinite alternate;
    }}
    
    @keyframes textGlow {{
        0% {{ text-shadow: 0 0 10px {current_aura['text_glow']}50; }}
        100% {{ text-shadow: 0 0 15px {current_aura['text_glow']}70, 0 0 25px {current_aura['text_glow']}30; }}
    }}
    
    /* Button styling matches mood */
    .stButton > button {{
        background: {current_aura['card_bg']} !important;
        border: 2px solid {current_aura['primary']} !important;
        box-shadow: 0 4px 15px {current_aura['primary']}40 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 8px 25px {current_aura['primary']}60, 0 0 20px {current_aura['text_glow']}50 !important;
        transform: translateY(-3px) !important;
    }}
    
    /* Progress bars match the aura */
    .progress-fill {{
        background: {current_aura['card_bg']} !important;
        box-shadow: inset 0 0 10px {current_aura['text_glow']}30;
    }}
    
    /* Sidebar matches mood */
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, {current_aura['primary']}, {current_aura['secondary']}) !important;
    }}
    
    /* Floating particles for extra aura effect */
    .aura-particles {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }}
    
    .particle {{
        position: absolute;
        width: 4px;
        height: 4px;
        background: {current_aura['particle_color']};
        border-radius: 50%;
        animation: float 15s infinite linear;
        opacity: 0.6;
    }}
    
    @keyframes float {{
        0% {{ transform: translateY(100vh) rotate(0deg); }}
        100% {{ transform: translateY(-100px) rotate(360deg); }}
    }}
    
    /* Create multiple particles with different delays */
    .particle:nth-child(1) {{ left: 10%; animation-delay: 0s; }}
    .particle:nth-child(2) {{ left: 20%; animation-delay: 2s; }}
    .particle:nth-child(3) {{ left: 30%; animation-delay: 4s; }}
    .particle:nth-child(4) {{ left: 40%; animation-delay: 6s; }}
    .particle:nth-child(5) {{ left: 50%; animation-delay: 8s; }}
    .particle:nth-child(6) {{ left: 60%; animation-delay: 10s; }}
    .particle:nth-child(7) {{ left: 70%; animation-delay: 12s; }}
    .particle:nth-child(8) {{ left: 80%; animation-delay: 14s; }}
    .particle:nth-child(9) {{ left: 90%; animation-delay: 16s; }}
    
    </style>
    
    <!-- Floating particles for aura effect -->
    <div class="aura-particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    
    <!-- Aura notification -->
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        background: {current_aura['card_bg']};
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        font-size: 0.9em;
        font-weight: 600;
        box-shadow: 0 8px 25px {current_aura['primary']}50;
        z-index: 1000;
        animation: auraNotification 4s ease-out;
    ">
        ✨ {current_aura['aura_name']} Activated ✨
    </div>
    
    @keyframes auraNotification {{
        0% {{ opacity: 0; transform: translateX(100px); }}
        20% {{ opacity: 1; transform: translateX(0); }}
        80% {{ opacity: 1; transform: translateX(0); }}
        100% {{ opacity: 0; transform: translateX(100px); }}
    }}
    
    """, unsafe_allow_html=True)
    
    st.session_state.current_vibe = current_vibe

with stress_col:
    stress_level = st.slider("Money stress level", 1, 10, 5, key="hero_stress_slider")

with conf_col:
    confidence_level = st.slider("Financial confidence", 1, 10, 6, key="hero_conf_slider")

# AI Response based on vibe (big, animated card) with dynamic aura
current_aura = vibe_auras[current_vibe]
vibe_response = st.session_state.agent.get_vibe_response(current_vibe)

# Enhanced response card with aura integration
st.markdown(f"""
<div style='
    background: {current_aura['card_bg']};
    padding: 2rem;
    border-radius: 20px;
    margin: 1.5rem 0 2.5rem 0;
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    box-shadow: 0 10px 30px {current_aura['primary']}40, 0 0 40px {current_aura['text_glow']}20;
    transition: all 0.3s;
    animation: heroFadeIn 1s, auraGlow 3s ease-in-out infinite alternate;
    border: 2px solid {current_aura['accent']}60;
'>
    <span style='font-size: 2.5rem; margin-right: 0.5rem; text-shadow: 0 0 15px {current_aura['text_glow']};'>{{current_vibe.value}}</span>
    {{vibe_response}}
    
    <div style='
        margin-top: 1rem; 
        font-size: 1rem; 
        opacity: 0.9; 
        font-style: italic;
        background: rgba(255,255,255,0.1); 
        padding: 0.8rem; 
        border-radius: 10px;
        border-left: 4px solid {current_aura['accent']};
    '>
        <strong>🌟 Current Aura:</strong> {current_aura['aura_name']}<br>
        <small>{current_aura['description']}</small>
    </div>
</div>

<style>
@keyframes heroFadeIn {{
    from {{ opacity: 0; transform: translateY(0); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes auraGlow {{
    0% {{ 
        box-shadow: 0 10px 30px {current_aura['primary']}40, 0 0 40px {current_aura['text_glow']}20;
        transform: scale(1);
    }}
    100% {{ 
        box-shadow: 0 15px 40px {current_aura['primary']}60, 0 0 60px {current_aura['text_glow']}40;
        transform: scale(1.02);
    }}
}}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# ENHANCED MONEY DASHBOARD
# =============================================================================

st.markdown("## 💰 Your Money Mood Board")

# Safe calculations with error handling
def calculate_dashboard_metrics():
    try:
        transactions = st.session_state.transactions or []
        total_spent = sum(t.amount for t in transactions if hasattr(t, 'amount') and t.amount)
        avg_daily = handle_calculation_error(lambda: total_spent / 7, 0)
        joy_spending = sum(t.amount for t in transactions if hasattr(t, 'category') and t.category == SpendingCategory.JOY and t.amount)
        essential_spending = sum(t.amount for t in transactions if hasattr(t, 'category') and t.category == SpendingCategory.ESSENTIAL and t.amount)
        return total_spent, avg_daily, joy_spending, essential_spending
    except Exception as e:
        logger.error(f"Dashboard calculation error: {str(e)}")
        st.session_state.error_count += 1
        st.session_state.last_error = str(e)
        return 0, 0, 0, 0

total_spent, avg_daily, joy_spending, essential_spending = calculate_dashboard_metrics()

# Get monthly_income safely
monthly_income = st.session_state.financial_profile.get('monthly_income', 0) if st.session_state.financial_profile else 0
current_savings = st.session_state.financial_profile.get('current_savings', 0) if st.session_state.financial_profile else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="money-card">
        <h3>💸 Total Spent</h3>
        <h2>{format_currency(total_spent, 2)}</h2>
        <p>Last 7 days</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="money-card">
        <h3>📅 Daily Average</h3>
        <h2>{format_currency(avg_daily, 2)}</h2>
        <p>Per day</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    joy_ratio = (joy_spending / total_spent * 100) if total_spent > 0 else 0
    st.markdown(f"""
    <div class="money-card">
        <h3>😊 Joy Ratio</h3>
        <h2>{joy_ratio:.1f}%</h2>
        <p>Happiness spending</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if monthly_income > 0:
        monthly_projected = total_spent * 4.33
        budget_remaining = monthly_income - monthly_projected
        st.markdown(f"""
        <div class="money-card">
            <h3>💰 Budget Left</h3>
            <h2>{format_currency(budget_remaining, 0)}</h2>
            <p>This month</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="money-card">
            <h3>✨ Joy Spending</h3>
            <h2>{format_currency(joy_spending, 2)}</h2>
            <p>Self-care investments</p>
        </div>
        """, unsafe_allow_html=True)

# Add a fifth column for savings/essentials if needed
col5 = None
if current_savings > 0 or essential_spending > 0:
    cols = st.columns(5)
    col5 = cols[4]
    with col5:
        if current_savings > 0:
            savings_growth = current_savings
            st.markdown(f"""
            <div class="money-card">
                <h3>📈 Savings</h3>
                <h2>{format_currency(savings_growth, 0)}</h2>
                <p>Total saved</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="money-card">
                <h3>🏠 Essentials</h3>
                <h2>{format_currency(essential_spending, 2)}</h2>
                <p>Responsible spending</p>
            </div>
            """, unsafe_allow_html=True)

# Budget vs Reality Check
if monthly_income > 0:
    st.markdown("### 📊 Budget vs Reality Check")
    # Remove planner reference and use budget_plan if available
    if st.session_state.budget_plan:
        budget = {
            'needs': st.session_state.budget_plan.needs_amount,
            'wants': st.session_state.budget_plan.wants_amount
        }
    else:
        budget = {'needs': 0, 'wants': 0}

    current_month_spending = total_spent * 4.33
    needs_budget = budget['needs']
    wants_budget = budget['wants']

    current_needs = essential_spending * 4.33
    current_wants = joy_spending * 4.33

    col1, col2, col3 = st.columns(3)

    with col1:
        needs_progress = (current_needs / needs_budget * 100) if needs_budget > 0 else 0
        st.markdown(f"**🏠 Needs: {format_currency(current_needs, 0)} / {format_currency(needs_budget, 0)}**")
        st.progress(min(needs_progress / 100, 1.0))
        if needs_progress > 100:
            st.markdown('<div class="warning-card">⚠️ Over budget on needs!</div>', unsafe_allow_html=True)

    with col2:
        wants_progress = (current_wants / wants_budget * 100) if wants_budget > 0 else 0
        st.markdown(f"**✨ Wants: {format_currency(current_wants, 0)} / {format_currency(wants_budget, 0)}**")
        st.progress(min(wants_progress / 100, 1.0))
        if wants_progress > 100:
            st.markdown('<div class="warning-card">⚠️ Over budget on wants!</div>', unsafe_allow_html=True)

    with col3:
        total_budget = needs_budget + wants_budget
        total_spent_month = current_needs + current_wants
        overall_progress = (total_spent_month / total_budget * 100) if total_budget > 0 else 0
        st.markdown(f"**💰 Overall: {format_currency(total_spent_month, 0)} / {format_currency(total_budget, 0)}**")
        st.progress(min(overall_progress / 100, 1.0))
        if overall_progress < 80:
            st.markdown('<div class="success-card">🎉 Under budget! Great job!</div>', unsafe_allow_html=True)

# =============================================================================
# TRANSACTION INPUT & INTERACTIVE FEATURES
# =============================================================================

st.markdown("## 💳 Add New Transaction")

# Transaction input form with error handling
with st.expander("➕ Add a New Transaction", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_amount = st.number_input("💰 Amount", min_value=0.01, value=10.0, step=0.5)
        new_description = st.text_input("📝 Description", placeholder="What did you spend on?")
    
    with col2:
        new_category = st.selectbox("📂 Category", list(SpendingCategory))
        new_merchant = st.text_input("🏪 Merchant", placeholder="Where did you spend?")
    
    with col3:
        new_vibe_impact = st.slider("😊 Vibe Impact", -1.0, 1.0, 0.0, 0.1, 
                                   help="How did this purchase make you feel?")
        
        if st.button("✅ Add Transaction", type="primary", use_container_width=True):
            try:
                if new_description.strip():
                    new_transaction = Transaction(
                        date=datetime.now(),
                        amount=float(new_amount),
                        description=new_description.strip(),
                        category=new_category,
                        merchant=new_merchant.strip(),
                        vibe_impact=float(new_vibe_impact)
                    )
                    st.session_state.transactions.append(new_transaction)
                    st.success(f"✅ Added: {new_description} - {format_currency(new_amount)}")
                    st.rerun()
                else:
                    st.warning("Please enter a description for your transaction!")
            except Exception as e:
                st.error(f"Error adding transaction: {str(e)}")
                st.session_state.error_count += 1
                st.session_state.last_error = str(e)

# =============================================================================
# TRANSACTION LOG & DISPLAY
# =============================================================================

st.markdown("## 🧾 Recent Spending Tea ☕")

# Safe transaction display with error handling
def create_transaction_dataframe():
    try:
        transactions = st.session_state.transactions or []
        if not transactions:
            return pd.DataFrame({'Message': ['No transactions yet! Add your first transaction above. 💸']})
        
        transaction_data = []
        for t in sorted(transactions, key=lambda x: getattr(x, 'date', datetime.now()), reverse=True):
            try:
                transaction_data.append({
                    'Date': getattr(t, 'date', datetime.now()).strftime('%m/%d'),
                    'Vibe': getattr(t, 'category', SpendingCategory.ESSENTIAL).value,
                    'Amount': format_currency(getattr(t, 'amount', 0)),
                    'Description': getattr(t, 'description', 'Unknown'),
                    'Merchant': getattr(t, 'merchant', 'Unknown'),
                    'Mood Impact': '😊' if getattr(t, 'vibe_impact', 0) > 0 else '😐' if getattr(t, 'vibe_impact', 0) == 0 else '😔'
                })
            except Exception as e:
                logger.warning(f"Error processing transaction: {str(e)}")
                continue
        
        return pd.DataFrame(transaction_data)
    except Exception as e:
        logger.error(f"Error creating transaction dataframe: {str(e)}")
        st.session_state.error_count += 1
        st.session_state.last_error = str(e)
        return pd.DataFrame({'Error': ['Unable to load transactions. Please try refreshing.']})

df_transactions = create_transaction_dataframe()
st.dataframe(df_transactions, use_container_width=True)

# Transaction analytics
if len(st.session_state.transactions) > 0:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            avg_transaction = handle_calculation_error(
                lambda: sum(t.amount for t in st.session_state.transactions) / len(st.session_state.transactions),
                0
            )
            st.metric("💰 Avg Transaction", format_currency(avg_transaction))
        except:
            st.metric("💰 Avg Transaction", "N/A")
    
    with col2:
        try:
            positive_vibes = len([t for t in st.session_state.transactions if getattr(t, 'vibe_impact', 0) > 0])
            st.metric("😊 Positive Purchases", f"{positive_vibes}")
        except:
            st.metric("😊 Positive Purchases", "N/A")
    
    with col3:
        try:
            most_category = max(SpendingCategory, key=lambda cat: len([t for t in st.session_state.transactions if getattr(t, 'category', None) == cat]))
            st.metric("🔥 Top Category", most_category.value)
        except:
            st.metric("🔥 Top Category", "N/A")

# =============================================================================
# ENHANCED SALARY INPUT & FINANCIAL PLANNING CALCULATOR
# =============================================================================

st.markdown("## 💰 Complete Financial Planning Calculator")

st.markdown("""
<div class="financial-setup-card">
    <h3>💸 Enter Your Financial Details</h3>
    <p>Let's create your personalized Gen Z survival & slay financial blueprint!</p>
</div>
""", unsafe_allow_html=True)

# Main salary input section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💵 Income Details")
    monthly_salary = st.number_input(
        "Monthly Salary/Income (After Tax)",
        min_value=0.0,
        value=4500.0,
        step=100.0,
        help="Your take-home pay per month"
    )
    
    additional_income = st.number_input(
        "Side Hustle/Additional Income",
        min_value=0.0,
        value=0.0,
        step=50.0,
        help="Freelance, part-time, passive income"
    )
    
    total_monthly_income = monthly_salary + additional_income
    annual_income = total_monthly_income * 12

with col2:
    st.markdown("### 🎯 Current Financial Status")
    current_debt = st.number_input(
        "Total Debt Amount",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Credit cards, student loans, personal loans"
    )
    
    current_savings_amount = st.number_input(
        "Current Savings Balance",
        min_value=0.0,
        value=1000.0,
        step=100.0,
        help="Emergency fund + other savings accounts"
    )
    
    monthly_debt_payment = st.number_input(
        "Current Monthly Debt Payments",
        min_value=0.0,
        value=0.0,
        step=25.0,
        help="Minimum payments on all debts"
    )

with col3:
    st.markdown("### 🚀 Your Financial Goals")
    financial_priority = st.selectbox(
        "Primary Financial Priority",
        [
            "🛡️ Build Emergency Fund",
            "💳 Pay Off Debt",
            "📈 Start Investing",
            "🏠 Save for Big Purchase",
            "👑 Maximize Wealth Building"
        ]
    )
    
    lifestyle_mode = st.selectbox(
        "Current Lifestyle Mode",
        [
            "😩 Survival Mode (Minimize expenses)",
            "😌 Comfort Mode (Balanced approach)", 
            "👑 Slay Mode (Aggressive wealth building)"
        ]
    )
    
    investment_risk = st.selectbox(
        "Investment Risk Tolerance",
        ["Conservative (Safety first)", "Moderate (Balanced)", "Aggressive (High growth)"]
    )

# =============================================================================
# ADVANCED FINANCIAL BREAKDOWN CALCULATOR
# =============================================================================

if total_monthly_income > 0:
    st.markdown("## 📊 Your Personalized Financial Blueprint")
    
    # Determine budget allocation based on lifestyle mode
    if "Survival" in lifestyle_mode:
        needs_percent = 70
        wants_percent = 15
        savings_percent = 15
        mode_emoji = "🛡️"
        mode_description = "Focus on stability and emergency fund"
    elif "Comfort" in lifestyle_mode:
        needs_percent = 50
        wants_percent = 30
        savings_percent = 20
        mode_emoji = "😌"
        mode_description = "Balanced living with room for fun"
    else:  # Slay mode
        needs_percent = 45
        wants_percent = 25
        savings_percent = 30
        mode_emoji = "👑"
        mode_description = "Aggressive wealth building for financial freedom"
    
    # Calculate allocations
    needs_amount = total_monthly_income * (needs_percent / 100)
    wants_amount = total_monthly_income * (wants_percent / 100)
    savings_amount = total_monthly_income * (savings_percent / 100)
    
    # Adjust for existing debt payments
    adjusted_savings = max(0, savings_amount - monthly_debt_payment)
    debt_payoff_extra = savings_amount - adjusted_savings
    
    # Display budget breakdown
    st.markdown(f"""
    <div class="main-header">
        <h2>{mode_emoji} {lifestyle_mode.split('(')[0]} Budget Breakdown</h2>
        <p><em>{mode_description}</em></p>
        <h3>Total Monthly Income: {format_currency(total_monthly_income, 2)}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="survival-card">
            <h3>🏠 NEEDS ({needs_percent}%)</h3>
            <h2>{format_currency(needs_amount, 0)}</h2>
            <div style="font-size: 0.9em; margin-top: 10px;">
                <strong>Includes:</strong><br>
                • Rent/Mortgage<br>
                • Groceries & Utilities<br>
                • Transportation<br>
                • Insurance & Phone<br>
                • Minimum Debt Payments
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="comfort-card">
            <h3>✨ WANTS ({wants_percent}%)</h3>
            <h2>{format_currency(wants_amount, 0)}</h2>
            <div style="font-size: 0.9em; margin-top: 10px;">
                <strong>Includes:</strong><br>
                • Dining Out & Entertainment<br>
                • Shopping & Hobbies<br>
                • Subscriptions<br>
                • Travel & Fun<br>
                • Personal Care
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="slay-card">
            <h3>💰 SAVINGS ({savings_percent}%)</h3>
            <h2>{format_currency(adjusted_savings, 0)}</h2>
            <div style="font-size: 0.9em; margin-top: 10px;">
                <strong>Breakdown:</strong><br>
                • Emergency Fund<br>
                • Investment Accounts<br>
                • Goal Savings<br>
                • Extra Debt Payment<br>
                • Future Planning
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if monthly_debt_payment > 0:
            total_debt_focus = monthly_debt_payment + debt_payoff_extra
            st.markdown(f"""
            <div class="investment-card">
                <h3>💳 DEBT PAYOFF</h3>
                <h2>{format_currency(total_debt_focus, 0)}</h2>
                <div style="font-size: 0.9em; margin-top: 10px;">
                    <strong>Strategy:</strong><br>
                    • Minimum: {format_currency(monthly_debt_payment, 0)}<br>
                    • Extra: {format_currency(debt_payoff_extra, 0)}<br>
                    • Total Focus<br>
                    • Avalanche Method
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="investment-card">
                <h3>🚀 BONUS POWER</h3>
                <h2>{format_currency(adjusted_savings, 0)}</h2>
                <div style="font-size: 0.9em; margin-top: 10px;">
                    <strong>Opportunity:</strong><br>
                    • Full Savings Potential<br>
                    • Investment Ready<br>
                    • Wealth Building<br>
                    • Financial Freedom
                </div>
            </div>
            """, unsafe_allow_html=True)

    # =============================================================================
    # EMERGENCY FUND CALCULATOR
    # =============================================================================
    
    st.markdown("### 🛡️ Emergency Fund Strategy")
    
    emergency_months = st.slider("Target Emergency Fund (Months of Expenses)", 3, 12, 6)
    emergency_target = needs_amount * emergency_months
    emergency_progress = (current_savings_amount / emergency_target * 100) if emergency_target > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="goal-tracker">
            <h4>🎯 Emergency Fund Goal</h4>
            <h2>{format_currency(emergency_target, 0)}</h2>
            <p>{emergency_months} months of expenses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="goal-tracker">
            <h4>💰 Current Progress</h4>
            <h2>{format_currency(current_savings_amount, 0)}</h2>
            <p>{emergency_progress:.1f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        months_to_goal = max(0, (emergency_target - current_savings_amount) / (adjusted_savings * 0.5)) if adjusted_savings > 0 else 0
        st.markdown(f"""
        <div class="goal-tracker">
            <h4>⏰ Time to Goal</h4>
            <h2>{months_to_goal:.1f} months</h2>
            <p>At 50% savings allocation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {min(emergency_progress, 100)}%;">
            Emergency Fund: {emergency_progress:.1f}% Complete
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =============================================================================
    # INVESTMENT ALLOCATION STRATEGY
    # =============================================================================
    
    st.markdown("### 📈 Investment Allocation Strategy")
    
    # Calculate investment amount (portion of savings after emergency fund priority)
    emergency_monthly_need = max(0, (emergency_target - current_savings_amount) / 12)
    available_for_investment = max(0, adjusted_savings - emergency_monthly_need)
    
    if available_for_investment > 0:
        # Age-based investment allocation
        user_age = st.slider("Your Age", 18, 35, 25)
        
        # Determine allocation based on age and risk tolerance
        if "Conservative" in investment_risk:
            stock_percent = max(20, 60 - user_age)
            bond_percent = min(50, 40 + (user_age - 20))
        elif "Aggressive" in investment_risk:
            stock_percent = min(95, 80 + (35 - user_age))
            bond_percent = max(5, 20 - (35 - user_age))
        else:  # Moderate
            stock_percent = max(40, 70 - (user_age - 20))
            bond_percent = min(40, 30 + (user_age - 20))
        
        cash_percent = 100 - stock_percent - bond_percent
        
        # Calculate dollar amounts
        stock_amount = available_for_investment * (stock_percent / 100)
        bond_amount = available_for_investment * (bond_percent / 100)
        cash_amount = available_for_investment * (cash_percent / 100)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="investment-card">
                <h4>📊 Total Monthly Investment</h4>
                <h2>{format_currency(available_for_investment, 0)}</h2>
                <p>Available after emergency fund</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="investment-card">
                <h4>📈 Stocks/ETFs ({stock_percent}%)</h4>
                <h2>{format_currency(stock_amount, 0)}</h2>
                <p>VTI, VXUS, Growth funds</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="investment-card">
                <h4>🏛️ Bonds ({bond_percent}%)</h4>
                <h2>{format_currency(bond_amount, 0)}</h2>
                <p>BND, Treasury bonds</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="investment-card">
                <h4>💵 Cash/HYSA ({cash_percent}%)</h4>
                <h2>{format_currency(cash_amount, 0)}</h2>
                <p>High-yield savings, CDs</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Specific investment recommendations
        st.markdown("#### 🎯 Specific Investment Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="financial-tip">
                <h4>🚀 Gen Z Investment Essentials</h4>
                <strong>Core Holdings:</strong><br>
                • VTI (Total Stock Market) - 40%<br>
                • VXUS (International) - 20%<br>
                • BND (Total Bond Market) - 20%<br>
                • HYSA (Emergency Buffer) - 20%<br><br>
                <strong>Advanced Options:</strong><br>
                • QQQ (Tech Growth)<br>
                • SCHD (Dividend Growth)<br>
                • REITs (Real Estate)<br>
                • Small allocation to crypto (5% max)
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="financial-tip">
                <h4>💡 Investment Platform Suggestions</h4>
                <strong>Best for Beginners:</strong><br>
                • Fidelity (No fees, great funds)<br>
                • Vanguard (Low-cost leader)<br>
                • Schwab (Excellent customer service)<br><br>
                <strong>Robo-Advisors:</strong><br>
                • Betterment (Auto-rebalancing)<br>
                • Wealthfront (Tax-loss harvesting)<br>
                • M1 Finance (Pie investing)<br><br>
                <strong>Monthly Investment:</strong> {format_currency(available_for_investment, 0)}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="warning-card">
            <h4>⚠️ Focus on Emergency Fund First</h4>
            <p>Prioritize building your emergency fund before investing. Once you have 3-6 months of expenses saved, redirect funds to investments!</p>
        </div>
        """, unsafe_allow_html=True)

    # =============================================================================
    # DEBT PAYOFF STRATEGY
    # =============================================================================
    
    if current_debt > 0:
        st.markdown("### 💳 Debt Elimination Strategy")
        
        # Debt payoff calculators
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔥 Avalanche Method (Recommended)")
            # Assuming average 18% APR for credit cards
            avg_apr = st.slider("Average Debt Interest Rate (%)", 3.0, 29.9, 18.0)
            
            total_debt_payment = monthly_debt_payment + debt_payoff_extra
            
            # Calculate payoff time
            if total_debt_payment > 0 and avg_apr > 0:
                monthly_rate = (avg_apr / 100) / 12
                if monthly_rate * current_debt < total_debt_payment:
                    months_to_payoff = -(1/12) * (math.log(1 - (monthly_rate * current_debt / total_debt_payment)) / math.log(1 + monthly_rate))
                    total_interest = (total_debt_payment * months_to_payoff) - current_debt
                else:
                    months_to_payoff = float('inf')
                    total_interest = float('inf')
            else:
                months_to_payoff = current_debt / total_debt_payment if total_debt_payment > 0 else float('inf')
                total_interest = 0
            
            if months_to_payoff != float('inf'):
                st.markdown(f"""
                <div class="goal-tracker">
                    <h4>⏰ Payoff Timeline</h4>
                    <h2>{months_to_payoff:.1f} months</h2>
                    <p>Total Payment: {format_currency(total_debt_payment, 0)}/month</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="survival-card">
                    <h4>💰 Total Interest Saved</h4>
                    <p>By paying {format_currency(total_debt_payment, 0)}/month instead of minimums:</p>
                    <h3>Interest: {format_currency(total_interest, 0)}</h3>
                    <p>vs paying minimums for years!</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🎯 Debt Freedom Goals")
            
            debt_free_date = datetime.now() + timedelta(days=months_to_payoff * 30) if months_to_payoff != float('inf') else None
            
            if debt_free_date:
                st.markdown(f"""
                <div class="slay-card">
                    <h4>🎉 Debt Freedom Date</h4>
                    <h2>{debt_free_date.strftime('%B %Y')}</h2>
                    <p>Your financial independence day!</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Monthly savings after debt payoff
            future_monthly_boost = total_debt_payment
            annual_boost = future_monthly_boost * 12
            
            st.markdown(f"""
            <div class="investment-card">
                <h4>🚀 Post-Debt Monthly Boost</h4>
                <h2>{format_currency(future_monthly_boost, 0)}</h2>
                <p>Extra for investments/goals</p>
                <small>Annual boost: {format_currency(annual_boost, 0)}</small>
            </div>
            """, unsafe_allow_html=True)

    # =============================================================================
    # GOAL-BASED SAVINGS CALCULATOR
    # =============================================================================
    
    st.markdown("### 🎯 Goal-Based Savings Planner")
    
    # Pre-defined common goals
    common_goals = {
        "🏖️ Dream Vacation": 3000,
        "🚗 Car Down Payment": 5000,  
        "🏠 House Down Payment": 40000,
        "💻 New Laptop/Setup": 2000,
        "📚 Education/Certification": 5000,
        "💍 Wedding Fund": 20000,
        "🎂 Custom Goal": 0
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_goal = st.selectbox("Choose Your Goal", list(common_goals.keys()))
        if selected_goal == "🎂 Custom Goal":
            goal_amount = st.number_input("Custom Goal Amount", min_value=100.0, value=5000.0, step=100.0)
            goal_name = st.text_input("Goal Name", value="My Custom Goal")
        else:
            goal_amount = common_goals[selected_goal]
            goal_name = selected_goal
    
    with col2:
        goal_timeline = st.selectbox(
            "Target Timeline",
            ["3 months", "6 months", "1 year", "2 years", "3 years", "5 years"]
        )
        timeline_months = {"3 months": 3, "6 months": 6, "1 year": 12, "2 years": 24, "3 years": 36, "5 years": 60}
        months = timeline_months[goal_timeline]
    
    with col3:
        goal_priority = st.selectbox(
            "Priority Level",
            ["🔥 High Priority", "⚡ Medium Priority", "💫 Low Priority"]
        )
    
    # Calculate required monthly savings
    if goal_amount > 0 and months > 0:
        required_monthly = goal_amount / months
        available_for_goal = adjusted_savings * 0.3  # 30% of savings can go to goals
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="goal-tracker">
                <h4>🎯 {goal_name}</h4>
                <h2>{format_currency(goal_amount, 0)}</h2>
                <p>Target in {goal_timeline}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="goal-tracker">
                <h4>💰 Required Monthly</h4>
                <h2>{format_currency(required_monthly, 0)}</h2>
                <p>To reach your goal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            feasibility = "✅ Totally Doable!" if required_monthly <= available_for_goal else "⚠️ Needs Adjustment"
            st.markdown(f"""
            <div class="goal-tracker">
                <h4>📊 Feasibility</h4>
                <h2>{feasibility}</h2>
                <p>Available: {format_currency(available_for_goal, 0)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Goal progress tracking
        if required_monthly <= available_for_goal:
            st.markdown(f"""
            <div class="success-card">
                <h4>🎉 Goal Strategy Approved!</h4>
                <p><strong>Monthly Allocation:</strong> {format_currency(required_monthly, 0)} from your {format_currency(adjusted_savings, 0)} savings budget</p>
                <p><strong>Timeline:</strong> {goal_timeline} | <strong>Achievement Date:</strong> {(datetime.now() + timedelta(days=months*30)).strftime('%B %Y')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Alternative suggestions
            realistic_timeline = goal_amount / available_for_goal
            st.markdown(f"""
            <div class="warning-card">
                <h4>💡 Alternative Suggestions</h4>
                <p><strong>Option 1:</strong> Extend timeline to {realistic_timeline:.1f} months</p>
                <p><strong>Option 2:</strong> Reduce goal to {format_currency(available_for_goal * months, 0)}</p>
                <p><strong>Option 3:</strong> Increase income or reduce other expenses</p>
            </div>
            """, unsafe_allow_html=True)

    # =============================================================================
    # WEALTH BUILDING PROJECTIONS
    # =============================================================================
    
    st.markdown("### 🚀 Long-Term Wealth Building Projections")
    
    # 10, 20, 30 year projections
    investment_return = 0.07  # 7% average annual return
    years_projections = [10, 20, 30]
    
    if available_for_investment > 0:
        st.markdown("#### 📈 Investment Growth Projections (7% Annual Return)")
        
        cols = st.columns(len(years_projections))
        
        for i, years in enumerate(years_projections):
            # Future value calculation: FV = PMT * [((1+r)^n - 1) / r]
            monthly_investment = available_for_investment
            monthly_rate = investment_return / 12
            months = years * 12
            
            future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
            total_contributions = monthly_investment * months
            investment_growth = future_value - total_contributions
            
            with cols[i]:
                st.markdown(f"""
                <div class="slay-card">
                    <h4>💰 {years} Year Projection</h4>
                    <h2>{format_currency(future_value, 0)}</h2>
                    <div style="font-size: 0.8em; margin-top: 10px;">
                        <p>Contributions: {format_currency(total_contributions, 0)}</p>
                        <p>Growth: {format_currency(investment_growth, 0)}</p>
                        <p>Monthly: {format_currency(monthly_investment, 0)}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Net worth milestones
    st.markdown("#### 🎯 Net Worth Milestones by Age")
    
    user_age = 25  # Default, can be adjusted above
    current_age = user_age
    target_ages = [30, 35, 40]
    
    # Rule of thumb: net worth should be 1x annual income by 30, 3x by 40
    milestone_multipliers = {30: 1, 35: 3, 40: 5}
    
    cols = st.columns(len(target_ages))
    
    for i, target_age in enumerate(target_ages):
        years_to_age = target_age - current_age
        target_multiplier = milestone_multipliers.get(target_age, target_age - 25)
        target_net_worth = annual_income * target_multiplier
        
        # Calculate if current savings rate will achieve this
        if years_to_age > 0 and adjusted_savings > 0:
            projected_savings = current_savings_amount + (adjusted_savings * 12 * years_to_age)
            # Assuming some investment growth
            projected_investments = available_for_investment * 12 * years_to_age * (1 + investment_return) ** years_to_age if available_for_investment > 0 else 0
            projected_net_worth = projected_savings + projected_investments
            
            achievement_status = "✅ On Track" if projected_net_worth >= target_net_worth else "⚠️ Need Boost"
        else:
            achievement_status = "🎯 Future Goal"
            projected_net_worth = 0
        
        with cols[i]:
            st.markdown(f"""
            <div class="milestone-badge" style="display: block; margin: 10px 0; padding: 15px;">
                <h4>Age {target_age} Goal</h4>
                <h3>{format_currency(target_net_worth, 0)}</h3>
                <p>{target_multiplier}x Annual Income</p>
                <small>{achievement_status}</small>
            </div>
            """, unsafe_allow_html=True)

    # =============================================================================
    # ACTIONABLE NEXT STEPS & RECOMMENDATIONS
    # =============================================================================
    
    st.markdown("### ✅ Your Personalized Action Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚨 Immediate Actions (This Week)")
        immediate_actions = []
        
        if current_savings_amount < 1000:
            immediate_actions.append("🏦 Open high-yield savings account (Marcus, Ally, Capital One)")
            immediate_actions.append("💰 Set up automatic transfer of $50-100/week to savings")
        
        if monthly_debt_payment > 0 and debt_payoff_extra > 0:
            immediate_actions.append("📞 Call credit card companies to negotiate lower rates")
            immediate_actions.append("💳 Set up automatic extra payments to highest interest debt")
        
        if available_for_investment > 100:
            immediate_actions.append("📊 Open investment account (Fidelity, Vanguard, or Schwab)")
            immediate_actions.append("🤖 Set up automatic investing in index funds")
        
        immediate_actions.append("📱 Download budgeting app (Mint, YNAB, or PocketGuard)")
        immediate_actions.append("🔍 Review and cancel unused subscriptions")
        
        for action in immediate_actions[:5]:
            st.markdown(f"• {action}")
    
    with col2:
        st.markdown("#### 📅 30-Day Goals")
        monthly_goals = []
        
        if emergency_progress < 100:
            monthly_goals.append(f"🛡️ Save {format_currency(emergency_monthly_need, 0)} for emergency fund")
        
        monthly_goals.append(f"📊 Track all expenses and stay within {format_currency(wants_amount, 0)} fun budget")
        monthly_goals.append(f"💰 Automate {format_currency(adjusted_savings, 0)} monthly savings")
        
        if current_debt > 0:
            monthly_goals.append(f"💳 Pay {format_currency(total_debt_payment, 0)} toward debt elimination")
        
        monthly_goals.append("📚 Read one personal finance book or take online course")
        monthly_goals.append("🎯 Set up goal tracking for your biggest financial priority")
        
        for goal in monthly_goals:
            st.markdown(f"• {goal}")

# Quick Win Tips
st.markdown("""
<div class="vibe-card">
    <h3>💡 Quick Wins for This Week</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 15px;">
        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
            <h4>🏦 Banking Hack</h4>
            <p>Switch to a high-yield savings account earning 4%+ instead of 0.01% at big banks</p>
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
            <h4>🤖 Automation</h4>
            <p>Set up automatic transfers on payday - pay yourself first before you can spend it</p>
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
            <h4>💳 Credit Boost</h4>
            <p>Pay credit cards twice monthly instead of once to lower utilization and boost score</p>
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
            <h4>📊 Track Everything</h4>
            <p>Use apps like Mint or YNAB to see where every dollar goes - awareness = control</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 🚨 MAIN ERROR: format_currency function is not defined
# FIX: Replace format_currency with standard Python formatting

# ❌ ORIGINAL (BROKEN):
# Your {lifestyle_mode.split('(')[0]} approach with {format_currency(total_monthly_income, 0)} monthly income

# ✅ FIXED VERSION:


# Motivational closing - FIXED
st.markdown(f"""
<div class="success-card">
    <h3>✨ You're Already Winning!</h3>
    <p>Just by using this calculator and thinking about your financial future, you're ahead of 70% of people your age. 
    Your {lifestyle_mode.split('(')[0]} approach with PKR {total_monthly_income:,.0f} monthly income puts you on track for 
    serious wealth building. Remember: every dollar you save in your 20s becomes $10+ in your future. 
    You've got this! 🚀</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# FOOTER SECTION
# =============================================================================

st.markdown("""
<div style="text-align:center; margin-top:60px; padding:40px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
  <h2 style="margin-bottom: 10px; background: linear-gradient(45deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">💸 FinAura: Where Gen Z Vibes Meet Financial Freedom</h2>
  
  <p style="font-size:1.1em; margin-bottom: 18px; opacity:0.95;">Revolutionizing financial wellness through AI-driven stress management and secure wealth building.</p>
  
  <div style="font-size:1.2em; margin-bottom: 20px; font-weight: 500;">🧠 Built to tackle Gen Z financial stress with intelligent insights, bulletproof security, and a fully automated companion that grows with your financial journey.</div>
  
  <div style="background: rgba(255, 255, 255, 0.15); border-radius: 15px; padding: 25px; margin: 25px auto; max-width: 600px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);">
    <div style="color: #FFD700; font-weight: 600; margin-bottom: 15px; font-size: 1.1em;">🏆 Why FinAura Stands Out</div>
    <div style="text-align: left; font-size: 0.95em; line-height: 1.6;">
      🔒 AI-powered financial stress detection and personalized wellness strategies<br>
      🔒 Bank-grade encryption with multi-layer security protocols<br>
      🔒 Behavioral analytics to combat Gen Z financial anxiety and decision paralysis<br>
      🔒 Gamified savings with real-time progress tracking and achievement systems<br>
      🔒 Zero-knowledge architecture ensuring complete data privacy<br>
      🔒 Smart budgeting algorithms designed for irregular income patterns
    </div>
    <div style="background: linear-gradient(45deg, #00C851, #007E33); color: white; padding: 8px 16px; border-radius: 20px; font-size: 0.85em; font-weight: 500; margin-top: 15px; display: inline-block; border: 1px solid rgba(255, 255, 255, 0.3);">
      🛡️ Enterprise-Grade Security & Privacy Guaranteed
    </div>
  </div>
  
  <div style="margin: 25px 0; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
    <a href="https://github.com/codewithEshaYoutube" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 15px; background: rgba(255, 255, 255, 0.2); border-radius: 25px; text-decoration: none; color: white; font-size: 0.9em; transition: all 0.3s ease;" target="_blank">
      🐙 GitHub
    </a>
    <a href="https://www.linkedin.com/in/esha-tariqdev/" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 15px; background: rgba(255, 255, 255, 0.2); border-radius: 25px; text-decoration: none; color: white; font-size: 0.9em; transition: all 0.3s ease;" target="_blank">
      💼 LinkedIn
    </a>
  </div>
  
  <div style="margin: 20px 0; font-size:1.2em; border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 20px;">
    Made with <span style="font-size:1.5em;">💖</span> by <b style="color: #FFD700;">Esha Tariq</b>
  </div>
  
  <div style="font-size:0.95em; opacity:0.9; margin: 15px 0; font-style: italic;">
    Empowering the next generation to conquer financial stress and build lasting wealth.<br>
    Every smart decision today creates the freedom you deserve tomorrow.
  </div>
  
  <div style="background: linear-gradient(45deg, #FF6B6B, #FF8E53); padding: 8px 16px; border-radius: 20px; font-size: 0.85em; font-weight: 500; margin-top: 15px; display: inline-block;">
    🏆 DevPost Girlies Hackathon Winner - Innovation in FinTech
  </div>
</div>
""", unsafe_allow_html=True)


