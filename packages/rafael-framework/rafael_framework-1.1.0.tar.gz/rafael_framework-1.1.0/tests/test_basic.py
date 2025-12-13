"""
Basic tests for RAFAEL Framework
Simple tests that verify core functionality
"""

import pytest


class TestImports:
    """Test that all modules can be imported"""
    
    def test_import_core(self):
        """Test importing core module"""
        from core import rafael_engine
        assert rafael_engine is not None
    
    def test_import_chaos_forge(self):
        """Test importing chaos forge"""
        from chaos_forge import simulator
        assert simulator is not None
    
    def test_import_vault(self):
        """Test importing vault"""
        from vault import resilience_vault
        assert resilience_vault is not None
    
    def test_import_guardian(self):
        """Test importing guardian"""
        from guardian import guardian_layer
        assert guardian_layer is not None


class TestCoreBasics:
    """Basic tests for core functionality"""
    
    def test_resilience_strategy_enum(self):
        """Test ResilienceStrategy enum exists"""
        from core.rafael_engine import ResilienceStrategy
        assert ResilienceStrategy is not None
        assert len(list(ResilienceStrategy)) > 0
    
    def test_gene_class_exists(self):
        """Test Gene class exists"""
        from core.rafael_engine import Gene
        assert Gene is not None
    
    def test_genome_class_exists(self):
        """Test AdaptiveResilienceGenome class exists"""
        from core.rafael_engine import AdaptiveResilienceGenome
        assert AdaptiveResilienceGenome is not None


class TestChaosForgeBasics:
    """Basic tests for chaos forge"""
    
    def test_threat_type_enum(self):
        """Test ThreatType enum exists"""
        from chaos_forge.simulator import ThreatType
        assert ThreatType is not None
        assert len(list(ThreatType)) > 0
    
    def test_threat_severity_enum(self):
        """Test ThreatSeverity enum exists"""
        from chaos_forge.simulator import ThreatSeverity
        assert ThreatSeverity is not None
        assert len(list(ThreatSeverity)) > 0
    
    def test_chaos_forge_class(self):
        """Test ChaosForge class exists"""
        from chaos_forge.simulator import ChaosForge
        assert ChaosForge is not None


class TestVaultBasics:
    """Basic tests for vault"""
    
    def test_pattern_category_enum(self):
        """Test PatternCategory enum exists"""
        from vault.resilience_vault import PatternCategory
        assert PatternCategory is not None
        assert len(list(PatternCategory)) > 0
    
    def test_resilience_pattern_class(self):
        """Test ResiliencePattern class exists"""
        from vault.resilience_vault import ResiliencePattern
        assert ResiliencePattern is not None
    
    def test_resilience_vault_class(self):
        """Test ResilienceVault class exists"""
        from vault.resilience_vault import ResilienceVault
        assert ResilienceVault is not None


class TestGuardianBasics:
    """Basic tests for guardian layer"""
    
    def test_approval_status_enum(self):
        """Test ApprovalStatus enum exists"""
        from guardian.guardian_layer import ApprovalStatus
        assert ApprovalStatus is not None
        assert len(list(ApprovalStatus)) > 0
    
    def test_guardian_layer_class(self):
        """Test GuardianLayer class exists"""
        from guardian.guardian_layer import GuardianLayer
        assert GuardianLayer is not None


class TestFrameworkIntegration:
    """Test basic framework integration"""
    
    def test_all_components_available(self):
        """Test all major components can be imported together"""
        from core.rafael_engine import RafaelCore
        from chaos_forge.simulator import ChaosForge
        from vault.resilience_vault import ResilienceVault
        from guardian.guardian_layer import GuardianLayer
        
        assert RafaelCore is not None
        assert ChaosForge is not None
        assert ResilienceVault is not None
        assert GuardianLayer is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
