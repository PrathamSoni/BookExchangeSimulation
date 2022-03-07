class Node:
    def __init__(self, base_obj):
        self.student = base_obj
        self.in_edges = []
        self.out_edges = []

    @property
    def in_degree(self):
        return len(self.in_edges)

    @property
    def out_degree(self):
        return len(self.out_edges)


class Graph:
    def __init__(self, nodes):
        self.nodes = [Node(student) for student in nodes]
        self.built = False
    
    def build(self):
        self.built = True

        for node in self.nodes:
            past_classes = node.student.past_classes
            for other_node in self.nodes:
                out_classes = other_node.student.classes
                for past in past_classes:
                    for out in out_classes:
                        if past.id == out.id:
                            node.out_edges.append((other_node, past.id))
                            other_node.in_edges.append((node, past.id))

