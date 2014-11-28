import sqlite3
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

new_conn = sqlite3.connect('data/filtered_logs.db')
new_conn.row_factory = sqlite3.Row

def run_kmeans(num_means=5):
	c = new_conn.cursor()
	c.execute("SELECT user_id from users")
	arr = c.fetchall()
	print arr
	c.execute("SELECT acquisition, lapses from users")
	arr = np.array(c.fetchall())
	estimator = KMeans(n_clusters=num_means)
	estimator.fit(arr)
	print "======================================="
	print "1. kmeans together"
	print estimator.cluster_centers_
	print estimator.labels_
	print estimator.inertia_
	print len(estimator.labels_)
	plt.plot(arr[:, 0], arr[:, 1], 'k.', markersize=2)
	plt.xlabel('acquisition rate')
	plt.ylabel('lapse rate')
	centroids = estimator.cluster_centers_
	plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3, zorder=10)
	plt.show()

	print "======================================="
	print "2. kmeans acquisition rate"
	c.execute("SELECT acquisition, lapses-lapses from users")
	arr = np.array(c.fetchall())
	estimator.fit(arr)
	print estimator.cluster_centers_
	print estimator.labels_
	print estimator.inertia_
	plt.hist(arr[:,0], bins=30)
	plt.xlabel('acquisition rate')
	plt.ylabel('frequency')
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
	plt.xlabel('lapse rate')
	plt.ylabel('frequency')
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
	plt.xlabel('retention rate')
	plt.ylabel('frequency')
	plt.show()

def run_kmeans2(num_means=8):
	c = new_conn.cursor()
	c.execute("SELECT grade, temp from users2")
	arr = np.array(c.fetchall())
	estimator = KMeans(n_clusters=num_means)
	estimator.fit(arr)
	print "======================================="
	print "1. kmeans average grade"
	print estimator.cluster_centers_
	print estimator.labels_
	print estimator.inertia_
	plt.plot(arr[:, 0], arr[:, 1], 'k.', markersize=2)
	plt.show()
	plt.hist(arr[:,0], bins=30)
	plt.show()


