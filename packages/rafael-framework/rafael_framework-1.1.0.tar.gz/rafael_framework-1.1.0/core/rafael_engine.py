"""
RAFAEL Core Engine
The heart of the Resilience-Adaptive Framework
"""

import asyncio
import uuid
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAFAEL")


class ResilienceStrategy(Enum):
    """Available resilience strategies"""
    RETRY_EXPONENTIAL = "retry_exponential"
    RETRY_ADAPTIVE = "retry_adaptive"
    CIRCUIT_BREAKER = "circuit_breaker"
    BULKHEAD = "bulkhead"
    FALLBACK = "fallback"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    CACHE = "cache"
    DEGRADATION = "degradation"


class IsolationLevel(Enum):
    """Isolation levels for testing mutations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Gene:
    """A single resilience gene in the ARG"""
    id: str
    strategy: ResilienceStrategy
    parameters: Dict[str, Any]
    fitness_score: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    last_used: Optional[datetime] = None
    
    def calculate_fitness(self) -> float:
        """Calculate fitness score based on success/failure ratio"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.5  # Neutral score for untested genes
        
        success_rate = self.success_count / total
        # Weight recent performance more heavily
        recency_bonus = 0.1 if self.last_used and \
            (datetime.now() - self.last_used).days < 7 else 0
        
        self.fitness_score = min(1.0, success_rate + recency_bonus)
        return self.fitness_score


@dataclass
class AdaptiveResilienceGenome:
    """
    ARG: The DNA of resilience for a module
    Contains multiple genes (strategies) that can be combined and mutated
    """
    module_id: str
    genes: List[Gene] = field(default_factory=list)
    active_combination: List[str] = field(default_factory=list)
    generation: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_gene(self, gene: Gene):
        """Add a new gene to the genome"""
        self.genes.append(gene)
        logger.info(f"Gene {gene.id} added to module {self.module_id}")
    
    def get_best_genes(self, top_n: int = 3) -> List[Gene]:
        """Get the top performing genes"""
        sorted_genes = sorted(self.genes, key=lambda g: g.calculate_fitness(), reverse=True)
        return sorted_genes[:top_n]
    
    def mutate(self) -> 'AdaptiveResilienceGenome':
        """Create a mutated version of this genome"""
        import random
        
        new_genome = AdaptiveResilienceGenome(
            module_id=self.module_id,
            genes=self.genes.copy(),
            generation=self.generation + 1
        )
        
        # Mutation strategies:
        # 1. Parameter mutation (80% chance)
        if random.random() < 0.8 and new_genome.genes:
            gene_to_mutate = random.choice(new_genome.genes)
            mutated_gene = Gene(
                id=str(uuid.uuid4()),
                strategy=gene_to_mutate.strategy,
                parameters=self._mutate_parameters(gene_to_mutate.parameters)
            )
            new_genome.genes.append(mutated_gene)
        
        # 2. Crossover (combine two high-performing genes)
        if random.random() < 0.3 and len(new_genome.genes) >= 2:
            best_genes = new_genome.get_best_genes(2)
            crossed_gene = self._crossover(best_genes[0], best_genes[1])
            new_genome.genes.append(crossed_gene)
        
        # 3. New random gene (10% chance)
        if random.random() < 0.1:
            new_genome.genes.append(self._random_gene())
        
        return new_genome
    
    def _mutate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mutate parameters slightly"""
        import random
        mutated = params.copy()
        
        for key, value in mutated.items():
            if isinstance(value, (int, float)):
                # Mutate numeric values by ±20%
                mutation_factor = random.uniform(0.8, 1.2)
                mutated[key] = type(value)(value * mutation_factor)
            elif isinstance(value, bool):
                # 10% chance to flip boolean
                if random.random() < 0.1:
                    mutated[key] = not value
        
        return mutated
    
    def _crossover(self, gene1: Gene, gene2: Gene) -> Gene:
        """Combine two genes"""
        import random
        
        # Mix parameters from both genes
        mixed_params = {}
        all_keys = set(gene1.parameters.keys()) | set(gene2.parameters.keys())
        
        for key in all_keys:
            if key in gene1.parameters and key in gene2.parameters:
                # Choose randomly from either parent
                mixed_params[key] = random.choice([
                    gene1.parameters[key],
                    gene2.parameters[key]
                ])
            elif key in gene1.parameters:
                mixed_params[key] = gene1.parameters[key]
            else:
                mixed_params[key] = gene2.parameters[key]
        
        return Gene(
            id=str(uuid.uuid4()),
            strategy=random.choice([gene1.strategy, gene2.strategy]),
            parameters=mixed_params
        )
    
    def _random_gene(self) -> Gene:
        """Generate a random gene"""
        import random
        
        strategy = random.choice(list(ResilienceStrategy))
        
        # Default parameters for each strategy
        param_templates = {
            ResilienceStrategy.RETRY_EXPONENTIAL: {
                "max_retries": random.randint(2, 5),
                "base_delay": random.uniform(0.1, 2.0)
            },
            ResilienceStrategy.CIRCUIT_BREAKER: {
                "failure_threshold": random.randint(3, 10),
                "timeout": random.uniform(30, 120)
            },
            ResilienceStrategy.TIMEOUT: {
                "timeout_seconds": random.uniform(5, 30)
            },
            ResilienceStrategy.RATE_LIMIT: {
                "max_requests": random.randint(10, 100),
                "window_seconds": random.randint(1, 60)
            }
        }
        
        return Gene(
            id=str(uuid.uuid4()),
            strategy=strategy,
            parameters=param_templates.get(strategy, {})
        )


@dataclass
class MutationResult:
    """Result of testing a mutation"""
    genome: AdaptiveResilienceGenome
    fitness_score: float
    test_results: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    adopted: bool = False


class MutationOrchestrator:
    """
    Orchestrates the testing and adoption of genome mutations
    """
    
    def __init__(self, isolation_level: IsolationLevel = IsolationLevel.HIGH):
        self.isolation_level = isolation_level
        self.sandbox_active = False
        self.test_scenarios: List[Callable] = []
    
    async def test_mutation(
        self,
        original_genome: AdaptiveResilienceGenome,
        mutated_genome: AdaptiveResilienceGenome,
        test_scenarios: Optional[List[Callable]] = None
    ) -> MutationResult:
        """
        Test a mutated genome in isolated sandbox
        """
        logger.info(f"Testing mutation for module {mutated_genome.module_id}")
        
        scenarios = test_scenarios or self.test_scenarios
        if not scenarios:
            logger.warning("No test scenarios provided, using default tests")
            scenarios = [self._default_test_scenario]
        
        # Run tests in sandbox
        test_results = {}
        total_fitness = 0.0
        
        for i, scenario in enumerate(scenarios):
            try:
                result = await self._run_in_sandbox(scenario, mutated_genome)
                test_results[f"scenario_{i}"] = result
                total_fitness += result.get("fitness", 0.0)
            except Exception as e:
                logger.error(f"Test scenario {i} failed: {e}")
                test_results[f"scenario_{i}"] = {"error": str(e), "fitness": 0.0}
        
        avg_fitness = total_fitness / len(scenarios) if scenarios else 0.0
        
        return MutationResult(
            genome=mutated_genome,
            fitness_score=avg_fitness,
            test_results=test_results
        )
    
    async def _run_in_sandbox(
        self,
        test_func: Callable,
        genome: AdaptiveResilienceGenome
    ) -> Dict[str, Any]:
        """
        Execute test in isolated sandbox based on isolation level
        """
        self.sandbox_active = True
        
        try:
            # Apply isolation based on level
            if self.isolation_level == IsolationLevel.CRITICAL:
                # Full process isolation (would use containers in production)
                result = await self._isolated_execution(test_func, genome)
            else:
                # Thread-level isolation
                result = await test_func(genome)
            
            return {
                "success": True,
                "fitness": result.get("fitness", 0.5),
                "metrics": result
            }
        except Exception as e:
            logger.error(f"Sandbox execution failed: {e}")
            return {
                "success": False,
                "fitness": 0.0,
                "error": str(e)
            }
        finally:
            self.sandbox_active = False
    
    async def _isolated_execution(
        self,
        test_func: Callable,
        genome: AdaptiveResilienceGenome
    ) -> Dict[str, Any]:
        """
        Execute in maximum isolation (placeholder for container/VM execution)
        """
        # In production, this would spawn a container or VM
        # For now, we'll use asyncio task isolation
        task = asyncio.create_task(test_func(genome))
        return await asyncio.wait_for(task, timeout=30.0)
    
    async def _default_test_scenario(
        self,
        genome: AdaptiveResilienceGenome
    ) -> Dict[str, Any]:
        """Default test scenario"""
        # Simulate some load and measure resilience
        success_count = 0
        total_tests = 10
        
        for _ in range(total_tests):
            try:
                # Simulate work
                await asyncio.sleep(0.01)
                success_count += 1
            except Exception:
                pass
        
        return {
            "fitness": success_count / total_tests,
            "success_rate": success_count / total_tests
        }


class FitnessEvaluator:
    """
    Evaluates and compares fitness of different genomes
    """
    
    def __init__(self, adoption_threshold: float = 0.85):
        self.adoption_threshold = adoption_threshold
        self.evaluation_history: List[MutationResult] = []
    
    def should_adopt(
        self,
        current_genome: AdaptiveResilienceGenome,
        mutation_result: MutationResult
    ) -> bool:
        """
        Determine if mutation should be adopted
        """
        # Calculate current genome fitness
        current_fitness = sum(g.calculate_fitness() for g in current_genome.genes) / \
                         len(current_genome.genes) if current_genome.genes else 0.0
        
        mutation_fitness = mutation_result.fitness_score
        
        logger.info(f"Current fitness: {current_fitness:.3f}, "
                   f"Mutation fitness: {mutation_fitness:.3f}")
        
        # Adopt if mutation is significantly better
        if mutation_fitness > current_fitness * self.adoption_threshold:
            logger.info("✅ Mutation adopted!")
            mutation_result.adopted = True
            self.evaluation_history.append(mutation_result)
            return True
        
        logger.info("❌ Mutation rejected")
        self.evaluation_history.append(mutation_result)
        return False
    
    def get_evolution_metrics(self) -> Dict[str, Any]:
        """Get metrics about the evolution process"""
        if not self.evaluation_history:
            return {"total_mutations": 0}
        
        adopted = [r for r in self.evaluation_history if r.adopted]
        
        return {
            "total_mutations": len(self.evaluation_history),
            "adopted_mutations": len(adopted),
            "adoption_rate": len(adopted) / len(self.evaluation_history),
            "avg_fitness": sum(r.fitness_score for r in self.evaluation_history) / \
                          len(self.evaluation_history),
            "best_fitness": max(r.fitness_score for r in self.evaluation_history),
            "generations": max(r.genome.generation for r in self.evaluation_history)
        }


class RafaelCore:
    """
    Main RAFAEL Core Engine
    Coordinates ARG, Mutation Orchestrator, and Fitness Evaluator
    """
    
    def __init__(
        self,
        app_name: str,
        resilience_level: str = "adaptive",
        config: Optional[Dict[str, Any]] = None
    ):
        self.app_name = app_name
        self.resilience_level = resilience_level
        self.config = config or {}
        
        # Core components
        self.genomes: Dict[str, AdaptiveResilienceGenome] = {}
        self.orchestrator = MutationOrchestrator()
        self.evaluator = FitnessEvaluator(
            adoption_threshold=self.config.get("adoption_threshold", 0.85)
        )
        
        # Evolution state
        self.evolution_active = False
        self.evolution_task: Optional[asyncio.Task] = None
        
        logger.info(f"🔱 RAFAEL Core initialized for {app_name}")
    
    def register_module(
        self,
        module_id: str,
        initial_strategies: Optional[List[ResilienceStrategy]] = None
    ) -> AdaptiveResilienceGenome:
        """Register a new module with its initial ARG"""
        genome = AdaptiveResilienceGenome(module_id=module_id)
        
        # Add initial strategies
        strategies = initial_strategies or [
            ResilienceStrategy.RETRY_ADAPTIVE,
            ResilienceStrategy.CIRCUIT_BREAKER,
            ResilienceStrategy.TIMEOUT
        ]
        
        for strategy in strategies:
            gene = Gene(
                id=str(uuid.uuid4()),
                strategy=strategy,
                parameters=self._default_parameters(strategy)
            )
            genome.add_gene(gene)
        
        self.genomes[module_id] = genome
        logger.info(f"Module {module_id} registered with {len(strategies)} initial genes")
        
        return genome
    
    def _default_parameters(self, strategy: ResilienceStrategy) -> Dict[str, Any]:
        """Get default parameters for a strategy"""
        defaults = {
            ResilienceStrategy.RETRY_ADAPTIVE: {
                "max_retries": 3,
                "base_delay": 1.0,
                "max_delay": 10.0
            },
            ResilienceStrategy.CIRCUIT_BREAKER: {
                "failure_threshold": 5,
                "timeout": 60,
                "half_open_max_calls": 3
            },
            ResilienceStrategy.TIMEOUT: {
                "timeout_seconds": 10.0
            },
            ResilienceStrategy.RATE_LIMIT: {
                "max_requests": 100,
                "window_seconds": 60
            }
        }
        return defaults.get(strategy, {})
    
    async def evolve_module(self, module_id: str) -> Optional[MutationResult]:
        """Trigger evolution for a specific module"""
        if module_id not in self.genomes:
            logger.error(f"Module {module_id} not registered")
            return None
        
        current_genome = self.genomes[module_id]
        
        # Generate mutation
        mutated_genome = current_genome.mutate()
        
        # Test mutation
        result = await self.orchestrator.test_mutation(current_genome, mutated_genome)
        
        # Evaluate and potentially adopt
        if self.evaluator.should_adopt(current_genome, result):
            self.genomes[module_id] = mutated_genome
            logger.info(f"Module {module_id} evolved to generation {mutated_genome.generation}")
        
        return result
    
    async def start_evolution(self, interval_seconds: int = 3600):
        """Start autonomous evolution process"""
        if self.evolution_active:
            logger.warning("Evolution already active")
            return
        
        self.evolution_active = True
        logger.info(f"🧬 Starting autonomous evolution (interval: {interval_seconds}s)")
        
        async def evolution_loop():
            while self.evolution_active:
                for module_id in self.genomes.keys():
                    if not self.evolution_active:
                        break
                    
                    try:
                        await self.evolve_module(module_id)
                    except Exception as e:
                        logger.error(f"Evolution failed for {module_id}: {e}")
                
                await asyncio.sleep(interval_seconds)
        
        self.evolution_task = asyncio.create_task(evolution_loop())
    
    def stop_evolution(self):
        """Stop autonomous evolution"""
        self.evolution_active = False
        if self.evolution_task:
            self.evolution_task.cancel()
        logger.info("Evolution stopped")
    
    def get_resilience_report(self) -> Dict[str, Any]:
        """Generate comprehensive resilience report"""
        return {
            "app_name": self.app_name,
            "timestamp": datetime.now().isoformat(),
            "modules": {
                module_id: {
                    "generation": genome.generation,
                    "genes_count": len(genome.genes),
                    "avg_fitness": sum(g.calculate_fitness() for g in genome.genes) / \
                                  len(genome.genes) if genome.genes else 0.0,
                    "best_genes": [
                        {
                            "strategy": g.strategy.value,
                            "fitness": g.calculate_fitness(),
                            "success_rate": g.success_count / (g.success_count + g.failure_count)
                            if (g.success_count + g.failure_count) > 0 else 0.0
                        }
                        for g in genome.get_best_genes(3)
                    ]
                }
                for module_id, genome in self.genomes.items()
            },
            "evolution_metrics": self.evaluator.get_evolution_metrics()
        }
    
    def export_genome(self, module_id: str) -> Optional[str]:
        """Export genome as JSON for sharing"""
        if module_id not in self.genomes:
            return None
        
        genome = self.genomes[module_id]
        data = {
            "module_id": genome.module_id,
            "generation": genome.generation,
            "genes": [
                {
                    "id": g.id,
                    "strategy": g.strategy.value,
                    "parameters": g.parameters,
                    "fitness_score": g.fitness_score
                }
                for g in genome.genes
            ]
        }
        return json.dumps(data, indent=2)
