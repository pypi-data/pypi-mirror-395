"""
Resilience Vault - Pattern Storage and Sharing System
Store, verify, and share proven resilience patterns
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("RAFAEL.Vault")


class PatternCategory(Enum):
    """Categories of resilience patterns"""
    RETRY = "retry"
    CIRCUIT_BREAKER = "circuit_breaker"
    BULKHEAD = "bulkhead"
    TIMEOUT = "timeout"
    FALLBACK = "fallback"
    CACHE = "cache"
    RATE_LIMIT = "rate_limit"
    LOAD_SHEDDING = "load_shedding"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    HEALTH_CHECK = "health_check"
    SECURITY = "security"
    MONITORING = "monitoring"


class TechnologyStack(Enum):
    """Supported technology stacks"""
    FLUTTER = "flutter"
    PYTHON = "python"
    NODEJS = "nodejs"
    REACT = "react"
    DJANGO = "django"
    FASTAPI = "fastapi"
    EXPRESS = "express"
    SUPABASE = "supabase"
    FIREBASE = "firebase"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    REDIS = "redis"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"


class VerificationStatus(Enum):
    """Verification status of patterns"""
    UNVERIFIED = "unverified"
    COMMUNITY_VERIFIED = "community_verified"
    EXPERT_VERIFIED = "expert_verified"
    PRODUCTION_PROVEN = "production_proven"


@dataclass
class ResiliencePattern:
    """A proven resilience pattern"""
    id: str
    name: str
    category: PatternCategory
    description: str
    problem: str
    solution: str
    technology_stack: List[TechnologyStack]
    code_example: str
    configuration: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    author: str = "anonymous"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    # Verification
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    reliability_score: float = 0.0
    usage_count: int = 0
    success_rate: float = 0.0
    
    # Community
    upvotes: int = 0
    downvotes: int = 0
    comments: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # Related patterns
    related_patterns: List[str] = field(default_factory=list)
    
    def calculate_reliability_score(self) -> float:
        """Calculate overall reliability score"""
        # Base score from verification status
        status_scores = {
            VerificationStatus.UNVERIFIED: 0.3,
            VerificationStatus.COMMUNITY_VERIFIED: 0.6,
            VerificationStatus.EXPERT_VERIFIED: 0.8,
            VerificationStatus.PRODUCTION_PROVEN: 1.0
        }
        base_score = status_scores[self.verification_status]
        
        # Adjust based on community feedback
        if self.upvotes + self.downvotes > 0:
            community_score = self.upvotes / (self.upvotes + self.downvotes)
            base_score = (base_score + community_score) / 2
        
        # Adjust based on success rate
        if self.usage_count > 10:
            base_score = (base_score + self.success_rate) / 2
        
        self.reliability_score = base_score
        return self.reliability_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        # Convert enums to strings
        data['category'] = self.category.value
        data['technology_stack'] = [t.value for t in self.technology_stack]
        data['verification_status'] = self.verification_status.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResiliencePattern':
        """Create from dictionary"""
        # Convert strings back to enums
        data['category'] = PatternCategory(data['category'])
        data['technology_stack'] = [TechnologyStack(t) for t in data['technology_stack']]
        data['verification_status'] = VerificationStatus(data['verification_status'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


@dataclass
class PatternCollection:
    """A curated collection of patterns"""
    id: str
    name: str
    description: str
    patterns: List[str]  # Pattern IDs
    curator: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)


class ResilienceVault:
    """
    Main vault for storing and managing resilience patterns
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or "./vault_data"
        self.patterns: Dict[str, ResiliencePattern] = {}
        self.collections: Dict[str, PatternCollection] = {}
        
        # Load built-in patterns
        self._load_builtin_patterns()
    
    def _load_builtin_patterns(self):
        """Load built-in resilience patterns"""
        
        # Pattern 1: Adaptive Retry for Flutter + Supabase
        self.add_pattern(ResiliencePattern(
            id="flutter_supabase_retry_001",
            name="Adaptive Retry for Flutter + Supabase",
            category=PatternCategory.RETRY,
            description="Intelligent retry mechanism for Supabase operations in Flutter apps",
            problem="Supabase API calls fail due to network issues or temporary unavailability",
            solution="Implement exponential backoff with jitter and adaptive retry based on error type",
            technology_stack=[TechnologyStack.FLUTTER, TechnologyStack.SUPABASE],
            code_example="""
// Flutter + Supabase Adaptive Retry
import 'package:supabase_flutter/supabase_flutter.dart';

class AdaptiveSupabaseClient {
  final SupabaseClient client;
  
  Future<T> withRetry<T>(
    Future<T> Function() operation, {
    int maxRetries = 3,
    Duration baseDelay = const Duration(seconds: 1),
  }) async {
    int attempt = 0;
    
    while (attempt < maxRetries) {
      try {
        return await operation();
      } catch (e) {
        attempt++;
        
        if (attempt >= maxRetries) rethrow;
        
        // Adaptive delay based on error type
        final delay = _calculateDelay(e, attempt, baseDelay);
        await Future.delayed(delay);
      }
    }
    
    throw Exception('Max retries exceeded');
  }
  
  Duration _calculateDelay(dynamic error, int attempt, Duration base) {
    // Exponential backoff with jitter
    final exponential = base * (1 << attempt);
    final jitter = Duration(
      milliseconds: Random().nextInt(1000)
    );
    return exponential + jitter;
  }
}
""",
            configuration={
                "max_retries": 3,
                "base_delay_ms": 1000,
                "max_delay_ms": 10000,
                "retry_on_errors": ["network", "timeout", "503"]
            },
            verification_status=VerificationStatus.PRODUCTION_PROVEN,
            tags=["flutter", "supabase", "mobile", "retry", "network"]
        ))
        
        # Pattern 2: Circuit Breaker for Microservices
        self.add_pattern(ResiliencePattern(
            id="nodejs_circuit_breaker_001",
            name="Circuit Breaker for Node.js Microservices",
            category=PatternCategory.CIRCUIT_BREAKER,
            description="Prevent cascading failures in microservice architectures",
            problem="Service failures cascade through dependent services",
            solution="Implement circuit breaker to fail fast and prevent resource exhaustion",
            technology_stack=[TechnologyStack.NODEJS, TechnologyStack.EXPRESS],
            code_example="""
// Node.js Circuit Breaker
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.timeout = options.timeout || 60000;
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.nextAttempt = Date.now();
  }
  
  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF_OPEN';
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
""",
            configuration={
                "failure_threshold": 5,
                "timeout_ms": 60000,
                "half_open_max_calls": 3
            },
            verification_status=VerificationStatus.EXPERT_VERIFIED,
            tags=["nodejs", "microservices", "circuit-breaker", "resilience"]
        ))
        
        # Pattern 3: SQL Injection Prevention
        self.add_pattern(ResiliencePattern(
            id="python_sql_injection_001",
            name="SQL Injection Prevention for Python",
            category=PatternCategory.SECURITY,
            description="Comprehensive SQL injection prevention using parameterized queries",
            problem="SQL injection vulnerabilities in database queries",
            solution="Use parameterized queries and input validation",
            technology_stack=[TechnologyStack.PYTHON, TechnologyStack.POSTGRESQL],
            code_example="""
# Python SQL Injection Prevention
import psycopg2
from typing import Any, List, Tuple

class SafeDatabase:
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)
    
    def execute_safe(
        self,
        query: str,
        params: Tuple[Any, ...] = ()
    ) -> List[Tuple]:
        '''Execute query with parameterized inputs'''
        with self.conn.cursor() as cursor:
            # Use parameterized query - NEVER string interpolation
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def validate_input(self, user_input: str) -> str:
        '''Validate and sanitize user input'''
        # Remove dangerous characters
        dangerous = [';', '--', '/*', '*/', 'xp_', 'sp_']
        for char in dangerous:
            if char in user_input:
                raise ValueError(f'Dangerous pattern detected: {char}')
        return user_input

# Usage
db = SafeDatabase('postgresql://...')
user_id = request.get('user_id')

# SAFE: Parameterized query
result = db.execute_safe(
    'SELECT * FROM users WHERE id = %s',
    (user_id,)
)

# UNSAFE: Never do this!
# query = f'SELECT * FROM users WHERE id = {user_id}'
""",
            configuration={
                "use_parameterized_queries": True,
                "validate_input": True,
                "escape_special_chars": True,
                "log_suspicious_queries": True
            },
            verification_status=VerificationStatus.PRODUCTION_PROVEN,
            tags=["python", "security", "sql-injection", "database"]
        ))
        
        # Pattern 4: Rate Limiting for APIs
        self.add_pattern(ResiliencePattern(
            id="python_rate_limit_001",
            name="Token Bucket Rate Limiter",
            category=PatternCategory.RATE_LIMIT,
            description="Flexible rate limiting using token bucket algorithm",
            problem="API abuse and resource exhaustion from excessive requests",
            solution="Implement token bucket algorithm for smooth rate limiting",
            technology_stack=[TechnologyStack.PYTHON, TechnologyStack.FASTAPI],
            code_example="""
# Token Bucket Rate Limiter
import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        
        self.tokens = min(
            self.capacity,
            self.tokens + tokens_to_add
        )
        self.last_refill = now

# FastAPI middleware
from fastapi import Request, HTTPException

rate_limiters = {}

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    
    if client_ip not in rate_limiters:
        rate_limiters[client_ip] = TokenBucket(
            capacity=100,
            refill_rate=10  # 10 tokens per second
        )
    
    if not rate_limiters[client_ip].consume():
        raise HTTPException(status_code=429, detail='Rate limit exceeded')
    
    return await call_next(request)
""",
            configuration={
                "capacity": 100,
                "refill_rate": 10,
                "per_ip": True,
                "burst_allowed": True
            },
            verification_status=VerificationStatus.EXPERT_VERIFIED,
            tags=["python", "fastapi", "rate-limiting", "api"]
        ))
        
        logger.info(f"Loaded {len(self.patterns)} built-in patterns")
    
    def add_pattern(self, pattern: ResiliencePattern) -> str:
        """Add a pattern to the vault"""
        pattern.calculate_reliability_score()
        self.patterns[pattern.id] = pattern
        logger.info(f"Pattern added: {pattern.name} (ID: {pattern.id})")
        return pattern.id
    
    def get_pattern(self, pattern_id: str) -> Optional[ResiliencePattern]:
        """Get a pattern by ID"""
        return self.patterns.get(pattern_id)
    
    def search_patterns(
        self,
        category: Optional[PatternCategory] = None,
        technology: Optional[TechnologyStack] = None,
        tags: Optional[List[str]] = None,
        min_reliability: float = 0.0
    ) -> List[ResiliencePattern]:
        """Search patterns by criteria"""
        results = list(self.patterns.values())
        
        if category:
            results = [p for p in results if p.category == category]
        
        if technology:
            results = [p for p in results if technology in p.technology_stack]
        
        if tags:
            results = [
                p for p in results
                if any(tag in p.tags for tag in tags)
            ]
        
        if min_reliability > 0:
            results = [p for p in results if p.reliability_score >= min_reliability]
        
        # Sort by reliability score
        results.sort(key=lambda p: p.reliability_score, reverse=True)
        
        return results
    
    def upvote_pattern(self, pattern_id: str):
        """Upvote a pattern"""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].upvotes += 1
            self.patterns[pattern_id].calculate_reliability_score()
    
    def downvote_pattern(self, pattern_id: str):
        """Downvote a pattern"""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].downvotes += 1
            self.patterns[pattern_id].calculate_reliability_score()
    
    def record_usage(self, pattern_id: str, success: bool):
        """Record pattern usage"""
        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            pattern.usage_count += 1
            
            # Update success rate
            if pattern.usage_count == 1:
                pattern.success_rate = 1.0 if success else 0.0
            else:
                # Running average
                pattern.success_rate = (
                    (pattern.success_rate * (pattern.usage_count - 1) +
                     (1.0 if success else 0.0)) / pattern.usage_count
                )
            
            pattern.calculate_reliability_score()
    
    def create_collection(
        self,
        name: str,
        description: str,
        pattern_ids: List[str],
        curator: str = "anonymous"
    ) -> str:
        """Create a curated collection"""
        collection_id = hashlib.md5(name.encode()).hexdigest()[:16]
        
        collection = PatternCollection(
            id=collection_id,
            name=name,
            description=description,
            patterns=pattern_ids,
            curator=curator
        )
        
        self.collections[collection_id] = collection
        logger.info(f"Collection created: {name}")
        return collection_id
    
    def export_pattern(self, pattern_id: str) -> Optional[str]:
        """Export pattern as JSON"""
        pattern = self.get_pattern(pattern_id)
        if not pattern:
            return None
        
        return json.dumps(pattern.to_dict(), indent=2)
    
    def import_pattern(self, json_data: str) -> str:
        """Import pattern from JSON"""
        data = json.loads(json_data)
        pattern = ResiliencePattern.from_dict(data)
        return self.add_pattern(pattern)
    
    def get_recommendations(
        self,
        technology_stack: List[TechnologyStack],
        problem_type: Optional[str] = None
    ) -> List[ResiliencePattern]:
        """Get recommended patterns for a technology stack"""
        # Find patterns matching the technology stack
        matches = []
        for pattern in self.patterns.values():
            # Check if any tech in pattern matches any in requested stack
            if any(tech in pattern.technology_stack for tech in technology_stack):
                matches.append(pattern)
        
        # Sort by reliability
        matches.sort(key=lambda p: p.reliability_score, reverse=True)
        
        return matches[:10]  # Top 10 recommendations
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate vault statistics report"""
        total_patterns = len(self.patterns)
        
        # Group by category
        by_category = {}
        for pattern in self.patterns.values():
            cat = pattern.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
        
        # Group by verification status
        by_status = {}
        for pattern in self.patterns.values():
            status = pattern.verification_status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        # Top patterns
        top_patterns = sorted(
            self.patterns.values(),
            key=lambda p: p.reliability_score,
            reverse=True
        )[:5]
        
        return {
            "total_patterns": total_patterns,
            "total_collections": len(self.collections),
            "by_category": by_category,
            "by_verification_status": by_status,
            "avg_reliability": sum(p.reliability_score for p in self.patterns.values()) / total_patterns
                if total_patterns > 0 else 0.0,
            "top_patterns": [
                {
                    "name": p.name,
                    "reliability": p.reliability_score,
                    "usage_count": p.usage_count
                }
                for p in top_patterns
            ]
        }
