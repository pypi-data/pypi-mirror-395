from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group

class Ball:
    """
    Generates uniform samples from :math:`B^d` embedded in :math:`\mathbb{R}^m`.
    """
    def __init__(self,
        n_points: int,
        intrinsic_dim: int,
        ambient_dim: int,
        radius: float,
        noise: float=0.,
        skip_basis: bool=False,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.intrinsic_dim = intrinsic_dim
        self.normal_dim = ambient_dim-intrinsic_dim
        self.ambient_dim = ambient_dim
        self.radius = radius
        self.noise = noise
        self.rng = rng

        # Generate ball
        self.points: Float[np.ndarray, "N d"] = self.rng.standard_normal((self.n_points, self.intrinsic_dim))
        self.points /= np.linalg.norm(self.points, axis = -1, keepdims=True)
        self.points *= (self.rng.uniform(0, self.radius, self.n_points)**(1./self.intrinsic_dim)).reshape(-1,1)

        # Embed in ambient dimension
        if skip_basis:
            self.basis: Float[np.ndarray, "d m"] = np.eye(self.ambient_dim)[:self.points.shape[1]]
        else:
            self.basis: Float[np.ndarray, "d m"] = ortho_group.rvs(self.ambient_dim, random_state=self.rng)[:self.points.shape[1]]
        self.points: Float[np.ndarray, "N m"] = self.points@self.basis

        # Add noise
        self.points += self.noise*self.rng.standard_normal((self.n_points, self.ambient_dim))/np.sqrt(self.ambient_dim)

    def __len__(self) -> int:
        return self.n_points

    def __getitem__(self, idx: int) -> Float[np.ndarray, "m"]:
        return self.points[idx]
    
    def path(self,
        distance: float,
        num_steps: int=100
    ) -> Float[np.ndarray, "N m"]:
        path = np.array([[step]+[0. for _ in range(self.intrinsic_dim-1)] for step in np.linspace(-distance/2.,distance/2.,num_steps)])
        return path@self.basis
    
    def evaluation_points(self) -> Float[np.ndarray, "1 m"]:
        return np.zeros((1,self.ambient_dim))