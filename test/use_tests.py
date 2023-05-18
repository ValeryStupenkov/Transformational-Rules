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

    def test_check_sample(self):
        check1 = tr.check_sample("баXан", "баклан")
        check2 = tr.check_sample("cXнY", "эквивалентный")
        self.assertTrue(check1)
        self.assertFalse(check2)



