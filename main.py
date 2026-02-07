from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(decisions)")
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()

