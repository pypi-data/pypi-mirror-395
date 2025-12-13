"""
RAFAEL Example: Fintech Application
Demonstrates fraud detection with adaptive resilience
"""

import asyncio
import random
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.rafael_engine import RafaelCore
from core.decorators import AntiFragile
from guardian.guardian_layer import GuardianLayer, MutationChange, ChangeImpact


class FintechApp:
    """Simulated fintech application"""
    
    def __init__(self):
        # Initialize RAFAEL
        self.rafael = RafaelCore(
            app_name="fintech-demo",
            resilience_level="adaptive"
        )
        
        # Initialize Guardian
        self.guardian = GuardianLayer()
        
        # Register critical modules
        self.rafael.register_module("payment_processor")
        self.rafael.register_module("fraud_detector")
        self.rafael.register_module("transaction_validator")
        
        # Set up decorator integration
        AntiFragile.set_core(self.rafael)
        
        print("🔱 RAFAEL Fintech Demo Initialized")
    
    @AntiFragile(
        retry_policy="adaptive",
        max_retries=3,
        timeout=5.0,
        circuit_breaker=True,
        threat_model="financial_fraud"
    )
    async def process_payment(self, transaction: dict) -> dict:
        """
        Process a payment transaction with RAFAEL protection
        """
        print(f"\n💳 Processing transaction: ${transaction['amount']}")
        
        # Simulate payment processing
        await asyncio.sleep(0.1)
        
        # Random failure simulation (10% chance)
        if random.random() < 0.1:
            raise Exception("Payment gateway timeout")
        
        # Check for fraud
        is_fraud = await self.detect_fraud(transaction)
        
        if is_fraud:
            print("⚠️  FRAUD DETECTED - Transaction blocked")
            return {
                "status": "blocked",
                "reason": "fraud_detected",
                "transaction_id": transaction['id']
            }
        
        print("✅ Payment processed successfully")
        return {
            "status": "success",
            "transaction_id": transaction['id'],
            "timestamp": datetime.now().isoformat()
        }
    
    @AntiFragile(
        retry_policy="adaptive",
        fallback="genomic",
        rate_limit=100
    )
    async def detect_fraud(self, transaction: dict) -> bool:
        """
        Detect fraudulent transactions
        RAFAEL automatically learns and adapts fraud patterns
        """
        # Simulate fraud detection
        await asyncio.sleep(0.05)
        
        # Check for suspicious patterns
        suspicious_patterns = [
            transaction['amount'] > 10000,  # Large amount
            transaction.get('ip_country') != transaction.get('card_country'),  # Location mismatch
            transaction.get('velocity', 0) > 5  # Too many transactions
        ]
        
        # Adaptive threshold (RAFAEL learns optimal threshold)
        fraud_score = sum(suspicious_patterns) / len(suspicious_patterns)
        
        return fraud_score > 0.5
    
    @AntiFragile(
        retry_policy="exponential",
        max_retries=5,
        timeout=10.0
    )
    async def validate_transaction(self, transaction: dict) -> bool:
        """Validate transaction details"""
        await asyncio.sleep(0.02)
        
        # Basic validation
        required_fields = ['id', 'amount', 'currency', 'user_id']
        return all(field in transaction for field in required_fields)
    
    async def simulate_spike_attack(self):
        """
        Simulate a spike in fraudulent transactions
        RAFAEL should adapt and strengthen defenses
        """
        print("\n" + "="*60)
        print("🔥 SIMULATING FRAUD ATTACK SPIKE")
        print("="*60)
        
        # Generate 50 transactions, 30% fraudulent
        transactions = []
        for i in range(50):
            is_fraud_attempt = random.random() < 0.3
            
            transaction = {
                'id': f'txn_{i}',
                'amount': random.randint(100, 15000) if is_fraud_attempt else random.randint(10, 500),
                'currency': 'USD',
                'user_id': f'user_{random.randint(1, 100)}',
                'ip_country': 'RU' if is_fraud_attempt else 'US',
                'card_country': 'US',
                'velocity': random.randint(6, 10) if is_fraud_attempt else random.randint(1, 3)
            }
            transactions.append(transaction)
        
        # Process all transactions
        results = {
            'success': 0,
            'blocked': 0,
            'failed': 0
        }
        
        for txn in transactions:
            try:
                result = await self.process_payment(txn)
                if result['status'] == 'success':
                    results['success'] += 1
                elif result['status'] == 'blocked':
                    results['blocked'] += 1
            except Exception as e:
                results['failed'] += 1
                print(f"❌ Transaction {txn['id']} failed: {e}")
        
        print(f"\n📊 Attack Simulation Results:")
        print(f"   Successful: {results['success']}")
        print(f"   Blocked (Fraud): {results['blocked']}")
        print(f"   Failed: {results['failed']}")
        
        return results
    
    async def demonstrate_evolution(self):
        """Demonstrate RAFAEL's evolution capabilities"""
        print("\n" + "="*60)
        print("🧬 DEMONSTRATING AUTONOMOUS EVOLUTION")
        print("="*60)
        
        # Trigger evolution for fraud detector
        print("\nEvolving fraud_detector module...")
        result = await self.rafael.evolve_module("fraud_detector")
        
        if result:
            print(f"✅ Evolution complete!")
            print(f"   Fitness Score: {result.fitness_score:.3f}")
            print(f"   Adopted: {result.adopted}")
            print(f"   Generation: {result.genome.generation}")
        
        # Show resilience report
        print("\n📊 Resilience Report:")
        report = self.rafael.get_resilience_report()
        
        for module_id, module_data in report['modules'].items():
            print(f"\n   Module: {module_id}")
            print(f"   Generation: {module_data['generation']}")
            print(f"   Genes: {module_data['genes_count']}")
            print(f"   Avg Fitness: {module_data['avg_fitness']:.3f}")
    
    async def demonstrate_guardian_layer(self):
        """Demonstrate Guardian Layer approval workflow"""
        print("\n" + "="*60)
        print("🛡️ DEMONSTRATING GUARDIAN LAYER")
        print("="*60)
        
        # Create a mutation change
        change = MutationChange(
            id="change_001",
            module_id="fraud_detector",
            change_type="genome_mutation",
            description="Increase fraud detection threshold based on recent patterns",
            impact=ChangeImpact.MEDIUM,
            old_genome={"threshold": 0.5},
            new_genome={"threshold": 0.65},
            fitness_improvement=0.15
        )
        
        # Request approval
        print("\n📝 Requesting approval for mutation...")
        request = self.guardian.request_approval(change)
        
        print(f"   Request ID: {request.id}")
        print(f"   Status: {request.status.value}")
        
        if request.status.value == "auto_approved":
            print(f"   ✅ Auto-approved: {request.auto_approval_reason}")
        else:
            print(f"   ⏳ Pending manual approval")
            
            # Simulate approval
            print("\n👤 Simulating approval by security_admin...")
            self.guardian.approve_change(request.id, "security_admin")
            print("   ✅ Change approved!")
        
        # Show audit log
        print("\n📋 Recent Audit Log:")
        recent_logs = self.guardian.get_audit_log()[-5:]
        for entry in recent_logs:
            print(f"   [{entry.timestamp.strftime('%H:%M:%S')}] {entry.event_type} by {entry.actor}")
        
        # Verify integrity
        integrity_ok = self.guardian.verify_audit_log_integrity()
        print(f"\n🔒 Audit Log Integrity: {'✅ PASS' if integrity_ok else '❌ FAIL'}")
    
    async def run_demo(self):
        """Run complete demonstration"""
        print("\n" + "="*60)
        print("🔱 RAFAEL FINTECH DEMO")
        print("="*60)
        
        # 1. Normal operation
        print("\n1️⃣ Normal Transaction Processing")
        normal_txn = {
            'id': 'txn_normal_001',
            'amount': 150,
            'currency': 'USD',
            'user_id': 'user_123',
            'ip_country': 'US',
            'card_country': 'US',
            'velocity': 2
        }
        await self.process_payment(normal_txn)
        
        # 2. Fraud detection
        print("\n2️⃣ Fraudulent Transaction Detection")
        fraud_txn = {
            'id': 'txn_fraud_001',
            'amount': 15000,
            'currency': 'USD',
            'user_id': 'user_456',
            'ip_country': 'RU',
            'card_country': 'US',
            'velocity': 8
        }
        await self.process_payment(fraud_txn)
        
        # 3. Attack simulation
        print("\n3️⃣ Fraud Attack Simulation")
        await self.simulate_spike_attack()
        
        # 4. Evolution demonstration
        print("\n4️⃣ Autonomous Evolution")
        await self.demonstrate_evolution()
        
        # 5. Guardian layer
        print("\n5️⃣ Guardian Layer & Compliance")
        await self.demonstrate_guardian_layer()
        
        # Final report
        print("\n" + "="*60)
        print("📊 FINAL RESILIENCE REPORT")
        print("="*60)
        
        report = self.rafael.get_resilience_report()
        print(f"\nApplication: {report['app_name']}")
        print(f"Timestamp: {report['timestamp']}")
        
        evolution_metrics = report['evolution_metrics']
        print(f"\nEvolution Metrics:")
        print(f"   Total Mutations: {evolution_metrics['total_mutations']}")
        print(f"   Adopted: {evolution_metrics['adopted_mutations']}")
        print(f"   Adoption Rate: {evolution_metrics['adoption_rate']:.1%}")
        
        print("\n✅ Demo Complete!")


async def main():
    """Main entry point"""
    app = FintechApp()
    await app.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
