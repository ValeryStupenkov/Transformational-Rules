import sys
import sqlite3
import pandas as pd
sys.path.append("Code/src")

import transformational_rules as tr

tr.initiate_rule_base()

db = sqlite3.connect('transformrules.db')
table = pd.read_sql_query("SELECT * from Rules", db)
table.to_csv('Rules' + '.csv', index_label='index')

tr.create_rule("Paul", "Paulina")
tr.get_all_rules()


