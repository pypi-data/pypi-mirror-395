from typing import Union, Callable
from jaxtyping import Float
import numpy as np
from sklearn.neighbors import NearestNeighbors
import networkx as nx
from GraphRicciCurvature.OllivierRicci import OllivierRicci
from GraphRicciCurvature.FormanRicci import FormanRicci

class GraphRicci:
    """
    Estimates the Graph Ricci Curvature
    See Ni et al. 2019 (https://arxiv.org/pdf/1907.03993)
    """
    @staticmethod
    def graph_ricci_curvature(
        manifold: Float[np.ndarray, "N m"],
        num_neighbors: int = None,
        radius: float = None,
        alpha: float = 0.,
        distance_kernel: Union[str,Callable[[Float[np.ndarray, "N N"]],Float[np.ndarray, "N N"]]] = lambda x: (x>0).astype(int),
        method: str = "ollivier",
        verbose: str = "TRACE", 
    ) -> Float[np.ndarray,"N"]:
        if not ((num_neighbors is None) ^ (radius is None)):
            raise ValueError("Must specify exactly one of num_neighbors or radius")
        if num_neighbors is not None:
            nbrs = NearestNeighbors(n_neighbors=num_neighbors).fit(manifold)
            G = nbrs.kneighbors_graph(mode="distance")
        else:
            nbrs = NearestNeighbors(radius=radius).fit(manifold)
            G = nbrs.radius_neighbors_graph(mode="distance")
        G = distance_kernel(G)
        G = nx.from_scipy_sparse_array(G)
        if method=="ollivier":
            ricci_curvature = OllivierRicci(G, alpha=alpha, verbose=verbose)
            ricci_curvature.compute_ricci_curvature()
            return np.array(list(nx.get_node_attributes(ricci_curvature.G,"ricciCurvature",default=np.nan).values()))
        elif method=="forman":
            ricci_curvature = FormanRicci(G, method="augmented")
            return np.array(list(nx.get_node_attributes(ricci_curvature.G,"formanCurvature",default=np.nan).values()))
        else:
            raise ValueError(f"Method must be 'ollivier' or 'forman' (got {method}).")