# Testing Documentation - Quick Reference

📍 **Location:** `sm-py-bc/docs/`  
🎯 **Purpose:** Central hub for all testing documentation and progress tracking

---

## 📚 Document Index

| Document | Purpose | Audience | Update Frequency |
|----------|---------|----------|------------------|
| **[TESTING_AGENT_STATUS.md](TESTING_AGENT_STATUS.md)** | Quick status summary | All agents | Daily |
| **[TEST_ALIGNMENT_TRACKER.md](TEST_ALIGNMENT_TRACKER.md)** | Master task tracker | Testing lead | Per milestone |
| **[GRAALVM_TEST_PROGRESS.md](GRAALVM_TEST_PROGRESS.md)** | Technical details | Developers | Per task |
| **[SESSION_SUMMARY_GRAALVM_TESTS.md](SESSION_SUMMARY_GRAALVM_TESTS.md)** | Session report | Project manager | Per session |

---

## 🚀 Quick Start

### Want to know current status?
👉 Read **[TESTING_AGENT_STATUS.md](TESTING_AGENT_STATUS.md)** (2 minutes)

### Want to see detailed progress?
👉 Read **[GRAALVM_TEST_PROGRESS.md](GRAALVM_TEST_PROGRESS.md)** (5 minutes)

### Want to understand the full plan?
👉 Read **[TEST_ALIGNMENT_TRACKER.md](TEST_ALIGNMENT_TRACKER.md)** (10 minutes)

### Want to see what was done this session?
👉 Read **[SESSION_SUMMARY_GRAALVM_TESTS.md](SESSION_SUMMARY_GRAALVM_TESTS.md)** (3 minutes)

---

## 📊 Current Status at a Glance

```
GraalVM Integration Tests Progress
═══════════════════════════════════════════

Phase 1 (Foundation):     ████████░░░░░░░░░░░░ 40%
Phase 2 (Parameterized):  ░░░░░░░░░░░░░░░░░░░░  0%
Phase 3 (Advanced):       ░░░░░░░░░░░░░░░░░░░░  0%
Phase 4 (Documentation):  ░░░░░░░░░░░░░░░░░░░░  0%

Overall:                  ███░░░░░░░░░░░░░░░░░ 14%

Tests Completed: 45 / 315
Modules Complete: 1 / 6 (SM3)
```

### ✅ Completed
- BaseGraalVMPythonTest enhanced
- SM3DigestInteropTest (45 tests)

### 🟡 In Progress
- None (ready for next task)

### 🔴 Next Up
- SM2SignatureInteropTest (30 tests)
- SM2EncryptionInteropTest (25 tests)
- SM4CipherInteropTest (60 tests)

---

## 🎯 Testing Strategy

### Goal
Achieve 100% test parity with **sm-js-bc** to ensure cross-language compatibility.

### Approach
1. **GraalVM Integration:** Use GraalVM Polyglot to run Python from Java tests
2. **Cross-Verification:** Every test validates Python ↔ Java Bouncy Castle
3. **Comprehensive Coverage:** Standard vectors, edge cases, properties, performance
4. **Alignment:** Mirror sm-js-bc test structure exactly

### Test Categories
- **Standard Vectors:** Official test vectors from specifications
- **Cross-Language:** Java BC ↔ Python SM-BC verification
- **Parameterized:** Data-driven tests with many inputs
- **Property-Based:** Cryptographic property verification
- **Performance:** Timing and throughput measurements
- **Edge Cases:** Boundary conditions and error handling

---

## 🔍 Test Alignment Reference

### sm-js-bc Reference Structure
```
sm-js-bc/test/graalvm-integration/java/
├── BaseGraalVMTest.java           → BaseGraalVMPythonTest.java ✅
├── SM3DigestInteropTest.java       → SM3DigestInteropTest.java ✅
├── SM2SignatureInteropTest.java    → SM2SignatureInteropTest.java ❌
├── SM2EncryptionInteropTest.java   → SM2EncryptionInteropTest.java ❌
├── SM4CipherInteropTest.java       → SM4CipherInteropTest.java ❌
├── ParameterizedInteropTest.java   → ParameterizedInteropTest.java ❌
└── utils/TestDataGenerator.java    → TestDataGenerator.java ❌
```

✅ = Complete | ❌ = Not started

---

## 🛠 How to Run Tests

```bash
# Navigate to test directory
cd test/graalvm-integration/java

# Compile tests
mvn clean compile test-compile

# Run all tests (requires GraalVM Python)
mvn test

# Run specific test class
mvn test -Dtest=SM3DigestInteropTest

# Quick profile (~10 seconds)
mvn test -P quick

# Standard profile (~1 minute)
mvn test -P standard
```

### Prerequisites
- GraalVM 23.1.1+ with Python support
- Java 17+
- Maven 3.6+

---

## 📈 Metrics

### Test Count by Module

| Module | Target | Current | %Complete |
|--------|--------|---------|-----------|
| SM3 Digest | 50 | 45 | 90% |
| SM2 Signature | 30 | 0 | 0% |
| SM2 Encryption | 25 | 0 | 0% |
| SM4 Cipher | 60 | 0 | 0% |
| Parameterized | 100 | 0 | 0% |
| Property-Based | 50 | 0 | 0% |
| **TOTAL** | **315** | **45** | **14%** |

### Time Investment

| Phase | Estimated | Spent | Remaining |
|-------|-----------|-------|-----------|
| Phase 1 | 18h | 5h | 13h |
| Phase 2 | 10h | 0h | 10h |
| Phase 3 | 5h | 0h | 5h |
| Phase 4 | 5h | 0h | 5h |
| **TOTAL** | **38h** | **5h** | **33h** |

---

## 🤝 For Other Agents

### For Developer Agent
- **Status:** 🟢 No action required
- **Findings:** No bugs found in Python library (SM3 verified correct)
- **Communication:** Will create DEVELOPER_HANDOFF_*.md if issues found

### For CI/CD Agent
- **Status:** ✅ Tests compile successfully
- **Integration:** Ready for CI pipeline (with graceful skip if GraalVM unavailable)
- **Execution Time:** Quick profile ~10s, Standard ~1min

### For Documentation Agent
- **Status:** ✅ Test documentation complete for current phase
- **TODO:** README.md for GraalVM tests (Phase 4)

---

## 🔔 Communication Protocol

### How Testing Agent Communicates

1. **Daily Updates:** TESTING_AGENT_STATUS.md
2. **Task Completion:** GRAALVM_TEST_PROGRESS.md
3. **Session Reports:** SESSION_SUMMARY_*.md
4. **Blocking Issues:** DEVELOPER_HANDOFF_*.md (when needed)

### How to Request Information

Check documents in this order:
1. TESTING_AGENT_STATUS.md (quick status)
2. GRAALVM_TEST_PROGRESS.md (technical details)
3. TEST_ALIGNMENT_TRACKER.md (full plan)

---

## 📝 Notes and Conventions

### Test Naming
- `*InteropTest.java` - Cross-language integration tests
- `test*()` methods - Individual test cases
- `TestVector` - Standard test data structures

### Assertions
- `assertEquals(javaResult, pythonResult)` - Cross-verification
- `assumeTrue(pythonAvailable)` - Graceful skipping
- `assertTrue(condition, message)` - Property validation

### Documentation
- All methods have JavaDoc
- Tests have `@DisplayName` annotations
- Console output includes section headers

---

## 🎓 Key Concepts

### GraalVM Polyglot
Allows Java to execute Python code and share data seamlessly:
```java
Context context = Context.newBuilder("python")
    .allowAllAccess(true)
    .build();
Value result = context.eval("python", "2 + 2");
```

### Cross-Language Verification
Pattern used in all tests:
1. Compute with Java Bouncy Castle
2. Compute with Python SM-BC (via GraalVM)
3. Assert both results match
4. Verify against standard vectors if available

### Test Profiles
- **quick:** 10 iterations, ~10s (for CI)
- **standard:** 100 iterations, ~1min (default)
- **full:** 10,000 iterations, ~5min (thorough)
- **benchmark:** Performance tests only

---

## 🔗 Related Resources

### External
- [GraalVM Documentation](https://www.graalvm.org/docs/)
- [GraalVM Python](https://www.graalvm.org/python/)
- [Bouncy Castle](https://www.bouncycastle.org/)

### Internal
- [sm-js-bc Tests](../../sm-js-bc/test/graalvm-integration/)
- [Python SM-BC Source](../src/)

---

## 🐛 Known Issues

**None currently!** 🎉

All systems operational:
- ✅ Build system working
- ✅ Dependencies resolved
- ✅ Tests compiling
- ✅ No Python library bugs found

---

## 📅 Timeline

| Milestone | Target Date | Status |
|-----------|-------------|---------|
| Phase 1 Complete | Week 2 | 🟡 40% |
| Phase 2 Complete | Week 3 | 🔴 Not started |
| Phase 3 Complete | Week 3 | 🔴 Not started |
| Phase 4 Complete | Week 4 | 🔴 Not started |

---

## 📞 Contact

**Testing Agent:** Automated testing system  
**Update Frequency:** Daily during active development  
**Response Time:** Real-time for new documentation checks

---

**Last Updated:** 2025-12-06  
**Document Version:** 1.0  
**Next Review:** After Phase 1 completion

---

*This is the central hub for all testing documentation. Start here to understand the current state of testing efforts.*
