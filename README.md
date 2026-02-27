# 🔒 Skill Security Scanner

Protect your OpenClaw installation from malicious skills with comprehensive static analysis.

## Overview

**Skill Security Scanner** performs deep security analysis on OpenClaw skills before installation, detecting:

- 🚨 **Critical Threats**: Code injection, keyloggers, cryptominers
- ⚠️ **High Risks**: System commands, credential theft, screen capture
- 📊 **Medium Risks**: Network requests, file deletion, obfuscation
- ℹ️ **Low Risks**: Best practice recommendations

## Features

| Feature | Description |
|---------|-------------|
| **Static Analysis** | Scans Python, JavaScript, TypeScript, Shell scripts |
| **20+ Detection Rules** | Covers common attack patterns |
| **Security Scoring** | 0-100 score with clear verdict |
| **Multiple Formats** | Text, JSON, Markdown reports |
| **Install Guard** | Interactive installation protection |
| **Test Suite** | Validates detection with malicious/benign samples |

## Installation

```bash
# Install from ClawHub
openclaw skill install skill-security-scanner

# Or manually
openclaw skill install skill-security-scanner.skill
```

## Quick Start

```bash
# Scan a skill before installing
python scripts/security_scanner.py /path/to/skill

# Interactive install guard
python scripts/install_guard.py /path/to/skill

# Generate detailed report
python scripts/security_scanner.py /path/to/skill --format markdown -o report.md
```

## Verdict Levels

| Level | Score | Action |
|-------|-------|--------|
| 🟢 **PASS** | 90-100 | Safe to install |
| 🟡 **REVIEW** | 50-89 | Review findings first |
| 🟠 **WARNING** | 0-49 | High risk - reconsider |
| 🔴 **REJECT** | 0 | **Do not install** |

## Detection Rules

### Critical (Auto-Reject)
- `EXEC001` - Code execution (eval, exec)
- `SUSPICIOUS001` - Keyloggers
- `SUSPICIOUS003` - Cryptocurrency mining

### High Risk
- `EXEC002` - System command execution
- `NET002` - Raw socket connections
- `ENV001` - Credential theft
- `SUSPICIOUS002` - Screen capture

### Medium Risk
- `NET001` - HTTP network requests
- `FILE001` - File deletion operations
- `OBF001` - Code obfuscation

## Example Output

```
============================================================
[SCAN] Skill Security Scan
============================================================
Skill: ./suspicious-skill
Score: 15/100
Verdict: 🔴 REJECT

Risk Distribution:
  🔴 CRITICAL: 5
  🟠 HIGH: 8
  🟡 MEDIUM: 3

⚠️ Top Findings:
  🔴 [EXEC001] Code Execution Functions
  🔴 [SUSPICIOUS003] Cryptomining Detected
  🟠 [ENV001] Credential Theft Pattern

🚫 INSTALLATION BLOCKED
Critical security threats detected.
```

## Testing

Validate the scanner with included test skills:

```bash
# Scan malicious skill (should REJECT)
python scripts/security_scanner.py tests/test-malicious

# Scan benign skill (should PASS)
python scripts/security_scanner.py tests/test-benign
```

## Integration

Add to your skill installation workflow:

```python
import subprocess
import sys

def install_skill(skill_path):
    result = subprocess.run([
        'python', 'scripts/install_guard.py', 
        skill_path, '--auto-reject'
    ])
    if result.returncode != 0:
        print("Installation cancelled")
        sys.exit(1)
    # Proceed with installation
```

## Documentation

- `SKILL.md` - Usage guide
- `references/rules-reference.md` - Complete rule reference
- `tests/` - Test suite for validation

## Why This Matters

OpenClaw skills have powerful capabilities:
- Execute system commands
- Access your files
- Make network requests
- Read environment variables

**A malicious skill can:**
- Steal your passwords and API keys
- Delete or encrypt your files
- Install persistent backdoors
- Use your computer for cryptomining
- Monitor your keystrokes and screen

**Skill Security Scanner** is your first line of defense.

## License

MIT License - See LICENSE file

## 💖 Support This Project

If this skill helps protect your OpenClaw installation, consider supporting its development:

### 打赏方式

| 方式 | 链接/方式 |
|------|----------|
| **GitHub Sponsors** | [github.com/sponsors/CookieMikeLiu](https://github.com/sponsors/CookieMikeLiu) |
| **爱发电** | [afdian.net/@CookieMikeLiu](https://afdian.net/@CookieMikeLiu) |
| **支付宝** | 扫码打赏 |
| **微信** | 扫码打赏 |

### 支持者特权

- 🌟 **$5+**: 名字出现在 README 感谢列表
- 🚀 **$20+**: 优先支持 + 新功能投票权
- 💎 **$50+**: 企业级定制咨询 30 分钟

### 赞助用途

你的支持将用于：
- 持续更新恶意软件特征库
- 开发更高级的静态分析引擎
- 支持更多编程语言检测
- 维护 ClawHub 免费版本

---

## Support

- Issues: GitHub Issues
- Discussions: OpenClaw Discord
- Updates: Watch this repository

## Thanks to Sponsors

<!-- 支持者名单将在这里列出 -->

*Become the first sponsor!*
