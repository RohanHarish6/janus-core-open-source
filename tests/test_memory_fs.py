import sys
for d in ["/working_dir/c_9ac93eb92ea76b9f", "/mnt/agentdata/tiered/c_9ac93eb92ea76b9f"]:
    if d not in sys.path: sys.path.insert(0, d)
"""
Tests for Persistent Memory Filesystem (Claude Fable 5.1 specification).
Compatible with pytest and unittest.
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from token_optimized_multiagent import PersistentMemoryFilesystem, CursorStylePatcher


class TestMemoryFilesystem(unittest.TestCase):
    def setUp(self):
        self.fs = PersistentMemoryFilesystem()

    def test_initial_seeded_files(self):
        listing = self.fs.memory_list()
        paths = [item["path"] for item in listing]
        self.assertIn("/profile.md", paths)
        self.assertIn("/preferences.md", paths)

    def test_memory_read_and_version(self):
        read_res = self.fs.memory_read("/profile.md")
        self.assertEqual(read_res["status"], "success")
        self.assertTrue(len(read_res["version"]) >= 8)
        self.assertIn("- [stated]", read_res["content"])

    def test_memory_append_and_stated_tag(self):
        read_res = self.fs.memory_read("/profile.md")
        v1 = read_res["version"]

        # Append fact without explicit tag; should auto-tag with - [stated]
        app_res = self.fs.memory_append("/profile.md", "Certified in Actuarial Risk Engineering.", if_version=v1)
        self.assertEqual(app_res["status"], "success")
        v2 = app_res["new_version"]
        self.assertNotEqual(v1, v2)

        # Verify fact was tagged
        updated_read = self.fs.memory_read("/profile.md")
        self.assertIn("- [stated] Certified in Actuarial Risk Engineering.", updated_read["content"])

    def test_concurrency_version_conflict(self):
        read_res = self.fs.memory_read("/profile.md")
        stale_version = "stale_ver_1234"

        app_res = self.fs.memory_append("/profile.md", "Concurrent update attempt", if_version=stale_version)
        self.assertEqual(app_res["status"], "version_conflict")

    def test_cursor_style_patcher(self):
        sample_doc = "header\nold_value_123\nfooter"
        success, patched, msg = CursorStylePatcher.patch(sample_doc, "old_value_123", "new_value_456")
        self.assertTrue(success)
        self.assertIn("new_value_456", patched)
        self.assertNotIn("old_value_123", patched)

        # Collision guard on duplicate occurrences
        duplicate_doc = "test_item\ntest_item\nother"
        success_dup, _, err = CursorStylePatcher.patch(duplicate_doc, "test_item", "replaced")
        self.assertFalse(success_dup)
        self.assertIn("occurs 2 times", err)


if __name__ == "__main__":
    unittest.main()
