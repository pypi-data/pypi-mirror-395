"""
RAFAEL Framework - Web Dashboard
Modern web interface for monitoring and managing RAFAEL systems
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import RafaelCore, AdaptiveResilienceGenome
from chaos_forge import ChaosForge, ThreatType
from vault import ResilienceVault
from guardian import GuardianLayer

app = Flask(__name__)
CORS(app)

# Initialize RAFAEL components
rafael = RafaelCore(app_name="rafael-dashboard")
chaos_forge = ChaosForge()
vault = ResilienceVault()
guardian = GuardianLayer()

# Sample data for demo
demo_modules = ["payment-service", "auth-service", "notification-service"]
for module in demo_modules:
    genome = rafael.register_module(module)
    # Add initial genes with some fitness scores for demo
    from core.rafael_engine import Gene, ResilienceStrategy
    import random
    
    # Add 3 sample genes with random fitness
    strategies = [
        ResilienceStrategy.RETRY_ADAPTIVE,
        ResilienceStrategy.CIRCUIT_BREAKER,
        ResilienceStrategy.FALLBACK
    ]
    
    for i, strategy in enumerate(strategies):
        gene = Gene(
            id=f"{module}-gene-{i}",
            strategy=strategy,
            parameters={"timeout": 30, "max_retries": 3},
            fitness_score=random.uniform(0.6, 0.95),  # Random fitness for demo
            success_count=random.randint(50, 200),
            failure_count=random.randint(5, 20)
        )
        genome.add_gene(gene)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get overall system status"""
    modules = []
    for module_id in demo_modules:
        genome = rafael.genomes.get(module_id)
        if genome:
            # Calculate average fitness from genes
            avg_fitness = sum(g.fitness_score for g in genome.genes) / len(genome.genes) if genome.genes else 0.0
            modules.append({
                'id': module_id,
                'fitness': avg_fitness,
                'generation': genome.generation,
                'genes_count': len(genome.genes),
                'status': 'healthy' if avg_fitness > 0.7 else 'warning' if avg_fitness > 0.4 else 'critical'
            })
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'total_modules': len(demo_modules),
        'healthy_modules': sum(1 for m in modules if m['status'] == 'healthy'),
        'modules': modules,
        'vault_patterns': len(vault.patterns),
        'pending_approvals': len(guardian.pending_approvals)
    })

@app.route('/api/modules')
def get_modules():
    """Get all registered modules"""
    modules = []
    for module_id in demo_modules:
        genome = rafael.genomes.get(module_id)
        if genome:
            avg_fitness = sum(g.fitness_score for g in genome.genes) / len(genome.genes) if genome.genes else 0.0
            modules.append({
                'id': module_id,
                'fitness': avg_fitness,
                'generation': genome.generation,
                'genes': [
                    {
                        'strategy': gene.strategy.value,
                        'params': gene.parameters,
                        'fitness': gene.fitness_score
                    } for gene in genome.genes
                ]
            })
    
    return jsonify({'modules': modules})

@app.route('/api/modules/<module_id>/evolve', methods=['POST'])
def evolve_module(module_id):
    """Trigger evolution for a module"""
    try:
        rafael.evolve_module(module_id)
        genome = rafael.genomes.get(module_id)
        
        avg_fitness = sum(g.fitness_score for g in genome.genes) / len(genome.genes) if genome.genes else 0.0
        return jsonify({
            'success': True,
            'module_id': module_id,
            'new_fitness': avg_fitness,
            'generation': genome.generation
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/chaos/simulate', methods=['POST', 'OPTIONS'])
def simulate_chaos():
    """Run chaos simulation"""
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    
    try:
        data = request.get_json(force=True, silent=True) or {}
        module_id = data.get('module_id', demo_modules[0])
        threat_type_str = data.get('threat_type', 'ddos_attack')
        severity = data.get('severity', 'medium')
        
        # Map threat type string to enum
        threat_map = {
            'ddos_attack': ThreatType.DDOS_ATTACK,
            'network_latency': ThreatType.NETWORK_LATENCY,
            'database_failure': ThreatType.DATABASE_FAILURE,
            'memory_pressure': ThreatType.MEMORY_PRESSURE,
            'cpu_spike': ThreatType.CPU_SPIKE
        }
        
        threat = threat_map.get(threat_type_str, ThreatType.DDOS_ATTACK)
        
        # For demo purposes, return simulated results immediately
        # In production, this would run actual chaos tests
        import random
        from chaos_forge import ThreatSeverity
        
        # Simulate realistic results
        success_rate = random.uniform(0.75, 0.95)
        resilience_score = random.uniform(0.70, 0.90)
        
        severity_map = {
            'low': ThreatSeverity.LOW,
            'medium': ThreatSeverity.MEDIUM,
            'high': ThreatSeverity.HIGH,
            'critical': ThreatSeverity.CRITICAL
        }
        
        result_severity = severity_map.get(severity, ThreatSeverity.MEDIUM)
        
        recommendations = [
            f"Increase retry attempts for {module_id}",
            f"Implement circuit breaker for {threat_type_str}",
            "Add fallback mechanisms",
            "Monitor system metrics closely"
        ]
        
        return jsonify({
            'success': True,
            'result': {
                'module_id': module_id,
                'threat_type': threat.value,
                'severity': result_severity.value,
                'success_rate': round(success_rate, 2),
                'resilience_score': round(resilience_score, 2),
                'recommendations': recommendations[:2]
            }
        })
    except Exception as e:
        import traceback
        return jsonify({
            'success': False, 
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/vault/patterns')
def get_patterns():
    """Get all resilience patterns"""
    patterns = []
    for pattern in vault.patterns.values():
        # Ensure reliability_score is a valid number
        reliability = pattern.reliability_score if hasattr(pattern, 'reliability_score') and pattern.reliability_score is not None else 0.85
        usage_count = pattern.usage_count if hasattr(pattern, 'usage_count') and pattern.usage_count is not None else 0
        
        patterns.append({
            'id': pattern.id,
            'name': pattern.name,
            'category': pattern.category.value,
            'description': pattern.description,
            'reliability': float(reliability),  # Ensure it's a float
            'usage_count': int(usage_count)  # Ensure it's an int
        })
    
    return jsonify({'patterns': patterns})

@app.route('/api/vault/search', methods=['POST'])
def search_patterns():
    """Search patterns by criteria"""
    data = request.json
    tech = data.get('tech')
    category = data.get('category')
    
    results = vault.search_patterns(
        technology=tech,
        category=category
    )
    
    patterns = []
    for pattern in results:
        reliability = pattern.reliability_score if hasattr(pattern, 'reliability_score') and pattern.reliability_score is not None else 0.85
        
        patterns.append({
            'id': pattern.id,
            'name': pattern.name,
            'category': pattern.category.value,
            'description': pattern.description,
            'reliability': float(reliability)
        })
    
    return jsonify({'patterns': patterns})

@app.route('/api/guardian/approvals')
def get_approvals():
    """Get pending approvals"""
    approvals = []
    for approval_id, request in guardian.pending_approvals.items():
        approvals.append({
            'id': approval_id,
            'module_id': request.module_id,
            'change_type': request.change.change_type,
            'timestamp': request.timestamp.isoformat(),
            'impact': request.impact.value if request.impact else 'unknown'
        })
    
    return jsonify({'approvals': approvals})

@app.route('/api/guardian/approve/<approval_id>', methods=['POST'])
def approve_change(approval_id):
    """Approve a pending change"""
    data = request.json
    approver = data.get('approver', 'admin')
    
    try:
        guardian.approve_change(approval_id, approver)
        return jsonify({'success': True, 'approval_id': approval_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/guardian/reject/<approval_id>', methods=['POST'])
def reject_change(approval_id):
    """Reject a pending change"""
    data = request.json
    approver = data.get('approver', 'admin')
    reason = data.get('reason', 'No reason provided')
    
    try:
        guardian.reject_change(approval_id, approver, reason)
        return jsonify({'success': True, 'approval_id': approval_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    total_genes = sum(len(g.genes) for g in rafael.genomes.values())
    avg_fitness = sum(g.fitness_score for g in rafael.genomes.values()) / len(rafael.genomes) if rafael.genomes else 0
    
    return jsonify({
        'total_modules': len(rafael.genomes),
        'total_genes': total_genes,
        'average_fitness': round(avg_fitness, 3),
        'vault_patterns': len(vault.patterns),
        'pending_approvals': len(guardian.pending_approvals),
        'audit_logs': len(guardian.audit_log)
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🔱 RAFAEL Dashboard starting...")
    print("📊 Dashboard URL: http://localhost:5000")
    print("🚀 API Docs: http://localhost:5000/api/status")
    app.run(host='0.0.0.0', port=5000, debug=True)
