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

# =============================================================================
# CUSTOM CSS (THE IMPROVED UI)
# Using #7c15e8 (Purple) as the Primary Brand Color
# =============================================================================

st.markdown("""
<style>
    /* --- GLOBAL VARIABLES & FONTS --- */
    :root {
        --brand-purple: #7c15e8;
        --brand-purple-light: #bfa3ff;
        --brand-purple-dark: #5a0eb5;
        --brand-accent: #00f2fe;
        --glass-bg: rgba(255, 255, 255, 0.9);
        --glass-border: rgba(124, 21, 232, 0.1);
        --card-shadow: 0 10px 30px -10px rgba(124, 21, 232, 0.15);
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f8f9fc;
        color: #1a202c;
    }

    /* --- SIDEBAR --- */
    .css-1d391kg {
        background: linear-gradient(180deg, #240b36 0%, #2d1b4e 100%);
    }
    
    .css-1d391kg .css-17ziqus {
        color: white;
    }

    /* --- HEADER --- */
    .main-header {
        background: linear-gradient(135deg, var(--brand-purple) 0%, #5a0eb5 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 15px 40px rgba(124, 21, 232, 0.3);
        position: relative;
        overflow: hidden;
    }

    .main-header::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: rotate 20s linear infinite;
        pointer-events: none;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }

    /* --- CARDS (Glassmorphism) --- */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: var(--brand-purple-light);
    }

    /* Specific Card Styles */
    .vibe-card {
        background: linear-gradient(135deg, var(--brand-purple) 0%, #9d4edd 100%);
        color: white;
        border: none;
    }
    
    .money-card {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        border: none;
    }
    
    .budget-card {
        background: white;
        border: 1px solid var(--glass-border);
        color: #2d3748;
        border-left: 5px solid var(--brand-purple);
    }
    
    .investment-card {
        background: white;
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .warning-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
        color: #4a4a4a;
        border: none;
        padding: 1rem;
        border-radius: 15px;
    }

    .success-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #2d3748;
        border: none;
        padding: 1rem;
        border-radius: 15px;
    }
    
    .financial-goal-card {
        background: var(--brand-purple);
        color: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(124, 21, 232, 0.2);
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: linear-gradient(90deg, var(--brand-purple) 0%, var(--brand-purple-dark) 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 5px 15px rgba(124, 21, 232, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(124, 21, 232, 0.6);
        letter-spacing: 1px;
    }

    /* --- METRICS --- */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a202c;
    }
    
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }

    /* --- PROGRESS BAR --- */
    .progress-bar {
        background: rgba(124, 21, 232, 0.1);
        border-radius: 10px;
        height: 12px;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--brand-purple), var(--brand-accent));
        border-radius: 10px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* --- CHAT INTERFACE --- */
    .chat-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 2px solid var(--brand-purple-light);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# ENHANCED DATA MODELS & CORE LOGIC
# =============================================================================

class VibeType(Enum):
    STRESSED = "😩 Stressed"
    CONFIDENT = "😎 Confident"
    CONFUSED = "🤔 Confused"
    EXCITED = "🚀 Excited"
    CHILL = "😌 Chill"
    GUILTY = "😬 Guilty"

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
    needs_percentage: float = 50.0
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
            ],
            VibeType.EXCITED: [
                "Let's GOO! 🚀 Channel this energy into your savings goals!",
                "I love this hype! Keep this momentum going.",
                "Turn that excitement into compound interest! 💸"
            ],
            VibeType.CHILL: [
                "A balanced vibe is the best vibe. 😌 Keep maintaining the course.",
                "Calm money minds make the best decisions.",
                "Enjoy the stability. You're building a solid foundation."
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
                "needs": 60, 
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
        
        roadmap.append({
            "priority": 1,
            "goal": "Emergency Fund",
            "target": min(income * 6, 10000),
            "description": "Your financial safety net - aim for 3-6 months expenses 🚨"
        })
        
        if age < 30:
            roadmap.extend([
                {
                    "priority": 2,
                    "goal": "Retirement Start",
                    "target": income * 0.15, 
                    "description": "Start early = retire like royalty 👑"
                },
                {
                    "priority": 3,
                    "goal": "Skill Investment",
                    "target": income * 0.05, 
                    "description": "Invest in yourself - best ROI ever 📚"
                }
            ])
        
        return roadmap

# =============================================================================
# SESSION STATE INITIALIZATION WITH ERROR HANDLING
# =============================================================================

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

if 'currency' not in st.session_state:
    st.session_state.currency = 'USD'

currency_symbols = {'USD': '$', 'PKR': 'Rs', 'EUR': '€'}
currency_rates = {'USD': 1.0, 'PKR': 280.0, 'EUR': 0.92} 

with st.sidebar:
    st.markdown('### 🌍 Global Settings')
    st.session_state.currency = st.selectbox(
        'Currency',
        options=['USD', 'PKR', 'EUR'],
        format_func=lambda x: f"{currency_symbols[x]} {x}",
        index=['USD', 'Rs', 'EUR'].index(st.session_state.currency) if st.session_state.currency in ['USD', 'Rs', 'EUR'] else 0
    )
    
    st.markdown('---')
    
    # Agentic AI Toggle
    st.markdown('### 🤖 Agentic AI Assistant')
    enable_agent = st.checkbox('🧠 Enable AI Agent', value=st.session_state.get('agent_enabled', False))
    st.session_state.agent_enabled = enable_agent
    
    if enable_agent:
        st.success('🚀 AI Agent Active!')
        agent_mode = st.selectbox(
            '🎯 Agent Focus',
            ['💰 Autonomous Slay Planner', '🧾 Emotional Spending Coach', '📊 Financial Advisor', '🎯 Goal Tracker'],
            help='Choose what your AI agent should focus on'
        )
        st.session_state.agent_mode = agent_mode
        
        # Agent intensity
        agent_intensity = st.slider('🔥 Agent Intensity', 1, 5, 3, help='How often should the agent intervene?')
        st.session_state.agent_intensity = agent_intensity

    # Navigation for Agent Mode
    if enable_agent:
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('🏠 Home', use_container_width=True):
                st.session_state.current_page = 'home'
                st.rerun()
        with col2:
            if st.button('🌈 Vibe', use_container_width=True):
                st.session_state.current_page = 'vibe'
                st.rerun()
        with col3:
             if st.button('🔥 Plan', use_container_width=True):
                st.session_state.current_page = 'planning'
                st.rerun()

# =============================================================================
# AGENTIC AI CHATBOT INTEGRATION
# =============================================================================

if st.session_state.get('agent_enabled', False):
    st.markdown("## 🤖 Your Personal AI Financial Coach")
    current_mode = st.session_state.get('agent_mode', '💰 Autonomous Slay Planner')
    st.info(f"🧠 **Active Agent Mode:** {current_mode}")
    
    st.markdown(f"""
    <div class="chat-container">
        <iframe
            src="https://www.chatbase.co/chatbot-iframe/97sccVBW3_J60VexD-2eY"
            width="100%"
            height="600"
            style="border:none; background:white;"
        ></iframe>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# AGENTIC AI FEATURES - AUTONOMOUS PLANNER & EMOTIONAL COACH
# =============================================================================

if st.session_state.get('agent_enabled', False):
    agent_mode = st.session_state.get('agent_mode', '💰 Autonomous Slay Planner')
    
    if agent_mode == '💰 Autonomous Slay Planner':
        st.markdown("### 🎯 Autonomous Slay Planner")
        
        with st.expander("🚀 Set Your Slay Goal", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                goal_item = st.text_input("🎯 What do you want to buy?", placeholder="e.g., iPad, vacation, car")
                goal_amount = st.number_input("💰 How much does it cost?", min_value=1.0, value=500.0, step=50.0)
            
            with col2:
                goal_months = st.slider("📅 In how many months?", 1, 24, 3)
                current_saved = st.number_input("💳 Already saved?", min_value=0.0, value=0.0, step=10.0)
            
            if st.button("🚀 Activate Slay Planner", type="primary"):
                remaining_amount = goal_amount - current_saved
                weeks_available = goal_months * 4.33 
                weekly_savings_needed = remaining_amount / weeks_available
                
                st.session_state.slay_goal = {
                    'item': goal_item,
                    'total_amount': goal_amount,
                    'months': goal_months,
                    'current_saved': current_saved,
                    'weekly_needed': weekly_savings_needed,
                    'created_date': datetime.now()
                }
                
                st.success(f"🎯 Goal Set! Save {format_currency(weekly_savings_needed)} per week to get your {goal_item}!")
        
        if 'slay_goal' in st.session_state:
            goal = st.session_state.slay_goal
            progress = (goal['current_saved'] / goal['total_amount']) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 Goal", goal['item'])
                st.metric("💰 Total Cost", format_currency(goal['total_amount']))
            
            with col2:
                st.metric("💳 Saved So Far", format_currency(goal['current_saved']))
                st.metric("📅 Time Left", f"{goal['months']} months")
            
            with col3:
                st.metric("💪 Weekly Target", format_currency(goal['weekly_needed']))
                st.metric("📈 Progress", f"{progress:.1f}%")
            
            st.progress(progress / 100)
            
            if goal['weekly_needed'] > 0:
                monthly_income = st.session_state.financial_profile.get('monthly_income', 0) if st.session_state.financial_profile else 3000
                weekly_income = monthly_income / 4.33
                savings_rate = (goal['weekly_needed'] / weekly_income) * 100
                
                if savings_rate > 30:
                    st.warning(f"🚨 **Agent Alert:** This goal requires {savings_rate:.1f}% of your weekly income.")
                elif savings_rate > 15:
                    st.info(f"💪 **Agent Suggestion:** This goal requires {savings_rate:.1f}% of weekly income.")
                else:
                    st.success(f"✅ **Agent Approved:** This goal is achievable!")
    
    elif agent_mode == '🧾 Emotional Spending Coach':
        st.markdown("### 🧾 Emotional Spending Tracker + Agentic Coaching")
        
        if st.session_state.transactions:
            st.markdown("#### 🔍 Recent Emotional Spending Analysis")
            
            emotional_categories = {'Joy': [], 'Regret': [], 'Impulse': [], 'Survival': []}
            
            for transaction in st.session_state.transactions[-10:]:
                vibe_impact = getattr(transaction, 'vibe_impact', 0)
                amount = getattr(transaction, 'amount', 0)
                description = getattr(transaction, 'description', '')
                
                if vibe_impact > 0.3:
                    emotional_categories['Joy'].append((description, amount))
                elif vibe_impact < -0.3:
                    emotional_categories['Regret'].append((description, amount))
                elif any(word in description.lower() for word in ['impulse', 'quick', 'saw', 'wanted']):
                    emotional_categories['Impulse'].append((description, amount))
                else:
                    emotional_categories['Survival'].append((description, amount))
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                joy_total = sum(amount for _, amount in emotional_categories['Joy'])
                st.metric("😊 Joy", f"{len(emotional_categories['Joy'])}", delta=format_currency(joy_total))
            with col2:
                regret_total = sum(amount for _, amount in emotional_categories['Regret'])
                st.metric("😔 Regret", f"{len(emotional_categories['Regret'])}", delta=format_currency(regret_total))
            with col3:
                impulse_total = sum(amount for _, amount in emotional_categories['Impulse'])
                st.metric("⚡ Impulse", f"{len(emotional_categories['Impulse'])}", delta=format_currency(impulse_total))
            with col4:
                survival_total = sum(amount for _, amount in emotional_categories['Survival'])
                st.metric("🛡️ Survival", f"{len(emotional_categories['Survival'])}", delta=format_currency(survival_total))
            
            total_emotional = regret_total + impulse_total
            if total_emotional > joy_total:
                st.warning("🚨 **Coach Alert:** You're spending more on regret/impulse than joy!")
                st.markdown("• **Pause Rule:** Wait 24 hours before any purchase over $25")
                st.markdown("• **Emotion Check:** Ask yourself 'Am I buying this because I'm sad/stressed?'")
        
        else:
            st.info("💝 Start making some purchases to unlock emotional spending insights!")

    # Agent Notifications
    if st.session_state.get('agent_intensity', 3) >= 3:
        st.markdown("### 🚨 Live Agent Interventions")
        if st.session_state.transactions:
            recent_spending = sum(t.amount for t in st.session_state.transactions[-5:])
            
            if recent_spending > 200:
                st.warning("🤖 **Agent Alert:** Heavy spending detected! Current session: " + format_currency(recent_spending))
                st.markdown("• Take a 10-minute break before your next purchase")
                st.markdown("• Consider if this aligns with your current goals")

# =============================================================================
# AGENT MILESTONE & REWARD SYSTEM
# =============================================================================

if st.session_state.get('agent_enabled', False) and 'slay_goal' in st.session_state:
    goal = st.session_state.slay_goal
    progress = (goal['current_saved'] / goal['total_amount']) * 100
    milestones = [25, 50, 75, 90, 100]
    
    if 'celebrated_milestones' not in st.session_state:
        st.session_state.celebrated_milestones = []
    
    for milestone in milestones:
        if progress >= milestone and milestone not in st.session_state.celebrated_milestones:
            st.session_state.celebrated_milestones.append(milestone)
            
            if milestone == 50:
                st.balloons()
                st.success("🚀 **Halfway There!** You're absolutely crushing this goal!")
            elif milestone == 100:
                st.success("🏆 **GOAL ACHIEVED!** You did it!")
                if st.button("🎯 Set New Goal"):
                    del st.session_state.slay_goal
                    st.rerun()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

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

def get_currency_label():
    symbol = currency_symbols[st.session_state.currency]
    code = st.session_state.currency
    return f"{symbol} ({code})"

# =============================================================================
# MAIN APP INTERFACE
# =============================================================================

try:
    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <h1 style="font-size: 3.5rem; font-weight: 800; margin: 0; line-height: 1.2;">💸 FinAura</h1>
            <h2 style="font-weight: 300; font-size: 1.5rem; margin-top: 0.5rem; opacity: 0.9;">Your Gen Z CFO</h2>
            <p style="font-style: italic; margin-top: 1rem; opacity: 0.8;">Emotionally Smart. Financially Sharp.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.debug_mode and st.session_state.error_count > 0:
        st.warning(f"⚠️ Debug Mode: {st.session_state.error_count} errors detected")

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
            value=st.session_state.financial_profile.get('monthly_income', 5000.0),
            step=100.0
        )
        age = st.slider("🎂 Age", min_value=18, max_value=35, value=st.session_state.financial_profile.get('age', 25))
    
    with col2:
        employment_status = st.selectbox("👔 Employment Status", ["Student", "Full-time Job", "Freelancer", "Part-time", "Unemployed", "Side Hustle King/Queen"], index=1)
        living_situation = st.selectbox("🏠 Living Situation", ["With Parents (blessed!)", "Shared Apartment", "Solo Living", "Dorm Life"], index=0)
    
    with col3:
        risk_tolerance = st.selectbox("📊 Investment Risk Tolerance", ["Conservative (play it safe)", "Moderate (balanced vibes)", "Aggressive (YOLO but smart)"], index=1)
        primary_goal = st.selectbox("🎯 Primary Financial Goal", list(FinancialGoal), format_func=lambda x: x.value)
    
    if st.button("💾 Save My Financial Profile", type="primary"):
        st.session_state.financial_profile = {
            'monthly_income': monthly_income, 'age': age, 'employment_status': employment_status,
            'living_situation': living_situation, 'risk_tolerance': risk_tolerance, 'primary_goal': primary_goal
        }
        
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
        <div class="budget-card glass-card">
            <h3 style="color:#7c15e8">💰 Monthly Income</h3>
            <h2 style="font-size: 2rem;">{format_currency(budget.monthly_income, 0)}</h2>
            <p>Your total hustle</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="budget-card glass-card">
            <h3 style="color:#7c15e8">🏠 Needs ({budget.needs_percentage}%)</h3>
            <h2 style="font-size: 2rem;">{format_currency(budget.needs_amount, 0)}</h2>
            <p>Rent, food, transport</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="budget-card glass-card">
            <h3 style="color:#7c15e8">✨ Wants ({budget.wants_percentage}%)</h3>
            <h2 style="font-size: 2rem;">{format_currency(budget.wants_amount, 0)}</h2>
            <p>Fun, joy, self-care</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="budget-card glass-card">
            <h3 style="color:#7c15e8">📈 Savings ({budget.savings_percentage}%)</h3>
            <h2 style="font-size: 2rem;">{format_currency(budget.savings_amount, 0)}</h2>
            <p>Future you fund</p>
        </div>
        """, unsafe_allow_html=True)
    
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
        color_discrete_sequence=['#7c15e8', '#bfa3ff', '#4facfe'], # Updated Colors
        hole=0.4
    )
    fig_budget.update_traces(textposition='inside', textinfo='percent+label')
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
                <h4 style="color: #7c15e8; margin-bottom: 0.2rem;">{inv['name']}</h4>
                <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">{inv['desc']}</p>
                <p style="font-size: 0.8rem;"><strong>Risk:</strong> {inv['risk']} | <strong>Expected Return:</strong> {inv['return']}</p>
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
                <p style="opacity: 0.9;">{item['description']}</p>
                <p style="font-weight: bold; margin-top: 0.5rem;">Target: {format_currency(item['target'], 0)}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
                <p style="text-align: right; font-size: 0.8rem; margin-top: 5px;">{progress}% Complete</p>
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
        """)
    
    with col2:
        st.markdown("""
        **💫 Budgeting Hacks:**
        - Automate savings (pay yourself first!)
        - Use the 24-hour rule for big purchases
        - Track spending with photos of receipts
        - Set up separate accounts for different goals
        - Use cash for discretionary spending
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
        """)
    
    with col2:
        st.markdown("""
        **⚡ Power Moves:**
        - Start with small amounts ($25-50/month)
        - Diversify (don't put all eggs in one basket)
        - Think long-term (10+ years)
        - Don't panic sell during market dips
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
        - Mental peace (priceless!)
        """)
    
    with col2:
        st.markdown("""
        **🔥 Building Strategy:**
        - Start with $1,000 (any amount is better than zero!)
        - Automate transfers (monthly)
        - Use windfalls (tax refunds, bonuses)
        - Sell stuff you don't need
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
        """)
    
    with col2:
        st.markdown("""
        **💡 Side Hustle Success Tips:**
        - Start with skills you already have
        - Set clear income goals
        - Track time vs. money earned
        - Separate business & personal finances
        - Save taxes (15-30% of earnings)
        """)

# =============================================================================
# HERO VIBE CHECK SECTION (RESTORED & IMPROVED)
# =============================================================================

st.markdown("---")
st.markdown(f"""
<div style='
    background: linear-gradient(135deg, #7c15e8 0%, #9d4edd 100%);
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

# Vibe Selector
col_vibe, col_stress, col_conf = st.columns([2, 1, 1])

with col_vibe:
    try:
        vibe_index = list(VibeType).index(st.session_state.current_vibe)
    except Exception:
        st.session_state.current_vibe = VibeType.CHILL
        vibe_index = list(VibeType).index(VibeType.CHILL)
        
    current_vibe = st.selectbox(
        "Select your current vibe:",
        options=list(VibeType),
        format_func=lambda x: f"{x.value} {x.name.title()}",
        index=vibe_index,
        key="hero_vibe_selectbox",
        label_visibility="collapsed"
    )
    
    # Check if vibe changed to trigger updates
    if 'previous_vibe' not in st.session_state:
        st.session_state.previous_vibe = current_vibe
    
    if current_vibe != st.session_state.previous_vibe:
        st.session_state.current_vibe = current_vibe
        st.session_state.previous_vibe = current_vibe
        st.rerun()

# Sliders for additional context
with col_stress:
    money_stress = st.slider("Money Stress Level", 1, 10, 3)
    
with col_conf:
    confidence_level = st.slider("Financial Confidence", 1, 10, 7)

# Display AI Response based on Vibe
if st.session_state.current_vibe:
    response = st.session_state.agent.get_vibe_response(st.session_state.current_vibe)
    
    st.markdown(f"""
    <div class="glass-card" style="background: white; border-left: 5px solid #7c15e8; margin-top: 1rem;">
        <h3 style="color: #7c15e8; margin-top:0;">💬 FinAura's Insight</h3>
        <p style="font-size: 1.2rem; line-height: 1.6;">{response}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Provide specific advice based on the sliders
    if money_stress > 7:
        st.warning("💜 **Tip:** High stress detected? Let's pause big purchases for 24 hours.")
    if confidence_level < 5:
        st.info("🌈 **Tip:** Low confidence is normal. Focus on one small financial win today!")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #718096; font-size: 0.8rem; padding: 1rem;'>
    <p>FinAura © 2026 | Built for Gen Z by Gen Z</p>
</div>
""", unsafe_allow_html=True)
