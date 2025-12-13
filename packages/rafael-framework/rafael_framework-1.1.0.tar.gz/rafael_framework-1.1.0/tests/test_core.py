"""
Tests for RAFAEL Core Engine
"""

import pytest
from datetime import datetime
from core.rafael_engine import (
    RafaelCore,
    AdaptiveResilienceGenome,
    Gene,
    ResilienceStrategy,
    MutationOrchestrator,
    FitnessEvaluator
)


class TestGene:
    """Test Gene class"""
    
    def test_gene_creation(self):
        """Test creating a gene"""
        gene = Gene(
            id="test-gene-1",
            strategy=ResilienceStrategy.RETRY,
            parameters={"max_retries": 3, "backoff": "exponential"},
            fitness_score=0.0
        )
        assert gene.id == "test-gene-1"
        assert gene.strategy == ResilienceStrategy.RETRY
        assert gene.fitness_score == 0.0
    
    def test_gene_fitness_calculation(self):
        """Test fitness score calculation"""
        gene = Gene(
            id="test-gene-2",
            strategy=ResilienceStrategy.CIRCUIT_BREAKER,
            parameters={},
            success_count=8,
            failure_count=2
        )
        fitness = gene.calculate_fitness()
        assert fitness == 0.8  # 8/(8+2)
    
    def test_gene_no_data(self):
        """Test fitness with no data"""
        gene = Gene(
            id="test-gene-3",
            strategy=ResilienceStrategy.FALLBACK,
            parameters={}
        )
        fitness = gene.calculate_fitness()
        assert fitness == 0.0


class TestAdaptiveResilienceGenome:
    """Test ARG class"""
    
    def test_genome_creation(self):
        """Test creating a genome"""
        genome = AdaptiveResilienceGenome(module_id="payment-service")
        assert genome.module_id == "payment-service"
        assert len(genome.genes) == 0
        assert genome.generation == 0
    
    def test_add_gene(self):
        """Test adding genes to genome"""
        genome = AdaptiveResilienceGenome(module_id="auth-service")
        gene = Gene(
            id="gene-1",
            strategy=ResilienceStrategy.RETRY,
            parameters={"max_retries": 3}
        )
        genome.add_gene(gene)
        assert len(genome.genes) == 1
        assert genome.genes[0].id == "gene-1"
    
    def test_get_gene(self):
        """Test retrieving a gene"""
        genome = AdaptiveResilienceGenome(module_id="test-service")
        gene = Gene(
            id="gene-1",
            strategy=ResilienceStrategy.RATE_LIMIT,
            parameters={"max_requests": 100}
        )
        genome.add_gene(gene)
        retrieved = genome.get_gene("gene-1")
        assert retrieved is not None
        assert retrieved.id == "gene-1"
    
    def test_get_nonexistent_gene(self):
        """Test retrieving non-existent gene"""
        genome = AdaptiveResilienceGenome(module_id="test-service")
        retrieved = genome.get_gene("nonexistent")
        assert retrieved is None


class TestMutationOrchestrator:
    """Test Mutation Orchestrator"""
    
    def test_orchestrator_creation(self):
        """Test creating mutation orchestrator"""
        orchestrator = MutationOrchestrator()
        assert orchestrator is not None
    
    def test_generate_mutation(self):
        """Test generating a mutation"""
        orchestrator = MutationOrchestrator()
        genome = AdaptiveResilienceGenome(module_id="test-service")
        gene = Gene(
            id="gene-1",
            strategy=ResilienceStrategy.RETRY,
            parameters={"max_retries": 3}
        )
        genome.add_gene(gene)
        
        mutation = orchestrator.generate_mutation(genome)
        assert mutation is not None


class TestFitnessEvaluator:
    """Test Fitness Evaluator"""
    
    def test_evaluator_creation(self):
        """Test creating fitness evaluator"""
        evaluator = FitnessEvaluator()
        assert evaluator is not None
    
    def test_evaluate_gene(self):
        """Test evaluating a gene"""
        evaluator = FitnessEvaluator()
        gene = Gene(
            id="gene-1",
            strategy=ResilienceStrategy.RETRY,
            parameters={"max_retries": 3},
            success_count=7,
            failure_count=3
        )
        
        score = evaluator.evaluate_gene(gene)
        assert score >= 0.0
        assert score <= 1.0


class TestRafaelCore:
    """Test RAFAEL Core Engine"""
    
    def test_core_creation(self):
        """Test creating RAFAEL core"""
        core = RafaelCore()
        assert core is not None
    
    def test_register_module(self):
        """Test registering a module"""
        core = RafaelCore()
        genome = core.register_module("test-module")
        assert genome is not None
        assert genome.module_id == "test-module"
    
    def test_get_module(self):
        """Test getting a module"""
        core = RafaelCore()
        core.register_module("test-module")
        genome = core.get_module("test-module")
        assert genome is not None
        assert genome.module_id == "test-module"
    
    def test_get_nonexistent_module(self):
        """Test getting non-existent module"""
        core = RafaelCore()
        genome = core.get_module("nonexistent")
        assert genome is None


class TestResilienceStrategy:
    """Test Resilience Strategy Enum"""
    
    def test_strategy_values(self):
        """Test all strategy values exist"""
        assert ResilienceStrategy.RETRY is not None
        assert ResilienceStrategy.CIRCUIT_BREAKER is not None
        assert ResilienceStrategy.FALLBACK is not None
        assert ResilienceStrategy.RATE_LIMIT is not None
        assert ResilienceStrategy.TIMEOUT is not None
        assert ResilienceStrategy.BULKHEAD is not None
        assert ResilienceStrategy.CACHE is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
