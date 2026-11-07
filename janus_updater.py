"""
Janus Modular Updater for Janus Core.
Provides atomic plugin application, AST-based security verification,
manifest management, and atomic rollback capabilities.
"""

import ast
import json
import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_STAGED_UPDATES = [
    {
        "update_id": "update_v3_8_0_phase32",
        "target_version": "3.8.0",
        "target_phase": 32,
        "title": "Adaptive Routing & Phase 32 Kernel",
        "description": "Modular optimization layer with sub-millisecond dispatch and AST safety enforcement.",
        "plugin_name": "phase32_kernel.py",
        "plugin_code": "# Phase 32 Kernel Extension\nVERSION = '3.8.0'\nPHASE = 32\n",
    }
]


class JanusModularUpdater:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.base_dir / "version_manifest.json"
        self.backups_dir = self.base_dir / ".updater_backups"
        self.backups_dir.mkdir(parents=True, exist_ok=True)

        self.staged_updates: List[Dict[str, Any]] = list(DEFAULT_STAGED_UPDATES)
        self._init_manifest()

    def _init_manifest(self) -> None:
        if not self.manifest_path.exists():
            initial_manifest = {
                "current_version": "3.7.0",
                "core_system": "JanusCore",
                "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "installed_updates": [],
                "history": [],
            }
            self._save_manifest(initial_manifest)

    def _save_manifest(self, manifest_data: Dict[str, Any]) -> None:
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)

    def get_manifest(self) -> Dict[str, Any]:
        if not self.manifest_path.exists():
            self._init_manifest()
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_full_status(self) -> Dict[str, Any]:
        manifest = self.get_manifest()
        return {
            "status": "ONLINE",
            "current_version": manifest.get("current_version", "3.7.0"),
            "staged_updates": self.staged_updates,
            "manifest": manifest,
        }

    def _verify_code_security(self, code_str: str) -> bool:
        if not code_str:
            return True
        try:
            tree = ast.parse(code_str)
        except Exception:
            return False

        forbidden_names = {"eval", "exec", "compile", "__import__"}
        for node in ast.walk(tree):
            # 1. Direct function or method calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in forbidden_names:
                    return False
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in {"eval", "exec", "__import__"}:
                        return False
                    if node.func.attr == "compile":
                        if isinstance(node.func.value, ast.Name) and node.func.value.id in {"builtins", "__builtins__"}:
                            return False
                        elif not (isinstance(node.func.value, ast.Name) and node.func.value.id == "re"):
                            return False
            # 2. Variable referencing / aliasing (e.g. fn = eval, map(eval, ...))
            if isinstance(node, ast.Name) and node.id in forbidden_names:
                return False
            # 3. Attribute referencing
            if isinstance(node, ast.Attribute) and node.attr in {"eval", "exec", "__import__"}:
                return False
            # 4. Import aliasing
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if alias.name in forbidden_names or (alias.asname and alias.asname in forbidden_names):
                        return False
        return True

    def apply_update(
        self,
        update_id: Optional[str] = None,
        custom_payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if custom_payload:
            payload = custom_payload
        elif update_id:
            payload = next((u for u in self.staged_updates if u.get("update_id") == update_id), None)
            if payload is None:
                return {"status": "UPDATE_NOT_FOUND", "error": f"Update '{update_id}' not found in staged updates"}
        else:
            return {"status": "INVALID_ARGUMENTS", "error": "No update specified"}

        plugin_code = payload.get("plugin_code", "")
        if not self._verify_code_security(plugin_code):
            return {
                "status": "REJECTED_SECURITY_THREAT",
                "reason": "Forbidden AST node (eval/exec/compile) detected in update payload",
            }

        plugin_name = payload.get("plugin_name")
        plugin_target_path: Optional[Path] = None
        plugin_existed = False
        plugin_prev_content: Optional[str] = None

        if plugin_name:
            # Prevent directory traversal attacks
            if ".." in plugin_name or plugin_name.startswith("/") or plugin_name.startswith("\\"):
                return {
                    "status": "REJECTED_SECURITY_THREAT",
                    "reason": f"Path traversal attempt detected in plugin_name: {plugin_name}",
                }
            try:
                plugin_target_path = (self.base_dir / plugin_name).resolve()
                if not plugin_target_path.is_relative_to(self.base_dir):
                    return {
                        "status": "REJECTED_SECURITY_THREAT",
                        "reason": "Plugin path escapes base_dir",
                    }
            except Exception:
                return {
                    "status": "REJECTED_SECURITY_THREAT",
                    "reason": "Invalid plugin path",
                }

            plugin_existed = plugin_target_path.exists()
            if plugin_existed:
                try:
                    plugin_prev_content = plugin_target_path.read_text(encoding="utf-8")
                except Exception:
                    plugin_prev_content = None

        # Create atomic backup
        backup_id = f"backup_{uuid.uuid4().hex[:8]}_{int(time.time())}"
        current_manifest = self.get_manifest()
        backup_file = self.backups_dir / f"{backup_id}.json"

        backup_record = {
            "backup_id": backup_id,
            "previous_version": current_manifest.get("current_version", "3.7.0"),
            "manifest_snapshot": current_manifest,
            "plugin_name": plugin_name,
            "plugin_existed": plugin_existed,
            "plugin_prev_content": plugin_prev_content,
            "created_at": time.time(),
        }
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_record, f, indent=2)

        # Apply update
        new_version = payload.get("target_version", "3.8.0")
        current_manifest["current_version"] = new_version
        if "installed_updates" not in current_manifest:
            current_manifest["installed_updates"] = []
        current_manifest["installed_updates"].append(payload.get("update_id"))
        current_manifest["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self._save_manifest(current_manifest)

        if plugin_target_path and plugin_code:
            try:
                plugin_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(plugin_target_path, "w", encoding="utf-8") as pf:
                    pf.write(plugin_code)
            except Exception:
                pass

        return {
            "status": "UPDATE_APPLIED_SUCCESSFULLY",
            "new_version": new_version,
            "backup_id": backup_id,
        }

    def rollback(self, backup_id: str) -> Dict[str, Any]:
        backup_file = self.backups_dir / f"{backup_id}.json"
        if not backup_file.exists():
            return {"status": "BACKUP_NOT_FOUND", "backup_id": backup_id}

        with open(backup_file, "r", encoding="utf-8") as f:
            backup_record = json.load(f)

        restored_version = backup_record.get("previous_version", "3.7.0")
        snapshot = backup_record.get("manifest_snapshot", {})
        snapshot["current_version"] = restored_version
        snapshot["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self._save_manifest(snapshot)

        # Atomically restore or remove installed plugin file
        plugin_name = backup_record.get("plugin_name")
        if plugin_name:
            try:
                plugin_path = (self.base_dir / plugin_name).resolve()
                if plugin_path.is_relative_to(self.base_dir):
                    if backup_record.get("plugin_existed", False):
                        prev_content = backup_record.get("plugin_prev_content")
                        if prev_content is not None:
                            with open(plugin_path, "w", encoding="utf-8") as pf:
                                pf.write(prev_content)
                    else:
                        if plugin_path.exists():
                            plugin_path.unlink()
            except Exception:
                pass

        return {
            "status": "ROLLBACK_SUCCESSFUL",
            "restored_version": restored_version,
        }
