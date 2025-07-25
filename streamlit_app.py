import streamlit as st
import pandas as pd
import math
from pathlib import Path
# FinSphere: Autonomous Financial Manager
# Multi-Agent AI System for Complete Finance Automation

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import sqlite3
from abc import ABC, abstractmethod
import pandas as pd
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# CORE MODELS & INTERFACES
# =============================================================================

class ActionType(Enum):
    TRANSACTION_CATEGORIZE = "transaction_categorize"
    BUDGET_ADJUST = "budget_adjust"
    PAYMENT_EXECUTE = "payment_execute"
    REPORT_GENERATE = "report_generate"
    TAX_PREPARE = "tax_prepare"
    INVOICE_SEND = "invoice_send"
    INVESTMENT_SUGGEST = "investment_suggest"
    ALERT_SEND = "alert_send"

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

@dataclass
class Transaction:
    id: str
    date: datetime
    amount: float
    description: str
    category: Optional[str] = None
    account: str = "main"
    type: str = "expense"  # expense, income, transfer
    is_recurring: bool = False
    merchant: Optional[str] = None

@dataclass
class Budget:
    category: str
    allocated: float
    spent: float
    period: str = "monthly"
    auto_adjust: bool = True

@dataclass
class AgentAction:
    id: str
    agent_name: str
    action_type: ActionType
    data: Dict[str, Any]
    timestamp: datetime
    status: ApprovalStatus = ApprovalStatus.PENDING
    approval_required: bool = True
    confidence: float = 0.8

# =============================================================================
# AGENT INTERFACE & MEMORY SYSTEM
# =============================================================================

class AgentMemory:
    """Persistent memory system for agents"""
    
    def __init__(self, db_path: str = "finsphere.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                date TEXT,
                amount REAL,
                description TEXT,
                category TEXT,
                account TEXT,
                type TEXT,
                merchant TEXT
            )
        ''')
        
        # Agent actions log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_actions (
                id TEXT PRIMARY KEY,
                agent_name TEXT,
                action_type TEXT,
                data TEXT,
                timestamp TEXT,
                status TEXT,
                confidence REAL
            )
        ''')
        
        # Budget table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                allocated REAL,
                spent REAL,
                period TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_transaction(self, transaction: Transaction):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO transactions 
            (id, date, amount, description, category, account, type, merchant)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction.id,
            transaction.date.isoformat(),
            transaction.amount,
            transaction.description,
            transaction.category,
            transaction.account,
            transaction.type,
            transaction.merchant
        ))
        conn.commit()
        conn.close()
    
    def get_transactions(self, days: int = 30) -> List[Transaction]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT * FROM transactions 
            WHERE date >= ? 
            ORDER BY date DESC
        ''', (since_date,))
        
        transactions = []
        for row in cursor.fetchall():
            transactions.append(Transaction(
                id=row[0],
                date=datetime.fromisoformat(row[1]),
                amount=row[2],
                description=row[3],
                category=row[4],
                account=row[5],
                type=row[6],
                merchant=row[7]
            ))
        
        conn.close()
        return transactions

class BaseAgent(ABC):
    """Base class for all FinSphere agents"""
    
    def __init__(self, name: str, memory: AgentMemory):
        self.name = name
        self.memory = memory
        self.actions_log: List[AgentAction] = []
    
    @abstractmethod
    async def execute(self) -> List[AgentAction]:
        """Execute agent's main functionality"""
        pass
    
    def log_action(self, action: AgentAction):
        """Log an action for audit trail"""
        self.actions_log.append(action)
        logger.info(f"{self.name}: {action.action_type.value} - {action.data}")

# =============================================================================
# SPECIALIZED AGENTS
# =============================================================================

class BookkeepingAgent(BaseAgent):
    """Autonomous bookkeeping and transaction categorization"""
    
    def __init__(self, memory: AgentMemory):
        super().__init__("BookkeepingAgent", memory)
        self.category_rules = {
            'food': ['restaurant', 'grocery', 'cafe', 'pizza', 'mcdonald'],
            'transport': ['uber', 'taxi', 'gas', 'fuel', 'parking'],
            'utilities': ['electric', 'water', 'internet', 'phone'],
            'entertainment': ['netflix', 'spotify', 'movie', 'game'],
            'shopping': ['amazon', 'store', 'mall', 'clothing'],
            'health': ['pharmacy', 'doctor', 'hospital', 'medical']
        }
    
    async def execute(self) -> List[AgentAction]:
        """Auto-categorize recent transactions"""
        actions = []
        transactions = self.memory.get_transactions(7)  # Last 7 days
        
        for transaction in transactions:
            if not transaction.category:
                category = self._categorize_transaction(transaction)
                if category:
                    transaction.category = category
                    self.memory.save_transaction(transaction)
                    
                    action = AgentAction(
                        id=f"cat_{transaction.id}",
                        agent_name=self.name,
                        action_type=ActionType.TRANSACTION_CATEGORIZE,
                        data={
                            "transaction_id": transaction.id,
                            "category": category,
                            "confidence": 0.85
                        },
                        timestamp=datetime.now(),
                        approval_required=False
                    )
                    actions.append(action)
                    self.log_action(action)
        
        return actions
    
    def _categorize_transaction(self, transaction: Transaction) -> Optional[str]:
        """Smart transaction categorization using rules"""
        description = transaction.description.lower()
        merchant = (transaction.merchant or "").lower()
        
        for category, keywords in self.category_rules.items():
            if any(keyword in description or keyword in merchant for keyword in keywords):
                return category
        
        # Default categorization based on amount patterns
        if transaction.amount > 1000:
            return 'major_expense'
        elif transaction.type == 'income':
            return 'revenue'
        
        return 'miscellaneous'

class BudgetingAgent(BaseAgent):
    """Adaptive budgeting and spending optimization"""
    
    def __init__(self, memory: AgentMemory):
        super().__init__("BudgetingAgent", memory)
        self.default_budgets = {
            'food': 800,
            'transport': 300,
            'utilities': 200,
            'entertainment': 150,
            'shopping': 400,
            'health': 200
        }
    
    async def execute(self) -> List[AgentAction]:
        """Monitor spending and adjust budgets"""
        actions = []
        transactions = self.memory.get_transactions(30)
        
        # Calculate spending by category
        spending = {}
        for transaction in transactions:
            if transaction.type == 'expense' and transaction.category:
                spending[transaction.category] = spending.get(transaction.category, 0) + transaction.amount
        
        # Check budget overruns and suggest adjustments
        for category, spent in spending.items():
            budget_limit = self.default_budgets.get(category, 0)
            
            if spent > budget_limit * 1.2:  # 20% over budget
                action = AgentAction(
                    id=f"budget_alert_{category}",
                    agent_name=self.name,
                    action_type=ActionType.BUDGET_ADJUST,
                    data={
                        "category": category,
                        "current_spent": spent,
                        "budget_limit": budget_limit,
                        "overage_percent": ((spent - budget_limit) / budget_limit) * 100,
                        "suggestion": "reduce_spending" if spent > budget_limit * 1.5 else "increase_budget"
                    },
                    timestamp=datetime.now(),
                    approval_required=True
                )
                actions.append(action)
                self.log_action(action)
        
        return actions

class PaymentAgent(BaseAgent):
    """Smart payment management and cash flow optimization"""
    
    def __init__(self, memory: AgentMemory):
        super().__init__("PaymentAgent", memory)
        self.recurring_payments = [
            {"name": "Office Rent", "amount": 2000, "due_date": 1},
            {"name": "Internet", "amount": 100, "due_date": 15},
            {"name": "Software Subscriptions", "amount": 299, "due_date": 20}
        ]
    
    async def execute(self) -> List[AgentAction]:
        """Execute smart payment scheduling"""
        actions = []
        today = datetime.now().day
        
        for payment in self.recurring_payments:
            if today == payment["due_date"]:
                action = AgentAction(
                    id=f"payment_{payment['name'].replace(' ', '_').lower()}",
                    agent_name=self.name,
                    action_type=ActionType.PAYMENT_EXECUTE,
                    data={
                        "payment_name": payment["name"],
                        "amount": payment["amount"],
                        "due_date": payment["due_date"],
                        "priority": "high" if payment["amount"] > 1000 else "medium"
                    },
                    timestamp=datetime.now(),
                    approval_required=payment["amount"] > 500
                )
                actions.append(action)
                self.log_action(action)
        
        return actions

class ReportingAgent(BaseAgent):
    """Autonomous financial reporting and analysis"""
    
    def __init__(self, memory: AgentMemory):
        super().__init__("ReportingAgent", memory)
    
    async def execute(self) -> List[AgentAction]:
        """Generate comprehensive financial reports"""
        actions = []
        transactions = self.memory.get_transactions(30)
        
        # Calculate key metrics
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
        net_cash_flow = total_income - total_expenses
        
        # Spending by category
        category_spending = {}
        for t in transactions:
            if t.type == 'expense' and t.category:
                category_spending[t.category] = category_spending.get(t.category, 0) + t.amount
        
        report_data = {
            "period": "last_30_days",
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_cash_flow": net_cash_flow,
            "category_breakdown": category_spending,
            "transaction_count": len(transactions),
            "average_transaction": total_expenses / len([t for t in transactions if t.type == 'expense']) if transactions else 0
        }
        
        action = AgentAction(
            id=f"report_{datetime.now().strftime('%Y%m%d')}",
            agent_name=self.name,
            action_type=ActionType.REPORT_GENERATE,
            data=report_data,
            timestamp=datetime.now(),
            approval_required=False
        )
        actions.append(action)
        self.log_action(action)
        
        return actions

class InvoiceAgent(BaseAgent):
    """Automated invoice generation and tracking"""
    
    def __init__(self, memory: AgentMemory):
        super().__init__("InvoiceAgent", memory)
        self.pending_invoices = [
            {"client": "ABC Corp", "amount": 5000, "due_date": datetime.now() + timedelta(days=7)},
            {"client": "XYZ Ltd", "amount": 3500, "due_date": datetime.now() + timedelta(days=14)}
        ]
    
    async def execute(self) -> List[AgentAction]:
        """Generate and track invoices"""
        actions = []
        
        for invoice in self.pending_invoices:
            days_until_due = (invoice["due_date"] - datetime.now()).days
            
            if days_until_due <= 3:  # Follow up 3 days before due
                action = AgentAction(
                    id=f"invoice_{invoice['client'].replace(' ', '_').lower()}",
                    agent_name=self.name,
                    action_type=ActionType.INVOICE_SEND,
                    data={
                        "client": invoice["client"],
                        "amount": invoice["amount"],
                        "due_date": invoice["due_date"].isoformat(),
                        "action": "followup" if days_until_due > 0 else "overdue_notice"
                    },
                    timestamp=datetime.now(),
                    approval_required=False
                )
                actions.append(action)
                self.log_action(action)
        
        return actions

class InvestmentAgent(BaseAgent):
    """Smart investment suggestions and portfolio management"""
    
    def __init__(self, memory: AgentMemory):
        super().__init__("InvestmentAgent", memory)
    
    async def execute(self) -> List[AgentAction]:
        """Analyze surplus and suggest investments"""
        actions = []
        transactions = self.memory.get_transactions(90)  # 3 months
        
        # Calculate available surplus
        monthly_income = sum(t.amount for t in transactions if t.type == 'income') / 3
        monthly_expenses = sum(t.amount for t in transactions if t.type == 'expense') / 3
        monthly_surplus = monthly_income - monthly_expenses
        
        if monthly_surplus > 1000:  # Minimum threshold for investment
            investment_suggestions = []
            
            if monthly_surplus > 5000:
                investment_suggestions.append({
                    "type": "mutual_fund",
                    "amount": monthly_surplus * 0.4,
                    "risk": "medium",
                    "expected_return": "12-15%"
                })
            
            if monthly_surplus > 2000:
                investment_suggestions.append({
                    "type": "fixed_deposit",
                    "amount": monthly_surplus * 0.3,
                    "risk": "low",
                    "expected_return": "6-8%"
                })
            
            investment_suggestions.append({
                "type": "liquid_fund",
                "amount": monthly_surplus * 0.3,
                "risk": "very_low",
                "expected_return": "4-6%"
            })
            
            action = AgentAction(
                id=f"investment_suggestion_{datetime.now().strftime('%Y%m')}",
                agent_name=self.name,
                action_type=ActionType.INVESTMENT_SUGGEST,
                data={
                    "monthly_surplus": monthly_surplus,
                    "suggestions": investment_suggestions,
                    "rationale": "Surplus detected, diversified investment recommended"
                },
                timestamp=datetime.now(),
                approval_required=True
            )
            actions.append(action)
            self.log_action(action)
        
        return actions

# =============================================================================
# MAIN FINSPHERE ORCHESTRATOR
# =============================================================================

class FinSphere:
    """Main orchestrator for all financial agents"""
    
    def __init__(self):
        self.memory = AgentMemory()
        self.agents = [
            BookkeepingAgent(self.memory),
            BudgetingAgent(self.memory),
            PaymentAgent(self.memory),
            ReportingAgent(self.memory),
            InvoiceAgent(self.memory),
            InvestmentAgent(self.memory)
        ]
        self.pending_approvals: List[AgentAction] = []
    
    async def run_cycle(self):
        """Execute one complete cycle of all agents"""
        logger.info("🚀 Starting FinSphere agent cycle...")
        
        all_actions = []
        for agent in self.agents:
            try:
                actions = await agent.execute()
                all_actions.extend(actions)
                logger.info(f"✅ {agent.name} completed with {len(actions)} actions")
            except Exception as e:
                logger.error(f"❌ {agent.name} failed: {str(e)}")
        
        # Separate actions by approval requirement
        auto_actions = [a for a in all_actions if not a.approval_required]
        approval_actions = [a for a in all_actions if a.approval_required]
        
        # Execute auto-approved actions
        for action in auto_actions:
            await self.execute_action(action)
        
        # Queue approval-required actions
        self.pending_approvals.extend(approval_actions)
        
        logger.info(f"📊 Cycle complete: {len(auto_actions)} auto-executed, {len(approval_actions)} pending approval")
        return all_actions
    
    async def execute_action(self, action: AgentAction):
        """Execute an approved action"""
        logger.info(f"🔄 Executing: {action.action_type.value}")
        
        # Here you would implement actual execution logic
        # For demo, we'll just log the action
        if action.action_type == ActionType.PAYMENT_EXECUTE:
            logger.info(f"💰 Payment executed: {action.data}")
        elif action.action_type == ActionType.REPORT_GENERATE:
            logger.info(f"📈 Report generated: {json.dumps(action.data, indent=2)[:200]}...")
        elif action.action_type == ActionType.ALERT_SEND:
            logger.info(f"🚨 Alert sent: {action.data}")
        
        action.status = ApprovalStatus.APPROVED
    
    def get_pending_approvals(self) -> List[AgentAction]:
        """Get all actions requiring approval"""
        return [a for a in self.pending_approvals if a.status == ApprovalStatus.PENDING]
    
    def approve_action(self, action_id: str) -> bool:
        """Approve a pending action"""
        for action in self.pending_approvals:
            if action.id == action_id:
                action.status = ApprovalStatus.APPROVED
                asyncio.create_task(self.execute_action(action))
                return True
        return False
    
    def add_sample_data(self):
        """Add sample transactions for demo"""
        sample_transactions = [
            Transaction("tx1", datetime.now() - timedelta(days=1), 45.50, "Starbucks Coffee", merchant="Starbucks"),
            Transaction("tx2", datetime.now() - timedelta(days=2), 120.00, "Uber ride", merchant="Uber"),
            Transaction("tx3", datetime.now() - timedelta(days=3), 2500.00, "Client payment", type="income"),
            Transaction("tx4", datetime.now() - timedelta(days=4), 85.30, "Grocery shopping", merchant="Walmart"),
            Transaction("tx5", datetime.now() - timedelta(days=5), 15.99, "Netflix subscription", merchant="Netflix"),
            Transaction("tx6", datetime.now() - timedelta(days=6), 1200.00, "Office rent", merchant="Property Manager"),
        ]
        
        for transaction in sample_transactions:
            self.memory.save_transaction(transaction)
        
        logger.info("📝 Sample data added to FinSphere")

# =============================================================================
# DEMO & USAGE
# =============================================================================

async def main():
    """Main demo function"""
    print("💼 FinSphere: Autonomous Financial Manager")
    print("🚀 Reimagining finance — no CA, no secretary, just Agentic AI.")
    print("-" * 60)
    
    # Initialize FinSphere
    finsphere = FinSphere()
    
    # Add sample data
    finsphere.add_sample_data()
    
    # Run a complete agent cycle
    actions = await finsphere.run_cycle()
    
    print("\n📊 CYCLE SUMMARY:")
    print(f"Total actions generated: {len(actions)}")
    
    # Show pending approvals
    pending = finsphere.get_pending_approvals()
    if pending:
        print(f"\n⏳ PENDING APPROVALS ({len(pending)}):")
        for action in pending:
            print(f"  • {action.agent_name}: {action.action_type.value}")
            print(f"    Data: {json.dumps(action.data, indent=4)[:200]}...")
            print()
    
    # Show recent transactions
    transactions = finsphere.memory.get_transactions(7)
    print(f"\n📝 RECENT TRANSACTIONS ({len(transactions)}):")
    for t in transactions[:5]:  # Show first 5
        print(f"  • {t.date.strftime('%Y-%m-%d')}: ${t.amount:.2f} - {t.description}")
        print(f"    Category: {t.category or 'Uncategorized'} | Type: {t.type}")
    
    print("\n✨ FinSphere is now running autonomously!")
    print("💡 In production, this would run as a background service with:")
    print("   - Real bank API integrations (Plaid)")
    print("   - WhatsApp/Email notifications")
    print("   - Web dashboard for approvals")
    print("   - Advanced ML for better categorization")

if __name__ == "__main__":
    asyncio.run(main())