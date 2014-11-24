import sqlite3

new_conn = sqlite3.connect('data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def create_userdb():
    c = new_conn.cursor()
    c.execute("DROP TABLE users")
    c.execute('''CREATE TABLE users
    	(user_id text, retention real, lapses real, acquisition real)''')
    c.execute('SELECT user_id, SUM(ret), SUM(lapse), SUM(acq) from (select user_id, MAX(ret_reps) as ret, MAX(lapses) as lapse, MAX(acq_reps) as acq from log GROUP BY user_id, object_id) WHERE user_id in (select user_id from (select user_id, count(distinct object_id) as cnt from log group by user_id) where cnt > 200 AND cnt < 300) GROUP BY user_id')
    r = c.fetchall()
    for row in r:
        new_row = [row[0], float(row[1])/float(row[1]+row[2]+row[3]), float(row[2])/float(row[1]+row[2]+row[3]), float(row[3])/float(row[1]+row[2]+row[3])]
        if (new_row[1] > 1):
            print ":("
            continue
        if (new_row[2] > 1):
            print ":(("
            continue
        if (new_row[3] > 1):
            print ":((("
            continue
        c.execute("INSERT INTO users values (?,?,?,?)", new_row)
    new_conn.commit()

def create_userdb2():
    c = new_conn.cursor()
    c.execute("DROP TABLE users2")
    c.execute('''CREATE TABLE users2
        (user_id text, grade real, temp real)''')
    c.execute('SELECT user_id, SUM(grade) from log GROUP BY user_id')
    r = c.fetchall()
    for row in r:
        new_row = [row[0], float(row[1])/500, 0.0]
        c.execute("INSERT INTO users2 values (?,?,?)", new_row)
    new_conn.commit()
