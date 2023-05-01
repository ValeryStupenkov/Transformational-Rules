import sys
import sqlite3
import pandas as pd
sys.path.append("Code/src")

import transformational_rules as tr
import TransformationalRule as rule

#tr.initiate_rule_base()

tr.create_rule("Paul", "Paulina")
tr.get_all_rules()

#create_rule("Paul", "Paulina")
#create_rule("Smth", "Smth2", 2, 2)
#create_rule("геометрия", "гомеопатия", 2, 1)


