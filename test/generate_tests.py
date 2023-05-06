import sys
import unittest
sys.path.append("D:\VMIK\Диплом\Transformational_rules\src")
import transformational_rules as tr
import TransformationalRule as r

class TestGenerateRules(unittest.TestCase):

    def test_generate_rules_without_blanks(self):
        rules = tr.generate_rules("геометрия", "гомеопатия", False)
        self.assertEqual(rules[0].left, "XеоYтрZ")
        self.assertEqual(rules[0].right, "XоYопатZ")
        self.assertEqual(rules[1].left, "геXтрY")
        self.assertEqual(rules[1].right, "гXопатY")

    def test_generate_rules_with_blanks(self):
        rules = tr.generate_rules("геометрия", "гомеопатия", True)
        self.assertEqual(rules[0].left, "XеYZрA")
        self.assertEqual(rules[0].right, "XYопаZA")

    def test_create_rules_from_samples(self):
        sample1 = {"гXмеYия": {'X': 'ео', 'Y': 'тр'}}
        sample2 = {"XомеYия": {'X': 'г', 'Y': 'опат'}}
        rules = tr.create_rules_from_samples(sample1, sample2)
        self.assertEqual(rules[0].left, "геоXтрY")
        self.assertEqual(rules[0].right, "гоXопатY")


