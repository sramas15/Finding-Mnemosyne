from sklearn.svm import SVR
import numpy as np
import training_data

(x, y) = training_data.get_training_data(1000)
x_train = x[:-200]
y_train = y[:-200]
x_test = x[-200:]
y_test = y[-200:]
clf = SVR(C=3.0)
clf.fit(x_train, y_train) 

#print('Coefficients: \n', clf.coef_)

print('Variance score: %.2f' % clf.score(x_test, y_test))
print('Variance score: %.2f' % clf.score(x_train, y_train))