# 🚀 RAFAEL Quick Start Guide

Get started with RAFAEL in 5 minutes!

## Installation

```bash
# Install RAFAEL
pip install rafael-framework

# Or install from source
git clone https://github.com/rafael-framework/rafael.git
cd rafael
pip install -e .
```

## Initialize Your Project

```bash
# Initialize RAFAEL in your project
rafael init project

# Follow the prompts:
# - Application name: my-app
# - Technology stack: python
```

This creates a `rafael.config.json` file with default settings.

## Basic Usage

### 1. Decorate Your Functions

```python
from rafael import AntiFragile, RafaelCore

# Initialize RAFAEL
rafael = RafaelCore(app_name="my-app")

# Make any function resilient
@AntiFragile(
    retry_policy="adaptive",
    max_retries=3,
    timeout=10.0,
    circuit_breaker=True
)
async def critical_function():
    # Your code here
    result = await external_api_call()
    return result
```

### 2. Start Autonomous Evolution

```python
import asyncio

async def main():
    # Register your modules
    rafael.register_module("api_client")
    rafael.register_module("database_handler")
    
    # Start autonomous evolution
    await rafael.start_evolution(interval_seconds=3600)  # Every hour
    
    # Your application runs normally
    # RAFAEL evolves in the background

asyncio.run(main())
```

### 3. Run Chaos Tests

```bash
# Test a specific scenario
rafael chaos test --scenario network_latency

# Run full chaos suite
rafael chaos test --all

# Generate resilience report
rafael chaos report
```

## Real-World Examples

### Fintech Application

```python
from rafael import AntiFragile

@AntiFragile(
    retry_policy="adaptive",
    circuit_breaker=True,
    threat_model="financial_fraud"
)
async def process_payment(transaction):
    # RAFAEL automatically:
    # - Retries on failure
    # - Opens circuit breaker on repeated failures
    # - Learns from fraud patterns
    # - Adapts strategies over time
    
    result = await payment_gateway.charge(transaction)
    return result
```

### Mobile Game Server

```python
@AntiFragile(
    load_strategy="adaptive_degradation",
    circuit_breaker=True
)
async def handle_game_session(player_id):
    # RAFAEL automatically:
    # - Monitors server load
    # - Degrades graphics quality under pressure
    # - Shifts logic to client-side when needed
    # - Learns optimal degradation strategies
    
    session = await create_game_session(player_id)
    return session
```

### dApp / Blockchain

```python
@AntiFragile(
    blockchain_fallback="layer2",
    timeout=30.0
)
async def execute_transaction(tx_data):
    # RAFAEL automatically:
    # - Switches to Layer-2 when mainnet is slow
    # - Maintains smooth UX during delays
    # - Optimizes strategy selection
    
    tx = await blockchain.send_transaction(tx_data)
    return tx
```

## CLI Commands

```bash
# Initialize project
rafael init project

# Register a module
rafael module register my_module --strategies retry circuit_breaker

# Trigger evolution
rafael module evolve my_module

# Run chaos tests
rafael chaos test --all
rafael chaos report

# Search resilience patterns
rafael vault search --category retry --tech python

# Show pattern details
rafael vault show flutter_supabase_retry_001

# View vault statistics
rafael vault stats

# Start dashboard
rafael dashboard --port 8080

# Check system status
rafael status
```

## Configuration

Edit `rafael.config.json`:

```json
{
  "app": {
    "name": "my-app",
    "technology": "python",
    "environment": "production"
  },
  "resilience": {
    "genome": {
      "mutation_rate": 0.1,
      "sandbox_isolation": true,
      "auto_adopt_threshold": 0.85
    },
    "chaos_forge": {
      "enabled": true,
      "schedule": "weekly"
    },
    "vault": {
      "auto_import": true,
      "community_patterns": true
    }
  },
  "guardian": {
    "approval_required": true,
    "audit_log": true,
    "compliance": ["ISO27001", "SOC2"]
  }
}
```

## Dashboard

Start the RAFAEL dashboard to monitor your system:

```bash
rafael dashboard --port 8080
```

Open http://localhost:8080 to view:
- Real-time resilience metrics
- Evolution timeline
- Active mutations
- Chaos test results
- Fitness scores

## Next Steps

1. **Read the Documentation**: Check out [docs/](./docs/) for detailed guides
2. **Run Examples**: Try the examples in [examples/](../examples/)
3. **Explore Patterns**: Browse the Resilience Vault for proven patterns
4. **Join Community**: Share your patterns and learn from others

## Common Patterns

### Retry with Exponential Backoff

```python
@AntiFragile(retry_policy="exponential", max_retries=5)
async def api_call():
    return await external_api.get_data()
```

### Circuit Breaker

```python
@AntiFragile(circuit_breaker=True, timeout=10.0)
async def unreliable_service():
    return await service.call()
```

### Rate Limiting

```python
@AntiFragile(rate_limit=100)  # 100 requests per minute
async def rate_limited_endpoint():
    return await process_request()
```

### Caching

```python
@AntiFragile(cache_results=True, timeout=5.0)
async def expensive_operation():
    return await compute_heavy_task()
```

## Troubleshooting

### RAFAEL not initialized
```bash
rafael init project
```

### Module not found
```bash
rafael module register your_module_name
```

### Chaos tests failing
Check your resilience configuration and increase retry limits or timeouts.

### Evolution not working
Ensure `start_evolution()` is called and the event loop is running.

## Support

- **Documentation**: [docs/](./docs/)
- **Examples**: [examples/](../examples/)
- **Issues**: GitHub Issues
- **Community**: Discord / Slack

---

**Ready to make your system antifragile? Let's go! 🔱**
