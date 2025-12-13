"""
Tests for Guardian Layer
"""

import pytest
from guardian.guardian_layer import (
    GuardianLayer,
    ApprovalRequest,
    ApprovalStatus,
    MutationChange
)


class TestApprovalStatus:
    """Test ApprovalStatus enum"""
    
    def test_statuses_exist(self):
        """Test all statuses are defined"""
        assert ApprovalStatus.PENDING is not None
        assert ApprovalStatus.APPROVED is not None
        assert ApprovalStatus.REJECTED is not None


class TestMutationChange:
    """Test MutationChange class"""
    
    def test_change_creation(self):
        """Test creating a mutation change"""
        change = MutationChange(
            module_id="test-module",
            gene_id="test-gene",
            old_parameters={"max_retries": 3},
            new_parameters={"max_retries": 5},
            reason="Improve resilience"
        )
        assert change.module_id == "test-module"
        assert change.gene_id == "test-gene"


class TestApprovalRequest:
    """Test ApprovalRequest class"""
    
    def test_request_creation(self):
        """Test creating an approval request"""
        change = MutationChange(
            module_id="test-module",
            gene_id="test-gene",
            old_parameters={},
            new_parameters={},
            reason="Test"
        )
        request = ApprovalRequest(
            id="req-1",
            change=change,
            status=ApprovalStatus.PENDING
        )
        assert request.id == "req-1"
        assert request.status == ApprovalStatus.PENDING


class TestGuardianLayer:
    """Test Guardian Layer"""
    
    def test_guardian_creation(self):
        """Test creating guardian layer"""
        guardian = GuardianLayer()
        assert guardian is not None
    
    def test_request_approval(self):
        """Test requesting approval"""
        guardian = GuardianLayer()
        change = MutationChange(
            module_id="test-module",
            gene_id="test-gene",
            old_parameters={"timeout": 30},
            new_parameters={"timeout": 60},
            reason="Increase timeout"
        )
        request = guardian.request_approval(change)
        assert request is not None
        assert request.status == ApprovalStatus.PENDING
    
    def test_approve_request(self):
        """Test approving a request"""
        guardian = GuardianLayer()
        change = MutationChange(
            module_id="test-module",
            gene_id="test-gene",
            old_parameters={},
            new_parameters={},
            reason="Test"
        )
        request = guardian.request_approval(change)
        guardian.approve(request.id)
        
        updated = guardian.get_request(request.id)
        assert updated.status == ApprovalStatus.APPROVED
    
    def test_reject_request(self):
        """Test rejecting a request"""
        guardian = GuardianLayer()
        change = MutationChange(
            module_id="test-module",
            gene_id="test-gene",
            old_parameters={},
            new_parameters={},
            reason="Test"
        )
        request = guardian.request_approval(change)
        guardian.reject(request.id, reason="Not safe")
        
        updated = guardian.get_request(request.id)
        assert updated.status == ApprovalStatus.REJECTED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
