# Getting Started with RAFAEL Framework

This tutorial will guide you through the basics of using RAFAEL Framework to build antifragile systems.

## Prerequisites

- Python 3.8 or higher
- Basic understanding of async/await
- Familiarity with resilience patterns (helpful but not required)

## Installation

Install RAFAEL Framework via pip:

```bash
pip install rafael-framework
```

For development with all extras:

```bash
pip install rafael-framework[all]
```

## Your First RAFAEL Application

Let's build a simple API service that becomes more resilient over time.

### Step 1: Initialize RAFAEL Core

```python
from core.rafael_engine import RafaelCore
import asyncio

# Create RAFAEL core instance
core = RafaelCore(
    app_name="my-api-service",
    resilience_level="adaptive"
)

print("🔱 RAFAEL initialized!")
```

### Step 2: Register Your Modules

```python
from core.rafael_engine import ResilienceStrategy

# Register your API module
api_genome = core.register_module(
    "api_handler",
    initial_strategies=[
        ResilienceStrategy.RETRY_ADAPTIVE,
        ResilienceStrategy.CIRCUIT_BREAKER,
        ResilienceStrategy.TIMEOUT
    ]
)

print(f"Module registered with {len(api_genome.genes)} resilience genes")
```

### Step 3: Apply Resilience to Your Functions

```python
from core.decorators import resilient, adaptive

@adaptive(module_id="api_handler")
@resilient(max_retries=3, base_delay=1.0)
async def fetch_user_data(user_id: int):
    """Fetch user data with automatic resilience"""
    # Your API logic here
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

# Use it
user = await fetch_user_data(123)
```

### Step 4: Start Autonomous Evolution

```python
async def main():
    # Start evolution (runs in background)
    await core.start_evolution(interval_seconds=3600)  # Evolve every hour
    
    # Your application runs here
    # RAFAEL continuously improves resilience in the background
    
    # When shutting down
    core.stop_evolution()

asyncio.run(main())
```

## Adding Chaos Testing

Test your system's resilience with Chaos Forge:

```python
from chaos_forge.simulator import ChaosForge, ThreatScenario, ThreatType, ThreatSeverity

# Initialize Chaos Forge
chaos = ChaosForge(target_system=fetch_user_data)

# Create a test scenario
scenario = ThreatScenario(
    id="network_test_1",
    name="Network Latency Test",
    threat_type=ThreatType.NETWORK_LATENCY,
    severity=ThreatSeverity.MEDIUM,
    description="Simulate 500ms network latency",
    parameters={"latency_ms": 500},
    duration_seconds=30.0
)

# Run the test
result = await chaos.run_simulation(scenario)

print(f"System survived: {result.system_survived}")
print(f"Resilience score: {result.resilience_score:.2f}")
print(f"Lessons learned: {result.lessons_learned}")
```

## Using the Resilience Vault

Access proven resilience patterns:

```python
from vault.resilience_vault import ResilienceVault, PatternCategory, TechnologyStack

# Initialize vault
vault = ResilienceVault()

# Search for patterns
patterns = vault.search_patterns(
    category=PatternCategory.RETRY,
    technology=TechnologyStack.PYTHON,
    min_reliability=0.8
)

# Use a pattern
for pattern in patterns:
    print(f"Pattern: {pattern.name}")
    print(f"Reliability: {pattern.reliability_score:.2f}")
    print(f"Code example:\n{pattern.code_example}")
    
    # Record usage
    vault.record_usage(pattern.id, success=True)
```

## Monitoring with Guardian Layer

Ensure all changes are safe and compliant:

```python
from guardian.guardian_layer import GuardianLayer, MutationChange, ChangeImpact

# Initialize Guardian
guardian = GuardianLayer()

# Guardian automatically monitors evolution
# You can also manually request approval for changes

change = MutationChange(
    id="change_001",
    module_id="api_handler",
    change_type="mutation",
    description="Optimize retry parameters",
    impact=ChangeImpact.LOW,
    old_genome={"max_retries": 3},
    new_genome={"max_retries": 5},
    fitness_improvement=0.15
)

request = guardian.request_approval(change)

if request.status.value == "auto_approved":
    print("Change auto-approved!")
else:
    print("Waiting for manual approval...")
```

## Complete Example

Here's a complete example putting it all together:

```python
import asyncio
from core.rafael_engine import RafaelCore, ResilienceStrategy
from core.decorators import resilient, adaptive
from chaos_forge.simulator import ChaosForge
from vault.resilience_vault import ResilienceVault
from guardian.guardian_layer import GuardianLayer

class ResilientAPIService:
    def __init__(self):
        # Initialize all components
        self.core = RafaelCore(app_name="api-service")
        self.chaos = ChaosForge()
        self.vault = ResilienceVault()
        self.guardian = GuardianLayer()
        
        # Register modules
        self.core.register_module("api", [
            ResilienceStrategy.RETRY_ADAPTIVE,
            ResilienceStrategy.CIRCUIT_BREAKER
        ])
    
    @adaptive(module_id="api")
    @resilient(max_retries=3)
    async def get_data(self, endpoint: str):
        """Resilient API call"""
        # Your API logic
        return {"data": "example"}
    
    async def start(self):
        """Start the service"""
        # Start autonomous evolution
        await self.core.start_evolution()
        
        # Run periodic chaos tests
        asyncio.create_task(self.run_chaos_tests())
        
        print("🔱 Resilient API Service started!")
    
    async def run_chaos_tests(self):
        """Periodically run chaos tests"""
        while True:
            await asyncio.sleep(3600)  # Every hour
            
            # Run chaos suite
            results = await self.chaos.run_full_suite()
            
            # Analyze and evolve
            for result in results:
                if result.resilience_score < 0.7:
                    # Trigger evolution for weak areas
                    await self.core.evolve_module("api")
    
    def get_status(self):
        """Get system status"""
        return {
            "core": self.core.get_resilience_report(),
            "chaos": self.chaos.export_report(),
            "vault": self.vault.generate_report(),
            "guardian": self.guardian.generate_compliance_report()
        }

# Usage
async def main():
    service = ResilientAPIService()
    await service.start()
    
    # Your application logic
    data = await service.get_data("/users")
    
    # Check status
    status = service.get_status()
    print(f"System resilience: {status}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Next Steps

- Read the [Architecture Guide](../concepts/architecture.md) to understand RAFAEL's design
- Explore [Advanced Patterns](../advanced/patterns.md) for complex scenarios
- Check out [Production Deployment](../advanced/deployment.md) guide
- Join the [Community](https://github.com/Rafael2022-prog/rafael) and share your patterns!

## Common Patterns

### Pattern 1: Database Resilience

```python
@adaptive(module_id="database")
@resilient(max_retries=5, base_delay=2.0)
async def query_database(query: str):
    """Resilient database query"""
    # Connection pooling, retry logic, and circuit breaker
    # are automatically applied
    pass
```

### Pattern 2: External API Calls

```python
@adaptive(module_id="external_api")
@resilient(
    max_retries=3,
    base_delay=1.0,
    fallback=lambda: {"status": "unavailable"}
)
async def call_external_api(endpoint: str):
    """Call external API with fallback"""
    pass
```

### Pattern 3: Background Jobs

```python
@adaptive(module_id="background_jobs")
@monitor_health(failure_threshold=5, circuit_breaker=True)
async def process_job(job_id: str):
    """Process background job with health monitoring"""
    pass
```

## Troubleshooting

### Issue: Evolution not happening

**Solution**: Check that you've called `start_evolution()` and that modules are registered.

```python
# Verify modules
print(core.genomes.keys())

# Check evolution status
print(core.evolution_active)
```

### Issue: High memory usage

**Solution**: Adjust evolution interval and limit genome size.

```python
core = RafaelCore(
    app_name="my-app",
    config={
        "max_genes_per_genome": 10,
        "evolution_interval": 7200  # 2 hours
    }
)
```

### Issue: Chaos tests too aggressive

**Solution**: Adjust threat severity and duration.

```python
scenario = ThreatScenario(
    # ... other params
    severity=ThreatSeverity.LOW,  # Start with LOW
    duration_seconds=10.0  # Shorter duration
)
```

## Getting Help

- 📖 [Documentation](https://github.com/Rafael2022-prog/rafael/tree/main/docs)
- 💬 [GitHub Discussions](https://github.com/Rafael2022-prog/rafael/discussions)
- 🐛 [Report Issues](https://github.com/Rafael2022-prog/rafael/issues)
- 📧 [Email Support](mailto:info@rafaelabs.xyz)

---

**Congratulations!** You've completed the getting started tutorial. Your system is now antifragile and will continuously improve its resilience over time. 🎉
