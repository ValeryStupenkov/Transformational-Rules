import sys
sys.path.append("Code/src")

import transformational_rules as tr
import TransformationalRule as rule



#rule = rule.TransformationalRule("1", "2")
rules = tr.generate_rules("геометрия", "гомеопатия", False)
for rule in rules:
    print(rule.left, rule.right)

sample1 = {"XомеYия": {"X":"ге", "Y":"тр"}}
sample2 = {"гXмеYия": {"X":"о", "Y":"опат"}}
rules = tr.create_rules_from_samples(sample1, sample2)
for rule in rules:
    print(rule.left, rule.right)


