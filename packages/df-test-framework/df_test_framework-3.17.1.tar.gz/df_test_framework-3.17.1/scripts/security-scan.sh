#!/bin/bash
# 本地安全扫描脚本
# 用途: 在提交代码前本地运行安全检查
# 使用: bash scripts/security-scan.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  DF Test Framework - 安全扫描工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 创建报告目录
REPORT_DIR="reports/security"
mkdir -p "$REPORT_DIR"

echo -e "${YELLOW}📦 正在安装扫描工具...${NC}"
pip install -q safety bandit pip-audit || {
    echo -e "${RED}❌ 安装扫描工具失败${NC}"
    exit 1
}

echo -e "${GREEN}✅ 工具安装完成${NC}"
echo ""

# ========================================
# 1. Safety - 依赖漏洞扫描
# ========================================
echo -e "${BLUE}🔍 [1/4] Safety - 依赖漏洞扫描...${NC}"
SAFETY_EXIT_CODE=0
safety check --json --output "$REPORT_DIR/safety-report.json" || SAFETY_EXIT_CODE=$?
safety check --output "$REPORT_DIR/safety-report.txt" || true

if [ $SAFETY_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Safety: 未发现依赖漏洞${NC}"
else
    VULN_COUNT=$(jq '.vulnerabilities | length' "$REPORT_DIR/safety-report.json" 2>/dev/null || echo "未知")
    echo -e "${RED}⚠️  Safety: 发现 $VULN_COUNT 个依赖漏洞${NC}"
    echo -e "${YELLOW}   详细报告: $REPORT_DIR/safety-report.txt${NC}"
fi
echo ""

# ========================================
# 2. Bandit - 代码安全审计
# ========================================
echo -e "${BLUE}🔐 [2/4] Bandit - 代码安全审计...${NC}"
BANDIT_EXIT_CODE=0
bandit -r src/ -f json -o "$REPORT_DIR/bandit-report.json" || BANDIT_EXIT_CODE=$?
bandit -r src/ -f txt -o "$REPORT_DIR/bandit-report.txt" || true

if [ $BANDIT_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Bandit: 未发现代码安全问题${NC}"
else
    if [ -f "$REPORT_DIR/bandit-report.json" ]; then
        HIGH_COUNT=$(jq '[.results[] | select(.issue_severity == "HIGH")] | length' "$REPORT_DIR/bandit-report.json" 2>/dev/null || echo "0")
        MEDIUM_COUNT=$(jq '[.results[] | select(.issue_severity == "MEDIUM")] | length' "$REPORT_DIR/bandit-report.json" 2>/dev/null || echo "0")
        LOW_COUNT=$(jq '[.results[] | select(.issue_severity == "LOW")] | length' "$REPORT_DIR/bandit-report.json" 2>/dev/null || echo "0")

        echo -e "${RED}⚠️  Bandit: 发现安全问题${NC}"
        echo -e "${YELLOW}   高危: $HIGH_COUNT | 中危: $MEDIUM_COUNT | 低危: $LOW_COUNT${NC}"
        echo -e "${YELLOW}   详细报告: $REPORT_DIR/bandit-report.txt${NC}"
    fi
fi
echo ""

# ========================================
# 3. pip-audit - 额外依赖检查
# ========================================
echo -e "${BLUE}📦 [3/4] pip-audit - 额外依赖检查...${NC}"
PIP_AUDIT_EXIT_CODE=0
pip-audit --format json --output "$REPORT_DIR/pip-audit-report.json" || PIP_AUDIT_EXIT_CODE=$?
pip-audit --format markdown --output "$REPORT_DIR/pip-audit-report.md" || true

if [ $PIP_AUDIT_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ pip-audit: 未发现依赖漏洞${NC}"
else
    if [ -f "$REPORT_DIR/pip-audit-report.json" ]; then
        VULN_COUNT=$(jq '.dependencies | length' "$REPORT_DIR/pip-audit-report.json" 2>/dev/null || echo "未知")
        echo -e "${RED}⚠️  pip-audit: 发现 $VULN_COUNT 个依赖漏洞${NC}"
        echo -e "${YELLOW}   详细报告: $REPORT_DIR/pip-audit-report.md${NC}"
    fi
fi
echo ""

# ========================================
# 4. 敏感信息检查
# ========================================
echo -e "${BLUE}🔑 [4/4] 检查敏感信息泄露...${NC}"
SECRETS_FOUND=0

# 检查常见的敏感信息模式
echo "正在扫描代码中的密钥、密码等敏感信息..."

# 密码模式
PASSWORD_MATCHES=$(grep -r -n "password\s*=\s*['\"][^'\"]*['\"]" src/ --include="*.py" 2>/dev/null | grep -v "Field(" | grep -v "SecretStr" | wc -l || echo "0")
if [ "$PASSWORD_MATCHES" -gt 0 ]; then
    echo -e "${RED}⚠️  发现 $PASSWORD_MATCHES 处可能的硬编码密码${NC}"
    SECRETS_FOUND=1
fi

# API密钥模式
API_KEY_MATCHES=$(grep -r -n "api[_-]key\s*=\s*['\"][^'\"]*['\"]" src/ --include="*.py" -i 2>/dev/null | grep -v "Field(" | wc -l || echo "0")
if [ "$API_KEY_MATCHES" -gt 0 ]; then
    echo -e "${RED}⚠️  发现 $API_KEY_MATCHES 处可能的硬编码API密钥${NC}"
    SECRETS_FOUND=1
fi

# Token模式
TOKEN_MATCHES=$(grep -r -n "token\s*=\s*['\"][^'\"]*['\"]" src/ --include="*.py" -i 2>/dev/null | grep -v "Field(" | grep -v "SecretStr" | wc -l || echo "0")
if [ "$TOKEN_MATCHES" -gt 0 ]; then
    echo -e "${RED}⚠️  发现 $TOKEN_MATCHES 处可能的硬编码Token${NC}"
    SECRETS_FOUND=1
fi

if [ $SECRETS_FOUND -eq 0 ]; then
    echo -e "${GREEN}✅ 未发现明显的敏感信息泄露${NC}"
fi
echo ""

# ========================================
# 生成汇总报告
# ========================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  扫描汇总${NC}"
echo -e "${BLUE}========================================${NC}"

TOTAL_ISSUES=0

# 统计总问题数
if [ $SAFETY_EXIT_CODE -ne 0 ]; then
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
fi
if [ $BANDIT_EXIT_CODE -ne 0 ]; then
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
fi
if [ $PIP_AUDIT_EXIT_CODE -ne 0 ]; then
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
fi
if [ $SECRETS_FOUND -ne 0 ]; then
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
fi

if [ $TOTAL_ISSUES -eq 0 ]; then
    echo -e "${GREEN}🎉 太棒了！未发现任何安全问题${NC}"
    echo -e "${GREEN}✅ 代码可以安全提交${NC}"
    EXIT_CODE=0
else
    echo -e "${YELLOW}⚠️  发现 $TOTAL_ISSUES 类安全问题${NC}"
    echo -e "${YELLOW}📁 详细报告保存在: $REPORT_DIR/${NC}"
    echo ""
    echo -e "${YELLOW}建议修复后再提交代码${NC}"
    EXIT_CODE=1
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  报告文件列表${NC}"
echo -e "${BLUE}========================================${NC}"
ls -lh "$REPORT_DIR/" | grep -v "^total" | awk '{print "  " $9 " (" $5 ")"}'
echo ""

exit $EXIT_CODE
