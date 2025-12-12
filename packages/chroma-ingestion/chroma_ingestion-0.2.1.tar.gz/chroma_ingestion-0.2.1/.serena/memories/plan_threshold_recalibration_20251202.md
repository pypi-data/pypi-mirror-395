# Threshold Recalibration Execution Plan

**Date:** December 2, 2025
**Status:** Planning Phase
**Goal:** Implement distance threshold fixes and validate with new thresholds

---

## Problem Statement

Distance thresholds documented as < 0.5 (great) but actual relevant results appear at 0.76-1.25.
Impact: Users filtering results < 0.5 would discard correct agents thinking they're poor quality.

---

## Solution Strategy

### Proposed New Thresholds
```
< 0.8   → Excellent (high confidence match)
0.8-1.0 → Good (solid match)
1.0-1.2 → Okay (acceptable, weaker relevance)
> 1.2   → Poor (likely noise)
```

**Rationale:** Aligns with observed actual distances where correct agents appear at 0.76-1.25 range

---

## Phase Structure

### Phase 1: Code & Documentation Updates (30 min)
**Goal:** Update all hardcoded thresholds and documentation

**Tasks:**
1. Update `src/retrieval.py` distance constants
2. Update `USAGE_GUIDE.md` with new threshold examples
3. Update `README.md` behavioral documentation
4. Update any inline code comments referencing old thresholds

**Success Criteria:**
- All threshold values consistent (< 0.8, 0.8-1.0, 1.0-1.2, > 1.2)
- All examples updated to reflect new ranges
- No remnants of old thresholds in codebase

**Deliverables:**
- Modified retrieval.py
- Updated USAGE_GUIDE.md
- Updated README.md

### Phase 2: Validation Testing (15 min)
**Goal:** Verify new thresholds work with existing test queries

**Tasks:**
1. Run existing test script: `python test_collection_queries.py`
2. Verify 4 test queries return correct agents within new threshold ranges
3. Document results

**Success Criteria:**
- All 4 test queries pass with new thresholds
- Relevant agents NOT filtered as "poor"
- Distance spread reasonable

**Deliverables:**
- Test results summary
- Updated test_collection_results.json

### Phase 3: Long-term Monitoring (60 min)
**Goal:** Implement automated detection of future threshold drift

**Tasks:**
1. Create `validate_thresholds.py` script for periodic checking
2. Add threshold check to existing test suite
3. Document monitoring procedures
4. Create threshold drift alert mechanism

**Success Criteria:**
- Automated script detects threshold violations
- Can run standalone or in CI/CD
- Produces actionable alerts

**Deliverables:**
- validate_thresholds.py
- Updated README with monitoring section
- CI/CD integration guide

---

## Dependencies

**Phase 1 → Phase 2:** Code must be updated before testing
**Phase 2 → Phase 3:** Validation must pass before investing in monitoring

---

## Execution Sequence

1. ✅ User approval of plan (you are here)
2. Phase 1: Update code & docs
3. Phase 2: Run validation tests
4. Phase 3: Implement monitoring
5. Final: Create execution report

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Thresholds still wrong | Will be evident in Phase 2 testing |
| Incomplete updates | Checklist approach for each file |
| Performance degradation | Test queries should execute in <2s |
| Future drift undetected | Phase 3 addresses with monitoring |

---

## Files to Modify

```
/home/ob/Development/Tools/chroma/
├── src/retrieval.py              [Update distance constants]
├── USAGE_GUIDE.md                [Update examples & thresholds]
├── README.md                     [Update documentation]
├── validate_thresholds.py        [NEW: Monitoring script]
└── test_collection_queries.py    [Reuse for validation]
```

---

## Time Estimate

| Phase | Estimate | Status |
|-------|----------|--------|
| Phase 1 | 30 min | Ready to execute |
| Phase 2 | 15 min | Ready to execute |
| Phase 3 | 60 min | Ready to execute |
| **Total** | **105 min** | **~2 hours** |

---

## Decision Points

**Proceed to Phase 1?** Awaiting user confirmation
