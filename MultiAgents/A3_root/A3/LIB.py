import csv, ast, flask, pandas
from pathlib import Path

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

def Parameters(Options):
    print(Options.Agents)
    DF = pandas.DataFrame();
    DF.to_csv("RoutesNew.csv", index = False);
    path = [1,2,3,4]
    for a in range(Options.Agents):
        for p in path:
            DF = pandas.DataFrame({"Node": [a], "Route": [p]});
            DF.to_csv("RoutesNew.csv", mode = "a", index = False, header = False);

    DF = pandas.DataFrame();
    DF.to_csv("NodesNew.csv", index = False);
    actual_number = 0
    for x in range(8):
        for y in range(8):
            DF = pandas.DataFrame({"Node": [actual_number], "Points": [("(%s,%s,0)") % (x, y)], "Dirt": [0]});
            DF.to_csv("NodesNew.csv", mode = "a", index = False, header = False);
            actual_number += 1

            
def Sim(Options):
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)
