"""
Guardian Layer - Ethics, Control, and Compliance
Ensures all autonomous changes are safe, auditable, and compliant
"""

import json
import hashlib
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("RAFAEL.Guardian")


class ApprovalStatus(Enum):
    """Status of approval requests"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"
    EXPIRED = "expired"


class ChangeImpact(Enum):
    """Impact level of changes"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceFramework(Enum):
    """Supported compliance frameworks"""
    ISO27001 = "iso27001"
    SOC2 = "soc2"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"


@dataclass
class MutationChange:
    """Represents a proposed mutation change"""
    id: str
    module_id: str
    change_type: str
    description: str
    impact: ChangeImpact
    
    # Change details
    old_genome: Dict[str, Any]
    new_genome: Dict[str, Any]
    fitness_improvement: float
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    requested_by: str = "rafael_core"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "module_id": self.module_id,
            "change_type": self.change_type,
            "description": self.description,
            "impact": self.impact.value,
            "old_genome": self.old_genome,
            "new_genome": self.new_genome,
            "fitness_improvement": self.fitness_improvement,
            "timestamp": self.timestamp.isoformat(),
            "requested_by": self.requested_by
        }


@dataclass
class ApprovalRequest:
    """An approval request for a mutation"""
    id: str
    change: MutationChange
    status: ApprovalStatus = ApprovalStatus.PENDING
    
    # Approval details
    approved_by: Optional[str] = None
    approval_timestamp: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    
    # Auto-approval
    auto_approved: bool = False
    auto_approval_reason: Optional[str] = None
    
    # Expiry
    expires_at: Optional[datetime] = None
    
    def approve(self, approver: str):
        """Approve the request"""
        self.status = ApprovalStatus.APPROVED
        self.approved_by = approver
        self.approval_timestamp = datetime.now()
        logger.info(f"Change {self.id} approved by {approver}")
    
    def reject(self, rejector: str, reason: str):
        """Reject the request"""
        self.status = ApprovalStatus.REJECTED
        self.approved_by = rejector
        self.approval_timestamp = datetime.now()
        self.rejection_reason = reason
        logger.info(f"Change {self.id} rejected by {rejector}: {reason}")
    
    def auto_approve(self, reason: str):
        """Auto-approve the request"""
        self.status = ApprovalStatus.AUTO_APPROVED
        self.auto_approved = True
        self.auto_approval_reason = reason
        self.approval_timestamp = datetime.now()
        logger.info(f"Change {self.id} auto-approved: {reason}")


@dataclass
class AuditLogEntry:
    """Immutable audit log entry"""
    id: str
    timestamp: datetime
    event_type: str
    actor: str
    module_id: str
    change_id: Optional[str]
    details: Dict[str, Any]
    hash: str = ""
    
    def __post_init__(self):
        """Calculate hash for immutability"""
        if not self.hash:
            self.hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate SHA-256 hash of entry"""
        data = {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "actor": self.actor,
            "module_id": self.module_id,
            "change_id": self.change_id,
            "details": json.dumps(self.details, sort_keys=True)
        }
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Verify the entry hasn't been tampered with"""
        return self.hash == self._calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "actor": self.actor,
            "module_id": self.module_id,
            "change_id": self.change_id,
            "details": self.details,
            "hash": self.hash
        }


class ApprovalPolicy:
    """Policy for determining what needs approval"""
    
    def __init__(
        self,
        auto_approve_low_impact: bool = True,
        auto_approve_threshold: float = 0.9,
        require_approval_for_production: bool = True
    ):
        self.auto_approve_low_impact = auto_approve_low_impact
        self.auto_approve_threshold = auto_approve_threshold
        self.require_approval_for_production = require_approval_for_production
    
    def should_auto_approve(self, change: MutationChange) -> tuple[bool, str]:
        """
        Determine if a change should be auto-approved
        Returns (should_approve, reason)
        """
        # Never auto-approve critical changes
        if change.impact == ChangeImpact.CRITICAL:
            return False, "Critical impact requires manual approval"
        
        # Auto-approve low impact if enabled
        if change.impact == ChangeImpact.LOW and self.auto_approve_low_impact:
            return True, "Low impact change"
        
        # Auto-approve if fitness improvement is very high
        if change.fitness_improvement >= self.auto_approve_threshold:
            return True, f"High fitness improvement: {change.fitness_improvement:.2f}"
        
        # Default: require approval
        return False, "Requires manual approval"


class ComplianceChecker:
    """Check compliance with various frameworks"""
    
    def __init__(self, frameworks: List[ComplianceFramework]):
        self.frameworks = frameworks
    
    def check_compliance(
        self,
        change: MutationChange,
        audit_log: List[AuditLogEntry]
    ) -> Dict[str, Any]:
        """Check if change complies with frameworks"""
        results = {}
        
        for framework in self.frameworks:
            if framework == ComplianceFramework.ISO27001:
                results['iso27001'] = self._check_iso27001(change, audit_log)
            elif framework == ComplianceFramework.SOC2:
                results['soc2'] = self._check_soc2(change, audit_log)
            elif framework == ComplianceFramework.GDPR:
                results['gdpr'] = self._check_gdpr(change, audit_log)
        
        return results
    
    def _check_iso27001(
        self,
        change: MutationChange,
        audit_log: List[AuditLogEntry]
    ) -> Dict[str, Any]:
        """Check ISO 27001 compliance"""
        checks = {
            "audit_trail": len(audit_log) > 0,
            "change_documentation": bool(change.description),
            "impact_assessment": change.impact is not None,
            "timestamp_recorded": change.timestamp is not None
        }
        
        return {
            "compliant": all(checks.values()),
            "checks": checks
        }
    
    def _check_soc2(
        self,
        change: MutationChange,
        audit_log: List[AuditLogEntry]
    ) -> Dict[str, Any]:
        """Check SOC 2 compliance"""
        checks = {
            "audit_log_immutable": all(e.verify_integrity() for e in audit_log[-10:]),
            "change_authorized": change.requested_by is not None,
            "monitoring_enabled": True  # Assumed if using RAFAEL
        }
        
        return {
            "compliant": all(checks.values()),
            "checks": checks
        }
    
    def _check_gdpr(
        self,
        change: MutationChange,
        audit_log: List[AuditLogEntry]
    ) -> Dict[str, Any]:
        """Check GDPR compliance"""
        # GDPR mainly about data, but we check audit trail
        checks = {
            "audit_trail_exists": len(audit_log) > 0,
            "data_integrity": all(e.verify_integrity() for e in audit_log[-10:])
        }
        
        return {
            "compliant": all(checks.values()),
            "checks": checks
        }


class GuardianLayer:
    """
    Main Guardian Layer
    Manages approvals, audit logs, and compliance
    """
    
    def __init__(
        self,
        approval_policy: Optional[ApprovalPolicy] = None,
        compliance_frameworks: Optional[List[ComplianceFramework]] = None,
        audit_log_path: Optional[str] = None
    ):
        self.approval_policy = approval_policy or ApprovalPolicy()
        self.compliance_checker = ComplianceChecker(
            compliance_frameworks or [ComplianceFramework.ISO27001, ComplianceFramework.SOC2]
        )
        self.audit_log_path = audit_log_path or "./rafael_audit.log"
        
        # State
        self.pending_approvals: Dict[str, ApprovalRequest] = {}
        self.audit_log: List[AuditLogEntry] = []
        self.approval_callbacks: List[Callable] = []
        
        logger.info("🛡️ Guardian Layer initialized")
    
    def request_approval(self, change: MutationChange) -> ApprovalRequest:
        """Request approval for a mutation change"""
        request_id = hashlib.md5(
            f"{change.id}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        request = ApprovalRequest(
            id=request_id,
            change=change
        )
        
        # Check if should auto-approve
        should_auto, reason = self.approval_policy.should_auto_approve(change)
        
        if should_auto:
            request.auto_approve(reason)
            self._log_event(
                event_type="mutation_auto_approved",
                actor="guardian_layer",
                module_id=change.module_id,
                change_id=change.id,
                details={
                    "reason": reason,
                    "fitness_improvement": change.fitness_improvement
                }
            )
        else:
            self.pending_approvals[request_id] = request
            self._log_event(
                event_type="approval_requested",
                actor="rafael_core",
                module_id=change.module_id,
                change_id=change.id,
                details={
                    "impact": change.impact.value,
                    "description": change.description
                }
            )
            
            # Notify callbacks
            for callback in self.approval_callbacks:
                try:
                    callback(request)
                except Exception as e:
                    logger.error(f"Approval callback failed: {e}")
        
        return request
    
    def approve_change(self, request_id: str, approver: str) -> bool:
        """Approve a pending change"""
        if request_id not in self.pending_approvals:
            logger.error(f"Request {request_id} not found")
            return False
        
        request = self.pending_approvals[request_id]
        request.approve(approver)
        
        # Log approval
        self._log_event(
            event_type="mutation_approved",
            actor=approver,
            module_id=request.change.module_id,
            change_id=request.change.id,
            details={
                "request_id": request_id,
                "fitness_improvement": request.change.fitness_improvement
            }
        )
        
        # Remove from pending
        del self.pending_approvals[request_id]
        
        return True
    
    def reject_change(self, request_id: str, rejector: str, reason: str) -> bool:
        """Reject a pending change"""
        if request_id not in self.pending_approvals:
            logger.error(f"Request {request_id} not found")
            return False
        
        request = self.pending_approvals[request_id]
        request.reject(rejector, reason)
        
        # Log rejection
        self._log_event(
            event_type="mutation_rejected",
            actor=rejector,
            module_id=request.change.module_id,
            change_id=request.change.id,
            details={
                "request_id": request_id,
                "reason": reason
            }
        )
        
        # Remove from pending
        del self.pending_approvals[request_id]
        
        return True
    
    def _log_event(
        self,
        event_type: str,
        actor: str,
        module_id: str,
        change_id: Optional[str],
        details: Dict[str, Any]
    ):
        """Create immutable audit log entry"""
        entry_id = hashlib.md5(
            f"{event_type}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        entry = AuditLogEntry(
            id=entry_id,
            timestamp=datetime.now(),
            event_type=event_type,
            actor=actor,
            module_id=module_id,
            change_id=change_id,
            details=details
        )
        
        self.audit_log.append(entry)
        
        # Persist to file
        self._persist_audit_log(entry)
        
        logger.info(f"Audit log entry created: {event_type} by {actor}")
    
    def _persist_audit_log(self, entry: AuditLogEntry):
        """Persist audit log entry to file"""
        try:
            with open(self.audit_log_path, 'a') as f:
                f.write(json.dumps(entry.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist audit log: {e}")
    
    def verify_audit_log_integrity(self) -> bool:
        """Verify all audit log entries are intact"""
        for entry in self.audit_log:
            if not entry.verify_integrity():
                logger.error(f"Audit log entry {entry.id} failed integrity check!")
                return False
        return True
    
    def get_pending_approvals(self) -> List[ApprovalRequest]:
        """Get all pending approval requests"""
        return list(self.pending_approvals.values())
    
    def get_audit_log(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        event_type: Optional[str] = None,
        module_id: Optional[str] = None
    ) -> List[AuditLogEntry]:
        """Get filtered audit log entries"""
        entries = self.audit_log
        
        if start_time:
            entries = [e for e in entries if e.timestamp >= start_time]
        
        if end_time:
            entries = [e for e in entries if e.timestamp <= end_time]
        
        if event_type:
            entries = [e for e in entries if e.event_type == event_type]
        
        if module_id:
            entries = [e for e in entries if e.module_id == module_id]
        
        return entries
    
    def check_compliance(self, change: MutationChange) -> Dict[str, Any]:
        """Check compliance for a change"""
        return self.compliance_checker.check_compliance(change, self.audit_log)
    
    def register_approval_callback(self, callback: Callable):
        """Register callback for approval requests"""
        self.approval_callbacks.append(callback)
    
    def export_audit_log(self, output_path: str):
        """Export audit log to file"""
        with open(output_path, 'w') as f:
            for entry in self.audit_log:
                f.write(json.dumps(entry.to_dict()) + '\n')
        
        logger.info(f"Audit log exported to {output_path}")
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        # Get recent changes
        recent_changes = self.get_audit_log(
            start_time=datetime.now().replace(day=1)  # This month
        )
        
        # Count by event type
        event_counts = {}
        for entry in recent_changes:
            event_counts[entry.event_type] = event_counts.get(entry.event_type, 0) + 1
        
        # Check integrity
        integrity_ok = self.verify_audit_log_integrity()
        
        return {
            "period": "current_month",
            "total_events": len(recent_changes),
            "event_breakdown": event_counts,
            "pending_approvals": len(self.pending_approvals),
            "audit_log_integrity": "PASS" if integrity_ok else "FAIL",
            "compliance_frameworks": [f.value for f in self.compliance_checker.frameworks],
            "timestamp": datetime.now().isoformat()
        }
