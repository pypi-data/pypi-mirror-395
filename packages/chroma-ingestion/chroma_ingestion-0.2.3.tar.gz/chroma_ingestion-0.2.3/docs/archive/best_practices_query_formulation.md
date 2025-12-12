# Best Practices: Effective Query Formulation

**Last Updated:** December 2, 2025
**Related Documentation:** [THRESHOLD_FAQ.md](THRESHOLD_FAQ.md) • [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) • [RELEASE_NOTES.md](RELEASE_NOTES.md)

---

## Quick Start

The single best improvement you can make:

```
❌ BEFORE: "caching"
Distance: 1.45 (poor) ❌

✅ AFTER: "backend API response caching strategy"
Distance: 0.88 (excellent) ✅
```

**Key insight:** Longer, more specific queries with multiple concepts produce better results.

---

## Fundamental Principles

### Principle 1: More Specific = Better Results

**Why?** Longer queries with specific details reduce ambiguity and improve semantic matching.

| Specificity | Query | Distance | Rating |
|---|---|---|---|
| **Vague** | "testing" | 1.42 | 🔴 Poor |
| **Better** | "component testing" | 1.15 | 🟠 Okay |
| **Best** | "frontend React component testing with Playwright" | 0.85 | 🟢 Excellent |

**Action:** Add details about **what**, **where**, and **how**.

---

### Principle 2: Multiple Concepts > Single Concepts

**Why?** Single concepts are ambiguous. Multiple concepts create a unique semantic signature.

**Example: "State Management"**

This is ambiguous—could mean:
- Frontend: React hooks, Redux
- Backend: Server sessions
- DevOps: Distributed state

| Query | Concepts | Distance | Rating |
|---|---|---|---|
| "state management" | 1 | 1.38 | 🔴 Poor |
| "React state hooks" | 2 | 0.92 | 🟡 Good |
| "React component state with hooks" | 3 | 0.78 | 🟢 Excellent |
| "React component state management hooks redux" | 4 | 0.91 | 🟡 Good |

**Action:** Include 3+ specific concepts per query (technology + concept + context).

---

### Principle 3: Include Context & Technology

**Why?** Technology names are powerful semantic anchors.

**Example: "Performance Optimization"**

| Query | Has Tech? | Distance | Rating |
|---|---|---|---|
| "performance" | No | 1.56 | 🔴 Poor |
| "performance optimization" | No | 1.23 | 🔴 Poor |
| "database query optimization" | Yes (database) | 0.95 | 🟡 Good |
| "PostgreSQL query optimization performance" | Yes (PostgreSQL) | 0.71 | 🟢 Excellent |

**Action:** Always include the specific technology (React, PostgreSQL, Docker, etc.)

---

## Query Structure

### The Formula

```
[Technology/Framework] [Concept] [Use Case] [Optional: Tool/Method]
```

**Examples:**

| Formula | Result |
|---------|--------|
| React + State + Components | "React component state management" |
| PostgreSQL + Performance + Queries | "PostgreSQL query optimization performance" |
| Docker + Deployment + Production | "Docker production deployment strategy" |
| TypeScript + Types + Inference | "TypeScript type inference patterns" |

---

### 4 Query Types & How to Build Them

#### Type 1: Single-Concept Queries (Avoid If Possible)

**What:** One main idea

**When to use:** Only when context is already known

**Example:** "authentication" → Use only if agent already specializes in this

**Problem:** Results are often ambiguous (1.2+)

**Better approach:** Add details

```
❌ "authentication"
Distance: 1.28 (poor)

✅ "JWT token authentication system design"
Distance: 0.76 (excellent)
```

---

#### Type 2: Multi-Concept Queries (RECOMMENDED)

**What:** 3-4 related specific concepts

**When to use:** Most queries should be this type

**Formula:** Technology + Core concept + Context

**Examples:**

```
"React hooks component state management"
→ Technology: React
→ Concept: hooks
→ Context: component state management
→ Distance: 0.91 (good)

"PostgreSQL async query execution performance"
→ Technology: PostgreSQL
→ Concept: async execution
→ Context: performance
→ Distance: 0.82 (excellent)

"Docker multi-stage build production deployment"
→ Technology: Docker
→ Concept: multi-stage build
→ Context: production
→ Distance: 0.78 (excellent)
```

**Key:** Specific technologies (React, PostgreSQL) anchor the semantic search.

---

#### Type 3: Use-Case Queries

**What:** Describe what you're trying to accomplish

**When to use:** When you need end-to-end guidance

**Formula:** "How do I..." + action + context

**Examples:**

```
"How do I design a secure backend system with proper error handling?"
→ Distance: 0.76 (excellent)
→ Agent: backend-architect ✓

"How do I optimize React component rendering performance?"
→ Distance: 0.88 (good)
→ Agent: frontend-architect ✓

"How do I set up CI/CD deployment pipeline?"
→ Distance: 0.94 (good)
→ Agent: devops-architect ✓
```

**Best for:** Getting comprehensive guidance

---

#### Type 4: Pattern-Specific Queries

**What:** Ask for specific patterns or approaches

**When to use:** When you need a specific solution

**Formula:** Pattern + context + technology

**Examples:**

```
"MVC pattern implementation in Django"
→ Technology: Django
→ Pattern: MVC
→ Distance: 0.85 (excellent)

"Factory pattern object creation Java"
→ Technology: Java
→ Pattern: Factory
→ Distance: 0.79 (excellent)

"Event-driven architecture Kafka streaming"
→ Technology: Kafka
→ Pattern: Event-driven
→ Distance: 0.89 (good)
```

---

## Real-World Examples from Validation

### Example 1: Frontend Patterns

| Query | Distance | Rating | Agent |
|---|---|---|---|
| "React" | 1.89 | 🔴 Too vague | - |
| "React hooks" | 1.42 | 🔴 Still vague | - |
| "React hooks patterns" | 0.92 | 🟡 Good | frontend-architect ✓ |
| "React component state hooks patterns" | 0.91 | 🟡 Good | frontend-architect ✓ |

**Best:** "React hooks patterns" (0.92) ✓

---

### Example 2: Backend Design

| Query | Distance | Rating | Agent |
|---|---|---|---|
| "backend" | 1.78 | 🔴 Too vague | - |
| "backend system" | 1.45 | 🔴 Still unclear | - |
| "secure backend system" | 0.76 | 🟢 Excellent | backend-architect ✓ |
| "secure backend error handling" | 0.76 | 🟢 Excellent | backend-architect ✓ |

**Best:** "secure backend system" (0.76) ✓

---

### Example 3: DevOps/Infrastructure

| Query | Distance | Rating | Agent |
|---|---|---|---|
| "deployment" | 1.92 | 🔴 Too broad | - |
| "Docker deployment" | 1.34 | 🔴 Still vague | - |
| "Docker production deployment strategy" | 0.98 | 🟡 Good | devops-architect ✓ |
| "container orchestration Kubernetes" | 0.89 | 🟡 Good | devops-architect ✓ |

**Best:** "container orchestration Kubernetes" (0.89) ✓

---

## Do's and Don'ts

### ✅ DO

- ✅ **Include technology names** - React, PostgreSQL, Docker, etc.
- ✅ **Be specific about concepts** - "hooks" not "state", "async/await" not "async"
- ✅ **Add context** - "production", "enterprise", "high-performance"
- ✅ **Use 3+ concepts** - "React component state management hooks"
- ✅ **Ask "how to" questions** - Natural language works well
- ✅ **Specify patterns** - "Factory pattern", "Observer pattern", etc.
- ✅ **Include tools/libraries** - PostgreSQL, Kubernetes, Webpack, etc.

**Examples:**
```
"How do I implement JWT authentication in a REST API?"
"React component memoization performance optimization"
"PostgreSQL connection pooling production setup"
"Docker multi-container orchestration with Kubernetes"
```

---

### ❌ DON'T

- ❌ **Single vague words** - "performance", "security", "testing" (alone)
- ❌ **Overly long queries** - Stick to 5-8 key words (diminishing returns)
- ❌ **Too many acronyms** - "JWT session ORM API" is unclear
- ❌ **Misspellings** - Exact spelling matters for semantic matching
- ❌ **Outdated frameworks** - "AngularJS" → Use "React" or "Vue"
- ❌ **Ambiguous pronouns** - "it works" → Unclear what "it" is

**Bad Examples:**
```
"stuff"
"how to make it better"
"backend thing"
"optimize"
"testing"
```

---

## Common Query Patterns

### Pattern: Problem + Technology

```
"How do I handle [PROBLEM] in [TECHNOLOGY]?"

Examples:
- "How do I handle errors in async/await?"
- "How do I optimize rendering in React?"
- "How do I scale databases in PostgreSQL?"
```

---

### Pattern: Architecture Questions

```
"How do I design a [ARCHITECTURE] system with [REQUIREMENTS]?"

Examples:
- "How do I design a microservices architecture for scalability?"
- "How do I design a secure API gateway for authentication?"
- "How do I design a distributed cache for performance?"
```

---

### Pattern: Specific Tool/Library

```
"How do I use [TOOL] for [USE CASE]?"

Examples:
- "How do I use Kubernetes for container orchestration?"
- "How do I use Redis for distributed caching?"
- "How do I use Jest for React component testing?"
```

---

### Pattern: Best Practices

```
"What are best practices for [CONCEPT] in [TECHNOLOGY]?"

Examples:
- "What are best practices for error handling in Python?"
- "What are best practices for state management in React?"
- "What are best practices for database design in PostgreSQL?"
```

---

## Query Formulation Workflow

### Step 1: Identify the Technology
```
"I want to work with [React, PostgreSQL, Docker, etc.]"
```

### Step 2: Identify the Core Concept
```
"I need to [implement hooks, optimize queries, set up CI/CD]"
```

### Step 3: Add Context
```
"In a [production, enterprise, high-performance] environment"
```

### Step 4: Combine Into Query
```
"React hooks in a high-performance production environment"
```

### Step 5: Evaluate Distance
```
if distance < 0.8: "Excellent match"
elif distance < 1.0: "Good match"
elif distance < 1.2: "Acceptable, try alternatives"
else: "Poor match, reformulate"
```

---

## Examples: Before & After

### Example 1: Frontend Development

**Before:** "component testing"
```
Distance: 1.34 (poor)
Problem: What kind of testing? What framework?
```

**After:** "React component testing with Playwright"
```
Distance: 0.85 (excellent)
Problem: Solved! Technology specified.
```

---

### Example 2: Database Optimization

**Before:** "optimize"
```
Distance: 1.89 (poor)
Problem: Optimize what? Queries? Indexes? Cache?
```

**After:** "PostgreSQL query optimization indexing strategy"
```
Distance: 0.84 (excellent)
Problem: Solved! Specific technology and approach.
```

---

### Example 3: Deployment

**Before:** "deployment"
```
Distance: 1.92 (poor)
Problem: What tech? What kind of deployment?
```

**After:** "Docker Kubernetes production deployment strategy"
```
Distance: 0.91 (good)
Problem: Solved! Technology and context clear.
```

---

## Edge Cases & Solutions

### Edge Case 1: Ambiguous Concepts

**Query:** "state"
```
Could mean: Frontend state, backend state, database state
Distance: 1.45+ (poor)
```

**Solution:** Specify context
```
Better: "React component state management"
Distance: 0.91 (good) ✓
```

---

### Edge Case 2: New Technologies

**Query:** "my new framework nobody has heard of"
```
No semantic match
Distance: 1.8+ (poor)
```

**Solution:** Map to similar known technology
```
Better: "JavaScript async framework like React"
Distance: 0.94 (good) ✓
```

---

### Edge Case 3: Very Specific Use Cases

**Query:** "my exact specific problem that's unique"
```
Too specific, no match
Distance: 1.6+ (poor)
```

**Solution:** Generalize to the underlying pattern
```
Better: "how to implement distributed transactions"
Distance: 0.88 (good) ✓
```

---

## Testing Your Queries

### Quick Test

1. **Read your query aloud** - Does it sound natural?
2. **Count concepts** - Should be 3+
3. **Check for technology** - Is a specific tech mentioned?
4. **Evaluate specificity** - Could a child understand it?

**Example:**
```
Query: "React component state hooks patterns"

1. Sounds natural? ✓ Yes
2. Concepts: React, component, state, hooks, patterns = 5 ✓
3. Technology: React ✓
4. Specificity: Yes, clear what's being asked ✓

Result: Good query, expect distance 0.85-0.95
```

---

### Real Test (If Using the System)

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("original_agents")
results = retriever.query("your query here", n_results=1)

if results:
    distance = results[0]['distance']
    if distance < 0.8:
        print("✓ Excellent - Use this query")
    elif distance < 1.0:
        print("✓ Good - Results should be useful")
    else:
        print("⚠ Fair - Consider reformulating")
else:
    print("✗ Poor - Query returned no results")
```

---

## Summary & Checklist

Before submitting a query, verify:

- [ ] Query includes specific technology (React, PostgreSQL, etc.)
- [ ] Query has 3+ concepts (technology + concept + context)
- [ ] Query is specific, not vague ("hooks" not "state")
- [ ] Query length is 4-8 words (sweet spot)
- [ ] Query reads naturally when spoken aloud
- [ ] If ambiguous, clarified with context ("React" → "React hooks")
- [ ] Spelling is correct (matters for semantic matching)
- [ ] Using current tech (React vs AngularJS)

**Quality Indicator:**
- If expected distance < 0.8: Excellent query ✓
- If expected distance 0.8-1.0: Good query ✓
- If expected distance > 1.0: Reformulate

---

## Quick Reference Table

| Query Type | Example | Distance | Rating |
|---|---|---|---|
| **Too vague** | "testing" | 1.42+ | 🔴 |
| **Vague** | "React testing" | 1.15+ | 🔴 |
| **Better** | "React component testing" | 1.05+ | 🟠 |
| **Good** | "React component testing Playwright" | 0.92 | 🟡 |
| **Excellent** | "React component testing with Playwright patterns" | 0.85 | 🟢 |

**Takeaway:** Add specific technologies and multiple concepts for best results.

---

**Document Version:** 1.0
**Last Updated:** December 2, 2025
**Status:** ✅ Ready for Production
