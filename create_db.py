import sqlite3
def create_rule_base(name):
   connection = sqlite3.connect('transformrules.db')

   cursor = connection.cursor()

   cursor.execute('''CREATE TABLE IF NOT EXISTS Rules
         (RULEID INT PRIMARY KEY     NOT NULL,
         SAMPLE           TEXT    NOT NULL,
         RESULT           TEXT     NOT NULL,
         GROUPID            INT,
         PRIORITY INT,
         TIMESTAMP TIMESTAMP);''')
   connection.commit()

   cursor.execute(''' CREATE TABLE IF NOT EXISTS Groups
   ( GROUPID INT PRIMARY KEY    NOT NULL,
     NAME             TEXT      NOT NULL
   );''')
   connection.commit()

   cursor.execute("INSERT INTO Groups (GROUPID,NAME) \
      VALUES (1, 'Common')")

   cursor.execute("INSERT INTO Rules (RULEID,SAMPLE,RESULT, GROUPID, PRIORITY) \
      VALUES (1, 'Paul', 'Paulina', 1, 1)")
   connection.commit()

   cursor = cursor.execute("SELECT ruleid, sample, result, groupid from Rules")

   for row in cursor:
      print("ID = ", row[0])
      print("SAMPLE = ", row[1])
      print("RESULT = ", row[2])
      print("GroupID = ", row[3])

   cursor = cursor.execute("SELECT groupid, name from Groups")
   for row in cursor:
      print("GroupId = ", row[0])
      print("Name = ", row[1])


   connection.close()

create_rule_base("transformrules")