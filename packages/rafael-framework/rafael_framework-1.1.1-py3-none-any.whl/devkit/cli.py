"""
RAFAEL CLI - Command Line Interface
Manage RAFAEL deployments, simulations, and monitoring
"""

import click
import asyncio
import json
from pathlib import Path
from typing import Optional
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.rafael_engine import RafaelCore, ResilienceStrategy
from chaos_forge.simulator import ChaosForge, ThreatScenario, ThreatType, ThreatSeverity
from vault.resilience_vault import ResilienceVault, PatternCategory, TechnologyStack


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🔱 RAFAEL - Resilience-Adaptive Framework for Autonomous Evolution & Learning"""
    pass


@cli.group()
def init():
    """Initialize RAFAEL in your project"""
    pass


@init.command()
@click.option('--name', prompt='Application name', help='Name of your application')
@click.option('--tech', prompt='Technology stack', 
              type=click.Choice(['python', 'nodejs', 'flutter', 'react']),
              help='Primary technology stack')
def project(name: str, tech: str):
    """Initialize a new RAFAEL project"""
    click.echo(f"🔱 Initializing RAFAEL for {name}...")
    
    # Create config file
    config = {
        "app": {
            "name": name,
            "technology": tech,
            "environment": "development"
        },
        "resilience": {
            "genome": {
                "mutation_rate": 0.1,
                "sandbox_isolation": True,
                "auto_adopt_threshold": 0.85
            },
            "chaos_forge": {
                "enabled": True,
                "schedule": "weekly"
            },
            "vault": {
                "auto_import": True,
                "community_patterns": True
            }
        },
        "guardian": {
            "approval_required": True,
            "audit_log": True
        }
    }
    
    config_path = Path('rafael.config.json')
    with open(config_path, 'w') as f:
        json.dump(config, indent=2, fp=f)
    
    click.echo(f"✅ Created {config_path}")
    click.echo(f"✅ RAFAEL initialized successfully!")
    click.echo(f"\nNext steps:")
    click.echo(f"  1. Review rafael.config.json")
    click.echo(f"  2. Run 'rafael module register' to register modules")
    click.echo(f"  3. Run 'rafael chaos test' to test resilience")


@cli.group()
def module():
    """Manage resilience modules"""
    pass


@module.command()
@click.argument('module_id')
@click.option('--strategies', multiple=True, 
              type=click.Choice(['retry', 'circuit_breaker', 'timeout', 'rate_limit']),
              help='Initial resilience strategies')
def register(module_id: str, strategies: tuple):
    """Register a new module"""
    click.echo(f"Registering module: {module_id}")
    
    # Load config
    config = _load_config()
    if not config:
        click.echo("❌ No rafael.config.json found. Run 'rafael init project' first.")
        return
    
    # Create RAFAEL core
    core = RafaelCore(
        app_name=config['app']['name'],
        config=config['resilience']
    )
    
    # Map strategy names to enums
    strategy_map = {
        'retry': ResilienceStrategy.RETRY_ADAPTIVE,
        'circuit_breaker': ResilienceStrategy.CIRCUIT_BREAKER,
        'timeout': ResilienceStrategy.TIMEOUT,
        'rate_limit': ResilienceStrategy.RATE_LIMIT
    }
    
    initial_strategies = [strategy_map[s] for s in strategies] if strategies else None
    
    # Register module
    genome = core.register_module(module_id, initial_strategies)
    
    click.echo(f"✅ Module {module_id} registered with {len(genome.genes)} genes")


@module.command()
@click.argument('module_id')
def evolve(module_id: str):
    """Trigger evolution for a module"""
    click.echo(f"Evolving module: {module_id}")
    
    config = _load_config()
    if not config:
        return
    
    core = RafaelCore(app_name=config['app']['name'])
    core.register_module(module_id)
    
    # Run evolution
    async def run_evolution():
        result = await core.evolve_module(module_id)
        if result:
            click.echo(f"✅ Evolution complete!")
            click.echo(f"   Fitness score: {result.fitness_score:.3f}")
            click.echo(f"   Adopted: {result.adopted}")
    
    asyncio.run(run_evolution())


@cli.group()
def chaos():
    """Chaos engineering and testing"""
    pass


@chaos.command()
@click.option('--scenario', type=click.Choice([
    'network_latency', 'database_failure', 'ddos', 'memory_pressure', 'cascading_failure'
]), help='Specific scenario to test')
@click.option('--all', 'run_all', is_flag=True, help='Run all scenarios')
def test(scenario: Optional[str], run_all: bool):
    """Run chaos tests"""
    click.echo("🔥 Starting Chaos Forge...")
    
    forge = ChaosForge()
    
    async def run_tests():
        if run_all:
            click.echo("Running full chaos suite...")
            results = await forge.run_full_suite()
            
            click.echo(f"\n✅ Completed {len(results)} simulations")
            
            # Summary
            survived = sum(1 for r in results if r.system_survived)
            avg_score = sum(r.resilience_score for r in results) / len(results)
            
            click.echo(f"\nResults:")
            click.echo(f"  Survived: {survived}/{len(results)}")
            click.echo(f"  Avg Resilience Score: {avg_score:.3f}")
            
        elif scenario:
            # Run specific scenario
            scenarios = {
                'network_latency': forge.scenarios[0],
                'database_failure': forge.scenarios[1],
                'ddos': forge.scenarios[2],
                'memory_pressure': forge.scenarios[3],
                'cascading_failure': forge.scenarios[4]
            }
            
            if scenario in scenarios:
                result = await forge.run_simulation(scenarios[scenario])
                
                click.echo(f"\n✅ Simulation complete")
                click.echo(f"  Survived: {result.system_survived}")
                click.echo(f"  Resilience Score: {result.resilience_score:.3f}")
                click.echo(f"  Recovery Time: {result.recovery_time_seconds:.2f}s")
                
                if result.lessons_learned:
                    click.echo(f"\n📚 Lessons Learned:")
                    for lesson in result.lessons_learned:
                        click.echo(f"  - {lesson}")
        else:
            click.echo("Please specify --scenario or --all")
    
    asyncio.run(run_tests())


@chaos.command()
def report():
    """Generate chaos testing report"""
    click.echo("Generating Resilience Delta Report...")
    
    forge = ChaosForge()
    
    # Run a quick test suite first
    async def generate():
        await forge.run_full_suite()
        report = forge.export_report()
        
        click.echo("\n" + "="*60)
        click.echo("RESILIENCE DELTA REPORT")
        click.echo("="*60)
        
        summary = report['summary']
        click.echo(f"\nSummary:")
        click.echo(f"  Total Simulations: {summary['total_simulations']}")
        click.echo(f"  Baseline Resilience: {summary['baseline_resilience']:.3f}")
        click.echo(f"  Current Resilience: {summary['current_resilience']:.3f}")
        click.echo(f"  Improvement: {summary['improvement']}")
        
        delta = report['resilience_delta']
        if delta['threats_mitigated']:
            click.echo(f"\n✅ Threats Mitigated:")
            for threat in delta['threats_mitigated']:
                click.echo(f"  - {threat}")
        
        if delta['vulnerabilities_found']:
            click.echo(f"\n⚠️  Vulnerabilities Found:")
            for vuln in delta['vulnerabilities_found']:
                click.echo(f"  - {vuln}")
        
        if delta['recommendations']:
            click.echo(f"\n💡 Recommendations:")
            for rec in delta['recommendations']:
                click.echo(f"  - {rec}")
        
        # Save to file
        report_path = Path('rafael_chaos_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, indent=2, fp=f)
        
        click.echo(f"\n📄 Full report saved to: {report_path}")
    
    asyncio.run(generate())


@cli.group()
def vault():
    """Manage resilience patterns"""
    pass


@vault.command()
@click.option('--category', type=click.Choice([
    'retry', 'circuit_breaker', 'timeout', 'rate_limit', 'security'
]), help='Filter by category')
@click.option('--tech', type=click.Choice([
    'python', 'nodejs', 'flutter', 'react', 'django', 'fastapi'
]), help='Filter by technology')
def search(category: Optional[str], tech: Optional[str]):
    """Search for resilience patterns"""
    vault_instance = ResilienceVault()
    
    # Convert to enums
    cat_enum = PatternCategory(category) if category else None
    tech_enum = TechnologyStack(tech) if tech else None
    
    patterns = vault_instance.search_patterns(
        category=cat_enum,
        technology=tech_enum,
        min_reliability=0.5
    )
    
    click.echo(f"Found {len(patterns)} patterns:\n")
    
    for pattern in patterns:
        click.echo(f"📦 {pattern.name}")
        click.echo(f"   ID: {pattern.id}")
        click.echo(f"   Category: {pattern.category.value}")
        click.echo(f"   Reliability: {pattern.reliability_score:.2f}")
        click.echo(f"   Status: {pattern.verification_status.value}")
        click.echo(f"   Usage: {pattern.usage_count} times")
        click.echo()


@vault.command()
@click.argument('pattern_id')
def show(pattern_id: str):
    """Show pattern details"""
    vault_instance = ResilienceVault()
    pattern = vault_instance.get_pattern(pattern_id)
    
    if not pattern:
        click.echo(f"❌ Pattern {pattern_id} not found")
        return
    
    click.echo(f"\n{'='*60}")
    click.echo(f"{pattern.name}")
    click.echo(f"{'='*60}\n")
    
    click.echo(f"ID: {pattern.id}")
    click.echo(f"Category: {pattern.category.value}")
    click.echo(f"Reliability: {pattern.reliability_score:.2f}")
    click.echo(f"Verification: {pattern.verification_status.value}")
    
    click.echo(f"\nProblem:")
    click.echo(f"  {pattern.problem}")
    
    click.echo(f"\nSolution:")
    click.echo(f"  {pattern.solution}")
    
    click.echo(f"\nTechnology Stack:")
    for tech in pattern.technology_stack:
        click.echo(f"  - {tech.value}")
    
    click.echo(f"\nCode Example:")
    click.echo(pattern.code_example)
    
    if pattern.tags:
        click.echo(f"\nTags: {', '.join(pattern.tags)}")


@vault.command()
@click.argument('pattern_id')
@click.argument('output_file')
def export(pattern_id: str, output_file: str):
    """Export a pattern to file"""
    vault_instance = ResilienceVault()
    json_data = vault_instance.export_pattern(pattern_id)
    
    if not json_data:
        click.echo(f"❌ Pattern {pattern_id} not found")
        return
    
    output_path = Path(output_file)
    with open(output_path, 'w') as f:
        f.write(json_data)
    
    click.echo(f"✅ Pattern exported to {output_path}")


@vault.command()
def stats():
    """Show vault statistics"""
    vault_instance = ResilienceVault()
    report = vault_instance.generate_report()
    
    click.echo("\n" + "="*60)
    click.echo("RESILIENCE VAULT STATISTICS")
    click.echo("="*60 + "\n")
    
    click.echo(f"Total Patterns: {report['total_patterns']}")
    click.echo(f"Total Collections: {report['total_collections']}")
    click.echo(f"Average Reliability: {report['avg_reliability']:.3f}")
    
    click.echo(f"\nBy Category:")
    for cat, count in report['by_category'].items():
        click.echo(f"  {cat}: {count}")
    
    click.echo(f"\nBy Verification Status:")
    for status, count in report['by_verification_status'].items():
        click.echo(f"  {status}: {count}")
    
    click.echo(f"\nTop Patterns:")
    for p in report['top_patterns']:
        click.echo(f"  - {p['name']} (reliability: {p['reliability']:.2f}, used {p['usage_count']} times)")


@cli.command()
@click.option('--port', default=8080, help='Dashboard port')
def dashboard(port: int):
    """Start RAFAEL dashboard"""
    click.echo(f"🔱 Starting RAFAEL Dashboard on port {port}...")
    click.echo(f"   Open http://localhost:{port} in your browser")
    click.echo(f"\n   Dashboard features:")
    click.echo(f"   - Real-time resilience metrics")
    click.echo(f"   - Evolution timeline")
    click.echo(f"   - Active mutations")
    click.echo(f"   - Chaos test results")
    click.echo(f"\n   Press Ctrl+C to stop")
    
    # In production, this would start a web server
    # For now, just keep running
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\n\n👋 Dashboard stopped")


@cli.command()
def status():
    """Show RAFAEL system status"""
    config = _load_config()
    
    if not config:
        click.echo("❌ RAFAEL not initialized. Run 'rafael init project' first.")
        return
    
    click.echo("\n" + "="*60)
    click.echo("🔱 RAFAEL SYSTEM STATUS")
    click.echo("="*60 + "\n")
    
    click.echo(f"Application: {config['app']['name']}")
    click.echo(f"Technology: {config['app']['technology']}")
    click.echo(f"Environment: {config['app']['environment']}")
    
    click.echo(f"\nResilience Configuration:")
    click.echo(f"  Mutation Rate: {config['resilience']['genome']['mutation_rate']}")
    click.echo(f"  Sandbox Isolation: {config['resilience']['genome']['sandbox_isolation']}")
    click.echo(f"  Auto-Adopt Threshold: {config['resilience']['genome']['auto_adopt_threshold']}")
    
    click.echo(f"\nChaos Forge:")
    click.echo(f"  Enabled: {config['resilience']['chaos_forge']['enabled']}")
    click.echo(f"  Schedule: {config['resilience']['chaos_forge']['schedule']}")
    
    click.echo(f"\nGuardian Layer:")
    click.echo(f"  Approval Required: {config['guardian']['approval_required']}")
    click.echo(f"  Audit Log: {config['guardian']['audit_log']}")
    
    click.echo(f"\n✅ RAFAEL is operational")


def _load_config() -> Optional[dict]:
    """Load RAFAEL configuration"""
    config_path = Path('rafael.config.json')
    if not config_path.exists():
        return None
    
    with open(config_path) as f:
        return json.load(f)


if __name__ == '__main__':
    cli()
