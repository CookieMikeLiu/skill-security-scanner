# 🔬 Security Scanner Test Suite

This directory contains test skills to validate the security scanner's detection capabilities.

## Test Skills

### test-malicious/
A deliberately malicious skill designed to test detection. **DO NOT INSTALL**.

Contains examples of:
- Code execution (eval/exec)
- System command injection
- Network exfiltration
- Keylogging patterns
- File destruction
- Cryptomining signatures

### test-benign/
A legitimate skill to test false positive rates.

Contains examples of:
- Normal API calls
- File operations with proper handling
- Environment variable reading
- Safe subprocess usage

## Running Tests

```bash
# Scan malicious skill (should detect many issues)
python scripts/security_scanner.py tests/test-malicious --strict

# Scan benign skill (should pass with minimal findings)
python scripts/security_scanner.py tests/test-benign

# Compare scores
python scripts/security_scanner.py tests/test-malicious --format json | grep security_score
python scripts/security_scanner.py tests/test-benign --format json | grep security_score
```

## Expected Results

### test-malicious
- **Verdict**: 🔴 REJECT
- **Score**: < 30
- **Critical Findings**: >= 3
- **Total Findings**: >= 10

### test-benign
- **Verdict**: 🟢 PASS or 🟡 REVIEW
- **Score**: >= 70
- **Critical Findings**: 0
- **Total Findings**: 0-3 (minor info/low only)
