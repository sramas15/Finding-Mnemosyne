import sqlite3

new_conn = sqlite3.connect('../data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def find_rep_user():
	c = new_conn.cursor()
	u_set = None
	for grade in range(6):
		for next_grade in range(6):
			c.execute("select distinct user_id from regression_log where grade=%d AND pred_grade=%d" % (grade, next_grade))
			users = [row[0] for row in c.fetchall()]
			if u_set is None:
				u_set = set(users)
			else:
				u_set.intersection_update(set(users))
	for u in u_set:
		c.execute('select grade, COUNT(*) from regression_log where user_id="%s" group by grade;' % u)
		freq = c.fetchall()
		print "%s 0:%d, 1:%d, 2:%d, 3:%d, 4:%d, 5:%d" % (u, freq[0][1], freq[1][1], freq[2][1], freq[3][1], freq[4][1], freq[5][1])
		c.execute('select interval, COUNT(*) from discrete_log where user_id="%s" group by interval;' % u)
		f = c.fetchall()
		print f
	return u_set