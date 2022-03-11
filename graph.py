import random

from scipy.stats import poisson


class Node:
    def __init__(self, base_obj):
        self.student = base_obj
        self.in_edges = {}
        self.out_edges = {}

    @property
    def in_degree(self):
        return sum([len(e) for e in self.in_edges.values()])

    @property
    def out_degree(self):
        return sum([len(e) for e in self.out_edges.values()])


class Graph:
    def __init__(self, students, classes):
        self.nodes = [Node(student) for student in students]
        self.classes = {c.id: c for c in classes}
        self.built = False
        self.clique_map = {}
        self.cliques = []

    def build(self):
        self.built = True

        for node in self.nodes:
            past_classes = node.student.past_classes
            for past in past_classes:
                for id, c in self.classes.items():
                    if past.id == id:
                        for other_student in c.students:
                            other_node = self.nodes[other_student.id]
                            l = node.out_edges.get(past.id, [])
                            l.append(other_node)
                            node.out_edges[past.id] = l
                            l = other_node.in_edges.get(past.id, [])
                            l.append(node)
                            other_node.in_edges[past.id] = l

        counter = len(self.nodes)
        dividers = []
        while counter > 0:
            size = poisson.rvs(10)
            counter -= size
            if counter < 0:
                size = size + counter
            dividers.append(size)

        curr = 0
        shuffled = self.nodes.copy()
        random.shuffle(shuffled)
        for divider in dividers:
            clique = shuffled[curr: curr + divider]
            for node in clique:
                self.clique_map[node.student.id] = clique
            self.cliques.append(clique)
            curr += divider
