import sqlite3

new_conn = sqlite3.connect('data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def create_userdb():
    """Compute retention, lapse, and acquisition rate for each user and
    load the values into a new 'users' table.
    """
    c = new_conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute('''CREATE TABLE users
    	(user_id text, retention real, lapses real, acquisition real)''')
    c.execute('''SELECT user_id, SUM(ret), SUM(lapse), SUM(acq)
                FROM
                    (SELECT user_id, MAX(ret_reps) AS ret, MAX(lapses) AS lapse, MAX(acq_reps) AS acq
                    FROM log
                    GROUP BY user_id, object_id)
                WHERE user_id IN
                    (SELECT user_id
                    FROM
                        (SELECT user_id, COUNT(DISTINCT object_id) AS cnt
                        FROM log
                        GROUP BY user_id)
                    WHERE cnt < 250)
                GROUP BY user_id''')
    rows = c.fetchall()
    for row in rows:
        c.execute('SELECT COUNT(DISTINCT object_id) FROM log WHERE user_id="%s"' % row[0])
        #dist_cards = c.fetchone()[0]
        new_row = [row[0],
                float(row[1]) / float(row[1]+row[2]+row[3]),
                float(row[2]) / float(row[1]+row[2]+row[3]),
                float(row[3]) / float(row[1]+row[2]+row[3])]
        #if (new_row[1] > 1):
        #    print ":("
        #    continue
        #if (new_row[2] > 1):
        #    print ":(("
        #    continue
        #if (new_row[3] > 1):
        #    print ":((("
        #    continue
        c.execute("INSERT INTO users VALUES (?,?,?,?)", new_row)
    new_conn.commit()

def create_userdb2():
    "obsolete"
    c = new_conn.cursor()
    c.execute("DROP TABLE IF EXISTS users2")
    c.execute('''CREATE TABLE users2
        (user_id text, grade real, temp real)''')
    c.execute('SELECT user_id, SUM(grade) from log GROUP BY user_id')
    r = c.fetchall()
    for row in r:
        new_row = [row[0], float(row[1])/500, 0.0]
        c.execute("INSERT INTO users2 values (?,?,?)", new_row)
    new_conn.commit()

if __name__ == '__main__':
    create_userdb()
    create_userdb2()
