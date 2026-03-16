# route_planner.py
# -------------------------------------------------------------
# UWE Advanced Algorithms - Activity 1.3 Route Planner
# -------------------------------------------------------------
# Features:
# - Loads the full UK railway network from activity1_3_railnetwork_data.csv
# - Asks user for:
#     * Start station
#     * End station
#     * Required stations (comma-separated)
# - Case-insensitive station matching
# - Automatic whitespace stripping
# - Precomputes Dijkstra shortest paths between all important stations
# - Tries all permutations of required stations to find the lowest-cost route
# - Saves:
#       output/route_result.txt
#       output/route_debug.json
# Done by: Tanjil Siam , ID: 24024535
# -------------------------------------------------------------

import csv
import json
import heapq
from itertools import permutations
from pathlib import Path

DATA_FILE = "activity1_3_railnetwork_data.csv"
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

# -------------------------------------------------------------
# Utility: Normalise station name (case-insensitive + strip spaces)
# -------------------------------------------------------------
def norm(s: str) -> str:
    return s.strip().lower()

# -------------------------------------------------------------
# Step 1: Load graph from CSV (undirected)
# -------------------------------------------------------------
def load_graph():
    graph = {}
    with open(DATA_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            a, b, c = row[0].strip(), row[1].strip(), float(row[2])
            na, nb = norm(a), norm(b)

            graph.setdefault(na, []).append((nb, c))
            graph.setdefault(nb, []).append((na, c))
    return graph

# -------------------------------------------------------------
# Step 2: Dijkstra (with path reconstruction)
# -------------------------------------------------------------
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        cost, node = heapq.heappop(pq)
        if cost > dist[node]:
            continue
        for neigh, w in graph[node]:
            new_cost = cost + w
            if new_cost < dist[neigh]:
                dist[neigh] = new_cost
                prev[neigh] = node
                heapq.heappush(pq, (new_cost, neigh))
    return dist, prev

# reconstruct path from dijkstra outputs

def build_path(prev, start, end):
    route = []
    cur = end
    while cur is not None:
        route.append(cur)
        if cur == start:
            break
        cur = prev[cur]
    route.reverse()
    return route

# -------------------------------------------------------------
# Step 3: Solve route optimisation
# -------------------------------------------------------------
def solve_route(start, end, required, graph):
    important = [start] + required + [end]

    # Precompute all-pairs shortest distances between important nodes
    dist_map = {}
    path_map = {}

    for s in important:
        d, p = dijkstra(graph, s)
        for t in important:
            if t in d and d[t] < float('inf'):
                dist_map[(s, t)] = d[t]
                path_map[(s, t)] = build_path(p, s, t)
            else:
                dist_map[(s, t)] = float('inf')
                path_map[(s, t)] = None

    best_cost = float('inf')
    best_route = None
    best_order = None

    for perm in permutations(required):
        seq = [start] + list(perm) + [end]

        total = 0
        possible = True
        full_path = []

        for i in range(len(seq)-1):
            a, b = seq[i], seq[i+1]
            cost = dist_map[(a, b)]
            if cost == float('inf'):
                possible = False
                break
            total += cost
        
        if possible and total < best_cost:
            # Build full expanded path
            expanded = []
            for i in range(len(seq)-1):
                a, b = seq[i], seq[i+1]
                seg = path_map[(a, b)]
                if i > 0:
                    seg = seg[1:]
                expanded.extend(seg)

            best_cost = total
            best_route = expanded
            best_order = perm

    return best_cost, best_route, best_order

# -------------------------------------------------------------
# MAIN PROGRAM (interactive input)
# -------------------------------------------------------------
if __name__ == "__main__":
    graph = load_graph()
    print("Loaded rail network with", len(graph), "stations.")

    start_raw = input("Enter start station: ").strip().lower()
    end_raw = input("Enter end station: ").strip().lower()
    req_raw = input("Enter required stations (comma separated): ").strip()

    required = [r.strip().lower() for r in req_raw.split(",") if r.strip()]
    start = start_raw
    end = end_raw

    for st in [start, end] + required:
        if st not in graph:
            print(f"Error: Station '{st}' not found in dataset.")
            exit(1)

    best_cost, best_route, best_order = solve_route(start, end, required, graph)

    if best_route is None:
        print("No valid route found.")
        exit(0)

    out_txt = OUT_DIR / "route_result.txt"
    out_json = OUT_DIR / "route_debug.json"

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"Start: {start}\n")
        f.write(f"End: {end}\n")
        f.write(f"Required order used: {list(best_order)}\n")
        f.write(f"Total cost: {best_cost}\n")
        f.write("Full route:\n")
        for st in best_route:
            f.write(st + "\n")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "start": start,
            "end": end,
            "required": required,
            "order_used": best_order,
            "total_cost": best_cost,
            "route": best_route
        }, f, indent=4)

    print("\nRoute computed successfully!")
    print("Total cost:", best_cost)
    print("Route saved to:", out_txt)
    print("Debug info saved to:", out_json)
