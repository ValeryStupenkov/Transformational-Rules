import sys
sys.path.append("D:\VMIK\Диплом\Transformational_rules\src")

import transformational_rules as tr
import TransformationalRule as r



#rule = rule.TransformationalRule("1", "2")
rules = tr.generate_rules("acgtacgtacgt", "agtacctaccgt", False)
for rule in rules:
    print(rule.left, rule.right)

sample1 = {"сXстематY ": {'X': 'cg', 'Y': 'g', 'Z': 'g'}}
sample2 = {"систXматY ": {'X': 'a', 'Y': 'c', 'Z': 'cg'}}
rules = tr.create_rules_from_samples(sample1, sample2)
for rule in rules:
    print(rule.left, rule.right)

#rule = r.TransformationalRule("разXо", "разXи")
#print(tr.use_rule("развезло", rule))


