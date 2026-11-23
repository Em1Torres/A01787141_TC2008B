import csv, ast, flask, pandas
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
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

class SpiralOrder:
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


def getMatrix(n,m):
    count=0
    matrix = np.zeros((n, m), dtype=int)
    for i in range(n):
        for j in range(m):
            matrix[i][j] = count
            count+=1
    return matrix


def Parameters(Options):
    print(Options.Agents)
    print(Options.Pathways)
    print(Options.Nodes)

    matrix = np.zeros((Options.Nodes, Options.Nodes))
    S = np.zeros((matrix.size, matrix.size))

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    try:
                        S[np.ravel_multi_index((i, j), matrix.shape), np.ravel_multi_index((i + x, j + y), matrix.shape)] = 1
                    except:
                        continue

    path = [0]
    if Options.Pathways == "ZZ": # Zig Zag in the grid
        columns = [[int(node) for node in nodes[x] if node != 0]
                   for x in range(height)]
        path = []
        for i, column in enumerate(columns):
            if i % 2 == 1:
                column = column[::-1]
            path.extend(column)

    elif Options.Pathways == "Spiral": # Spiral in the grid
        matrix = getMatrix(Options.Nodes,Options.Nodes)
        path = SpiralOrder().spiralOrder(matrix)

    elif Options.Pathways == "Rnm": # Random in the grid
        for i in range(Options.Nodes**2-1):
            neighbors = np.flatnonzero(S[path[-1]])
            path.append(int(np.random.choice(neighbors)))
        
    # path = [1, 2, 3, 4]

    pandas.DataFrame(
        [{"Agent": a, "Node": p} for a in range(Options.Agents) for p in path]
    ).to_csv("Routes.csv", index=False)

    rows = []
    n = 0
    for x in range(Options.Nodes):
        for y in range(Options.Nodes):
            rows.append({"Node": n, "Points": f"({x},{y},0)", "Dirt": 0})
            n += 1
    pandas.DataFrame(rows).to_csv("Nodes.csv", index=False)

            
def Sim(Options):
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)
