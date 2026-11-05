import os
import tempfile
import unittest
from unittest.mock import patch
from access_control import authorized, reserve_quota

class SecurityTests(unittest.TestCase):
    def test_auth_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(authorized(None))
        with patch.dict(os.environ, {"GENERATOR_ACCESS_TOKEN": "x" * 32}):
            self.assertFalse(authorized("Bearer wrong"))
            self.assertTrue(authorized("Bearer " + "x" * 32))
            self.assertFalse(authorized("Bearer Я"))
    def test_persistent_limits(self):
        with tempfile.TemporaryDirectory() as d:
            p = d + "/quota.db"
            for _ in range(5):
                self.assertTrue(reserve_quota(p, 100))
            self.assertFalse(reserve_quota(p, 100))
            self.assertTrue(reserve_quota(p, 161))
    def test_daily_limit(self):
        with tempfile.TemporaryDirectory() as d:
            p = d + "/quota.db"
            for n in range(100):
                self.assertTrue(reserve_quota(p, n * 61))
            self.assertFalse(reserve_quota(p, 7000))
            self.assertTrue(reserve_quota(p, 86401))
