from students import *
from solvers import *
from tqdm import tqdm

iters = 100
for quarter in [0, 1, 2]:
    data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in tqdm(range(iters)):
        generated_students, generated_classes = make_students(quarter)
        g = Graph(generated_students, generated_classes)
        g.build()
        a, b, c, d = maximal(g)
        data[0][0] = a / iters
        data[0][1] = b / iters
        data[0][2] = c / iters
        data[0][3] = d / iters

        generated_students, generated_classes = make_students(quarter)
        g = Graph(generated_students, generated_classes)
        g.build()
        a, b, c, d = priority(g)
        data[1][0] = a / iters
        data[1][1] = b / iters
        data[1][2] = c / iters
        data[1][3] = d / iters

        generated_students, generated_classes = make_students(quarter)
        g = Graph(generated_students, generated_classes)
        g.build()
        a, b, c, d = pre_alloc(g)
        data[2][0] = a / iters
        data[2][1] = b / iters
        data[2][2] = c / iters
        data[2][3] = d / iters

    print(data)
