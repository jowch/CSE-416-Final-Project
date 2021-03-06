import numpy as np
import graph_tool.all as gt


def degree(g: gt.Graph, deg='total'):
    '''
    Returns array of degree frequencies.
    '''
    degrees = g.degree_property_map(deg=deg).a
    counts = np.bincount(degrees)[1:]
    pdf = counts / counts.sum()
    k = np.arange(degrees.max()) + 1
    return pdf, np.dot(k, pdf)

def excess_degree(g: gt.Graph, deg='total'):
    '''
    Returns array of excess degree frequencies.
    '''
    def compute_excess(k, degrees):
        edges = g.get_edges()[:, :2]
        # find all nodes with degree k+1
        nodes = g.get_vertices()[degrees == k + 1]
        # find all edges that contain those nodes
        associated_edges = np.any(np.isin(edges, nodes), axis=1)
        # return the number of edges found
        return np.sum(associated_edges)

    degrees = g.degree_property_map(deg=deg).a
    q = np.vectorize(lambda k: compute_excess(k, degrees))
    k = np.arange(1, degrees.max() + 1)
    counts = q(k)
    pdf = counts / np.sum(counts)
    return pdf, np.dot(k, pdf)

def power(g: gt.Graph, a_hat, k_min=1):
    degrees = g.degree_property_map('total')
    k = np.arange(1, degrees.max())
    return (a_hat - 1) / k_min * np.power(k / k_min, -a_hat)


if __name__ == '__main__':
    pass
