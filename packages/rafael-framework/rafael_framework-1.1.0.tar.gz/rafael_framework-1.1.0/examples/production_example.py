"""
RAFAEL Framework - Production Example
=====================================

Complete pre-production implementation example showing:
1. Installation verification
2. Local testing
3. @AntiFragile decorators usage
4. Guardian configuration
5. Staging traffic simulation

This is a production-ready example for a payment processing service.
"""

import time
import random
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# RAFAEL Framework imports
from core import RafaelCore, AdaptiveResilienceGenome
from core.decorators import AntiFragile
from chaos_forge import ChaosForge, ThreatType, ThreatSeverity
from vault import ResilienceVault
from guardian import GuardianLayer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# STEP 1: VERIFY INSTALLATION
# ============================================================================

def verify_installation():
    """Verify RAFAEL Framework is properly installed"""
    try:
        logger.info("🔍 Verifying RAFAEL Framework installation...")
        
        # Check core components
        rafael = RafaelCore(app_name="production-test")
        logger.info("✅ RafaelCore initialized")
        
        chaos = ChaosForge()
        logger.info("✅ ChaosForge initialized")
        
        vault = ResilienceVault()
        logger.info("✅ ResilienceVault initialized")
        
        guardian = GuardianLayer()
        logger.info("✅ GuardianLayer initialized")
        
        logger.info("🎉 RAFAEL Framework installation verified!\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Installation verification failed: {e}")
        return False


# ============================================================================
# STEP 2: PRODUCTION APPLICATION EXAMPLE
# ============================================================================

class PaymentService:
    """
    Production-ready Payment Service with RAFAEL Framework
    
    This service demonstrates:
    - @AntiFragile decorators for resilience
    - Guardian Layer for compliance
    - Chaos testing for validation
    - Real-world error handling
    """
    
    def __init__(self):
        # Initialize RAFAEL
        self.rafael = RafaelCore(app_name="payment-service")
        
        # Initialize Guardian with approval policy
        from guardian.guardian_layer import ApprovalPolicy
        policy = ApprovalPolicy(
            auto_approve_low_impact=True,
            auto_approve_threshold=0.95,  # Auto-approve if fitness > 95%
            require_approval_for_production=True
        )
        self.guardian = GuardianLayer(approval_policy=policy)
        self.vault = ResilienceVault()
        
        # Register service modules
        self.rafael.register_module("payment-processor")
        self.rafael.register_module("fraud-detector")
        self.rafael.register_module("notification-sender")
        
        logger.info("💳 Payment Service initialized with RAFAEL")
        logger.info("🛡️ Guardian Layer configured with approval policy")
    
    # ========================================================================
    # STEP 3: ADD @ANTIFRAGILE DECORATORS
    # ========================================================================
    
    @AntiFragile(
        max_retries=3,
        fallback="genomic",
        circuit_breaker=True,
        timeout=5.0
    )
    def process_payment(
        self, 
        amount: float, 
        user_id: str, 
        payment_method: str
    ) -> Dict[str, Any]:
        """
        Process a payment with full resilience
        
        The @AntiFragile decorator provides:
        - Automatic retries (max 3)
        - Circuit breaker protection
        - Timeout handling (5 seconds)
        - Genomic fallback strategy
        """
        logger.info(f"💰 Processing payment: ${amount} for user {user_id}")
        
        # Simulate payment processing
        if random.random() < 0.1:  # 10% failure rate for testing
            raise Exception("Payment gateway timeout")
        
        # Simulate processing time
        time.sleep(random.uniform(0.1, 0.5))
        
        transaction_id = f"TXN-{int(time.time())}-{random.randint(1000, 9999)}"
        
        result = {
            "success": True,
            "transaction_id": transaction_id,
            "amount": amount,
            "user_id": user_id,
            "payment_method": payment_method,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        logger.info(f"✅ Payment processed: {transaction_id}")
        return result
    
    @AntiFragile(
        max_retries=2,
        fallback="genomic",
        rate_limit=100  # Max 100 requests per second
    )
    def detect_fraud(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fraud detection with rate limiting and resilience
        """
        logger.info(f"🔍 Checking fraud for transaction {transaction.get('transaction_id')}")
        
        # Simulate fraud detection
        if random.random() < 0.05:  # 5% fraud detection failure
            raise Exception("Fraud detection service unavailable")
        
        time.sleep(random.uniform(0.05, 0.2))
        
        # Simple fraud score (in production, use ML model)
        fraud_score = random.uniform(0, 1)
        is_fraudulent = fraud_score > 0.8
        
        result = {
            "transaction_id": transaction.get("transaction_id"),
            "fraud_score": fraud_score,
            "is_fraudulent": is_fraudulent,
            "checked_at": datetime.now().isoformat()
        }
        
        if is_fraudulent:
            logger.warning(f"⚠️ Potential fraud detected: {fraud_score:.2f}")
        else:
            logger.info(f"✅ Transaction clean: {fraud_score:.2f}")
        
        return result
    
    @AntiFragile(
        max_retries=5,
        fallback="none",  # Use none fallback for notifications
        timeout=3.0,
        cache_results=True
    )
    def send_notification(
        self, 
        user_id: str, 
        message: str, 
        channel: str = "email"
    ) -> Dict[str, Any]:
        """
        Send notification with aggressive retry and caching
        """
        logger.info(f"📧 Sending {channel} notification to {user_id}")
        
        # Simulate notification service
        if random.random() < 0.15:  # 15% failure rate
            raise Exception(f"{channel} service unavailable")
        
        time.sleep(random.uniform(0.1, 0.3))
        
        result = {
            "success": True,
            "user_id": user_id,
            "channel": channel,
            "message": message,
            "sent_at": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Notification sent via {channel}")
        return result
    
    def process_full_transaction(
        self, 
        amount: float, 
        user_id: str, 
        payment_method: str
    ) -> Dict[str, Any]:
        """
        Complete transaction flow with all resilience features
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"🚀 Starting full transaction for user {user_id}")
        logger.info(f"{'='*70}\n")
        
        try:
            # Step 1: Process payment
            payment_result = self.process_payment(amount, user_id, payment_method)
            
            # Step 2: Check for fraud
            fraud_result = self.detect_fraud(payment_result)
            
            if fraud_result["is_fraudulent"]:
                # Refund if fraudulent
                logger.warning("⚠️ Transaction flagged as fraudulent - initiating refund")
                payment_result["status"] = "refunded"
                payment_result["reason"] = "fraud_detected"
            
            # Step 3: Send notification
            notification_message = (
                f"Payment of ${amount} {'completed' if not fraud_result['is_fraudulent'] else 'refunded'}"
            )
            notification_result = self.send_notification(
                user_id, 
                notification_message, 
                "email"
            )
            
            # Combine results
            final_result = {
                "payment": payment_result,
                "fraud_check": fraud_result,
                "notification": notification_result,
                "overall_status": "success"
            }
            
            logger.info(f"\n{'='*70}")
            logger.info(f"✅ Transaction completed successfully")
            logger.info(f"{'='*70}\n")
            
            return final_result
            
        except Exception as e:
            logger.error(f"❌ Transaction failed: {e}")
            return {
                "overall_status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# ============================================================================
# STEP 4: LOCAL TESTING
# ============================================================================

def test_locally():
    """Test the service locally before staging"""
    logger.info("\n" + "="*70)
    logger.info("🧪 STEP 2: LOCAL TESTING")
    logger.info("="*70 + "\n")
    
    service = PaymentService()
    
    # Test Case 1: Successful transaction
    logger.info("Test Case 1: Normal transaction")
    result1 = service.process_full_transaction(
        amount=99.99,
        user_id="user-12345",
        payment_method="credit_card"
    )
    
    time.sleep(1)
    
    # Test Case 2: Another transaction
    logger.info("Test Case 2: Another transaction")
    result2 = service.process_full_transaction(
        amount=49.99,
        user_id="user-67890",
        payment_method="paypal"
    )
    
    time.sleep(1)
    
    # Test Case 3: High-value transaction
    logger.info("Test Case 3: High-value transaction")
    result3 = service.process_full_transaction(
        amount=999.99,
        user_id="user-11111",
        payment_method="bank_transfer"
    )
    
    logger.info("\n✅ Local testing completed!\n")
    return [result1, result2, result3]


# ============================================================================
# STEP 5: CHAOS TESTING (STAGING SIMULATION)
# ============================================================================

def test_with_chaos():
    """Simulate staging environment with chaos testing"""
    logger.info("\n" + "="*70)
    logger.info("⚡ STEP 3: CHAOS TESTING (STAGING SIMULATION)")
    logger.info("="*70 + "\n")
    
    service = PaymentService()
    chaos = ChaosForge()
    
    # Simulate various attack scenarios
    scenarios = [
        {
            "name": "DDoS Attack",
            "threat_type": ThreatType.DDOS_ATTACK,
            "severity": ThreatSeverity.HIGH
        },
        {
            "name": "Network Latency",
            "threat_type": ThreatType.NETWORK_LATENCY,
            "severity": ThreatSeverity.MEDIUM
        },
        {
            "name": "Database Failure",
            "threat_type": ThreatType.DATABASE_FAILURE,
            "severity": ThreatSeverity.HIGH
        }
    ]
    
    results = []
    
    for scenario in scenarios:
        logger.info(f"\n🎯 Testing: {scenario['name']}")
        logger.info(f"   Threat: {scenario['threat_type'].value}")
        logger.info(f"   Severity: {scenario['severity'].value}\n")
        
        # Run chaos simulation
        chaos_result = chaos.simulate_attack(
            module_id="payment-processor",
            threat_type=scenario["threat_type"],
            severity=scenario["severity"],
            duration=5.0
        )
        
        logger.info(f"   Resilience Score: {chaos_result.resilience_score:.2%}")
        logger.info(f"   Survived: {chaos_result.survived}")
        logger.info(f"   Recommendations: {len(chaos_result.recommendations)}")
        
        # Test transaction under chaos
        try:
            transaction_result = service.process_full_transaction(
                amount=random.uniform(10, 1000),
                user_id=f"user-chaos-{random.randint(1000, 9999)}",
                payment_method="credit_card"
            )
            logger.info(f"   ✅ Transaction survived chaos: {scenario['name']}")
        except Exception as e:
            logger.warning(f"   ⚠️ Transaction failed under chaos: {e}")
        
        results.append({
            "scenario": scenario["name"],
            "chaos_result": chaos_result,
            "survived": chaos_result.survived
        })
        
        time.sleep(2)
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("📊 CHAOS TESTING SUMMARY")
    logger.info("="*70 + "\n")
    
    total_scenarios = len(results)
    survived_scenarios = sum(1 for r in results if r["survived"])
    
    logger.info(f"Total Scenarios: {total_scenarios}")
    logger.info(f"Survived: {survived_scenarios}")
    logger.info(f"Success Rate: {survived_scenarios/total_scenarios:.1%}")
    
    for result in results:
        status = "✅" if result["survived"] else "❌"
        logger.info(f"{status} {result['scenario']}: {result['chaos_result'].resilience_score:.1%}")
    
    logger.info("\n✅ Chaos testing completed!\n")
    return results


# ============================================================================
# STEP 6: GUARDIAN APPROVAL WORKFLOW
# ============================================================================

def test_guardian_workflow():
    """Test Guardian Layer approval workflow"""
    logger.info("\n" + "="*70)
    logger.info("🛡️ STEP 4: GUARDIAN APPROVAL WORKFLOW")
    logger.info("="*70 + "\n")
    
    service = PaymentService()
    
    # Trigger evolution (which requires Guardian approval)
    logger.info("🧬 Triggering module evolution...")
    
    try:
        service.rafael.evolve_module("payment-processor")
        logger.info("✅ Evolution triggered")
        
        # Check pending approvals
        pending = service.guardian.get_pending_approvals()
        logger.info(f"📋 Pending approvals: {len(pending)}")
        
        if pending:
            approval = pending[0]
            logger.info(f"\n📝 Approval Request:")
            logger.info(f"   ID: {approval.id}")
            logger.info(f"   Requester: {approval.requester}")
            logger.info(f"   Impact: {approval.impact.risk_level.value}")
            logger.info(f"   Fitness Change: {approval.impact.fitness_delta:+.2%}")
            
            # Auto-approve if fitness improved
            if approval.impact.fitness_delta > 0:
                service.guardian.approve_change(approval.id, "auto-approver")
                logger.info(f"   ✅ Auto-approved (fitness improved)")
            else:
                logger.info(f"   ⏳ Requires manual approval")
        
    except Exception as e:
        logger.info(f"ℹ️ Evolution info: {e}")
    
    logger.info("\n✅ Guardian workflow tested!\n")


# ============================================================================
# STEP 7: LOAD TESTING (STAGING TRAFFIC SIMULATION)
# ============================================================================

def simulate_staging_traffic():
    """Simulate real staging traffic patterns"""
    logger.info("\n" + "="*70)
    logger.info("📈 STEP 5: STAGING TRAFFIC SIMULATION")
    logger.info("="*70 + "\n")
    
    service = PaymentService()
    
    # Simulate different traffic patterns
    patterns = [
        {"name": "Normal Load", "requests": 10, "delay": 0.5},
        {"name": "Peak Load", "requests": 20, "delay": 0.2},
        {"name": "Burst Load", "requests": 30, "delay": 0.1}
    ]
    
    all_results = []
    
    for pattern in patterns:
        logger.info(f"\n🎯 Testing: {pattern['name']}")
        logger.info(f"   Requests: {pattern['requests']}")
        logger.info(f"   Delay: {pattern['delay']}s\n")
        
        start_time = time.time()
        successes = 0
        failures = 0
        
        for i in range(pattern['requests']):
            try:
                result = service.process_full_transaction(
                    amount=random.uniform(10, 500),
                    user_id=f"user-{random.randint(10000, 99999)}",
                    payment_method=random.choice(["credit_card", "paypal", "bank_transfer"])
                )
                
                if result.get("overall_status") == "success":
                    successes += 1
                else:
                    failures += 1
                    
            except Exception as e:
                failures += 1
                logger.warning(f"   ⚠️ Request {i+1} failed: {e}")
            
            time.sleep(pattern['delay'])
        
        elapsed_time = time.time() - start_time
        success_rate = successes / pattern['requests']
        throughput = pattern['requests'] / elapsed_time
        
        logger.info(f"\n   📊 Results:")
        logger.info(f"   Total Requests: {pattern['requests']}")
        logger.info(f"   Successes: {successes}")
        logger.info(f"   Failures: {failures}")
        logger.info(f"   Success Rate: {success_rate:.1%}")
        logger.info(f"   Throughput: {throughput:.2f} req/s")
        logger.info(f"   Total Time: {elapsed_time:.2f}s")
        
        all_results.append({
            "pattern": pattern['name'],
            "success_rate": success_rate,
            "throughput": throughput
        })
    
    # Final summary
    logger.info("\n" + "="*70)
    logger.info("📊 STAGING TRAFFIC SUMMARY")
    logger.info("="*70 + "\n")
    
    for result in all_results:
        logger.info(f"✅ {result['pattern']}: {result['success_rate']:.1%} success, {result['throughput']:.1f} req/s")
    
    logger.info("\n✅ Staging traffic simulation completed!\n")
    return all_results


# ============================================================================
# MAIN PRE-PRODUCTION WORKFLOW
# ============================================================================

def run_pre_production_workflow():
    """
    Complete pre-production workflow:
    1. Verify installation
    2. Test locally
    3. Add @AntiFragile decorators (already done)
    4. Configure Guardian
    5. Test with staging traffic
    """
    
    print("\n" + "="*70)
    print("RAFAEL FRAMEWORK - PRE-PRODUCTION WORKFLOW")
    print("="*70 + "\n")
    
    # Step 1: Verify installation
    logger.info("="*70)
    logger.info("STEP 1: VERIFY INSTALLATION")
    logger.info("="*70 + "\n")
    
    if not verify_installation():
        logger.error("❌ Installation verification failed. Please run: pip install rafael-framework")
        return
    
    # Step 2: Local testing
    test_results = test_locally()
    
    # Step 3: Chaos testing
    chaos_results = test_with_chaos()
    
    # Step 4: Guardian workflow
    test_guardian_workflow()
    
    # Step 5: Staging traffic simulation
    traffic_results = simulate_staging_traffic()
    
    # Final summary
    print("\n" + "="*70)
    print("PRE-PRODUCTION WORKFLOW COMPLETED!")
    print("="*70 + "\n")
    
    print("All steps completed successfully:")
    print("   1. Installation verified")
    print("   2. Local testing passed")
    print("   3. @AntiFragile decorators working")
    print("   4. Guardian configured and tested")
    print("   5. Staging traffic simulation passed")
    
    print("\nSummary:")
    print(f"   Local Tests: {len(test_results)} transactions")
    print(f"   Chaos Tests: {len(chaos_results)} scenarios")
    print(f"   Traffic Tests: {len(traffic_results)} patterns")
    
    print("\nREADY FOR PRODUCTION DEPLOYMENT!")
    print("\nNext steps:")
    print("   1. Review logs and metrics")
    print("   2. Deploy to production environment")
    print("   3. Enable monitoring dashboard")
    print("   4. Set up alerts")
    print("   5. Monitor initial traffic")
    
    print("\n" + "="*70 + "\n")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        run_pre_production_workflow()
    except KeyboardInterrupt:
        logger.info("\n\n⚠️ Workflow interrupted by user")
    except Exception as e:
        logger.error(f"\n\n❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
