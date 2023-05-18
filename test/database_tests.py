import sys
import unittest
sys.path.append("Code/src")

import transformational_rules as tr
import TransformationalRule as rule

#tr.initiate_rule_base()

tr.create_rule("Paul", "Paulina")
tr.get_all_rules()

#create_rule("Paul", "Paulina")
#create_rule("Smth", "Smth2", 2, 2)
#create_rule("геометрия", "гомеопатия", 2, 1)
# TODO
class TestDatabase(unittest.TestCase):
    def __init__(self):
        tr.initiate_rule_base()

    def test_create_rule(self):
        rule = tr.create_rule("Paul", "Paulina")
        self.assertEqual("Paul", rule.left)
        self.assertEqual("Paulina", rule.right)

    def test_get_rule_by_id(self):
        rule = tr.get_rule_by_id(1)
        self.assertEqual("Paul", rule.left)
        self.assertEqual("Paulina", rule.right)




