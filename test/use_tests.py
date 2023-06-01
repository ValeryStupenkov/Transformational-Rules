import unittest
import sys
sys.path.append("D:\VMIK\Диплом\Transformational_rules\src")

import transformational_rules as tr
import TransformationalRule as r

class TestUseRules(unittest.TestCase):
    def test_use_rule(self):
        rule = r.TransformationalRule("XеоYтрZ", "XоYопатZ")
        result = tr.use_rule("геометрия", rule)
        self.assertEqual(result, "гомеопатия")

    def test_check_sample(self):
        check1 = tr.check_sample("баXан", "баклан")
        check2 = tr.check_sample("cXнY", "эквивалентный")
        self.assertTrue(check1)
        self.assertFalse(check2)



