import sys
import unittest
sys.path.append("D:\VMIK\Диплом\Transformational_rules\src")

import transformational_rules as tr
import TransformationalRule as r

#tr.initiate_rule_base()

class TestDatabase(unittest.TestCase):
    def test_create_rule(self):
        rule = tr.create_rule("Paul", "Paulina")
        self.assertEqual("Paul", rule.left)
        self.assertEqual("Paulina", rule.right)

    def test_get_rule_by_id(self):
        rule = tr.get_rule_by_id(1)
        self.assertEqual("Paul", rule.left)
        self.assertEqual("Paulina", rule.right)




