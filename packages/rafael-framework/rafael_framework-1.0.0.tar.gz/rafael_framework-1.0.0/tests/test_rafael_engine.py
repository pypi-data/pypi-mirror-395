"""
Tests for RAFAEL Core Engine
"""

import pytest
import asyncio
from core.rafael_engine import (
    RafaelCore,
    AdaptiveResilienceGenome,
    Gene,
    ResilienceStrategy,
    MutationOrchestrator,
    FitnessEvaluator
)


class TestAdaptiveResilienceGenome:
    """Test ARG functionality"""
    
    def test_genome_creation(self):
        """Test creating a genome"""
        genome = AdaptiveResilienceGenome(module_id="test_module")
        assert genome.module_id == "test_module"
        assert len(genome.genes) == 0
        assert genome.generation == 0
    
    def test_add_gene(self):
        """Test adding genes to genome"""
        genome = AdaptiveResilienceGenome(module_id="test_module")
        
        gene = Gene(
            id="gene_1",
            strategy=ResilienceStrategy.RETRY_ADAPTIVE,
            parameters={"max_retries": 3}
        )
        
        genome.add_gene(gene)
        assert len(genome.genes) == 1
        assert genome.genes[0].id == "gene_1"
    
    def test_gene_fitness_calculation(self):
        """Test fitness score calculation"""
        gene = Gene(
            id="gene_1",
            strategy=ResilienceStrategy.RETRY_ADAPTIVE,
            parameters={"max_retries": 3}
        )
        
        # Simulate successes
        gene.success_count = 8
        gene.failure_count = 2
        
        fitness = gene.calculate_fitness()
        assert fitness == 0.8  # 8/10 success rate
    
    def test_genome_mutation(self):
        """Test genome mutation"""
        genome = AdaptiveResilienceGenome(module_id="test_module")
        
        gene = Gene(
            id="gene_1",
            strategy=ResilienceStrategy.RETRY_ADAPTIVE,
            parameters={"max_retries": 3}
        )
        genome.add_gene(gene)
        
        # Create mutation
        mutated = genome.mutate()
        
        assert mutated.module_id == genome.module_id
        assert mutated.generation == genome.generation + 1
        # Mutation should add new genes
        assert len(mutated.genes) >= len(genome.genes)
    
    def test_get_best_genes(self):
        """Test getting best performing genes"""
        genome = AdaptiveResilienceGenome(module_id="test_module")
        
        # Add genes with different fitness
        for i in range(5):
            gene = Gene(
                id=f"gene_{i}",
                strategy=ResilienceStrategy.RETRY_ADAPTIVE,
                parameters={"max_retries": i + 1}
            )
            gene.success_count = i * 2
            gene.failure_count = 10 - (i * 2)
            genome.add_gene(gene)
        
        best = genome.get_best_genes(top_n=3)
        assert len(best) == 3
        # Should be sorted by fitness
        assert best[0].calculate_fitness() >= best[1].calculate_fitness()


class TestMutationOrchestrator:
    """Test Mutation Orchestrator"""
    
    @pytest.mark.asyncio
    async def test_mutation_testing(self):
        """Test mutation testing in sandbox"""
        orchestrator = MutationOrchestrator()
        
        original = AdaptiveResilienceGenome(module_id="test")
        mutated = original.mutate()
        
        result = await orchestrator.test_mutation(original, mutated)
        
        assert result.genome == mutated
        assert 0.0 <= result.fitness_score <= 1.0
        assert isinstance(result.test_results, dict)


class TestFitnessEvaluator:
    """Test Fitness Evaluator"""
    
    @pytest.mark.asyncio
    async def test_adoption_decision(self):
        """Test mutation adoption decision"""
        evaluator = FitnessEvaluator(adoption_threshold=0.85)
        
        # Create genomes
        current = AdaptiveResilienceGenome(module_id="test")
        gene = Gene(
            id="gene_1",
            strategy=ResilienceStrategy.RETRY_ADAPTIVE,
            parameters={"max_retries": 3}
        )
        gene.success_count = 5
        gene.failure_count = 5
        current.add_gene(gene)
        
        # Create mutation result with higher fitness
        from core.rafael_engine import MutationResult
        from datetime import datetime
        
        mutated = current.mutate()
        result = MutationResult(
            genome=mutated,
            fitness_score=0.9,
            test_results={}
        )
        
        should_adopt = evaluator.should_adopt(current, result)
        assert isinstance(should_adopt, bool)


class TestRafaelCore:
    """Test RAFAEL Core"""
    
    def test_core_initialization(self):
        """Test core initialization"""
        core = RafaelCore(app_name="test-app")
        
        assert core.app_name == "test-app"
        assert len(core.genomes) == 0
        assert core.orchestrator is not None
        assert core.evaluator is not None
    
    def test_module_registration(self):
        """Test module registration"""
        core = RafaelCore(app_name="test-app")
        
        genome = core.register_module("test_module")
        
        assert "test_module" in core.genomes
        assert genome.module_id == "test_module"
        assert len(genome.genes) > 0  # Should have default genes
    
    @pytest.mark.asyncio
    async def test_module_evolution(self):
        """Test module evolution"""
        core = RafaelCore(app_name="test-app")
        core.register_module("test_module")
        
        result = await core.evolve_module("test_module")
        
        assert result is not None
        assert result.genome.module_id == "test_module"
        assert 0.0 <= result.fitness_score <= 1.0
    
    def test_resilience_report(self):
        """Test resilience report generation"""
        core = RafaelCore(app_name="test-app")
        core.register_module("module_1")
        core.register_module("module_2")
        
        report = core.get_resilience_report()
        
        assert report["app_name"] == "test-app"
        assert "modules" in report
        assert len(report["modules"]) == 2
        assert "evolution_metrics" in report
    
    def test_genome_export(self):
        """Test genome export"""
        core = RafaelCore(app_name="test-app")
        core.register_module("test_module")
        
        exported = core.export_genome("test_module")
        
        assert exported is not None
        assert isinstance(exported, str)
        assert "test_module" in exported


@pytest.mark.asyncio
async def test_integration():
    """Integration test"""
    # Create core
    core = RafaelCore(app_name="integration-test")
    
    # Register modules
    core.register_module("module_a")
    core.register_module("module_b")
    
    # Evolve modules
    result_a = await core.evolve_module("module_a")
    result_b = await core.evolve_module("module_b")
    
    assert result_a is not None
    assert result_b is not None
    
    # Get report
    report = core.get_resilience_report()
    assert len(report["modules"]) == 2
    
    # Check evolution metrics
    metrics = report["evolution_metrics"]
    assert metrics["total_mutations"] >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
