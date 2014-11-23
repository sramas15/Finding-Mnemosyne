import sqlite3
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

new_conn = sqlite3.connect('data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def run_kmeans(num_means=8):
	c = new_conn.cursor()
	c.execute("SELECT retention, lapses from users")
	arr = np.array(c.fetchall())
	estimator = KMeans(n_clusters=num_means)
	estimator.fit(arr)
	print "======================================="
	print "1. kmeans together"
	print estimator.cluster_centers_
	print estimator.labels_
	print estimator.inertia_
	plt.plot(arr[:, 0], arr[:, 1], 'k.', markersize=2)
	plt.show()

	print "======================================="
	print "2. kmeans retention rate"
	c.execute("SELECT retention, lapses-lapses from users")
	arr = np.array(c.fetchall())
	estimator.fit(arr)
	print estimator.cluster_centers_
	print estimator.labels_
	print estimator.inertia_
	plt.hist(arr[:,0], bins=30)
	plt.show()

	print "======================================="
	print "3. kmeans lapse rate"
	c.execute("SELECT retention-retention, lapses from users")
	arr = np.array(c.fetchall())
	estimator.fit(arr)
	print estimator.cluster_centers_
	print estimator.labels_
	print estimator.inertia_
	plt.hist(arr[:,1], bins=30)
	plt.show()


