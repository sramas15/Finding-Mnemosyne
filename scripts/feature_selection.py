import numpy as np
from sklearn import linear_model
import training_data
from sklearn.feature_selection import RFE

def scorer(reg, X, y):
    return reg.score(X, y)

(x_train, y_train) = training_data.get_training_data(1000)
regr = linear_model.LinearRegression()
rfecv = RFE(estimator=regr)
rfecv.fit(x_train, y_train)
print("Optimal number of features : %d" % rfecv.n_features_)
print("Ranking: ", rfecv.ranking_)