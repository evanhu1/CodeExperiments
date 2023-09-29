# Add extra cost for turning around
# Order is a list of the indices of the requests list in the order the strategy traverses them

# Measures cost of an elevator traversal strategy
def cost(requests, times, strategy):
  # Call the provided strategy to determine the order for fulfilling the requests
  order = strategy(requests, times)

  dist_cost = distance_cost(requests, times, order)
  average_wait_cost = average_request_wait_cost(requests, times, order)

  return [dist_cost, average_wait_cost]

# Measures total distance travelled by elevator
def distance_cost(requests, times, order):
    floor_order = [requests[order[i]] for i in range(len(order))]
    return floor_order[0] + sum([abs(floor_order[i] - floor_order[i - 1]) for i in range(len(floor_order))])

# Measures the average time for a request to be fulfilled
def average_request_wait_cost(requests, times, order):
    elapsed_time = 0
    total_wait_time = 0

    for i, index in enumerate(order):
        destination_floor = requests[index]
        request_arrival_time = times[index]

        if i == 0:
          elapsed_time += (request_arrival_time + destination_floor)
        else:
          floors_difference = abs(destination_floor - requests[order[i - 1]])

          if elapsed_time >= request_arrival_time:
            elapsed_time += floors_difference
          else:
            elapsed_time += floors_difference + request_arrival_time - elapsed_time
        print(elapsed_time)
        print(elapsed_time - request_arrival_time)
        total_wait_time += elapsed_time - request_arrival_time

    return total_wait_time / len(requests)

# Offline strategies
def sort_by_time_strategy(requests, times):
    # Sort the requests based on their arrival times
    sorted_order = [i for _, __, i in sorted(zip(times, requests, range(len(times))))]
    return sorted_order

# Online strategies


# Compare costs of different strategies

requests = [4, 2, 5, 1, 3]
times = [10, 5, 8, 3, 6]

costs = cost(requests, times, sort_by_time_strategy)

print("Strategy traversal order:", sort_by_time_strategy(requests, times))
print("Total distance travelled:", costs[0])
print("Average request wait time:", costs[1])
