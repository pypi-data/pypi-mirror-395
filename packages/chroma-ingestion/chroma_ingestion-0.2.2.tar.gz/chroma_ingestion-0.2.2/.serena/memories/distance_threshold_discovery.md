# Critical Discovery: Distance Thresholds Are Wrong

## Problem
Even with high-quality original agents (8-26 KB, 311 chunks), query results show 0% excellent/good matches using our thresholds:
- Excellent: distance < 0.3 (0% of results)
- Good: 0.3-0.5 (0% of results)
- Weak: 0.5-0.7 (6.2% of results)
- Poor: > 0.7 (93.8% of results)

## Evidence of Issue
Query: "backend architecture system design"
- Returns: backend-architect.prompt.md (distance 0.786)
- Document LITERALLY CONTAINS: "Expert Backend Architect specializing in designing reliable backend systems"
- Marked as: "Poor" (0.786 > 0.7)

## Root Cause Hypothesis
**Our distance thresholds are fundamentally wrong for Chroma's cosine distance metric.**

### Cosine Distance Math
- Range: 0 to 2 (can exceed 1)
- 0 = identical vectors
- 1 = 90 degree angle (orthogonal)
- 2 = opposite vectors

Distance 0.786 ≈ 38 degree angle = MODERATE RELEVANCE

### The Mismatch
Our thresholds (< 0.3 for excellent) assume:
- Very high similarity needed (< 0.3 radians ≈ 17 degrees)
- But text queries and source documents are inherently different
- Even relevant documents won't have perfect angle match

## What Real Thresholds Should Be
Need to research OR empirically test with known-relevant pairs:
- 0.5-0.7 might be "good"
- 0.7-0.9 might be "acceptable"
- > 0.9 might be "poor"

## Test Evidence
- All 32 queries returning highest match 0.572-0.987
- Multi-word queries worse than single-concept queries
- Most matches in 0.7-1.2 range (not anomalous)

## Next Steps
1. **DON'T change the data** - it's good quality now
2. **CHANGE THE EVALUATION CRITERIA** - adjust distance thresholds
3. Re-run same 32 queries with adjusted thresholds
4. Document proper threshold expectations
