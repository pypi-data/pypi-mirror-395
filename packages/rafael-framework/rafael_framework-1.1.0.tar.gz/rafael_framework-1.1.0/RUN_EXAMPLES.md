# 🚀 Running RAFAEL Examples

This guide shows you how to run the RAFAEL examples and see the framework in action.

## Prerequisites

```bash
# Install RAFAEL
cd R:/RAFAEL
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

## Example 1: Fintech Application

Demonstrates fraud detection with adaptive resilience.

```bash
# Run the fintech example
python examples/fintech_example.py
```

### What You'll See

1. **Normal Transaction Processing**: See how RAFAEL handles regular payments
2. **Fraud Detection**: Watch RAFAEL block suspicious transactions
3. **Attack Simulation**: 50 transactions with 30% fraud attempts
4. **Autonomous Evolution**: RAFAEL evolves its fraud detection strategies
5. **Guardian Layer**: Approval workflow and audit logging

### Expected Output

```
🔱 RAFAEL FINTECH DEMO
============================================================

1️⃣ Normal Transaction Processing
💳 Processing transaction: $150
✅ Payment processed successfully

2️⃣ Fraudulent Transaction Detection
💳 Processing transaction: $15000
⚠️  FRAUD DETECTED - Transaction blocked

3️⃣ Fraud Attack Simulation
🔥 SIMULATING FRAUD ATTACK SPIKE
============================================================
📊 Attack Simulation Results:
   Successful: 35
   Blocked (Fraud): 15
   Failed: 0

4️⃣ Autonomous Evolution
🧬 DEMONSTRATING AUTONOMOUS EVOLUTION
============================================================
✅ Evolution complete!
   Fitness Score: 0.850
   Adopted: True
   Generation: 1

5️⃣ Guardian Layer & Compliance
🛡️ DEMONSTRATING GUARDIAN LAYER
============================================================
📝 Requesting approval for mutation...
   ✅ Auto-approved: High fitness improvement: 0.15
🔒 Audit Log Integrity: ✅ PASS

✅ Demo Complete!
```

## Example 2: Mobile Game Server

Demonstrates adaptive load management and graceful degradation.

```bash
# Run the game example
python examples/game_example.py
```

### What You'll See

1. **Normal Gameplay**: Regular game session handling
2. **Matchmaking**: Player matching with caching
3. **Leaderboard**: Score updates with rate limiting
4. **Player Surge**: 100 concurrent players joining
5. **Adaptive Degradation**: Graphics quality adjustment under load

### Expected Output

```
🎮 RAFAEL MOBILE GAME DEMO
============================================================

1️⃣ Normal Gameplay Session
🎮 Player player_0001 joining (Load: 0.1%)
✅ Session created

2️⃣ Matchmaking Service
🔍 Finding match for player_0001 (skill: 1500)
   Match found: match_5432
   Players: 4
   Map: desert

3️⃣ Leaderboard Update
📊 Leaderboard updated: player_0001 = 2500 points

4️⃣ Player Surge Simulation
🌊 SIMULATING PLAYER SURGE: 100 players
============================================================
⚠️  High server load detected!
   🔽 Graphics quality: HIGH → MEDIUM
   🔄 Reducing particle effects

📊 Surge Results:
   Successful: 98/100
   Failed: 2/100
   Success Rate: 98.0%
   Peak Load: 85.0%
   Final Graphics Quality: medium

5️⃣ Autonomous Evolution
🧬 DEMONSTRATING GAME SERVER EVOLUTION
============================================================
✅ Evolution complete!
💡 Improvements:
   - Learned optimal degradation thresholds
   - Improved load balancing strategies
   - Enhanced failover mechanisms

✅ Game Demo Complete!
```

## Using the CLI

### Initialize a Project

```bash
# Create a new RAFAEL project
rafael init project

# Follow prompts:
# - Application name: my-app
# - Technology stack: python
```

### Register Modules

```bash
# Register a module with strategies
rafael module register payment_processor --strategies retry circuit_breaker

# Trigger evolution
rafael module evolve payment_processor
```

### Run Chaos Tests

```bash
# Test specific scenario
rafael chaos test --scenario network_latency

# Run all scenarios
rafael chaos test --all

# Generate report
rafael chaos report
```

### Search Patterns

```bash
# Search by category
rafael vault search --category retry

# Search by technology
rafael vault search --tech python

# Show pattern details
rafael vault show flutter_supabase_retry_001

# View statistics
rafael vault stats
```

### Dashboard

```bash
# Start dashboard
rafael dashboard --port 8080

# Open in browser: http://localhost:8080
```

### Check Status

```bash
# View system status
rafael status
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_rafael_engine.py

# Run with coverage
pytest --cov=rafael --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## Troubleshooting

### Import Errors

```bash
# Make sure RAFAEL is installed
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:R:/RAFAEL"
```

### Module Not Found

```bash
# Initialize RAFAEL first
rafael init project

# Then register modules
rafael module register your_module
```

### Permission Errors

```bash
# Run with appropriate permissions
# On Windows, run PowerShell as Administrator if needed
```

## Next Steps

1. **Modify Examples**: Customize the examples for your use case
2. **Create Your Own**: Build your own RAFAEL-powered application
3. **Explore Patterns**: Browse the Resilience Vault for proven patterns
4. **Run Chaos Tests**: Test your application's resilience
5. **Monitor Evolution**: Watch your system evolve and improve

## Getting Help

- **Documentation**: Check `docs/` folder
- **Examples**: Review `examples/` folder
- **Issues**: Open a GitHub issue
- **Community**: Join our Discord/Slack

---

**Ready to see RAFAEL in action? Run the examples and watch your system evolve! 🔱**
