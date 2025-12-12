# Blocker Resolution: Chroma Metadata Type Constraint

**Date:** December 2, 2025
**Status:** RESOLVED
**Issue:** ValueError during re-ingestion - tech_stack as list not supported

## The Problem

Chroma Cloud API validation rejects list values in metadata. Error:

```
ValueError: Expected metadata value to be a str, int, float, bool, SparseVector, or None,
got ['ai', 'html', 'integration', ...] which is a list in upsert.
```

## Root Cause

Chroma's metadata validation (chromadb/api/types.py) only accepts specific types:
- `str` ✅
- `int` ✅
- `float` ✅
- `bool` ✅
- `SparseVector` ✅
- `None` ✅
- **NOT lists or dicts** ❌

## Solution Implemented

### 1. Revert tech_stack to String Format
- Change agent_ingestion.py line 218 back to comma-separated string
- This is the only format Chroma accepts for arrays of values

### 2. Document Chroma's Constraints
- Updated all documentation to reflect metadata type limitations
- Clarified that $in operator cannot be used with string tech_stack (would need custom comparison)

### 3. Provide Workaround for Filtering
Instead of Chroma-native filtering, use client-side filtering:

```python
# ❌ NOT POSSIBLE (Chroma doesn't support $in with strings)
where={"tech_stack": {"$in": ["react", "next.js"]}}

# ✅ WORKAROUND: Client-side filtering
results = retriever.query("Next.js patterns", n_results=10)
filtered = [
    r for r in results
    if all(tech in r['metadata']['tech_stack'] for tech in ['react', 'next.js'])
]
```

## Key Learning

**Chroma's metadata is optimized for**:
- Simple values (str, int, float, bool)
- Exact matching with $eq operator
- Numeric comparisons ($gt, $lt, $gte, $lte)
- NOT complex data structures

**For arrays of values**:
- Store as comma-separated string
- Use client-side filtering for complex queries
- Or use a separate metadata field per value (not scalable)

## Files Reverted

- `src/agent_ingestion.py` line 218: tech_stack back to string
- All documentation updated to remove array-based filtering mentions

## Impact on Task 2

**Original Goal:** "Restructure tech_stack as array for better filtering"

**Actual Outcome:**
- ❌ Cannot use Chroma's native filtering ($in operator) due to type constraints
- ✅ Can keep comma-separated string format
- ✅ Provide client-side filtering workaround
- ✅ Document constraint for future developers

This is a Chroma API limitation, not a code issue.
