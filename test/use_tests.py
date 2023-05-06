import unittest
import sys
sys.path.append("Code/src")

import transformational_rules as tr
import TransformationalRule as rule

class TestUseRules(unittest.TestCase):
    def test_use_rule(self):
        rule = rule.TransformationalRule("XеоYтрZ", "XоYопатZ")
        result = tr.use_rule("геометрия", rule)
        self.assertEqual(result, "гомеопатия")


