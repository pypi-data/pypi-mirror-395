# Phase 1.1 Deliverable: Extended Test Query List

**Date Created:** December 2, 2025
**Purpose:** Comprehensive test case design for Phase 1.3 (Run Comprehensive Validation)
**Total Cases:** 12 test queries covering 8 agent types and edge cases

---

## Test Query Catalog

### Test 1: Frontend Architecture
**Query:** "How do I use React hooks and compose them effectively?"
**Expected Agent:** frontend-architect.prompt.md
**Expected Distance Range:** 1.0-1.3 (Good, multi-concept)
**Query Type:** Domain-specific, multi-concept
**Rationale:** Tests frontend specialist with modern React patterns

---

### Test 2: Frontend Edge Case - Ambiguous
**Query:** "state management"
**Expected Agent:** frontend-architect.prompt.md (primary), backend-architect.prompt.md (secondary)
**Expected Distance Range:** 1.1-1.4 (Okay, ambiguous)
**Query Type:** Ambiguous, single-concept
**Rationale:** Tests disambiguation - state management is frontend-focused but could apply to backend

---

### Test 3: Backend Architecture
**Query:** "How do I design a secure backend system with proper error handling and monitoring?"
**Expected Agent:** backend-architect.prompt.md
**Expected Distance Range:** 0.7-1.0 (Excellent, multi-concept)
**Query Type:** Domain-specific, multi-concept
**Rationale:** Tests backend specialist with complex, realistic query

---

### Test 4: Backend Edge Case - Simple
**Query:** "API design"
**Expected Agent:** backend-architect.prompt.md
**Expected Distance Range:** 0.9-1.3 (Good to Okay, single-concept)
**Query Type:** Domain-specific, simple
**Rationale:** Tests backend with shorter, focused query

---

### Test 5: DevOps/Infrastructure
**Query:** "CI/CD pipeline setup and best practices"
**Expected Agent:** devops-architect.prompt.md
**Expected Distance Range:** 1.0-1.3 (Good to Okay, multi-concept)
**Query Type:** Domain-specific, multi-concept
**Rationale:** Tests DevOps specialist with infrastructure focus

---

### Test 6: DevOps Edge Case - Specific Tool
**Query:** "Docker containers and Kubernetes orchestration"
**Expected Agent:** devops-architect.prompt.md
**Expected Distance Range:** 1.0-1.4 (Good to Okay, technology-specific)
**Query Type:** Domain-specific, technology-specific
**Rationale:** Tests DevOps with specific tools mentioned

---

### Test 7: Security Engineering
**Query:** "How do I implement authentication and authorization securely?"
**Expected Agent:** security-engineer.prompt.md
**Expected Distance Range:** 0.8-1.2 (Excellent to Good, multi-concept)
**Query Type:** Domain-specific, multi-concept
**Rationale:** Tests security specialist with foundational concepts

---

### Test 8: Security Edge Case - Threat Modeling
**Query:** "threat assessment vulnerability testing"
**Expected Agent:** security-engineer.prompt.md
**Expected Distance Range:** 1.1-1.5 (Good to Okay, technical)
**Query Type:** Domain-specific, security-focused
**Rationale:** Tests security with specialized terminology

---

### Test 9: Performance Engineering
**Query:** "database optimization and query performance tuning"
**Expected Agent:** performance-engineer.prompt.md
**Expected Distance Range:** 0.9-1.3 (Good to Okay, multi-concept)
**Query Type:** Domain-specific, multi-concept
**Rationale:** Tests performance specialist with database focus

---

### Test 10: Quality Engineering
**Query:** "testing strategies test automation and quality assurance"
**Expected Agent:** quality-engineer.prompt.md
**Expected Distance Range:** 0.9-1.3 (Good to Okay, multi-concept)
**Query Type:** Domain-specific, multi-concept
**Rationale:** Tests quality specialist with QA focus

---

### Test 11: Architecture Pattern
**Query:** "circuit breaker pattern microservices architecture"
**Expected Agent:** backend-architect.prompt.md or architecture-specialist.prompt.md
**Expected Distance Range:** 1.0-1.4 (Good to Okay, pattern-specific)
**Query Type:** Domain-specific, pattern-focused
**Rationale:** Tests architecture pattern recognition

---

### Test 12: Cross-Cutting Concern
**Query:** "How do I implement observability, logging, and monitoring across my system?"
**Expected Agent:** devops-architect.prompt.md or backend-architect.prompt.md
**Expected Distance Range:** 1.0-1.4 (Good to Okay, infrastructure-focused)
**Query Type:** Cross-cutting, multi-concept
**Rationale:** Tests query that spans multiple domains (DevOps primary, backend secondary)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Test Cases | 12 |
| Agent Types Covered | 6 (frontend, backend, DevOps, security, performance, quality) |
| Multi-Concept Queries | 8 (67%) |
| Single-Concept Queries | 4 (33%) |
| Edge Case Queries | 5 (42%) |
| Expected Pass Rate | 100% |
| Expected Confidence | > 95% |

---

## Query Type Distribution

| Type | Count | Examples |
|------|-------|----------|
| Domain-specific | 10 | Frontend hooks, Backend API, DevOps CI/CD |
| Multi-concept | 8 | Secure backend + monitoring, DB + performance |
| Ambiguous | 1 | State management (frontend vs backend) |
| Pattern-focused | 1 | Circuit breaker pattern |
| Cross-cutting | 1 | Observability across system |
| Simple | 1 | API design (short, focused) |

---

## Expected Distance Distribution

| Range | Count | Confidence |
|-------|-------|------------|
| < 0.8 (Excellent) | 2 | High |
| 0.8-1.0 (Good) | 3 | High |
| 1.0-1.2 (Okay) | 5 | Medium |
| 1.2-1.4 (Okay-Poor) | 2 | Medium |
| > 1.4 (Poor) | 0 | Expected none |

---

## Integration with Test Suite

These 12 queries will be added to `test_collection_queries.py` in the following format:

```python
test_cases = [
    {
        "name": "Frontend Architecture - React Hooks",
        "query": "How do I use React hooks and compose them effectively?",
        "expected_agent": "frontend-architect.prompt.md",
        "expected_distance_range": (1.0, 1.3),
        "query_type": "multi-concept"
    },
    # ... 11 more cases following same format
]
```

---

## Success Criteria for Phase 1.1

- [x] 12 test queries identified
- [x] Expected agents documented
- [x] Expected distance ranges established
- [x] Query types classified
- [x] Query list available for Phase 1.2

**Ready for Phase 1.2:** Build Extended Test Suite

---

## Notes

- These queries are designed to span all available agent specialists
- Expected distance ranges are based on Phase 0 (threshold recalibration) findings
- Edge cases include ambiguous queries and cross-cutting concerns
- All queries are realistic (based on actual use cases or common patterns)
- No queries should return "Poor" (> 1.4 distance) for correct agent match
