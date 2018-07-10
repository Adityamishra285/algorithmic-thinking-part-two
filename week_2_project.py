'''ALGORITHMIC THINKING Class 2 Week 2'''

import math
import random
import clusterclass as alg_cluster

def slow_closest_pair(cluster_list):
  '''Given a list of Cluster objects, return a closest pair where the pair is 
  represented by the tuple (dist, idx1, idx2)'''
  output_tuple = (float('inf'), -1, -1)
  min_distance = float('inf')
  for idx in range(0, len(cluster_list) - 1):
    for jdx in range(idx + 1, len(cluster_list)):
      cluster_one = cluster_list[idx]
      cluster_two = cluster_list[jdx]
      if cluster_one.distance(cluster_two) < min_distance:
        min_distance = cluster_one.distance(cluster_two)
        output_tuple = (min_distance, idx, jdx)

  return output_tuple

def closest_pair_strip(cluster_list, horiz_center, half_width):
  '''Given a list of Cluster objects and two floats: horiz_center and half_width
  (Half_width = max distance of any pt in the strip from the center line),
  return the closest pair of pts that are in that strip.'''

  within_strip_indices = []
  for idx in range(0, len(cluster_list)):
    cluster = cluster_list[idx]
    if abs(cluster.horiz_center() - horiz_center) < half_width:
      within_strip_indices.append(idx)
  
  within_strip_indices.sort(key = lambda index: cluster_list[index].vert_center())
  number_points_within_strip = len(within_strip_indices)
  output_tuple = (float('inf'), -1, -1)
  min_distance = float('inf')


  #ALL BUT THE LAST ONE IS WHERE THE -2 COMES FROM
  for idx in range(0, number_points_within_strip - 1):
    for jdx in range(idx + 1, min(idx + 4, number_points_within_strip)):
      original_idx_one = within_strip_indices[idx]
      original_idx_two = within_strip_indices[jdx]
      cluster_one = cluster_list[original_idx_one]
      cluster_two = cluster_list[original_idx_two]
      if cluster_one.distance(cluster_two) < min_distance:
        min_distance = cluster_one.distance(cluster_two)
        if original_idx_one < original_idx_two:
          output_tuple = (min_distance, original_idx_one, original_idx_two)
        else:
          output_tuple = (min_distance, original_idx_two, original_idx_one)
        

  return output_tuple

def fast_closest_pair(cluster_list):
  '''Fast version of slow_closest_pair'''

  number_clusters = len(cluster_list)

  if number_clusters < 3:
    output_tuple = slow_closest_pair(cluster_list)
  else:
    midpoint = int(math.ceil(number_clusters / 2))
    left_portion = cluster_list[0:midpoint]
    right_portion = cluster_list[midpoint:number_clusters]
    left_min = fast_closest_pair(left_portion)
    right_min = fast_closest_pair(right_portion)
    if left_min[0] <= right_min[0]:
      output_tuple = left_min
    else:
      output_tuple = (right_min[0], right_min[1] + midpoint, right_min[2] + midpoint)
    cutoff_x = (cluster_list[midpoint - 1].horiz_center() + cluster_list[midpoint].horiz_center()) / 2
    closest_pair_strip_result = closest_pair_strip(cluster_list, cutoff_x, output_tuple[0])
    if closest_pair_strip_result[0] < output_tuple[0]:
      output_tuple = closest_pair_strip_result

  return output_tuple

def hierarchical_clustering(cluster_list, num_clusters):

  '''Given a list of cluster objects and number of clusters, cluster some clusters together until you have num_clusters clusters'''

  cluster_list.sort(key = lambda cluster: cluster.horiz_center())
  while len(cluster_list) > num_clusters:

    fast_closest_pair_info = fast_closest_pair(cluster_list)
    cluster_one_index = fast_closest_pair_info[1]
    cluster_two_index = fast_closest_pair_info[2]
    cluster_one = cluster_list[cluster_one_index]
    cluster_two = cluster_list[cluster_two_index]
    cluster_one.merge_clusters(cluster_two)
    cluster_list[cluster_one_index] = cluster_one
    cluster_list.pop(cluster_two_index)

  return cluster_list

def get_nearest_center_index(cluster, center_positions):
  '''Given a cluster and a list of center positions, return the index corresponding to the nearest center position to that cluster'''
  min_distance = float('inf')
  nearest_center_index = 0
  current_index = 0

  for center_position in center_positions:
    horiz_dist = cluster.horiz_center() - center_position[0]
    vert_dist = cluster.vert_center() - center_position[1]  
    distance = math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
    if distance < min_distance:
      min_distance = distance
      nearest_center_index = current_index
    current_index += 1

  return nearest_center_index

def kmeans_clustering(cluster_list, num_clusters, num_iterations):

  '''Given a list of cluster objects, number of iterations, and number of clusters required, create a new list of clusters using
  k-means clustering'''
  cluster_list_copy = []
  for cluster in cluster_list:
    cluster_list_copy.append(cluster.copy())

  #sort the current cluster list by population
  cluster_list_copy.sort(key = lambda cluster: cluster.total_population(), reverse=True)
  #create an initial list of clusters where we initialize a group of clusters equal to num_clusters, taking the first of the sorted cluster list
  center_positions = []
  for idx in range(0, num_clusters):
    current_cluster = cluster_list_copy[idx]
    center_positions.append((current_cluster.horiz_center(), current_cluster.vert_center()))
  #map the center positions so that they are not modified.

  #for each iteration:
  for dummy_jdx in range(0, num_iterations):
    #Make num_clusters empty clusters(same length as the population list we made)
    center_clusters = []
    for kdx in range(0, len(center_positions)):
      position = center_positions[kdx]
      center_clusters.append(alg_cluster.Cluster(set([]), position[0], position[1], 0, 0))
      #these clusters should have no counties and no total population
    for cluster in cluster_list_copy:
      nearest_center_index = get_nearest_center_index(cluster, center_positions)
      nearest_cluster = center_clusters[nearest_center_index]
      nearest_cluster.merge_clusters(cluster)
    #for each element in the cluster list, find the right cluster to merge it with.
    #once you find it, merge clusters(update the current cluster list)
    for kdx in range(0, len(center_clusters)):
      current_center_cluster = center_clusters[kdx]
      center_positions[kdx] = (current_center_cluster.horiz_center(), current_center_cluster.vert_center())

    #replace each center position with the new center position.
  return center_clusters
  #return the final cluster list





#print fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 0, 1, 1, 0), alg_cluster.Cluster(set([]), 0, 2, 1, 0)])
#print closest_pair_strip([alg_cluster.Cluster(set([]), 1.0, 1.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 5.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 4.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 7.0, 1, 0)], 1.0, 3.0)
