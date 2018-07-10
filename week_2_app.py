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

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]

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



def compute_distortion(cluster_list, data_url):

  data_table = load_data_table(data_url)
  distortion = 0

  for cluster in cluster_list:
    distortion += cluster.cluster_error(data_table)

  return distortion

def initialize_cluster_list(data_url):
  data_table = load_data_table(data_url)

  singleton_list = []
  for line in data_table:
    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

  return singleton_list

def plot_clustering_algs_distortion(data_url):

  number_clusters = []
  hierarchical_distortions = []
  k_means_distortions = []

  hierarchical_cluster_list = initialize_cluster_list(data_url)

  for cluster_number in range(20, 5, -1):
    number_clusters.append(cluster_number)
    hierarchical_cluster_list = provided.hierarchical_clustering(hierarchical_cluster_list, cluster_number)
    hierarchical_distortion = compute_distortion(hierarchical_cluster_list, data_url)
    hierarchical_distortions.append(hierarchical_distortion)

    k_means_cluster_list = initialize_cluster_list(data_url)
    k_means_cluster_list = provided.kmeans_clustering(k_means_cluster_list, cluster_number, 5)
    k_means_distortion = compute_distortion(k_means_cluster_list, data_url)
    k_means_distortions.append(k_means_distortion)

  plt.plot(number_clusters, hierarchical_distortions, '-g', label = "Hierarchical clustering distortions")
  plt.plot(number_clusters, k_means_distortions, '-b', label = "K means clustering distortions")
  plt.xlabel('Number of clusters')
  plt.ylabel('Distortion')
  plt.suptitle('Comparison of k-means and hierarchical clustering distortion measures')
  plt.legend(loc = 'upper right')
  plt.show()





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
#uncomment below to plot cp running time comparison
#plot_cp_running_times()


'''
QUESTION 2:

Use alg_project3_viz to create an image of the 15 clusters generated by applying hierarchical
clustering to the 3108 cancer risk data set. You may submit an image with the 3108 counties
colored by clusters or an enhanced visualization with the original counties colored by cluster
and linked to the center of their corresponding clusters by lines.
'''

'''
QUESTION 3:

Use alg_project3_viz to create an image of the 15 clusters generated by applying k means
clustering to the 3108 cancer risk data set using 5 iterations. You may submit an image with the 3108 counties
colored by clusters or an enhanced visualization with the original counties colored by cluster
and linked to the center of their corresponding clusters by lines.
'''

'''
QUESTION 4:
Which clustering method is faster when the number of output clusters is either a small fixed number
or a small fraction of the number of input clusters? Provide a short explanation in terms of the asymptotic 
running times of both methods. 

K-means clustering is much faster when the number of clusters is a small fraction of the number
of input clusters. The running time here should be O(k * n) where n is the cluster
list length, and which if k is much smaller than n, should reduce to O(n).
This is because for k-means clustering, as long as the number of iterations stays small, the
number of distance comparisons between clusters is much lower since the centers are predetermined. 

Hierarchical clustering, on the other hand performs fast closest pair a number of times equal to the initial 
size of the input list minus the desired number of output clusters, which results in O((n - k)n log n),
which will be considerably higher than O(n).
'''

'''
QUESTION 5:

Use alg_project3_viz to create an image of the 9 clusters generated by applying
hierarchical clustering to the 111 county cancer risk data set.
'''

'''
QUESTION 6:

Use alg_project3_viz to create an image of the 9 clusters generated by applying
5 iterations of k-means clustering to the 111 county cancer risk data set.

'''

'''
QUESTION 7:

Write a function compute_distortion(cluster_list) that takes a list of clusters and uses cluster_error
to compute its distortion. Then, use compute_distortion to compute the distortions of the two 
clusterings in questions 5 and 6.

'''

#Uncomment below to see the answer to question 7.

#initialize cluster list



#Run tests provided by instructor
#data_url = DATA_290_URL
#cluster_list = initialize_cluster_list(data_url)
#hierarchical_cluster_list = provided.hierarchical_clustering(cluster_list, 16)
#print 'error for hierarchical', compute_distortion(hierarchical_cluster_list, data_url)
#cluster_list = initialize_cluster_list(data_url)
#k_means_cluster_list = provided.kmeans_clustering(cluster_list, 16, 5)
#print 'error for k means', compute_distortion(k_means_cluster_list, data_url)

#Get values required for problem: 9 clusters for 111 county data set, 5 iterations for kmeans

#data_url = DATA_111_URL
#cluster_list = initialize_cluster_list(data_url)
#hierarchical_cluster_list = provided.hierarchical_clustering(cluster_list, 9)
#print 'error for hierarchical', compute_distortion(hierarchical_cluster_list, data_url)
#cluster_list = initialize_cluster_list(data_url)
#k_means_cluster_list = provided.kmeans_clustering(cluster_list, 9, 5)
#print 'error for k means', compute_distortion(k_means_cluster_list, data_url)

#***********ANSWER**************
#Error for hierarchical: 1.7516E11
#Error for kmeans: 2.7125E11

'''
QUESTION 8:
Examine the clusterings generated in questions 5 and 6, focusing on west coast.

Describe the difference between the shapes produced by these two methods. What caused
one method to produce a clustering with much higher distortion?

ANSWER: K-means clustering will result in a bias since clusters are initialized in the most populated
cities. Three of these cities happen to be in California and are all relatively close to each other.
Because we initialized very few clusters to distribute, many counties will end up without a cluster center
anywhere near them due to this bias, resulting in high error.

Hierarchical clustering doesn't have this bias, since with every cluster merge, all possible distances
are tested to find the closest pair, regardless of population.
'''

'''
QUESTION 9:
Based on your answer to Question 8, which method requires less human supervision to produce 
clusterings with relatively low distortion?

ANSWER: Hierarchical clustering doesn't have the population bias, so K-means clustering would require more
human supervision for the centers initialization. To prevent this bias during k-means clustering 
initialization, when counties are chosen, human supervision could be used to distribute the initialized 
clusters more evenly location-wise to mitigate the location bias resulting in high distortion.
'''

'''
QUESTION 10:
Compute the distortion of the list of clusters produced by hierarchical clustering and 
k-means clustering(using 5 itereations) on the 111, 290 and 896 county data sets where the # of output clusters
ranges from 6 to 20.

Create three plots that compare the distortion of the clusterings produced by both methods.
Each plot should include two curves drawn as line plots.
X-axis: number of output clusters
Y-axis: distortion
'''

#Uncomment below to see the plots for the 111, 290 or 896 county data sets.

#plot_clustering_algs_distortion(DATA_111_URL)
#plot_clustering_algs_distortion(DATA_290_URL)
#plot_clustering_algs_distortion(DATA_896_URL)

'''
QUESTION 11:
For each data set (111, 290, and 896 counties), does one clustering method consistently 
produce lower distortion clusterings when the number of output clusters is in the range 6 to 20? 
Is so, indicate on which data set(s) one method is superior to the other.

ANSWER: As the number of data points goes up, there is less of a difference between algorithms as far as 
cluster distortion. Given a higher number of data points, k-means may be preferable due to lower run time,
but with lower sample sizes, hierarchical distortion would be preferred preferred due to better accuracy.
For the 111 county data set, the k-means clustering produces far higher distortion 
than hierarchical clustering. For the 290 county data set this difference still exists, but is less notable.
'''

