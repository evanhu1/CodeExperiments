import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import timeit
from tqdm import tqdm
from math import log2, sqrt

def main():
  np.random.seed(1)

  def euclid(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

  def nearestSeed(x, y, points, distance):
    points_prime = [[points[i], euclid([x, y], points[i]), i] for i in range(len(points))]
    return min(points_prime, key=lambda x: x[1])[-1]
  
  def voronoiNaive(rows, columns, points):
    grid = np.zeros((rows, columns))
    
    for row in range(rows):
      for column in range(columns):
        grid[row][column] = nearestSeed(column, row, points, euclidean_distances)
    return grid
  
  def voronoiNaiveParallel(rows, columns, points, distanceFunction):
    row_indices, col_indices = np.meshgrid(np.arange(rows), np.arange(columns), indexing='ij')
    index_pairs_matrix = np.stack((row_indices, col_indices), axis=-1).reshape(-1, 2)

    distances = distanceFunction(points, index_pairs_matrix)
    minSeeds = np.argmin(distances, axis=0)
    
    return minSeeds.reshape((rows, columns)).T
  
  def visualizeGrid(grid):
    plt.close('all')
    plt.matshow(grid)
    plt.savefig("voronoi.png")

  def voronoiJumpFloodAlgorithm(rows, columns, points, distanceFunction):
    stepSize = max(rows, columns) // 2
    grid = np.zeros((rows, columns))
    seeds = []
    seedMap = {}
    seedUniqueCount = 1

    for point in points:
      grid[point[0], point[1]] = seedUniqueCount
      seedMap[seedUniqueCount] = point
      seedUniqueCount += 1
      seeds.append(point)

    largestDimension = max(rows, columns)
    stepSizes = [1] + [largestDimension // (2 ** i) for i in range(1, int(log2(largestDimension)) + 1)]

    moves = [1, -1, 0]

    for stepSize in stepSizes:
      for seed in seeds:
        x, y = seed[0], seed[1]
        p = grid[x, y]

        for i in moves:
          for j in moves:
            x_, y_ = x + stepSize*j, y + stepSize*i

            if min(x_, y_) < 0 or x_ >= columns or y_ >= rows or grid[x_, y_] == p:
              continue

            q = grid[x_,  y_]

            if q == 0:
              seeds.append([x_, y_])
              grid[x_,  y_] = p

            else:
              s = seedMap[p]
              s_ = seedMap[q]
              if distanceFunction([x_, y_], s) < distanceFunction([x_, y_], s_):
                grid[x_, y_] = p

    visualizeGrid(grid)

  def visualizeVoronoi(rows, columns, n_seed):
    points = (np.random.rand(n_seed, 2) * [rows, columns]).astype(int)
    grid = voronoiNaiveParallel(rows, columns, points, euclidean_distances)
    plt.matshow(grid)
    plt.scatter(points[:,0], points[:,1], c="black", s=4)
    plt.savefig("voronoi.png")

  def plotNComplexity():
    times = []
    n_range = range(5, 100, 5)
    rows, columns = 1024, 1024
    for n in tqdm(n_range):
      times.append(timeit.timeit(lambda: visualizeVoronoi(rows, columns, n), number=2))
    
    plt.plot(n_range, times)
    plt.show()

  def plotSizeComplexity():
    times = []
    sides = range(100, 2000, 100)
    for side in tqdm(sides):
      rows, columns = side, side
      times.append(timeit.timeit(lambda: visualizeVoronoi(rows, columns, 10), number=2))
    
    plt.plot(sides, times)
    plt.show()

  rows, columns = 1024, 1024
  points = (np.random.rand(10, 2) * [rows, columns]).astype(int)
  # print(timeit.timeit(lambda: voronoiJumpFloodAlgorithm(rows, columns, points, euclid), number=1))
  # print(timeit.timeit(lambda: voronoiJumpFloodAlgorithmParallel(rows, columns, points, euclid), number=1))
  # visualizeVoronoi(rows, columns, 10)

main()
