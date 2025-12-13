@echo off
REM 本地安全扫描脚本 - Windows版本
REM 用途: 在提交代码前本地运行安全检查
REM 使用: scripts\security-scan.bat

setlocal enabledelayedexpansion

echo ========================================
echo   DF Test Framework - 安全扫描工具
echo ========================================
echo.

REM 创建报告目录
set REPORT_DIR=reports\security
if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

echo [安装] 正在安装扫描工具...
pip install -q safety bandit pip-audit >nul 2>&1
if errorlevel 1 (
    echo [错误] 安装扫描工具失败
    exit /b 1
)
echo [完成] 工具安装完成
echo.

REM ========================================
REM 1. Safety - 依赖漏洞扫描
REM ========================================
echo [1/4] Safety - 依赖漏洞扫描...
safety check --json --output "%REPORT_DIR%\safety-report.json" >nul 2>&1
set SAFETY_EXIT_CODE=!errorlevel!
safety check --output "%REPORT_DIR%\safety-report.txt" >nul 2>&1

if !SAFETY_EXIT_CODE! equ 0 (
    echo [OK] Safety: 未发现依赖漏洞
) else (
    echo [警告] Safety: 发现依赖漏洞
    echo        详细报告: %REPORT_DIR%\safety-report.txt
)
echo.

REM ========================================
REM 2. Bandit - 代码安全审计
REM ========================================
echo [2/4] Bandit - 代码安全审计...
bandit -r src\ -f json -o "%REPORT_DIR%\bandit-report.json" >nul 2>&1
set BANDIT_EXIT_CODE=!errorlevel!
bandit -r src\ -f txt -o "%REPORT_DIR%\bandit-report.txt" >nul 2>&1

if !BANDIT_EXIT_CODE! equ 0 (
    echo [OK] Bandit: 未发现代码安全问题
) else (
    echo [警告] Bandit: 发现安全问题
    echo        详细报告: %REPORT_DIR%\bandit-report.txt
)
echo.

REM ========================================
REM 3. pip-audit - 额外依赖检查
REM ========================================
echo [3/4] pip-audit - 额外依赖检查...
pip-audit --format json --output "%REPORT_DIR%\pip-audit-report.json" >nul 2>&1
set PIP_AUDIT_EXIT_CODE=!errorlevel!
pip-audit --format markdown --output "%REPORT_DIR%\pip-audit-report.md" >nul 2>&1

if !PIP_AUDIT_EXIT_CODE! equ 0 (
    echo [OK] pip-audit: 未发现依赖漏洞
) else (
    echo [警告] pip-audit: 发现依赖漏洞
    echo        详细报告: %REPORT_DIR%\pip-audit-report.md
)
echo.

REM ========================================
REM 4. 敏感信息检查
REM ========================================
echo [4/4] 检查敏感信息泄露...
set SECRETS_FOUND=0

REM 检查硬编码密码 (简化版本，Windows下grep功能受限)
findstr /S /N /I /R "password.*=.*['\"]" src\*.py >nul 2>&1
if !errorlevel! equ 0 (
    echo [警告] 发现可能的硬编码密码
    set SECRETS_FOUND=1
)

findstr /S /N /I /R "api_key.*=.*['\"]" src\*.py >nul 2>&1
if !errorlevel! equ 0 (
    echo [警告] 发现可能的硬编码API密钥
    set SECRETS_FOUND=1
)

if !SECRETS_FOUND! equ 0 (
    echo [OK] 未发现明显的敏感信息泄露
)
echo.

REM ========================================
REM 生成汇总报告
REM ========================================
echo ========================================
echo   扫描汇总
echo ========================================

set TOTAL_ISSUES=0
if !SAFETY_EXIT_CODE! neq 0 set /a TOTAL_ISSUES+=1
if !BANDIT_EXIT_CODE! neq 0 set /a TOTAL_ISSUES+=1
if !PIP_AUDIT_EXIT_CODE! neq 0 set /a TOTAL_ISSUES+=1
if !SECRETS_FOUND! neq 0 set /a TOTAL_ISSUES+=1

if !TOTAL_ISSUES! equ 0 (
    echo [成功] 太棒了！未发现任何安全问题
    echo [OK] 代码可以安全提交
    set EXIT_CODE=0
) else (
    echo [警告] 发现 !TOTAL_ISSUES! 类安全问题
    echo [提示] 详细报告保存在: %REPORT_DIR%\
    echo.
    echo 建议修复后再提交代码
    set EXIT_CODE=1
)

echo.
echo ========================================
echo   报告文件列表
echo ========================================
dir /B "%REPORT_DIR%"
echo.

exit /b !EXIT_CODE!
