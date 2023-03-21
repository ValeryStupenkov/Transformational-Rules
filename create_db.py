import sqlite3

connection = sqlite3.connect('transformrules.db')

cursor = connection.cursor()

cursor.execute('''CREATE TABLE Rules
         (ID INT PRIMARY KEY     NOT NULL,
         SAMPLE           TEXT    NOT NULL,
         RESULT           TEXT     NOT NULL);''')
connection.commit()

cursor.execute("INSERT INTO Rules (ID,SAMPLE,RESULT) \
      VALUES (1, 'Paul', 'Paulina')")
connection.commit()

cursor = cursor.execute("SELECT id, sample, result from Rules")

for row in cursor:
   print("ID = ", row[0])
   print("SAMPLE = ", row[1])
   print("RESULT = ", row[2])


connection.close()