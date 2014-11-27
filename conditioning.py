import sqlite3
import numpy as np
import random
from sklearn import linear_model

conn = sqlite3.connect('data/filtered_logs.db')
conn.row_factory = sqlite3.Row

ACQ_LAPSE_GROUP = [1, 1, 2, 4, 2, 2, 2, 2, 1, 3, 2, 4, 0, 2, 2, 4, 1, 4, 1, 0, 2, 2, 2, 4, 1, 1, 2, 4, 0, 2, 2, 2, 2, 4, 4, 3, 0,
 1, 2, 0, 1, 4, 1, 4, 4, 4, 2, 4, 4, 1, 0, 2, 0, 2, 2, 1, 4, 2, 2, 1, 2, 2, 2, 0, 4, 2, 2, 4, 2, 2, 0, 4, 0, 4,
 4, 1, 3, 1, 0, 2, 3, 0, 4, 0, 4, 1, 1, 2, 4, 4, 2, 4, 2, 2, 2, 0, 0, 0, 0, 2, 1, 2, 3, 1, 1, 2, 2, 0, 0, 0, 2,
 0, 4, 1, 0, 1, 3, 0, 2, 2, 3, 0, 0, 4, 0, 4, 2, 3, 0, 2, 2, 2]

ACQ_GROUP = [4, 4, 1, 0, 4, 1, 1, 1, 4, 3, 1, 0, 2, 1, 1, 0, 4, 0, 4, 2, 4, 1, 1, 0, 4, 4, 1, 0, 2, 1, 1, 1, 1, 0, 0, 3, 2,
 4, 1, 2, 4, 0, 4, 0, 0, 0, 1, 0, 0, 4, 2, 1, 2, 1, 1, 1, 0, 1, 1, 4, 1, 1, 1, 2, 0, 1, 1, 0, 1, 1, 2, 0, 2, 0,
 0, 4, 3, 4, 2, 1, 3, 2, 0, 2, 0, 4, 4, 1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 1, 4, 1, 3, 4, 4, 1, 1, 2, 2, 2, 1,
 2, 0, 4, 2, 4, 3, 2, 1, 1, 3, 2, 2, 0, 2, 0, 1, 3, 2, 1, 1, 1]

LAPSE_GROUP = [0, 0, 4, 4, 3, 2, 1, 1, 0, 2, 3, 3, 1, 2, 4, 3, 0, 4, 2, 2, 1, 0, 4, 2, 0, 4, 3, 1, 1, 3, 3, 4, 0, 1, 2, 2, 2,
 0, 1, 0, 0, 1, 0, 3, 4, 4, 0, 1, 3, 0, 1, 4, 4, 1, 2, 2, 2, 1, 3, 2, 1, 2, 1, 4, 1, 3, 2, 1, 0, 4, 4, 1, 4, 2,
 4, 0, 0, 0, 2, 2, 0, 2, 1, 1, 4, 0, 0, 4, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 4, 2, 1, 0, 0, 0, 4, 2, 1, 0, 1, 4,
 4, 0, 0, 2, 0, 0, 2, 4, 2, 0, 4, 1, 4, 1, 3, 2, 0, 2, 1, 2, 4]

RET_GROUP = [4, 4, 0, 2, 0, 2, 2, 2, 4, 3, 2, 1, 1, 0, 0, 1, 4, 1, 4, 3, 0, 0, 0, 2, 4, 0, 2, 1, 3, 2, 2, 0, 0, 2, 2, 3, 1,
 4, 2, 1, 4, 2, 4, 1, 1, 2, 0, 2, 1, 4, 3, 0, 3, 2, 0, 0, 2, 0, 2, 4, 2, 0, 0, 1, 1, 2, 0, 1, 0, 2, 1, 2, 3, 2,
 1, 4, 3, 4, 3, 0, 3, 1, 2, 1, 2, 4, 4, 0, 2, 1, 2, 1, 0, 2, 0, 1, 1, 3, 1, 0, 4, 2, 3, 4, 4, 0, 0, 1, 1, 1, 0,
 3, 2, 4, 1, 4, 3, 1, 0, 0, 3, 1, 3, 2, 3, 1, 0, 3, 1, 0, 0, 0]

NUM_GROUPS = 5

def run_conditioning(grouping, num_runs):
	groups = []
	for i in range(NUM_GROUPS):
		groups.append([])
	c = conn.cursor()
	c.execute("SELECT user_id from users")
	arr = c.fetchall()
	for i in range(len(grouping)):
		groups[grouping[i]].append(arr[i])
	for r in range(num_runs):
		for i in range(NUM_GROUPS):
			print "GROUP %d" % i
			[train_ind, test_ind] = random.sample(range(len(groups[i])), 2)
			u1 = groups[i][train_ind][0]
			u2 = groups[i][test_ind][0]
			c.execute('SELECT grade, easiness, ret_reps, ret_reps_since_lapse, lapses, pred_grade from regression_log where user_id="%s"' % u1)
			x_train = np.array(c.fetchall())
			#print len(x_train)
			c.execute('SELECT grade, easiness, ret_reps, ret_reps_since_lapse, lapses, pred_grade from regression_log where user_id="%s"' % u2)
			x_test = np.array(c.fetchall())
			#print len(x_test)
			c.execute('SELECT interval from regression_log where user_id="%s"' % u1)
			y_train = np.array(c.fetchall())
			c.execute('SELECT interval from regression_log where user_id="%s"' % u2)
			y_test = np.array(c.fetchall())
			regr = linear_model.LinearRegression()
			regr.fit(x_train, y_train)
			#print regr.coef_
			#print("Residual sum of squares: %.2f"
			#	% np.mean((regr.predict(x_test) - y_test) ** 2))
			print('Variance score: %.2f' % regr.score(x_test, y_test))
			#print('Variance score: %.2f' % regr.score(x_train, y_train))


