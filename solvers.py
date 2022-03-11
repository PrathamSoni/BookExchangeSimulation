import random

from graph import Graph
from copy import deepcopy


def maximal(graph: Graph):
    assert graph.built
    exchanges = 0
    alpha_dif = 0
    total_demand = 0
    for node in graph.nodes:
        total_demand += len(node.student.classes)

    supply = {}
    demand = {}

    for node in graph.nodes:
        for c in node.student.classes:
            l = demand.get(c.id, set())
            l.add(node)
            demand[c.id] = l

        for c in node.student.past_classes:
            l = supply.get(c.id, set())
            l.add(node)
            supply[c.id] = l

    for k, s in supply.items():
        s = list(s)
        random.shuffle(s)
        supply[k] = s
    for k, d in demand.items():
        d = list(d)
        random.shuffle(d)
        demand[k] = d

    for c_id, d in demand.items():
        s = supply.get(c_id, [])
        exchanges += min(len(d), len(s))

        for i in range(min(len(d), len(s))):
            d[i].student.received += 1
            s[i].student.donated += 1

    rec = 0
    zero_alph = 0
    for node in graph.nodes:
        rec += node.student.received
        zero_alph_ = max(node.student.donated - node.student.received, 0)
        alpha_dif += max(zero_alph_ - node.student.alpha, 0)
        zero_alph += zero_alph_

    return rec / total_demand, exchanges, alpha_dif, zero_alph


def priority(graph: Graph):
    assert graph.built
    exchanges = 0
    alpha_dif = 0
    total_demand = 0
    for node in graph.nodes:
        total_demand += len(node.student.classes)

    donate_queue = [node.student.id for node in sorted(graph.nodes, key=lambda x: x.student.donated-x.student.received )]
    receive_queue = deepcopy(donate_queue)[::-1]

    while len(receive_queue) > 0 and len(donate_queue) > 0:
        receiver_id = receive_queue.pop(0)
        rec_node = graph.nodes[receiver_id]
        donate_ids = [node.student.id for l in rec_node.in_edges.values() for node in l]
        donate_class_ids = [k for k, l in rec_node.in_edges.items() for node in l]
        found = False
        for idx, donate_id in enumerate(donate_queue):
            if not found:
                for candidate, candidate_class_id in zip(donate_ids, donate_class_ids):
                    if donate_id == candidate:
                        don_node = graph.nodes[donate_id]
                        don_node.student.donated += 1
                        change_nodes = don_node.out_edges.pop(candidate_class_id)
                        for node in change_nodes:
                            node.in_edges[candidate_class_id].remove(don_node)

                        rec_node.student.received += 1
                        change_nodes = rec_node.in_edges.pop(candidate_class_id)
                        for node in change_nodes:
                            node.out_edges[candidate_class_id].remove(rec_node)

                        donate_queue.pop(idx)
                        if don_node.out_degree > 0:
                            donate_queue.append(donate_id)
                        if rec_node.out_degree > 0:
                            donate_queue.remove(receiver_id)
                            donate_queue.insert(0, receiver_id)

                        if rec_node.in_degree > 0:
                            receive_queue.append(receiver_id)
                        if don_node.in_degree > 0:
                            receive_queue.remove(donate_id)
                            receive_queue.insert(0, donate_id)

                        found = True
                        exchanges +=1
                        break

    rec = 0
    zero_alph = 0
    for node in graph.nodes:
        rec += node.student.received
        zero_alph_ = max(node.student.donated - node.student.received, 0)
        alpha_dif += max(zero_alph_ - node.student.alpha, 0)
        zero_alph += zero_alph_

    return rec / total_demand, exchanges, alpha_dif, zero_alph


def pre_alloc(graph: Graph):
    assert graph.built

    for clique in graph.cliques:
        supply = {}
        demand = {}

        for node in clique:
            for c in node.student.classes:
                l = demand.get(c.id, set())
                l.add(node)
                demand[c.id] = l

            for c in node.student.past_classes:
                l = supply.get(c.id, set())
                l.add(node)
                supply[c.id] = l

        for k, s in supply.items():
            s = list(s)
            random.shuffle(s)
            supply[k] = s
        for k, d in demand.items():
            d = list(d)
            random.shuffle(d)
            demand[k] = d

        for c_id, d in demand.items():
            s = supply.get(c_id, [])
            for i in range(min(len(d), len(s))):
                don_node = s[i]
                rec_node = d[i]
                don_node.student.donated += 1
                change_nodes = don_node.out_edges.pop(c_id)
                for node in change_nodes:
                    node.in_edges[c_id].remove(don_node)

                rec_node.student.received += 1
                change_nodes = rec_node.in_edges.pop(c_id)
                for node in change_nodes:
                    node.out_edges[c_id].remove(rec_node)

    return priority(graph)
