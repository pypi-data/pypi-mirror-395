from jaxtyping import Float
import numpy as np
from datasets import load_dataset
import open3d as o3d

class StanfordBunny:
    """
    Generates samples from StanfordBunny
    """
    def __init__(self,
        n_points: int=None,
        rescale: float=10.,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.rescale = rescale
        self.rng = rng
        self.dataset = np.array(o3d.io.read_point_cloud(o3d.data.BunnyMesh().path).points)
        if self.n_points is not None and self.n_points<=len(self.dataset):
            self.dataset = self.dataset[:self.n_points]
        self.dataset *= rescale
        rng.shuffle(self.dataset,axis=0)
