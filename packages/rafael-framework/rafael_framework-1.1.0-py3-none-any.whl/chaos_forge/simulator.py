"""
Chaos Forge - Intelligent Attack Simulator
Adaptive chaos engineering that learns from real threat patterns
"""

import asyncio
import random
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("RAFAEL.ChaosForge")


class ThreatType(Enum):
    """Types of threats to simulate"""
    NETWORK_LATENCY = "network_latency"
    NETWORK_PARTITION = "network_partition"
    SERVICE_UNAVAILABLE = "service_unavailable"
    DATABASE_FAILURE = "database_failure"
    MEMORY_PRESSURE = "memory_pressure"
    CPU_SPIKE = "cpu_spike"
    DDOS_ATTACK = "ddos_attack"
    SQL_INJECTION = "sql_injection"
    XSS_ATTACK = "xss_attack"
    RATE_LIMIT_BREACH = "rate_limit_breach"
    AUTH_FAILURE = "auth_failure"
    DATA_CORRUPTION = "data_corruption"
    CASCADING_FAILURE = "cascading_failure"
    BYZANTINE_FAULT = "byzantine_fault"


class ThreatSeverity(Enum):
    """Severity levels for threats"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ThreatScenario:
    """A specific threat scenario to simulate"""
    id: str
    name: str
    threat_type: ThreatType
    severity: ThreatSeverity
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    success_probability: float = 0.5
    duration_seconds: float = 10.0
    
    def __post_init__(self):
        """Validate parameters"""
        if not 0 <= self.success_probability <= 1:
            raise ValueError("success_probability must be between 0 and 1")


@dataclass
class SimulationResult:
    """Result of a chaos simulation"""
    scenario: ThreatScenario
    start_time: datetime
    end_time: datetime
    success: bool
    system_survived: bool
    recovery_time_seconds: float
    metrics: Dict[str, Any] = field(default_factory=dict)
    resilience_score: float = 0.0
    lessons_learned: List[str] = field(default_factory=list)
    
    def calculate_resilience_score(self) -> float:
        """Calculate resilience score based on results"""
        base_score = 1.0 if self.system_survived else 0.0
        
        # Bonus for quick recovery
        if self.recovery_time_seconds < 5.0:
            base_score += 0.3
        elif self.recovery_time_seconds < 15.0:
            base_score += 0.15
        
        # Penalty for high severity threats
        severity_penalty = (self.scenario.severity.value - 1) * 0.05
        base_score -= severity_penalty
        
        self.resilience_score = max(0.0, min(1.0, base_score))
        return self.resilience_score


@dataclass
class ResilienceDelta:
    """Report showing resilience improvement over time"""
    baseline_score: float
    current_score: float
    improvement_percentage: float
    simulations_run: int
    threats_mitigated: List[str]
    vulnerabilities_found: List[str]
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


class ThreatIntelligence:
    """
    Simulates global threat intelligence feed
    In production, this would integrate with real threat feeds
    """
    
    def __init__(self):
        self.threat_patterns: List[Dict[str, Any]] = []
        self._load_threat_patterns()
    
    def _load_threat_patterns(self):
        """Load known threat patterns"""
        self.threat_patterns = [
            {
                "name": "Credential Stuffing",
                "type": ThreatType.AUTH_FAILURE,
                "indicators": ["multiple_failed_logins", "distributed_ips"],
                "mitigation": "rate_limiting + captcha"
            },
            {
                "name": "Slowloris Attack",
                "type": ThreatType.DDOS_ATTACK,
                "indicators": ["slow_connections", "connection_exhaustion"],
                "mitigation": "connection_timeout + load_balancing"
            },
            {
                "name": "SQL Injection",
                "type": ThreatType.SQL_INJECTION,
                "indicators": ["sql_keywords", "unusual_query_patterns"],
                "mitigation": "parameterized_queries + input_validation"
            },
            {
                "name": "Memory Leak Attack",
                "type": ThreatType.MEMORY_PRESSURE,
                "indicators": ["gradual_memory_increase", "oom_errors"],
                "mitigation": "memory_limits + garbage_collection"
            },
            {
                "name": "Cascading Service Failure",
                "type": ThreatType.CASCADING_FAILURE,
                "indicators": ["dependency_timeout", "error_propagation"],
                "mitigation": "circuit_breaker + bulkhead_isolation"
            }
        ]
    
    def get_trending_threats(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get currently trending threats"""
        # In production, this would query real threat intelligence APIs
        return random.sample(self.threat_patterns, min(count, len(self.threat_patterns)))
    
    def get_threat_by_type(self, threat_type: ThreatType) -> Optional[Dict[str, Any]]:
        """Get threat pattern by type"""
        for pattern in self.threat_patterns:
            if pattern["type"] == threat_type:
                return pattern
        return None


class ChaosForge:
    """
    Main Chaos Forge simulator
    Generates and executes adaptive attack scenarios
    """
    
    def __init__(
        self,
        target_system: Optional[Callable] = None,
        threat_intel: Optional[ThreatIntelligence] = None
    ):
        self.target_system = target_system
        self.threat_intel = threat_intel or ThreatIntelligence()
        self.simulation_history: List[SimulationResult] = []
        self.baseline_resilience: Optional[float] = None
        self.scenarios: List[ThreatScenario] = []
        
        # Load default scenarios
        self._load_default_scenarios()
    
    def _load_default_scenarios(self):
        """Load default threat scenarios"""
        self.scenarios = [
            ThreatScenario(
                id="net_latency_1",
                name="Network Latency Spike",
                threat_type=ThreatType.NETWORK_LATENCY,
                severity=ThreatSeverity.MEDIUM,
                description="Simulate 500ms-2s network latency",
                parameters={"latency_ms": 1000, "jitter_ms": 500},
                duration_seconds=30.0
            ),
            ThreatScenario(
                id="db_failure_1",
                name="Database Connection Loss",
                threat_type=ThreatType.DATABASE_FAILURE,
                severity=ThreatSeverity.HIGH,
                description="Simulate complete database unavailability",
                parameters={"failure_type": "connection_refused"},
                duration_seconds=20.0
            ),
            ThreatScenario(
                id="ddos_1",
                name="DDoS Attack Simulation",
                threat_type=ThreatType.DDOS_ATTACK,
                severity=ThreatSeverity.CRITICAL,
                description="Simulate 10,000 requests per second",
                parameters={"requests_per_second": 10000, "duration": 60},
                duration_seconds=60.0
            ),
            ThreatScenario(
                id="memory_1",
                name="Memory Pressure",
                threat_type=ThreatType.MEMORY_PRESSURE,
                severity=ThreatSeverity.HIGH,
                description="Simulate memory exhaustion",
                parameters={"memory_mb": 1024, "rate": "gradual"},
                duration_seconds=45.0
            ),
            ThreatScenario(
                id="cascade_1",
                name="Cascading Service Failure",
                threat_type=ThreatType.CASCADING_FAILURE,
                severity=ThreatSeverity.CRITICAL,
                description="Simulate chain reaction of service failures",
                parameters={"failure_chain": ["service_a", "service_b", "service_c"]},
                duration_seconds=40.0
            )
        ]
    
    def add_custom_scenario(self, scenario: ThreatScenario):
        """Add a custom threat scenario"""
        self.scenarios.append(scenario)
        logger.info(f"Added custom scenario: {scenario.name}")
    
    async def run_simulation(
        self,
        scenario: ThreatScenario,
        target_function: Optional[Callable] = None
    ) -> SimulationResult:
        """
        Run a single chaos simulation
        """
        logger.info(f"🔥 Starting chaos simulation: {scenario.name}")
        logger.info(f"   Severity: {scenario.severity.name}, Duration: {scenario.duration_seconds}s")
        
        start_time = datetime.now()
        target = target_function or self.target_system
        
        # Initialize result
        result = SimulationResult(
            scenario=scenario,
            start_time=start_time,
            end_time=start_time,  # Will be updated
            success=False,
            system_survived=False,
            recovery_time_seconds=0.0
        )
        
        try:
            # Apply the chaos
            chaos_task = asyncio.create_task(
                self._apply_chaos(scenario)
            )
            
            # Monitor system behavior
            if target:
                monitor_task = asyncio.create_task(
                    self._monitor_system(target, scenario.duration_seconds)
                )
                
                # Wait for both to complete
                chaos_result, monitor_result = await asyncio.gather(
                    chaos_task, monitor_task, return_exceptions=True
                )
                
                result.system_survived = not isinstance(monitor_result, Exception)
                result.metrics = monitor_result if isinstance(monitor_result, dict) else {}
            else:
                # No target system, just run chaos
                await chaos_task
                result.system_survived = True
                result.metrics = {"note": "No target system specified"}
            
            result.success = True
            
        except Exception as e:
            logger.error(f"Simulation failed: {e}")
            result.system_survived = False
            result.metrics["error"] = str(e)
        
        finally:
            end_time = datetime.now()
            result.end_time = end_time
            result.recovery_time_seconds = (end_time - start_time).total_seconds()
            
            # Calculate resilience score
            result.calculate_resilience_score()
            
            # Generate lessons learned
            result.lessons_learned = self._generate_lessons(result)
            
            # Store in history
            self.simulation_history.append(result)
            
            logger.info(f"✅ Simulation complete. Resilience score: {result.resilience_score:.2f}")
        
        return result
    
    async def _apply_chaos(self, scenario: ThreatScenario):
        """Apply the chaos scenario"""
        logger.info(f"Applying chaos: {scenario.threat_type.value}")
        
        # Simulate different types of chaos
        if scenario.threat_type == ThreatType.NETWORK_LATENCY:
            await self._simulate_network_latency(scenario.parameters)
        
        elif scenario.threat_type == ThreatType.DATABASE_FAILURE:
            await self._simulate_database_failure(scenario.parameters)
        
        elif scenario.threat_type == ThreatType.DDOS_ATTACK:
            await self._simulate_ddos(scenario.parameters)
        
        elif scenario.threat_type == ThreatType.MEMORY_PRESSURE:
            await self._simulate_memory_pressure(scenario.parameters)
        
        elif scenario.threat_type == ThreatType.CASCADING_FAILURE:
            await self._simulate_cascading_failure(scenario.parameters)
        
        else:
            # Generic chaos
            await asyncio.sleep(scenario.duration_seconds)
    
    async def _simulate_network_latency(self, params: Dict[str, Any]):
        """Simulate network latency"""
        latency = params.get("latency_ms", 1000) / 1000.0
        jitter = params.get("jitter_ms", 500) / 1000.0
        
        # Simulate variable latency
        for _ in range(10):
            actual_latency = latency + random.uniform(-jitter, jitter)
            await asyncio.sleep(max(0, actual_latency))
    
    async def _simulate_database_failure(self, params: Dict[str, Any]):
        """Simulate database failure"""
        failure_type = params.get("failure_type", "connection_refused")
        logger.warning(f"Simulating database failure: {failure_type}")
        
        # In production, this would actually interfere with DB connections
        await asyncio.sleep(5.0)
    
    async def _simulate_ddos(self, params: Dict[str, Any]):
        """Simulate DDoS attack"""
        rps = params.get("requests_per_second", 10000)
        duration = params.get("duration", 60)
        
        logger.warning(f"Simulating DDoS: {rps} req/s for {duration}s")
        
        # Simulate load
        await asyncio.sleep(duration)
    
    async def _simulate_memory_pressure(self, params: Dict[str, Any]):
        """Simulate memory pressure"""
        memory_mb = params.get("memory_mb", 1024)
        logger.warning(f"Simulating memory pressure: {memory_mb}MB")
        
        # In production, would actually allocate memory
        await asyncio.sleep(10.0)
    
    async def _simulate_cascading_failure(self, params: Dict[str, Any]):
        """Simulate cascading failures"""
        chain = params.get("failure_chain", [])
        logger.warning(f"Simulating cascading failure: {' -> '.join(chain)}")
        
        # Simulate failures propagating through services
        for service in chain:
            logger.warning(f"Service {service} failing...")
            await asyncio.sleep(2.0)
    
    async def _monitor_system(
        self,
        target_function: Callable,
        duration: float
    ) -> Dict[str, Any]:
        """Monitor system during chaos"""
        metrics = {
            "requests_attempted": 0,
            "requests_succeeded": 0,
            "requests_failed": 0,
            "avg_response_time": 0.0,
            "errors": []
        }
        
        start_time = asyncio.get_event_loop().time()
        response_times = []
        
        while asyncio.get_event_loop().time() - start_time < duration:
            metrics["requests_attempted"] += 1
            
            try:
                req_start = asyncio.get_event_loop().time()
                
                # Call target function
                if asyncio.iscoroutinefunction(target_function):
                    await target_function()
                else:
                    target_function()
                
                req_end = asyncio.get_event_loop().time()
                response_times.append(req_end - req_start)
                
                metrics["requests_succeeded"] += 1
                
            except Exception as e:
                metrics["requests_failed"] += 1
                metrics["errors"].append(str(e))
            
            await asyncio.sleep(0.1)  # 10 requests per second
        
        if response_times:
            metrics["avg_response_time"] = sum(response_times) / len(response_times)
        
        return metrics
    
    def _generate_lessons(self, result: SimulationResult) -> List[str]:
        """Generate lessons learned from simulation"""
        lessons = []
        
        if not result.system_survived:
            lessons.append(f"System failed under {result.scenario.threat_type.value}")
            lessons.append("Consider implementing circuit breaker pattern")
        
        if result.recovery_time_seconds > 30:
            lessons.append("Recovery time is high - implement faster failover")
        
        if result.metrics.get("requests_failed", 0) > result.metrics.get("requests_succeeded", 0):
            lessons.append("High failure rate - strengthen retry mechanisms")
        
        # Threat-specific lessons
        threat_intel = self.threat_intel.get_threat_by_type(result.scenario.threat_type)
        if threat_intel:
            lessons.append(f"Recommended mitigation: {threat_intel.get('mitigation', 'N/A')}")
        
        return lessons
    
    async def run_full_suite(
        self,
        scenarios: Optional[List[ThreatScenario]] = None
    ) -> List[SimulationResult]:
        """Run full suite of chaos scenarios"""
        scenarios = scenarios or self.scenarios
        
        logger.info(f"🔥 Running full chaos suite: {len(scenarios)} scenarios")
        
        results = []
        for scenario in scenarios:
            result = await self.run_simulation(scenario)
            results.append(result)
            
            # Brief pause between scenarios
            await asyncio.sleep(2.0)
        
        logger.info("✅ Full chaos suite complete")
        return results
    
    def calculate_resilience_delta(self) -> ResilienceDelta:
        """Calculate resilience improvement over time"""
        if not self.simulation_history:
            return ResilienceDelta(
                baseline_score=0.0,
                current_score=0.0,
                improvement_percentage=0.0,
                simulations_run=0,
                threats_mitigated=[],
                vulnerabilities_found=[],
                recommendations=[]
            )
        
        # Calculate baseline (first 10 simulations)
        baseline_sims = self.simulation_history[:10]
        baseline_score = sum(s.resilience_score for s in baseline_sims) / len(baseline_sims) \
            if baseline_sims else 0.0
        
        # Calculate current (last 10 simulations)
        current_sims = self.simulation_history[-10:]
        current_score = sum(s.resilience_score for s in current_sims) / len(current_sims)
        
        # Calculate improvement
        improvement = ((current_score - baseline_score) / baseline_score * 100) \
            if baseline_score > 0 else 0.0
        
        # Identify mitigated threats
        threats_mitigated = [
            s.scenario.name for s in current_sims
            if s.system_survived and s.resilience_score > 0.7
        ]
        
        # Identify vulnerabilities
        vulnerabilities = [
            s.scenario.name for s in current_sims
            if not s.system_survived or s.resilience_score < 0.3
        ]
        
        # Generate recommendations
        recommendations = []
        if improvement < 10:
            recommendations.append("Resilience improvement is low - review mitigation strategies")
        if len(vulnerabilities) > 5:
            recommendations.append("Multiple vulnerabilities detected - prioritize fixes")
        if current_score < 0.5:
            recommendations.append("Overall resilience is low - implement comprehensive hardening")
        
        return ResilienceDelta(
            baseline_score=baseline_score,
            current_score=current_score,
            improvement_percentage=improvement,
            simulations_run=len(self.simulation_history),
            threats_mitigated=threats_mitigated,
            vulnerabilities_found=vulnerabilities,
            recommendations=recommendations
        )
    
    def export_report(self) -> Dict[str, Any]:
        """Export comprehensive chaos testing report"""
        delta = self.calculate_resilience_delta()
        
        return {
            "summary": {
                "total_simulations": len(self.simulation_history),
                "baseline_resilience": delta.baseline_score,
                "current_resilience": delta.current_score,
                "improvement": f"{delta.improvement_percentage:.1f}%"
            },
            "resilience_delta": {
                "threats_mitigated": delta.threats_mitigated,
                "vulnerabilities_found": delta.vulnerabilities_found,
                "recommendations": delta.recommendations
            },
            "recent_simulations": [
                {
                    "scenario": s.scenario.name,
                    "survived": s.system_survived,
                    "resilience_score": s.resilience_score,
                    "recovery_time": s.recovery_time_seconds,
                    "lessons": s.lessons_learned
                }
                for s in self.simulation_history[-10:]
            ],
            "timestamp": datetime.now().isoformat()
        }
