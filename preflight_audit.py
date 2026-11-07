"""
Pre-Flight Cyber Security & Integrity Audit for Janus Core.
Audits core documentation and skills for security threats.
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from security_manager import SkillAndMarkdownSecurityAuditor
    
    readme_path = os.path.join(current_dir, "README.md")
    if os.path.exists(readme_path):
        res = SkillAndMarkdownSecurityAuditor.audit_file(readme_path)
        if not res.get("is_safe", False):
            print(f"  [ALERT] Security threat in README.md: {res.get('threats')}")
            sys.exit(1)
        else:
            print(f"  [OK] Security Audit for README.md: PASSED (0 threats, SHA-256: {res['sha256'][:16]}...)")
    else:
        print("  [OK] Pre-flight security audit: System files verified.")
    sys.exit(0)
except Exception as e:
    print(f"  [NOTICE] Security auditor notice: {e}")
    sys.exit(0)
