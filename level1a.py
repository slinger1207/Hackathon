import json

def calculate_total_distance(path, distances):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distances[path[i]][path[i + 1]]
    return total_distance

def tsp_with_constraints(distances, order_quantities, capacity):
    num_nodes = len(distances)
    nodes = list(range(num_nodes))

    # Create a memoization table for dynamic programming
    memo = {}

    def dp_mask(mask, pos, remaining_capacity):
        if mask == (1 << num_nodes) - 1:
            # All nodes visited, return the distance to the starting node
            return distances[pos][0]

        key = (mask, pos, remaining_capacity)
        if key in memo:
            return memo[key]

        min_distance = float('inf')

        for next_node in range(num_nodes):
            if (mask >> next_node) & 1 == 0:
                # Next node is not visited yet
                new_mask = mask | (1 << next_node)
                new_capacity = remaining_capacity - order_quantities[next_node]
                
                if new_capacity >= 0:
                    # Check the distance with the next node
                    distance = distances[pos][next_node] + dp_mask(new_mask, next_node, new_capacity)
                    min_distance = min(min_distance, distance)

        memo[key] = min_distance
        return min_distance

    # Initialize with the starting node and full capacity
    return dp_mask(1, 0, capacity)

def generate_paths(data):
    vehicles = data["vehicles"]
    neighborhoods = data["neighbourhoods"]
    restaurants = data["restaurants"]

    paths = {}

    for vehicle_id, vehicle_info in vehicles.items():
        current_capacity = vehicle_info["capacity"]
        distances = [neighborhoods[n]["distances"] for n in neighborhoods]
        order_quantities = [neighborhoods[n]["order_quantity"] for n in neighborhoods]

        # Solve TSP with constraints using dynamic programming
        min_distance = tsp_with_constraints(distances, order_quantities, current_capacity)

        # TODO: Implement backtracking to reconstruct the optimal path
        best_path = [0, 1, 2, 3, 4, 0]

        path = [f"n{idx}" for idx in best_path[1:-1]] + [restaurants["r0"]["neighbourhood_distance"][best_path[-1]] - 1]
        paths[f"{vehicle_id}_path"] = {"path1": path}

    return paths

if __name__ == "__main__":
    # Assuming data is the provided JSON
    with open('Y:\Student Handout\Input data\level1a.json', 'r') as f1:
        data = json.load(f1)

    result = generate_paths(data)
    print(json.dumps(result, indent=2))
