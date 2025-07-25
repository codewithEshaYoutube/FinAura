# 💸 FinAura: Your Gen Z CFO – Where Vibes Meet Value
# Streamlit App with Cool UI and Full Functionality

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
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA MODELS & CORE LOGIC
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

@dataclass
class Transaction:
    date: datetime
    amount: float
    description: str
    category: SpendingCategory
    merchant: str = ""
    vibe_impact: float = 0.0  # -1 to 1, how this affects your vibe

@dataclass
class VibeData:
    current_vibe: VibeType
    money_stress_level: int  # 1-10
    spending_guilt: int  # 1-10
    financial_confidence: int  # 1-10

class FinAuraAgent:
    """The Gen Z AI Agent that gets your vibes"""
    
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
        
        self.spending_wisdom = {
            SpendingCategory.ESSENTIAL: "Proud of you for prioritizing needs! 🏠",
            SpendingCategory.JOY: "Joy spending in moderation = self-care ✨",
            SpendingCategory.OOPS: "We've all been there! No shame, just learn 😅",
            SpendingCategory.INVESTMENT: "Future you is gonna thank present you! 📈"
        }
    
    def get_vibe_response(self, vibe: VibeType) -> str:
        return random.choice(self.vibe_responses.get(vibe, ["You're doing great! 💜"]))
    
    def analyze_spending_vibe(self, transactions: List[Transaction]) -> Dict:
        total_spent = sum(t.amount for t in transactions)
        joy_spending = sum(t.amount for t in transactions if t.category == SpendingCategory.JOY)
        oops_spending = sum(t.amount for t in transactions if t.category == SpendingCategory.OOPS)
        
        # Calculate vibe metrics
        joy_ratio = joy_spending / total_spent if total_spent > 0 else 0
        oops_ratio = oops_spending / total_spent if total_spent > 0 else 0
        
        vibe_score = 5 + (joy_ratio * 3) - (oops_ratio * 4)  # 1-10 scale
        
        return {
            "vibe_score": max(1, min(10, vibe_score)),
            "dominant_category": max(
                [SpendingCategory.ESSENTIAL, SpendingCategory.JOY, SpendingCategory.OOPS],
                key=lambda cat: sum(t.amount for t in transactions if t.category == cat)
            ),
            "spending_personality": self._get_spending_personality(joy_ratio, oops_ratio)
        }
    
    def _get_spending_personality(self, joy_ratio: float, oops_ratio: float) -> str:
        if joy_ratio > 0.3:
            return "💖 Self-Care Spender"
        elif oops_ratio > 0.2:
            return "🎭 Impulse Explorer"
        else:
            return "🧠 Mindful Manager"

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

if 'transactions' not in st.session_state:
    # Sample Gen Z transactions
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
    st.session_state.agent = FinAuraAgent()

# =============================================================================
# MAIN APP INTERFACE
# =============================================================================

# Header with Gen Z energy
st.markdown("""
<div class="main-header">
    <h1>💸 FinAura: Your Gen Z CFO</h1>
    <p><em>"Forget spreadsheets. Feel your finances."</em></p>
    <p>Where vibes meet value ✨</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# VIBE CHECK SECTION
# =============================================================================

st.markdown("## 🌈 Daily Vibe Check")

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

# AI Response based on vibe
vibe_response = st.session_state.agent.get_vibe_response(current_vibe)
st.markdown(f"""
<div class="chat-bubble">
    <strong>FinBot says:</strong> {vibe_response}
</div>
""", unsafe_allow_html=True)

# =============================================================================
# MONEY DASHBOARD
# =============================================================================

st.markdown("## 💰 Your Money Mood Board")

# Calculate key metrics
transactions = st.session_state.transactions
total_spent = sum(t.amount for t in transactions)
avg_daily = total_spent / 7  # Last 7 days
joy_spending = sum(t.amount for t in transactions if t.category == SpendingCategory.JOY)
essential_spending = sum(t.amount for t in transactions if t.category == SpendingCategory.ESSENTIAL)

# Money cards
col1, col2, col3, col4 = st.columns(4)

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
    st.markdown(f"""
    <div class="money-card">
        <h3>✨ Joy Spending</h3>
        <h2>${joy_spending:.2f}</h2>
        <p>Self-care investments</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    joy_ratio = (joy_spending / total_spent * 100) if total_spent > 0 else 0
    st.markdown(f"""
    <div class="money-card">
        <h3>😊 Joy Ratio</h3>
        <h2>{joy_ratio:.1f}%</h2>
        <p>Happiness spending</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# SPENDING BREAKDOWN CHARTS
# =============================================================================

st.markdown("## 📊 Spending Vibes Analysis")

col1, col2 = st.columns(2)

with col1:
    # Category breakdown pie chart
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
    # Daily spending trend
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
# TRANSACTION LOG WITH GEN Z FLAIR
# =============================================================================

st.markdown("## 🧾 Recent Spending Tea ☕")

# Create DataFrame for display
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

st.dataframe(
    df_transactions,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Amount": st.column_config.TextColumn(width="small"),
        "Mood Impact": st.column_config.TextColumn(width="small"),
    }
)

# =============================================================================
# AI INSIGHTS & RECOMMENDATIONS
# =============================================================================

st.markdown("## 🤖 FinBot Insights")

# Get AI analysis
spending_analysis = st.session_state.agent.analyze_spending_vibe(transactions)

col1, col2 = st.columns(2)

with col1:
    vibe_score = spending_analysis['vibe_score']
    if vibe_score >= 8:
        insight_class = "success-card"
        insight_emoji = "🔥"
        insight_text = "Your spending game is absolutely iconic! Keep this energy."
    elif vibe_score >= 6:
        insight_class = "vibe-card"
        insight_emoji = "✨"
        insight_text = "Solid vibes! Your money mindset is in a good place."
    else:
        insight_class = "warning-card"
        insight_emoji = "💜"
        insight_text = "No judgment! Every financial journey has ups and downs."
    
    st.markdown(f"""
    <div class="{insight_class}">
        <h3>{insight_emoji} Vibe Score: {vibe_score:.1f}/10</h3>
        <p>{insight_text}</p>
        <p><strong>Your spending personality:</strong> {spending_analysis['spending_personality']}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Personalized recommendations
    recommendations = []
    
    oops_spending = sum(t.amount for t in transactions if t.category == SpendingCategory.OOPS)
    if oops_spending > 50:
        recommendations.append("💡 Try the '24-hour rule' before impulse purchases")
    
    if joy_spending < total_spent * 0.1:
        recommendations.append("✨ You deserve some joy spending! Treat yourself mindfully")
    
    if essential_spending > total_spent * 0.7:
        recommendations.append("🏠 Great job prioritizing essentials! You're so responsible")
    
    if not recommendations:
        recommendations.append("🌟 Your spending balance is chef's kiss perfect!")
    
    st.markdown("### 💭 Personalized Recommendations")
    for rec in recommendations:
        st.markdown(f"- {rec}")

# =============================================================================
# INTERACTIVE FEATURES
# =============================================================================

st.markdown("## 🎮 Interactive Zone")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔮 Predict Next Week", type="primary"):
        predicted_spending = avg_daily * 7 * random.uniform(0.8, 1.2)
        st.success(f"Based on your vibes, you'll likely spend ${predicted_spending:.2f} next week!")

with col2:
    if st.button("💸 Add Quick Transaction"):
        # Simple transaction adder
        with st.expander("Add a transaction"):
            desc = st.text_input("What did you buy?", placeholder="bubble tea emergency")
            amount = st.number_input("How much?", min_value=0.01, step=0.01)
            category = st.selectbox("Vibe category", options=list(SpendingCategory), format_func=lambda x: x.value)
            
            if st.button("Add to my spending"):
                new_transaction = Transaction(
                    datetime.now(),
                    amount,
                    desc,
                    category,
                    vibe_impact=random.uniform(-0.3, 0.3)
                )
                st.session_state.transactions.append(new_transaction)
                st.success("Added! Your spending vibe has been updated ✨")
                st.rerun()

with col3:
    if st.button("📱 Send Vibe Update"):
        st.info("📲 Vibe update sent to your phone! (This would integrate with WhatsApp in production)")

# =============================================================================
# WEEKLY DIGEST
# =============================================================================

st.markdown("## 📰 Your Weekly Financial Digest")

st.markdown(f"""
<div class="vibe-card">
    <h3>💌 This Week's Money Story</h3>
    <p>Hey bestie! This week you spent <strong>${total_spent:.2f}</strong> across {len(transactions)} transactions. 
    Your biggest vibe was <strong>{spending_analysis['dominant_category'].value}</strong> spending, 
    which honestly? No judgment here.</p>
    
    <p>Your <strong>{spending_analysis['spending_personality']}</strong> energy is showing, 
    and your vibe score of <strong>{spending_analysis['vibe_score']:.1f}/10</strong> means you're 
    {"absolutely crushing it! 🔥" if spending_analysis['vibe_score'] >= 8 else "doing pretty well! ✨" if spending_analysis['vibe_score'] >= 6 else "being kind to yourself during a tough time 💜"}</p>
    
    <p><em>Remember: Your worth isn't your spending. You're doing better than you think! 💜</em></p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# FOOTER WITH SOCIAL VIBES
# =============================================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💜 FinAura Team")
    st.markdown("Built with love by **Team Aptiva AI**")
    st.markdown("**Eesha Tariq** - Gen Z Systems Thinker & Code Queen 👑")

with col2:
    st.markdown("### 🏆 Hackathon")
    st.markdown("**Push the Limits – Beyond Automation**")
    st.markdown("*#FinAura #VibesBasedBudgeting #AgenticAI*")

with col3:
    st.markdown("### 🌍 Global Vibes")
    st.markdown("🇵🇰 Pakistan | 🇮🇳 India | 🇬🇧 UK")
    st.markdown("*Where financial wellness meets emotional wellness*")

# Hidden debug info for development
if st.checkbox("🔧 Debug Mode (Dev Only)"):
    st.json({
        "total_transactions": len(transactions),
        "current_vibe": current_vibe.name,
        "vibe_score": spending_analysis['vibe_score'],
        "spending_personality": spending_analysis['spending_personality']
    })