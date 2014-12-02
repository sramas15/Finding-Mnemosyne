import sqlite3
import numpy as np
from sklearn.svm import SVC

new_conn = sqlite3.connect('../data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def find_rep_users():
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
		c.execute('select interval_bucket, COUNT(*) from discrete_log where user_id="%s" group by interval_bucket;' % u)
		f = c.fetchall()
		print f
	return u_set

def test_potential_users():
	users = ("c6961489", "c347533d", "c6a60c92", "c5yziX7H0Tb0TitCyZKRSg")
	for user in users:
		print "*****%s*******"%user
		condition_on_grades(user)


#c6961489, c347533d, c6a60c92, c5yziX7H0Tb0TitCyZKRSg
def condition_on_grades(user="c6961489"):
	c = new_conn.cursor()
	models = [None, None, None, None, None, None]
	for i in range(6):
		c.execute('SELECT easiness, ret_reps, ret_reps_since_lapse, lapses, pred_grade, acq_reps from discrete_log where user_id="%s" and grade=%d' % (user, i))
		x_train = np.array(c.fetchall())
		c.execute('SELECT interval_bucket from discrete_log where user_id="%s" and grade=%d' % (user, i))
		y_train = np.array(c.fetchall())[:,0]
		clf = SVC()
		clf.fit(x_train, y_train)
		print clf.score(x_train, y_train)
		models[i] = clf
	print "====================="
	c.execute('SELECT user_id from (select user_id, count(distinct grade) as cnt from discrete_log group by user_id) where cnt = 6 limit 5')
	users = [row[0] for row in c.fetchall()]
	scores = [0, 0, 0, 0, 0, 0]
	for user in users:
		for i in range(6):
			c.execute('SELECT easiness, ret_reps, ret_reps_since_lapse, lapses, pred_grade, acq_reps from discrete_log where user_id="%s" and grade=%d' % (user, i))
			x_train = np.array(c.fetchall())
			c.execute('SELECT interval_bucket from discrete_log where user_id="%s" and grade=%d' % (user, i))
			y_train = np.array(c.fetchall())[:,0]
			scores[i] += models[i].score(x_train, y_train)
	for i in range(6):
		scores[i] /= len(users);
		print scores[i]

