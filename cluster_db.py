import sqlite3

new_conn = sqlite3.connect('data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def create_userdb():
    c = new_conn.cursor()
    c.execute("DROP TABLE users")
    c.execute('''CREATE TABLE users
    	(user_id text, retention real, lapses real)''')
    c.execute('SELECT user_id, SUM(ret), SUM(lapse), SUM(ct) from (select user_id, (MAX(ret_reps)-MIN(ret_reps)) as ret, (MAX(lapses)-MIN(lapses)) as lapse, COUNT(*) as ct from log GROUP BY user_id, object_id) WHERE ct > 1 GROUP BY user_id')
    r = c.fetchall()
    for row in r:
        new_row = [row[0], float(row[1])/float(row[3]), float(row[2])/float(row[3])]
        if (row[1] > 500):
            continue
        if (row[2] > 500):
            continue
        c.execute("INSERT INTO users values (?,?,?)", new_row)
    new_conn.commit()