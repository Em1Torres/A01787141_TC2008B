import csv, ast, flask, pandas
from pathlib import Path
import numpy as np
from typing import List

app = flask.Flask(__name__)
BASE = Path(__file__).resolve().parent

def load_nodes():
    nodes = {}
    with open(BASE / "Nodes.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            point = tuple(float(v) for v in ast.literal_eval(row["Points"]))
            nodes[int(row["Node"])] = {
                "node": int(row["Node"]),
                "agent": int(row["Agent"]) if row.get("Agent") else None,
                "point": point,
                "dirt": int(row["Dirt"])
            }
    return nodes

def load_routes():
    routes = {}
    with open(BASE / "Routes.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            agent = int(row["Agent"])
            routes.setdefault(agent, []).append(int(row["Node"]))
    return routes

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/api/data")
def data():
    return flask.jsonify({"nodes": load_nodes(), "routes": load_routes()})

class SpiralOrder:  # Using my own spiral code I previously had
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        spiral = []
        m = len(matrix)
        n = len(matrix[0])
        size = m*n
        i = 1 # Count for all elements of the matrix

        # Boundaries
        right=n-1
        left=0
        bottom=m-1
        top = 0

        # Looping to make spiral
        
        while i <= size:
            # Go left to right in a row
            
            j = left
            while j <= right:
                if i > size:
                    break
                spiral.append(matrix[top][j])
                j+=1
                i+=1
            top+=1

            # From right column, go up to down
            
            j = top
            while j <= bottom:
                if i > size:
                    break
                spiral.append(matrix[j][right])
                j+=1
                i+=1
            right-=1

            # From bottom row, go right to left
            
            j=right
            while j >=left:
                if i > size:
                    break
                spiral.append(matrix[bottom][j])
                i+=1
                j-=1
            bottom-=1

            # From left column, go bottom to up
            
            j=bottom
            while j>=top:
                if i > size:
                    break
                spiral.append(matrix[j][left])
                i+=1
                j-=1
            left+=1

        return spiral


def make_path(cells, pathway, grid_size):
    pathway = pathway.strip().lower()
    if pathway in ("zz", "zigzag"):
        return [
            int(node)
            for row_index, row in enumerate(cells)
            for node in (row if row_index % 2 == 0 else row[::-1])
        ]
    elif pathway == "spiral":
        return SpiralOrder().spiralOrder(cells.tolist())
    elif pathway in ("rnm", "random"):
        available = set(int(node) for node in cells.ravel())
        path = [int(cells[0, 0])]
        for _ in range(len(available) - 1):
            row, col = divmod(path[-1], grid_size)
            neighbors = [
                node for node in available
                if node != path[-1]
                and abs(node // grid_size - row) <= 1
                and abs(node % grid_size - col) <= 1
            ]
            path.append(int(np.random.choice(neighbors)))
        return path

def Parameters(Options):
    print(Options.Agents)
    print(Options.Pathways)
    print(Options.Nodes)

    grid = np.arange(Options.Nodes**2).reshape(Options.Nodes, Options.Nodes)
    row_groups = np.array_split(np.arange(Options.Nodes), Options.Agents)
    routes = []
    row_owners = {}
    for agent, rows in enumerate(row_groups):
        section = grid[rows, :]
        path = make_path(section, Options.Pathways, Options.Nodes)
        if path[0] != 0:
            path.insert(0, 0)
        path.append(0)
        routes.extend({"Agent": agent, "Node": node} for node in path)
        row_owners.update({int(row): agent for row in rows})

    pandas.DataFrame(routes).to_csv("Routes.csv", index=False)
    path_nodes = {route["Node"] for route in routes}
    dirt_probability = Options.Dirt / 100

    rows = []
    n = 0
    for x in range(Options.Nodes):
        for y in range(Options.Nodes):
            rows.append({
                "Node": n,
                "Agent": row_owners[x],
                "Points": f"({y},{x},0)",
                "Dirt": int(
                    n in path_nodes and np.random.random() < dirt_probability
                )
            })
            n += 1
    pandas.DataFrame(rows).to_csv("Nodes.csv", index=False)

            
def Sim(Options):
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)
