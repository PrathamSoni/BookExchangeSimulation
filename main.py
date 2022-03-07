from graph import *
from students import *

quarter = 2
generated_students = make_students(quarter)

supply = []
demand = []
for s in generated_students:
    demand.extend([c.id for c in s.classes])
    supply.extend([c.id for c in s.past_classes])

supply = Counter(supply)
demand = Counter(demand)

out = {}
for k, v in supply.items():
    try:
        out[k] = v/demand[k]
    except ZeroDivisionError:
        out[k] = float("inf")

print(sorted(out.values()))


g = Graph(generated_students)
g.build()

print(g.nodes[0].in_degree, g.nodes[0].out_degree, )