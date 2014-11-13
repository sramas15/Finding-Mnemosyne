import sqlite3

conn = sqlite3.connect('data/2014-01-27-mnemosynelogs-all.db')

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
    pass


