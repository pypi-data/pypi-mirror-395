"""
Tests for Resilience Vault
"""

import pytest
from vault.resilience_vault import (
    ResilienceVault,
    ResiliencePattern,
    PatternCategory,
    TechnologyStack
)


class TestPatternCategory:
    """Test PatternCategory enum"""
    
    def test_categories_exist(self):
        """Test all categories are defined"""
        assert PatternCategory.RETRY is not None
        assert PatternCategory.CIRCUIT_BREAKER is not None
        assert PatternCategory.FALLBACK is not None
        assert PatternCategory.RATE_LIMITING is not None


class TestTechnologyStack:
    """Test TechnologyStack enum"""
    
    def test_stacks_exist(self):
        """Test technology stacks are defined"""
        assert TechnologyStack.PYTHON is not None
        assert TechnologyStack.NODEJS is not None
        assert TechnologyStack.FLUTTER is not None


class TestResiliencePattern:
    """Test ResiliencePattern class"""
    
    def test_pattern_creation(self):
        """Test creating a pattern"""
        pattern = ResiliencePattern(
            id="test-pattern-1",
            name="Exponential Backoff Retry",
            category=PatternCategory.RETRY,
            description="Retry with exponential backoff",
            code_snippet="# retry logic",
            technology_stack=TechnologyStack.PYTHON,
            reliability_score=0.85,
            usage_count=100
        )
        assert pattern.id == "test-pattern-1"
        assert pattern.name == "Exponential Backoff Retry"
        assert pattern.reliability_score == 0.85


class TestResilienceVault:
    """Test Resilience Vault"""
    
    def test_vault_creation(self):
        """Test creating vault"""
        vault = ResilienceVault()
        assert vault is not None
    
    def test_add_pattern(self):
        """Test adding a pattern"""
        vault = ResilienceVault()
        pattern = ResiliencePattern(
            id="pattern-1",
            name="Test Pattern",
            category=PatternCategory.RETRY,
            description="Test",
            code_snippet="# test",
            technology_stack=TechnologyStack.PYTHON,
            reliability_score=0.9,
            usage_count=10
        )
        vault.add_pattern(pattern)
        retrieved = vault.get_pattern("pattern-1")
        assert retrieved is not None
        assert retrieved.id == "pattern-1"
    
    def test_search_patterns(self):
        """Test searching patterns"""
        vault = ResilienceVault()
        pattern = ResiliencePattern(
            id="pattern-2",
            name="Circuit Breaker Pattern",
            category=PatternCategory.CIRCUIT_BREAKER,
            description="Circuit breaker implementation",
            code_snippet="# circuit breaker",
            technology_stack=TechnologyStack.NODEJS,
            reliability_score=0.95,
            usage_count=50
        )
        vault.add_pattern(pattern)
        
        results = vault.search_patterns(category=PatternCategory.CIRCUIT_BREAKER)
        assert len(results) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
