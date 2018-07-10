'''
APPLICATION 3: Efficiency of hierarchical clustering and k-means clustering
'''

import urllib2
import random
import time
import math
import matplotlib.pyplot as plt
import week_2_project as provided
import clusterclass as alg_cluster

def gen_random_clusters(num_clusters):
  cluster_list = []

  for dummy_idx in range(0, num_clusters):
    random_zip = random.randrange(10000, 99999)
    random_pop = random.randrange(0, 100000)
    random_issue = random.randrange(0, 130)
    random_x_dir = random.choice([-1, 1])
    random_y_dir = random.choice([-1, 1])
    random_x = random.random() * random_x_dir
    random_y = random.random() * random_y_dir
    new_cluster = alg_cluster.Cluster(set([random_zip]), random_x, random_y, random_pop, random_issue)
    cluster_list.append(new_cluster)

  return cluster_list

def get_slow_cp_run_time(cluster_list):
  t0 = time.time()
  provided.slow_closest_pair(cluster_list)
  t1 = time.time()
  return t1 - t0


def get_fast_cp_run_time(cluster_list):
  t0 = time.time()
  provided.fast_closest_pair(cluster_list)
  t1 = time.time()
  return t1 - t0

def plot_cp_running_times():

  number_clusters = []
  slow_run_times = []
  fast_run_times = []
  for i in range(2, 200, 1):
    number_clusters.append(i)
    test_clusters = gen_random_clusters(i)
    slow_run_times.append(get_slow_cp_run_time(test_clusters))
    fast_run_times.append(get_fast_cp_run_time(test_clusters))

  print slow_run_times
  print fast_run_times
  plt.plot(number_clusters, slow_run_times, '-r', label = "Slow closest pair run time")
  plt.plot(number_clusters, fast_run_times, '-b', label = "Fast closest pair run time")
  plt.xlabel('Number of clusters')
  plt.ylabel('Running time (seconds)')
  plt.suptitle('Comparing slow and fast closest pair run times')
  plt.legend(loc = 'upper right')
  plt.show()

plot_cp_running_times()





'''
QUESTION 1:

Write a function gen_random_clusters(num_clusters) that creates a list of 
clusters where each cluster in this list corresponds to one randomly generated point in the
square with corners (+/- 1, +/- 1). Use this function and your favorite Python timing code to
compute the running times of the functions slow_closest_pair and fast_closest_pair for lists 
of clusters of size 2 to 200

Plot the result as two curves combined into a single plot.
x-axis: number of initial clusters
y-axis: running time of function in seconds
'''

