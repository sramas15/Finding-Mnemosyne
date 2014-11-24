import sqlite3

conn = sqlite3.connect('data/2014-01-27-mnemosynelogs-all.db')
conn.row_factory = sqlite3.Row

CLEAN_ROW_CONDITIONS = """grade NOT NULL AND
acq_reps NOT NULL AND
ret_reps NOT NULL AND
lapses NOT NULL AND
acq_reps_since_lapse NOT NULL AND
ret_reps_since_lapse NOT NULL AND
actual_interval NOT NULL""";

new_conn = sqlite3.connect('data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def create_newdb(limit=850):
    c = conn.cursor()
    c.execute('SELECT DISTINCT user_id FROM log WHERE %s LIMIT %s' % (CLEAN_ROW_CONDITIONS, limit))
    users = [row[0] for row in c.fetchall()]
    num_users = 0
    new_c = new_conn.cursor()
    new_c.execute("DROP TABLE log")
    new_c.execute('''CREATE TABLE log
    	(user_id text, event integer, timestamp integer, object_id text,
    		grade integer, easiness real, acq_reps integer, ret_reps integer,
    		lapses integer, acq_reps_since_lapse integer, ret_reps_since_lapse integer,
    		scheduled_interval integer, actual_interval integer, thinking_time integer,
    		next_rep integer)''')
    for u in users:
        c.execute('SELECT * FROM log WHERE user_id = "%s" AND event = 9 ORDER BY timestamp ASC LIMIT 500'
                % u)
        r = c.fetchall()
        if len(r) < 500:
            continue
        new_c.executemany("INSERT INTO log values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", r)
        num_users += 1
        if num_users == 500:
        	break
    new_conn.commit()
    print "Num greater than 500 %d" % num_users
    return users