"""
linear_regression.py

Run linear regression to learn a linear function from
features on a pair of consecutive repetitions to the
interval of time between the repetitions.

Sheila Ramaswamy <s.ramaswamy92@gmail.com>
"""
import numpy as np
from sklearn import linear_model
import training_data

(x, y) = training_data.get_training_data(1000)
x_train = x[:-200]
y_train = y[:-200]
x_test = x[-200:]
y_test = y[-200:]


regr = linear_model.LinearRegression()
regr.fit(x_train, y_train)

print 'Coefficients:'
print regr.coef_
print "Residual sum of squares: %.2f" % np.mean((regr.predict(x_test) - y_test) ** 2)
print 'Variance score: %.2f' % regr.score(x_test, y_test)
print 'Variance score: %.2f' % regr.score(x_train, y_train)
