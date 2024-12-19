import sys
import networkx as nx
from networkx.algorithms.components import connected_components
from networkx.algorithms.connectivity import minimum_edge_cut


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        G = nx.Graph()
        all_edges = []
        for ln in lines:
            node, nodes = ln.split(': ')
            all_edges.extend([(node, n) for n in nodes.split(' ')])
        G.add_edges_from(all_edges)

        spliter_edges = minimum_edge_cut(G)
        G.remove_edges_from(spliter_edges)
        c1, c2 = list(connected_components(G))
        r1 = len(c1) * len(c2)

        r2 = None

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
