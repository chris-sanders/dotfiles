import importlib.machinery
import importlib.util
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

source = Path(__file__).resolve().parents[1] / "dot_local/bin/executable_go-cache-maintenance"
loader = importlib.machinery.SourceFileLoader("maintenance", str(source))
spec = importlib.util.spec_from_loader(loader.name, loader)
m = importlib.util.module_from_spec(spec)
loader.exec_module(m)

class MaintenanceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "go-build"
        self.root.mkdir()
        (self.root / "aa").mkdir()
        self.now = time.time()
    def file(self, suffix, hours):
        p = self.root / "aa" / ("aa" + suffix * 62 + "-d")
        p.write_bytes(b"x" * 4096)
        os.utime(p, (self.now - hours * m.HOUR,) * 2)
        return p
    def test_age_and_non_artifact_safety(self):
        old = self.file("b", 49)
        recent = self.file("c", 1)
        unrelated = self.root / "aa" / "keep"
        unrelated.write_text("keep")
        fuzz = self.root / "fuzz"
        fuzz.mkdir()
        (fuzz / "keep").write_text("keep")
        link = self.root / "aa" / ("aa" + "d" * 62 + "-d")
        link.symlink_to(unrelated)
        with patch.object(m, "budget", return_value=100 * m.GIB):
            m.clean(self.root, True, self.now)
            self.assertTrue(old.exists())
            m.clean(self.root, False, self.now)
        self.assertFalse(old.exists())
        self.assertTrue(recent.exists() and unrelated.exists() and link.is_symlink())
        self.assertTrue((fuzz / "keep").exists())
    def test_size_and_recent_guard(self):
        older = self.file("a", 12)
        younger = self.file("b", 8)
        recent = self.file("c", 1)
        with patch.object(m, "budget", return_value=0):
            m.clean(self.root, False, self.now)
        self.assertFalse(older.exists() or younger.exists())
        self.assertTrue(recent.exists())
    def test_pressure(self):
        old = self.file("b", 12)
        recent = self.file("c", 1)
        from types import SimpleNamespace
        fs = SimpleNamespace(f_blocks=100, f_bfree=10, f_bavail=10, f_frsize=4096)
        with patch.object(m.os, "statvfs", return_value=fs), patch.object(m, "budget", return_value=100*m.GIB):
            m.clean(self.root, False, self.now)
        self.assertFalse(old.exists())
        self.assertTrue(recent.exists())
    def test_budget(self):
        with patch.dict(os.environ, {"GO_CACHE_MAX_GIB":"100","GO_CACHE_MAX_PERCENT":"15"}):
            self.assertEqual(m.budget(200*m.GIB), 30*m.GIB)
            self.assertEqual(m.budget(1000*m.GIB), 100*m.GIB)
