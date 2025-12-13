"""
Integration tests for RAFAEL Framework
Tests the interaction between all major components
"""

import pytest
import asyncio
from datetime import datetime
from core.rafael_engine import RafaelCore, ResilienceStrategy
from chaos_forge.simulator import ChaosForge, ThreatScenario, ThreatType, ThreatSeverity
from vault.resilience_vault import ResilienceVault, PatternCategory, TechnologyStack
from guardian.guardian_layer import GuardianLayer, MutationChange, ChangeImpact


class TestCoreAndVaultIntegration:
    """Test integration between Core Engine and Resilience Vault"""
    
    def test_core_uses_vault_patterns(self):
        """Test Core Engine can use patterns from Vault"""
        core = RafaelCore(app_name="vault-test")
        vault = ResilienceVault()
        
        # Register module
        core.register_module("test_module")
        
        # Get patterns from vault
        patterns = vault.search_patterns(
            category=PatternCategory.RETRY,
            min_reliability=0.7
        )
        
        assert len(patterns) > 0
        assert core.genomes["test_module"] is not None
    
    def test_vault_pattern_application(self):
        """Test applying vault patterns to core modules"""
        core = RafaelCore(app_name="pattern-app")
        vault = ResilienceVault()
        
        # Register module
        genome = core.register_module("api_module")
        
        # Get recommended patterns
        patterns = vault.get_recommendations(
            technology_stack=[TechnologyStack.PYTHON, TechnologyStack.FASTAPI]
        )
        
        assert len(patterns) > 0
        assert genome.module_id == "api_module"
    
    def test_pattern_usage_tracking(self):
        """Test pattern usage is tracked correctly"""
        vault = ResilienceVault()
        
        # Get a pattern
        patterns = vault.search_patterns(category=PatternCategory.RETRY)
        if patterns:
            pattern_id = patterns[0].id
            
            # Record usage
            vault.record_usage(pattern_id, success=True)
            vault.record_usage(pattern_id, success=True)
            vault.record_usage(pattern_id, success=False)
            
            # Check usage count
            pattern = vault.get_pattern(pattern_id)
            assert pattern.usage_count == 3
            assert 0 <= pattern.success_rate <= 1


class TestCoreAndChaosIntegration:
    """Test integration between Core Engine and Chaos Forge"""
    
    @pytest.mark.asyncio
    async def test_chaos_tests_core_resilience(self):
        """Test Chaos Forge can test Core Engine resilience"""
        core = RafaelCore(app_name="chaos-test")
        chaos = ChaosForge()
        
        # Register module
        core.register_module("resilient_module")
        
        # Create simple target function
        async def target_function():
            await asyncio.sleep(0.01)
            return "success"
        
        # Run chaos simulation
        scenario = ThreatScenario(
            id="test_scenario",
            name="Test Network Latency",
            threat_type=ThreatType.NETWORK_LATENCY,
            severity=ThreatSeverity.LOW,
            description="Test scenario",
            parameters={"latency_ms": 100},
            duration_seconds=1.0
        )
        
        result = await chaos.run_simulation(scenario, target_function)
        
        assert result.success
        assert result.resilience_score >= 0
    
    @pytest.mark.asyncio
    async def test_core_evolves_from_chaos_results(self):
        """Test Core Engine evolves based on chaos test results"""
        core = RafaelCore(app_name="evolution-test")
        chaos = ChaosForge()
        
        # Register module
        core.register_module("evolving_module")
        
        # Run chaos tests
        results = await chaos.run_full_suite()
        
        # Trigger evolution based on results
        evolution_result = await core.evolve_module("evolving_module")
        
        assert evolution_result is not None
        assert len(results) > 0
    
    @pytest.mark.asyncio
    async def test_chaos_delta_tracking(self):
        """Test resilience delta tracking across chaos tests"""
        chaos = ChaosForge()
        
        async def improving_function():
            # Simulate improving resilience
            await asyncio.sleep(0.01)
            return "success"
        
        # Run multiple simulations
        for _ in range(5):
            scenario = ThreatScenario(
                id=f"scenario_{_}",
                name=f"Test {_}",
                threat_type=ThreatType.NETWORK_LATENCY,
                severity=ThreatSeverity.LOW,
                description="Test",
                parameters={"latency_ms": 50},
                duration_seconds=0.5
            )
            await chaos.run_simulation(scenario, improving_function)
        
        # Calculate delta
        delta = chaos.calculate_resilience_delta()
        
        assert delta.simulations_run == 5
        assert delta.baseline_score >= 0
        assert delta.current_score >= 0


class TestCoreAndGuardianIntegration:
    """Test integration between Core Engine and Guardian Layer"""
    
    @pytest.mark.asyncio
    async def test_guardian_approves_mutations(self):
        """Test Guardian Layer approves Core Engine mutations"""
        core = RafaelCore(app_name="guardian-test")
        guardian = GuardianLayer()
        
        # Register module
        genome = core.register_module("guarded_module")
        
        # Create mutation
        mutated = genome.mutate()
        
        # Request approval
        change = MutationChange(
            id="change_001",
            module_id="guarded_module",
            change_type="mutation",
            description="Test mutation",
            impact=ChangeImpact.LOW,
            old_genome={"generation": 0},
            new_genome={"generation": 1},
            fitness_improvement=0.15
        )
        
        request = guardian.request_approval(change)
        
        # Low impact should auto-approve
        assert request.status.value in ["auto_approved", "pending"]
    
    def test_guardian_audit_log_for_evolution(self):
        """Test Guardian creates audit log for evolution events"""
        core = RafaelCore(app_name="audit-test")
        guardian = GuardianLayer()
        
        # Register module
        core.register_module("audited_module")
        
        # Create change
        change = MutationChange(
            id="change_002",
            module_id="audited_module",
            change_type="evolution",
            description="Evolution event",
            impact=ChangeImpact.MEDIUM,
            old_genome={},
            new_genome={},
            fitness_improvement=0.25
        )
        
        guardian.request_approval(change)
        
        # Check audit log
        audit_entries = guardian.get_audit_log(module_id="audited_module")
        assert len(audit_entries) > 0
    
    def test_guardian_blocks_critical_changes(self):
        """Test Guardian blocks critical changes without approval"""
        guardian = GuardianLayer()
        
        # Create critical change
        change = MutationChange(
            id="critical_001",
            module_id="critical_module",
            change_type="major_mutation",
            description="Critical system change",
            impact=ChangeImpact.CRITICAL,
            old_genome={},
            new_genome={},
            fitness_improvement=0.50
        )
        
        request = guardian.request_approval(change)
        
        # Critical changes should require manual approval
        assert request.status.value == "pending"
        assert not request.auto_approved


class TestFullSystemIntegration:
    """Test full system integration with all components"""
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        """Test complete workflow: Core -> Chaos -> Vault -> Guardian"""
        # Initialize all components
        core = RafaelCore(app_name="full-system")
        chaos = ChaosForge()
        vault = ResilienceVault()
        guardian = GuardianLayer()
        
        # Step 1: Register module with Core
        genome = core.register_module("complete_module", [
            ResilienceStrategy.RETRY_ADAPTIVE,
            ResilienceStrategy.CIRCUIT_BREAKER
        ])
        
        assert genome is not None
        
        # Step 2: Get patterns from Vault
        patterns = vault.search_patterns(
            category=PatternCategory.RETRY,
            min_reliability=0.5
        )
        
        assert len(patterns) > 0
        
        # Step 3: Run chaos test
        async def test_target():
            await asyncio.sleep(0.01)
            return "success"
        
        scenario = ThreatScenario(
            id="full_test",
            name="Full System Test",
            threat_type=ThreatType.NETWORK_LATENCY,
            severity=ThreatSeverity.MEDIUM,
            description="Integration test",
            parameters={"latency_ms": 200},
            duration_seconds=1.0
        )
        
        chaos_result = await chaos.run_simulation(scenario, test_target)
        assert chaos_result.success
        
        # Step 4: Evolve based on chaos results
        evolution_result = await core.evolve_module("complete_module")
        assert evolution_result is not None
        
        # Step 5: Request Guardian approval
        change = MutationChange(
            id="full_change",
            module_id="complete_module",
            change_type="evolution",
            description="Evolution from chaos test",
            impact=ChangeImpact.MEDIUM,
            old_genome={"generation": 0},
            new_genome={"generation": 1},
            fitness_improvement=evolution_result.fitness_score
        )
        
        approval = guardian.request_approval(change)
        assert approval is not None
        
        # Step 6: Generate reports
        core_report = core.get_resilience_report()
        vault_report = vault.generate_report()
        chaos_report = chaos.export_report()
        guardian_report = guardian.generate_compliance_report()
        
        assert "modules" in core_report
        assert "total_patterns" in vault_report
        assert "summary" in chaos_report
        assert "total_events" in guardian_report
    
    @pytest.mark.asyncio
    async def test_continuous_evolution_cycle(self):
        """Test continuous evolution cycle"""
        core = RafaelCore(app_name="continuous-test")
        chaos = ChaosForge()
        
        # Register module
        core.register_module("continuous_module")
        
        # Run multiple evolution cycles
        for cycle in range(3):
            # Evolve
            result = await core.evolve_module("continuous_module")
            assert result is not None
            
            # Run chaos test
            scenario = ThreatScenario(
                id=f"cycle_{cycle}",
                name=f"Cycle {cycle}",
                threat_type=ThreatType.NETWORK_LATENCY,
                severity=ThreatSeverity.LOW,
                description=f"Cycle {cycle} test",
                parameters={"latency_ms": 100},
                duration_seconds=0.5
            )
            
            async def target():
                await asyncio.sleep(0.01)
            
            await chaos.run_simulation(scenario, target)
        
        # Check evolution progress
        report = core.get_resilience_report()
        module_info = report["modules"]["continuous_module"]
        
        assert module_info["generation"] >= 0
        assert module_info["genes_count"] > 0
    
    def test_pattern_sharing_workflow(self):
        """Test pattern sharing between vault and core"""
        core = RafaelCore(app_name="sharing-test")
        vault = ResilienceVault()
        
        # Register module
        genome = core.register_module("sharing_module")
        
        # Export genome
        exported = core.export_genome("sharing_module")
        assert exported is not None
        
        # Get patterns from vault
        patterns = vault.search_patterns(
            technology=TechnologyStack.PYTHON
        )
        
        # Record pattern usage
        if patterns:
            vault.record_usage(patterns[0].id, success=True)
            vault.upvote_pattern(patterns[0].id)
        
        # Generate vault report
        report = vault.generate_report()
        assert report["total_patterns"] > 0


class TestErrorHandlingIntegration:
    """Test error handling across components"""
    
    @pytest.mark.asyncio
    async def test_chaos_failure_handling(self):
        """Test system handles chaos test failures gracefully"""
        core = RafaelCore(app_name="error-test")
        chaos = ChaosForge()
        
        core.register_module("error_module")
        
        async def failing_target():
            raise RuntimeError("Intentional failure")
        
        scenario = ThreatScenario(
            id="error_scenario",
            name="Error Test",
            threat_type=ThreatType.SERVICE_UNAVAILABLE,
            severity=ThreatSeverity.HIGH,
            description="Error handling test",
            parameters={},
            duration_seconds=1.0
        )
        
        result = await chaos.run_simulation(scenario, failing_target)
        
        # Should handle failure gracefully
        assert result is not None
        assert not result.system_survived
    
    def test_invalid_module_operations(self):
        """Test handling of invalid module operations"""
        core = RafaelCore(app_name="invalid-test")
        
        # Try to evolve non-existent module
        result = asyncio.run(core.evolve_module("non_existent"))
        assert result is None
        
        # Try to export non-existent genome
        exported = core.export_genome("non_existent")
        assert exported is None
    
    def test_guardian_invalid_approvals(self):
        """Test Guardian handles invalid approval requests"""
        guardian = GuardianLayer()
        
        # Try to approve non-existent request
        result = guardian.approve_change("invalid_id", "approver")
        assert not result
        
        # Try to reject non-existent request
        result = guardian.reject_change("invalid_id", "rejector", "reason")
        assert not result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
