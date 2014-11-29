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

USER_ID = 0
EVENT = 1
TIMESTAMP = 2
OBJECT_ID = 3
GRADE = 4
EASINESS = 5
ACQ_REPS = 6
RET_REPS = 7
LAPSES = 8
ACQ_REPS_SL = 9
RET_REPS_SL = 10
SCHEDULED_INTERVAL = 11
ACTUAL_INTERVAL = 12
THINKING_TIME = 13
NEXT_REP = 14

def create_newdb(limit=1300):
    """
    Creates smaller database
    """
    c = conn.cursor()
    c.execute('SELECT DISTINCT user_id FROM log WHERE %s LIMIT %s' % (CLEAN_ROW_CONDITIONS, limit))
    users = [row[0] for row in c.fetchall()]
    num_users = 0
    new_c = new_conn.cursor()
    new_c.execute("DROP TABLE IF EXISTS log")
    new_c.execute('''CREATE TABLE log
        (user_id text, event integer, timestamp integer, object_id text,
            grade integer, easiness real, acq_reps integer, ret_reps integer,
            lapses integer, acq_reps_since_lapse integer, ret_reps_since_lapse integer,
            scheduled_interval integer, actual_interval integer, thinking_time integer,
            next_rep integer)''')
    for u in users:
        c.execute('SELECT * FROM log WHERE user_id = "%s" AND event = 9 ORDER BY timestamp ASC LIMIT 1000'
                % u)
        r = c.fetchall()
        if len(r) < 1000:
            continue
        new_c.executemany("INSERT INTO log values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", r)
        num_users += 1
        if num_users == 500:
            break
    new_conn.commit()
    print "Num greater than 500 %d" % num_users
    return users

def create_regressiondb():
    """Combines two rows at a time"""
    c = new_conn.cursor()
    c.execute('SELECT * FROM log ORDER BY user_id, object_id, timestamp')
    row = None
    prev_row = c.fetchone()
    rows = []
    while True:
        row = c.fetchone()
        if row == None:
            break
        if (prev_row[USER_ID] == row[USER_ID] and prev_row[OBJECT_ID] == row[OBJECT_ID]):
            rows.append([row[USER_ID], row[OBJECT_ID], prev_row[GRADE], prev_row[EASINESS], prev_row[RET_REPS], prev_row[RET_REPS_SL], prev_row[LAPSES], row[GRADE], row[TIMESTAMP]-prev_row[TIMESTAMP]])
        prev_row = row
    c.execute("DROP TABLE IF EXISTS regression_log")
    c.execute('''CREATE TABLE regression_log
        (user_id text, object_id test, grade integer, easiness real, ret_reps integer,
         ret_reps_since_lapse integer, lapses integer, pred_grade integer,
         interval integer)''')
    c.executemany("INSERT INTO regression_log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
    new_conn.commit()
    print len(rows)

def create_discretizeddb():
    """Goes through regression db and discretizes intervals """
    c = new_conn.cursor()
    c.execute('SELECT * FROM log ORDER BY user_id, object_id, timestamp')
    c.execute("DROP TABLE IF EXISTS discrete_log")
    c.execute('''CREATE TABLE discrete_log
        (user_id text, object_id test, grade integer, easiness real, ret_reps integer,
         ret_reps_since_lapse integer, lapses integer, pred_grade integer,
         interval integer)''')
    c.execute('SELECT * from regression_log')
    row = None
    rows = []
    while True:
        row = c.fetchone()
        if row == None:
            break
        interval = getInterval(row[8])
        rows.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], interval])
    c.executemany("INSERT INTO discrete_log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
    new_conn.commit()

def getInterval(interval):
    if interval < 60*60:
        return 0
    if interval < 60*60*4:
        return 1
    if interval < 60*60*12:
        return 2
    if interval < 60*60*24:
        return 3
    if interval < 60*60*24*2:
        return 4
    if interval < 60*60*24*4:
        return 5
    if interval < 60*60*24*8:
        return 6
    if interval < 60*60*24*16:
        return 7
    if interval < 60*60*24*64:
        return 8
    return 9


if __name__ == '__main__':
    create_newdb()
    create_regressiondb()


