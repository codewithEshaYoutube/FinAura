# 💸 FinAura: Your Gen Z CFO – Enhanced Financial Planning
# Complete Streamlit App with Advanced Financial Planning & Goal Tracking

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

# Page config with Gen Z vibes
st.set_page_config(
    page_title="💸 FinAura - Your Gen Z CFO",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for Gen Z aesthetic
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }
    
    .financial-setup-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 40%, #fee140 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        color: #2d3748;
        box-shadow: 0 8px 32px rgba(255, 154, 158, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .budget-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 0.5rem;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.3);
        transition: transform 0.3s ease;
    }
    
    .budget-card:hover {
        transform: translateY(-5px);
    }
    
    .survival-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #2d3748;
        border-left: 5px solid #ff6b6b;
        box-shadow: 0 4px 15px rgba(252, 182, 159, 0.4);
    }
    
    .comfort-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #2d3748;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(168, 237, 234, 0.4);
    }
    
    .slay-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #2d3748;
        border-left: 5px solid #ff6b6b;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
    }
    
    .goal-tracker {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    .investment-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
    }
    
    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        height: 30px;
        margin: 1rem 0;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        transition: width 0.8s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    .milestone-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .vibe-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    .money-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        transition: transform 0.3s ease;
    }
    
    .money-card:hover {
        transform: scale(1.05);
    }
    
    .chat-bubble {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 15px 15px 0;
        font-style: italic;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .financial-tip {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #2d3748;
        border-left: 3px solid #667eea;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
    }
    
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #2d3748;
        box-shadow: 0 4px 15px rgba(168, 237, 234, 0.3);
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
    SURVIVAL = "🛡️ Survival Mode"
    COMFORT = "😌 Comfort Zone"
    SLAY = "👑 Slay Mode"

class LifeStage(Enum):
    STUDENT = "🎓 Student Life"
    EARLY_CAREER = "🚀 Early Career"
    ESTABLISHED = "💼 Established Professional"

@dataclass
class Transaction:
    date: datetime
    amount: float
    description: str
    category: SpendingCategory
    merchant: str = ""
    vibe_impact: float = 0.0

@dataclass
class FinancialProfile:
    monthly_income: float
    age: int
    life_stage: LifeStage
    financial_goal: FinancialGoal
    debt_amount: float = 0.0
    current_savings: float = 0.0
    risk_tolerance: str = "Medium"

@dataclass
class GoalTracker:
    name: str
    target_amount: float
    current_amount: float
    target_date: datetime
    category: str
    priority: str

class EnhancedGenZFinancialPlanner:
    """Advanced Financial planning structure tailored for Gen Z survival and slaying"""
    
    def __init__(self):
        self.frameworks = {
            FinancialGoal.SURVIVAL: {
                "needs": 65,  # Higher for survival mode
                "wants": 20,  # Minimal fun spending
                "savings": 15,  # Focus on emergency fund
                "description": "Focus on stability and building emergency fund"
            },
            FinancialGoal.COMFORT: {
                "needs": 50,  # Standard 50/30/20 rule
                "wants": 30,
                "savings": 20,
                "description": "Balanced approach with room for enjoyment"
            },
            FinancialGoal.SLAY: {
                "needs": 45,  # Lower needs ratio for higher income
                "wants": 25,  # Controlled wants
                "savings": 30,  # Aggressive savings/investments
                "description": "Aggressive wealth building and investment focus"
            }
        }
        
        self.life_stage_multipliers = {
            LifeStage.STUDENT: {"emergency_months": 3, "investment_risk": "High"},
            LifeStage.EARLY_CAREER: {"emergency_months": 4, "investment_risk": "Medium-High"},
            LifeStage.ESTABLISHED: {"emergency_months": 6, "investment_risk": "Medium"}
        }
    
    def calculate_comprehensive_budget(self, profile: FinancialProfile) -> Dict:
        """Calculate detailed budget based on complete financial profile"""
        
        framework = self.frameworks[profile.financial_goal]
        life_multipliers = self.life_stage_multipliers[profile.life_stage]
        
        # Base calculations
        needs = profile.monthly_income * (framework["needs"] / 100)
        wants = profile.monthly_income * (framework["wants"] / 100)
        savings = profile.monthly_income * (framework["savings"] / 100)
        
        # Debt adjustment
        if profile.debt_amount > 0:
            min_debt_payment = min(profile.debt_amount * 0.02, savings * 0.5)  # 2% of debt or 50% of savings
            savings -= min_debt_payment
            debt_payment = min_debt_payment
        else:
            debt_payment = 0
        
        # Emergency fund calculation
        emergency_target = needs * life_multipliers["emergency_months"]
        
        # Investment allocation
        investment_amount = max(0, savings - min(200, savings * 0.3))  # Reserve some for emergency
        emergency_contribution = savings - investment_amount
        
        return {
            "needs": needs,
            "wants": wants,
            "savings": savings,
            "debt_payment": debt_payment,
            "emergency_target": emergency_target,
            "emergency_contribution": emergency_contribution,
            "investment_amount": investment_amount,
            "framework": framework,
            "life_stage_advice": life_multipliers,
            "net_income_after_budget": profile.monthly_income - (needs + wants + savings + debt_payment)
        }
    
    def get_investment_allocation(self, amount: float, profile: FinancialProfile) -> Dict:
        """Get detailed investment allocation suggestions"""
        
        risk_level = self.life_stage_multipliers[profile.life_stage]["investment_risk"]
        
        if profile.age < 25:
            # Aggressive growth for young investors
            allocation = {
                "🏦 High-Yield Savings": amount * 0.1,
                "📊 Index Funds (VTI/VXUS)": amount * 0.6,
                "🚀 Growth Stocks": amount * 0.2,
                "🌟 Crypto/Alternative": amount * 0.1
            }
        elif profile.age < 30:
            # Balanced aggressive approach
            allocation = {
                "🏦 High-Yield Savings": amount * 0.15,
                "📊 Index Funds (VTI/VXUS)": amount * 0.55,
                "🚀 Growth Stocks": amount * 0.20,
                "🏠 REITs": amount * 0.05,
                "🌟 Crypto/Alternative": amount * 0.05
            }
        else:
            # More conservative as income stabilizes
            allocation = {
                "🏦 High-Yield Savings": amount * 0.2,
                "📊 Index Funds (VTI/VXUS)": amount * 0.5,
                "🚀 Growth Stocks": amount * 0.15,
                "🏠 REITs": amount * 0.1,
                "🌟 Crypto/Alternative": amount * 0.05
            }
        
        return allocation
    
    def generate_milestone_plan(self, profile: FinancialProfile) -> List[Dict]:
        """Generate age-based financial milestones"""
        
        current_age = profile.age
        milestones = []
        
        # Emergency Fund Milestone
        if profile.current_savings < profile.monthly_income * 3:
            milestones.append({
                "age": current_age + 1,
                "goal": "🛡️ Emergency Fund Complete",
                "target": profile.monthly_income * 6,
                "description": "6 months of expenses saved"
            })
        
        # Net Worth Milestones
        age_milestones = [
            (25, profile.monthly_income * 12, "1x Annual Income"),
            (30, profile.monthly_income * 36, "3x Annual Income"),
            (35, profile.monthly_income * 60, "5x Annual Income")
        ]
        
        for milestone_age, target_amount, description in age_milestones:
            if current_age < milestone_age:
                milestones.append({
                    "age": milestone_age,
                    "goal": f"💰 Net Worth Milestone",
                    "target": target_amount,
                    "description": description
                })
        
        return milestones[:5]  # Return top 5 milestones
    
    def get_personalized_advice(self, profile: FinancialProfile) -> Dict:
        """Get comprehensive personalized advice"""
        
        advice = {
            "immediate": [],
            "short_term": [],
            "long_term": [],
            "life_stage_specific": []
        }
        
        # Immediate advice (next 30 days)
        if profile.current_savings < 1000:
            advice["immediate"].append("🚨 Priority: Build $1000 emergency fund immediately")
            advice["immediate"].append("📱 Use cash-back apps for every purchase (Rakuten, Honey)")
        
        if profile.debt_amount > profile.monthly_income * 3:
            advice["immediate"].append("💳 Focus on high-interest debt - avalanche method")
            advice["immediate"].append("📞 Call creditors to negotiate lower rates")
        
        # Short-term advice (next 6 months)
        advice["short_term"].append("🤖 Automate savings - pay yourself first")
        advice["short_term"].append("📊 Open high-yield savings account (Marcus, Ally)")
        
        if profile.financial_goal == FinancialGoal.SLAY:
            advice["short_term"].append("💼 Develop multiple income streams")
            advice["short_term"].append("📈 Start investing in index funds")
        
        # Long-term advice (1+ years)
        advice["long_term"].append("🏠 Start planning for major purchases")
        advice["long_term"].append("📚 Invest in skills that increase earning potential")
        
        if profile.age < 30:
            advice["long_term"].append("⚡ Time is your superpower - start investing NOW")
        
        # Life stage specific advice
        if profile.life_stage == LifeStage.STUDENT:
            advice["life_stage_specific"].extend([
                "🎓 Build credit history with student card",
                "💡 Focus on internships and networking",
                "📖 Learn about personal finance early"
            ])
        elif profile.life_stage == LifeStage.EARLY_CAREER:
            advice["life_stage_specific"].extend([
                "🚀 Negotiate salary increases aggressively",
                "🏦 Max out employer 401k match",
                "🎯 Set specific financial goals"
            ])
        else:
            advice["life_stage_specific"].extend([
                "👑 Consider real estate investment",
                "💼 Diversify investment portfolio",
                "📊 Plan for major life events"
            ])
        
        return advice

class EnhancedFinAuraAgent:
    """Enhanced Gen Z AI Agent with advanced financial coaching"""
    
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
        
        self.coaching_tips = {
            "debt_stress": "Debt doesn't define your worth! Every payment is progress 💪",
            "low_income": "Starting somewhere is better than not starting at all! 🌱",
            "overspending": "Awareness is the first step to change. You got this! ✨",
            "saving_struggle": "Even $5/week adds up! Small steps, big dreams 🎯"
        }
    
    def get_contextual_coaching(self, profile: FinancialProfile, budget: Dict) -> str:
        """Get personalized coaching based on financial situation"""
        
        coaching_messages = []
        
        # Income-based coaching
        if profile.monthly_income < 3000:
            coaching_messages.append("🌟 Every dollar you save is a win! You're building habits that will serve you for life.")
        elif profile.monthly_income < 6000:
            coaching_messages.append("💪 You're in a great position to build wealth! Time to level up your money game.")
        else:
            coaching_messages.append("👑 Your income is your superpower! Let's make it work harder for you.")
        
        # Debt coaching
        if profile.debt_amount > 0:
            debt_ratio = profile.debt_amount / (profile.monthly_income * 12)
            if debt_ratio > 0.3:
                coaching_messages.append("🎯 Debt payoff is your main quest right now. Every extra payment is XP!")
            else:
                coaching_messages.append("📈 Your debt is manageable! Balance payoff with building wealth.")
        
        # Goal-based coaching
        if profile.financial_goal == FinancialGoal.SURVIVAL:
            coaching_messages.append("🛡️ Survival mode is temporary! You're building the foundation for your comeback story.")
        elif profile.financial_goal == FinancialGoal.SLAY:
            coaching_messages.append("✨ Slay mode activated! Your future self is going to thank you SO much.")
        
        return random.choice(coaching_messages)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

# Initialize session state with enhanced data
if 'financial_profile' not in st.session_state:
    st.session_state.financial_profile = FinancialProfile(
        monthly_income=0.0,
        age=25,
        life_stage=LifeStage.EARLY_CAREER,
        financial_goal=FinancialGoal.COMFORT,
        debt_amount=0.0,
        current_savings=0.0
    )

if 'goal_trackers' not in st.session_state:
    st.session_state.goal_trackers = [
        GoalTracker("Emergency Fund", 6000, 1200, datetime.now() + timedelta(days=365), "Safety", "High"),
        GoalTracker("Vacation Fund", 2000, 300, datetime.now() + timedelta(days=180), "Joy", "Medium"),
        GoalTracker("Investment Portfolio", 10000, 500, datetime.now() + timedelta(days=730), "Wealth", "High")
    ]

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

if 'planner' not in st.session_state:
    st.session_state.planner = EnhancedGenZFinancialPlanner()

if 'agent' not in st.session_state:
    st.session_state.agent = EnhancedFinAuraAgent()

# =============================================================================
# MAIN APP INTERFACE
# =============================================================================

# Header with enhanced Gen Z energy
st.markdown("""
<div class="main-header">
    <h1>💸 FinAura: Your Gen Z CFO</h1>
    <p><em>"Forget spreadsheets. Feel your finances."</em></p>
    <p>Where vibes meet value ✨ | Complete Financial Planning & Goal Tracking</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# ENHANCED FINANCIAL PROFILE SETUP
# =============================================================================

st.markdown("## 🎯 Complete Your Financial Profile")

st.markdown("""
<div class="financial-setup-card">
    <h3>✨ Let's Get Your Money Story Started!</h3>
    <p>Tell us about your financial situation so we can create your personalized Gen Z survival & slay plan!</p>
</div>
""", unsafe_allow_html=True)

# Profile input form
col1, col2, col3, col4 = st.columns(4)

with col1:
    monthly_income = st.number_input(
        "💵 Monthly Income (after taxes)",
        min_value=0.0,
        value=float(st.session_state.financial_profile.monthly_income),
        step=100.0,
        help="Your take-home pay per month"
    )

with col2:
    age = st.slider("🎂 Age", 18, 35, st.session_state.financial_profile.age)

with col3:
    life_stage = st.selectbox(
        "🎭 Life Stage",
        options=list(LifeStage),
        format_func=lambda x: x.value,
        index=list(LifeStage).index(st.session_state.financial_profile.life_stage)
    )

with col4:
    financial_goal = st.selectbox(
        "🎯 Current Mode",
        options=list(FinancialGoal),
        format_func=lambda x: x.value,
        index=list(FinancialGoal).index(st.session_state.financial_profile.financial_goal)
    )

# Additional financial details
col1, col2, col3 = st.columns(3)

with col1:
    debt_amount = st.number_input(
        "💳 Total Debt",
        min_value=0.0,
        value=float(st.session_state.financial_profile.debt_amount),
        step=100.0,
        help="Credit cards, student loans, etc."
    )

with col2:
    current_savings = st.number_input(
        "💰 Current Savings",
        min_value=0.0,
        value=float(st.session_state.financial_profile.current_savings),
        step=100.0,
        help="Emergency fund + other savings"
    )

with col3:
    risk_tolerance = st.selectbox(
        "📊 Investment Risk Tolerance",
        ["Conservative", "Medium", "Aggressive"],
        index=1
    )

# Update profile
st.session_state.financial_profile = FinancialProfile(
    monthly_income=monthly_income,
    age=age,
    life_stage=life_stage,
    financial_goal=financial_goal,
    debt_amount=debt_amount,
    current_savings=current_savings,
    risk_tolerance=risk_tolerance
)

# =============================================================================
# COMPREHENSIVE BUDGET BREAKDOWN
# =============================================================================

if monthly_income > 0:
    budget = st.session_state.planner.calculate_comprehensive_budget(st.session_state.financial_profile)
    
    st.markdown("## 📊 Your Personalized Gen Z Budget Blueprint")
    
    # Budget overview cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        needs_amount = budget['needs']
        needs_pct = budget['framework']['needs']
        st.markdown(f"""
        <div class="survival-card">
            <h3>🏠 NEEDS ({needs_pct}%)</h3>
            <h2>${needs_amount:.0f}</h2>
            <p>Rent, groceries, utilities, transport, insurance, minimum debt payments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        wants_amount = budget['wants']
        wants_pct = budget['framework']['wants']
        st.markdown(f"""
        <div class="comfort-card">
            <h3>✨ WANTS ({wants_pct}%)</h3>
            <h2>${wants_amount:.0f}</h2>
            <p>Entertainment, dining out, shopping, subscriptions, hobbies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        savings_amount = budget['savings']
        savings_pct = budget['framework']['savings']
        st.markdown(f"""
        <div class="slay-card">
            <h3>📈 SAVINGS ({savings_pct}%)</h3>
            <h2>${savings_amount:.0f}</h2>
            <p>Emergency fund, investments, extra debt payments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if budget['debt_payment'] > 0:
            st.markdown(f"""
            <div class="investment-card">
                <h3>💳 DEBT PAYOFF</h3>
                <h2>${budget['debt_payment']:.0f}</h2>
                <p>Minimum + extra debt payments</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            leftover = budget['net_income_after_budget']
            st.markdown(f"""
            <div class="investment-card">
                <h3>🎉 EXTRA CASH</h3>
                <h2>${leftover:.0f}</h2>
                <p>Bonus for goals!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Emergency Fund Progress
    st.markdown("### 🛡️ Emergency Fund Progress")
    emergency_target = budget['emergency_target']
    current_emergency = st.session_state.financial_profile.current_savings
    progress_pct = (current_emergency / emergency_target) * 100 if emergency_target > 0 else 0
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {min(progress_pct, 100)}%;">
            {progress_pct:.1f}% Complete
        </div>
    </div>
    <p><strong>Goal:</strong> ${emergency_target:.0f} | <strong>Current:</strong> ${current_emergency:.0f} | <strong>Monthly Contribution:</strong> ${budget['emergency_contribution']:.0f}</p>
    """, unsafe_allow_html=True)
    
    # Investment Allocation
    if budget['investment_amount'] > 0:
        st.markdown("### 📈 Investment Allocation Strategy")
        
        investment_allocation = st.session_state.planner.get_investment_allocation(
            budget['investment_amount'], st.session_state.financial_profile
        )
        
        cols = st.columns(len(investment_allocation))
        for i, (investment_type, amount) in enumerate(investment_allocation.items()):
            with cols[i]:
                st.markdown(f"""
                <div class="investment-card">
                    <h4>{investment_type}</h4>
                    <h3>${amount:.0f}</h3>
                    <p>Monthly allocation</p>
                </div>
                """, unsafe_allow_html=True)
    
    # =============================================================================
    # GOAL TRACKING SYSTEM
    # =============================================================================
    
    st.markdown("## 🎯 Goal Tracking Dashboard")
    
    for goal in st.session_state.goal_trackers:
        progress = (goal.current_amount / goal.target_amount) * 100 if goal.target_amount > 0 else 0
        days_left = (goal.target_date - datetime.now()).days
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="goal-tracker">
                <h4>{goal.name} - {goal.category}</h4>
                <div class="progress-container">
                    <div class="progress-fill" style="width: {min(progress, 100)}%;">
                        ${goal.current_amount:.0f} / ${goal.target_amount:.0f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="milestone-badge">
                {progress:.1f}% Complete
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="milestone-badge">
                {days_left} days left
            </div>
            """, unsafe_allow_html=True)
    
    # =============================================================================
    # FINANCIAL MILESTONES & ROADMAP
    # =============================================================================
    
    st.markdown("### 🗺️ Your Financial Roadmap")
    
    milestones = st.session_state.planner.generate_milestone_plan(st.session_state.financial_profile)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Upcoming Milestones")
        for milestone in milestones:
            st.markdown(f"""
            <div class="financial-tip">
                <strong>Age {milestone['age']}:</strong> {milestone['goal']}<br>
                <em>Target: ${milestone['target']:,.0f} - {milestone['description']}</em>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Personalized advice
        advice = st.session_state.planner.get_personalized_advice(st.session_state.financial_profile)
        
        st.markdown("#### 💡 Personalized Action Plan")
        
        with st.expander("🚨 Immediate Actions (Next 30 Days)"):
            for tip in advice["immediate"]:
                st.markdown(f"• {tip}")
        
        with st.expander("📅 Short-term Goals (Next 6 Months)"):
            for tip in advice["short_term"]:
                st.markdown(f"• {tip}")
        
        with st.expander("🌟 Long-term Vision (1+ Years)"):
            for tip in advice["long_term"]:
                st.markdown(f"• {tip}")
        
        with st.expander(f"🎭 {st.session_state.financial_profile.life_stage.value} Specific"):
            for tip in advice["life_stage_specific"]:
                st.markdown(f"• {tip}")

# =============================================================================
# ENHANCED VIBE CHECK & AI COACHING
# =============================================================================

st.markdown("## 🌈 Daily Vibe Check & AI Coaching")

col1, col2, col3 = st.columns(3)

with col1:
    current_vibe = st.selectbox(
        "How are you feeling about money today?",
        options=list(VibeType),
        format_func=lambda x: f"{x.value} {x.name.title()}",
        index=list(VibeType).index(st.session_state.current_vibe)
    )
    st.session_state.current_vibe = current_vibe

with col2:
    stress_level = st.slider("Money stress level", 1, 10, 5)

with col3:
    confidence_level = st.slider("Financial confidence", 1, 10, 6)

# Enhanced AI Response
if monthly_income > 0:
    budget = st.session_state.planner.calculate_comprehensive_budget(st.session_state.financial_profile)
    coaching_response = st.session_state.agent.get_contextual_coaching(
        st.session_state.financial_profile, budget
    )
    vibe_response = st.session_state.agent.vibe_responses[current_vibe][0]
    
    st.markdown(f"""
    <div class="chat-bubble">
        <strong>FinBot says:</strong> {vibe_response}<br><br>
        <strong>Personal Coaching:</strong> {coaching_response}
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# MONEY DASHBOARD WITH ENHANCED METRICS
# =============================================================================

st.markdown("## 💰 Your Money Mood Board")

transactions = st.session_state.transactions
total_spent = sum(t.amount for t in transactions)
avg_daily = total_spent / 7
joy_spending = sum(t.amount for t in transactions if t.category == SpendingCategory.JOY)
essential_spending = sum(t.amount for t in transactions if t.category == SpendingCategory.ESSENTIAL)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="money-card">
        <h3>💸 Total Spent</h3>
        <h2>${total_spent:.2f}</h2>
        <p>Last 7 days</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="money-card">
        <h3>📅 Daily Average</h3>
        <h2>${avg_daily:.2f}</h2>
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
            <h2>${budget_remaining:.0f}</h2>
            <p>This month</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="money-card">
            <h3>✨ Joy Spending</h3>
            <h2>${joy_spending:.2f}</h2>
            <p>Self-care investments</p>
        </div>
        """, unsafe_allow_html=True)

with col5:
    if st.session_state.financial_profile.current_savings > 0:
        savings_growth = st.session_state.financial_profile.current_savings
        st.markdown(f"""
        <div class="money-card">
            <h3>📈 Savings</h3>
            <h2>${savings_growth:.0f}</h2>
            <p>Total saved</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="money-card">
            <h3>🏠 Essentials</h3>
            <h2>${essential_spending:.2f}</h2>
            <p>Responsible spending</p>
        </div>
        """, unsafe_allow_html=True)

# Budget vs Reality Check
if monthly_income > 0:
    st.markdown("### 📊 Budget vs Reality Check")
    budget = st.session_state.planner.calculate_comprehensive_budget(st.session_state.financial_profile)
    
    current_month_spending = total_spent * 4.33
    needs_budget = budget['needs']
    wants_budget = budget['wants']
    
    current_needs = essential_spending * 4.33
    current_wants = joy_spending * 4.33
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        needs_progress = (current_needs / needs_budget * 100) if needs_budget > 0 else 0
        st.markdown(f"**🏠 Needs: ${current_needs:.0f} / ${needs_budget:.0f}**")
        st.progress(min(needs_progress / 100, 1.0))
        if needs_progress > 100:
            st.markdown('<div class="warning-card">⚠️ Over budget on needs!</div>', unsafe_allow_html=True)
        
    with col2:
        wants_progress = (current_wants / wants_budget * 100) if wants_budget > 0 else 0
        st.markdown(f"**✨ Wants: ${current_wants:.0f} / ${wants_budget:.0f}**")
        st.progress(min(wants_progress / 100, 1.0))
        if wants_progress > 100:
            st.markdown('<div class="warning-card">⚠️ Over budget on wants!</div>', unsafe_allow_html=True)
    
    with col3:
        total_budget = needs_budget + wants_budget
        total_spent_month = current_needs + current_wants
        overall_progress = (total_spent_month / total_budget * 100) if total_budget > 0 else 0
        st.markdown(f"**💰 Overall: ${total_spent_month:.0f} / ${total_budget:.0f}**")
        st.progress(min(overall_progress / 100, 1.0))
        if overall_progress < 80:
            st.markdown('<div class="success-card">🎉 Under budget! Great job!</div>', unsafe_allow_html=True)

# =============================================================================
# SPENDING ANALYSIS CHARTS
# =============================================================================

st.markdown("## 📊 Spending Vibes Analysis")

col1, col2 = st.columns(2)

with col1:
    category_data = {}
    for transaction in transactions:
        cat_name = transaction.category.value
        category_data[cat_name] = category_data.get(cat_name, 0) + transaction.amount
    
    if category_data:
        fig_pie = px.pie(
            values=list(category_data.values()),
            names=list(category_data.keys()),
            title="💫 Spending by Vibe Category",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    daily_spending = {}
    for transaction in transactions:
        date_str = transaction.date.strftime('%Y-%m-%d')
        daily_spending[date_str] = daily_spending.get(date_str, 0) + transaction.amount
    
    if daily_spending:
        df_daily = pd.DataFrame(list(daily_spending.items()), columns=['Date', 'Amount'])
        df_daily['Date'] = pd.to_datetime(df_daily['Date'])
        
        fig_line = px.line(
            df_daily,
            x='Date',
            y='Amount',
            title='📈 Daily Spending Trend',
            color_discrete_sequence=['#667eea']
        )
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig_line, use_container_width=True)

# =============================================================================
# TRANSACTION LOG & INTERACTIVE FEATURES
# =============================================================================

st.markdown("## 🧾 Recent Spending Tea ☕")

df_transactions = pd.DataFrame([
    {
        'Date': t.date.strftime('%m/%d'),
        'Vibe': t.category.value,
        'Amount': f"${t.amount:.2f}",
        'Description': t.description,
        'Merchant': t.merchant,
        'Mood Impact': '😊' if t.vibe_impact > 0 else '😐' if t.vibe_impact == 0 else '😔'
    }
    for t in sorted(transactions, key=lambda x: x.date, reverse=True)
])

st.dataframe(df_transactions, use_container_width)
with col3:
    if st.session_state.financial_profile.current_savings > 0:
        savings_growth = st.session_state.financial_profile.current_savings
        st.markdown(f"""
        <div class="money-card">
            <h3>📈 Savings</h3>
            <h2>${savings_growth:.0f}</h2>
            <p>Total saved</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="money-card">
            <h3>🏠 Essentials</h3>
            <h2>${essential_spending:.2f}</h2>
            <p>Responsible spending</p>
        </div>
        """, unsafe_allow_html=True)

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
        <h3>Total Monthly Income: ${total_monthly_income:,.2f}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="survival-card">
            <h3>🏠 NEEDS ({needs_percent}%)</h3>
            <h2>${needs_amount:,.0f}</h2>
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
            <h2>${wants_amount:,.0f}</h2>
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
            <h2>${adjusted_savings:,.0f}</h2>
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
                <h2>${total_debt_focus:,.0f}</h2>
                <div style="font-size: 0.9em; margin-top: 10px;">
                    <strong>Strategy:</strong><br>
                    • Minimum: ${monthly_debt_payment:,.0f}<br>
                    • Extra: ${debt_payoff_extra:,.0f}<br>
                    • Total Focus<br>
                    • Avalanche Method
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="investment-card">
                <h3>🚀 BONUS POWER</h3>
                <h2>${adjusted_savings:,.0f}</h2>
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
            <h2>${emergency_target:,.0f}</h2>
            <p>{emergency_months} months of expenses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="goal-tracker">
            <h4>💰 Current Progress</h4>
            <h2>${current_savings_amount:,.0f}</h2>
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
                <h2>${available_for_investment:,.0f}</h2>
                <p>Available after emergency fund</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="investment-card">
                <h4>📈 Stocks/ETFs ({stock_percent}%)</h4>
                <h2>${stock_amount:,.0f}</h2>
                <p>VTI, VXUS, Growth funds</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="investment-card">
                <h4>🏛️ Bonds ({bond_percent}%)</h4>
                <h2>${bond_amount:,.0f}</h2>
                <p>BND, Treasury bonds</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="investment-card">
                <h4>💵 Cash/HYSA ({cash_percent}%)</h4>
                <h2>${cash_amount:,.0f}</h2>
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
                <strong>Monthly Investment:</strong> ${available_for_investment:,.0f}
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
                    <p>Total Payment: ${total_debt_payment:,.0f}/month</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="survival-card">
                    <h4>💰 Total Interest Saved</h4>
                    <p>By paying ${total_debt_payment:,.0f}/month instead of minimums:</p>
                    <h3>Interest: ${total_interest:,.0f}</h3>
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
                <h2>${future_monthly_boost:,.0f}</h2>
                <p>Extra for investments/goals</p>
                <small>Annual boost: ${annual_boost:,.0f}</small>
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
                <h2>${goal_amount:,.0f}</h2>
                <p>Target in {goal_timeline}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="goal-tracker">
                <h4>💰 Required Monthly</h4>
                <h2>${required_monthly:,.0f}</h2>
                <p>To reach your goal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            feasibility = "✅ Totally Doable!" if required_monthly <= available_for_goal else "⚠️ Needs Adjustment"
            st.markdown(f"""
            <div class="goal-tracker">
                <h4>📊 Feasibility</h4>
                <h2>{feasibility}</h2>
                <p>Available: ${available_for_goal:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Goal progress tracking
        if required_monthly <= available_for_goal:
            st.markdown(f"""
            <div class="success-card">
                <h4>🎉 Goal Strategy Approved!</h4>
                <p><strong>Monthly Allocation:</strong> ${required_monthly:,.0f} from your ${adjusted_savings:,.0f} savings budget</p>
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
                <p><strong>Option 2:</strong> Reduce goal to ${available_for_goal * months:,.0f}</p>
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
                    <h2>${future_value:,.0f}</h2>
                    <div style="font-size: 0.8em; margin-top: 10px;">
                        <p>Contributions: ${total_contributions:,.0f}</p>
                        <p>Growth: ${investment_growth:,.0f}</p>
                        <p>Monthly: ${monthly_investment:,.0f}</p>
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
                <h3>${target_net_worth:,.0f}</h3>
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
            monthly_goals.append(f"🛡️ Save ${emergency_monthly_need:,.0f} for emergency fund")
        
        monthly_goals.append(f"📊 Track all expenses and stay within ${wants_amount:,.0f} fun budget")
        monthly_goals.append(f"💰 Automate ${adjusted_savings:,.0f} monthly savings")
        
        if current_debt > 0:
            monthly_goals.append(f"💳 Pay ${total_debt_payment:,.0f} toward debt elimination")
        
        monthly_goals.append("📚 Read one personal finance book or take online course")
        monthly_goals.append("🎯 Set up goal tracking for your biggest financial priority")
        
        for goal in monthly_goals:
            st.markdown(f"• {goal}")
    
   # Final summary card
st.markdown(f"""
<div class="main-header">
    <h2>🎉 Your Financial Power Summary</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px;">
        <div style="text-align: center;">
            <h3>💰 Monthly Power</h3>
            <h2>${total_monthly_income:,.0f}</h2>
            <p>Total Income</p>
        </div>
        <div style="text-align: center;">
            <h3>🎯 Savings Rate</h3>
            <h2>{(adjusted_savings/total_monthly_income*100):.1f}%</h2>
            <p>Wealth Building</p>
        </div>
        <div style="text-align: center;">
            <h3>🚀 Investment Ready</h3>
            <h2>${available_for_investment:,.0f}</h2>
            <p>Monthly Growth</p>
        </div>
        <div style="text-align: center;">
            <h3>⏰ Debt Freedom</h3>
            <h2>{months_to_payoff:.1f if 'months_to_payoff' in locals() and months_to_payoff != float('inf') else 'N/A'}</h2>
            <p>Months to Freedom</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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

# Motivational closing
st.markdown(f"""
<div class="success-card">
    <h3>✨ You're Already Winning!</h3>
    <p>Just by using this calculator and thinking about your financial future, you're ahead of 70% of people your age. 
    Your {lifestyle_mode.split('(')[0]} approach with ${total_monthly_income:,.0f} monthly income puts you on track for 
    serious wealth building. Remember: every dollar you save in your 20s becomes $10+ in your future. 
    You've got this! 🚀</p>
</div>
""", unsafe_allow_html=True)

# Beautiful Footer
st.markdown("""
<div style="margin-top: 80px; padding: 40px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; text-align: center; color: white; position: relative; overflow: hidden;">
    <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><defs><pattern id=\"grain\" width=\"100\" height=\"100\" patternUnits=\"userSpaceOnUse\"><circle cx=\"20\" cy=\"20\" r=\"1\" fill=\"white\" opacity=\"0.1\"/><circle cx=\"80\" cy=\"40\" r=\"1\" fill=\"white\" opacity=\"0.1\"/><circle cx=\"40\" cy=\"60\" r=\"1\" fill=\"white\" opacity=\"0.1\"/><circle cx=\"60\" cy=\"80\" r=\"1\" fill=\"white\" opacity=\"0.1\"/></pattern></defs><rect width=\"100\" height=\"100\" fill=\"url(%23grain)\"/></svg>'); opacity: 0.3;"></div>
    
    <div style="position: relative; z-index: 2;">
        <div style="font-size: 3rem; margin-bottom: 20px;">
            💸✨🚀
        </div>
        
        <h2 style="margin: 0; font-size: 2.5rem; font-weight: bold; background: linear-gradient(45deg, #fff, #f0f8ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            FinAura
        </h2>
        
        <p style="font-size: 1.2rem; margin: 10px 0; font-style: italic; opacity: 0.9;">
            Where Gen Z Vibes Meet Financial Freedom
        </p>
        
        <div style="height: 2px; width: 100px; background: linear-gradient(90deg, transparent, white, transparent); margin: 20px auto;"></div>
        
        <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin: 20px 0; flex-wrap: wrap;">
            <span style="font-size: 1.1rem;">Made with</span>
            <div style="display: inline-flex; align-items: center; gap: 5px;">
                <span style="font-size: 1.8rem; animation: heartbeat 1.5s ease-in-out infinite;">💖</span>
                <span style="font-size: 1.8rem;">✨</span>
                <span style="font-size: 1.8rem;">🎯</span>
            </div>
            <span style="font-size: 1.1rem;">by</span>
            <span style="font-size: 1.3rem; font-weight: bold; background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                Eesha Tariq
            </span>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 20px; margin: 25px 0; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3);">
                <span style="font-size: 0.9rem;">🌟 Financial Empowerment</span>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3);">
                <span style="font-size: 0.9rem;">💪 Gen Z Strong</span>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3);">
                <span style="font-size: 0.9rem;">🚀 Future Ready</span>
            </div>
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.3);">
            <p style="font-size: 0.9rem; opacity: 0.8; margin: 5px 0;">
                "Your financial journey starts with a single step. Every dollar saved today is freedom earned tomorrow."
            </p>
            <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 15px;">
                © 2024 FinAura | Empowering the next generation of wealth builders
            </p>
        </div>
        
        <div style="position: absolute; top: 20px; right: 20px; font-size: 2rem; opacity: 0.3;">
            💎
        </div>
        <div style="position: absolute; bottom: 20px; left: 20px; font-size: 1.5rem; opacity: 0.3;">
            ⭐
        </div>
    </div>
</div>

<style>
@keyframes heartbeat {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.footer-icon {
    animation: float 3s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# Optional: Add some final spacing
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
