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

def list_user_ids(limit=100):
    c = conn.cursor()
    c.execute('SELECT DISTINCT user_id FROM log WHERE %s LIMIT %s' % (CLEAN_ROW_CONDITIONS, limit))
    return [row[0] for row in c.fetchall()]

def fetch_logs(user_id):
    c = conn.cursor()
    c.execute('SELECT DISTINCT object_id FROM log WHERE user_id = "%s" AND %s' % (user_id, CLEAN_ROW_CONDITIONS))
    object_ids = [row[0] for row in c.fetchall()]

    logs = []
    for object_id in object_ids:
        c.execute('SELECT * FROM log WHERE user_id = "%s" AND object_id = "%s" AND %s ORDER BY timestamp'
                % (user_id, object_id, CLEAN_ROW_CONDITIONS))
        logs.append(c.fetchall())

    return logs




