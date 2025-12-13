"""
Tests for Chaos Forge
"""

import pytest
from chaos_forge.simulator import (
    ChaosForge,
    ThreatType,
    ThreatSeverity,
    ThreatScenario
)


class TestThreatType:
    """Test ThreatType enum"""
    
    def test_threat_types_exist(self):
        """Test all threat types are defined"""
        assert ThreatType.DDOS is not None
        assert ThreatType.NETWORK_LATENCY is not None
        assert ThreatType.DATABASE_FAILURE is not None
        assert ThreatType.MEMORY_PRESSURE is not None
        assert ThreatType.CPU_SPIKE is not None


class TestThreatSeverity:
    """Test ThreatSeverity enum"""
    
    def test_severity_levels_exist(self):
        """Test all severity levels are defined"""
        assert ThreatSeverity.LOW is not None
        assert ThreatSeverity.MEDIUM is not None
        assert ThreatSeverity.HIGH is not None
        assert ThreatSeverity.CRITICAL is not None


class TestThreatScenario:
    """Test ThreatScenario class"""
    
    def test_scenario_creation(self):
        """Test creating a threat scenario"""
        scenario = ThreatScenario(
            id="test-scenario-1",
            threat_type=ThreatType.DDOS,
            severity=ThreatSeverity.HIGH,
            description="DDoS attack simulation",
            parameters={"requests_per_second": 10000}
        )
        assert scenario.id == "test-scenario-1"
        assert scenario.threat_type == ThreatType.DDOS
        assert scenario.severity == ThreatSeverity.HIGH


class TestChaosForge:
    """Test Chaos Forge"""
    
    def test_forge_creation(self):
        """Test creating chaos forge"""
        forge = ChaosForge()
        assert forge is not None
    
    def test_create_scenario(self):
        """Test creating a scenario"""
        forge = ChaosForge()
        scenario = forge.create_scenario(
            threat_type=ThreatType.NETWORK_LATENCY,
            severity=ThreatSeverity.MEDIUM
        )
        assert scenario is not None
        assert scenario.threat_type == ThreatType.NETWORK_LATENCY
        assert scenario.severity == ThreatSeverity.MEDIUM


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
