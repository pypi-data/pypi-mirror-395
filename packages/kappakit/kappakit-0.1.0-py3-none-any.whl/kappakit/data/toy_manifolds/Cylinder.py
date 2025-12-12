from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group

class Cylinder:
    """
    Generates uniform samples from :math:`S^d\\times[-h/2,h/2]^k` embedded in :math:`\mathbb{R}^m`.
    """
    def __init__(self,
        n_points: int,
        sphere_dim: int,
        linear_dim: int,
        ambient_dim: int,
        radius: float,
        width: float,
        noise: float=0.,
        skip_basis: bool=False,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.sphere_dim = sphere_dim
        self.linear_dim = linear_dim
        self.intrinsic_dim = sphere_dim+linear_dim
        self.normal_dim = ambient_dim-self.intrinsic_dim
        self.ambient_dim = ambient_dim
        self.radius = radius
        self.width = width
        self.noise = noise
        self.rng = rng

        # Generate sphere
        self.points: Float[np.ndarray, "N d+1"] = self.rng.standard_normal((self.n_points, self.sphere_dim+1))
        self.points = self.radius * self.points / np.linalg.norm(self.points, axis = -1, keepdims=True)
        
        # Generate linear
        self.points = np.concatenate((self.points,self.rng.uniform(-self.width/2.,self.width/2.,size=(self.n_points,self.linear_dim))),axis=1)

        # Embed in ambient dimension
        if skip_basis:
            self.basis: Float[np.ndarray, "d+1 m"] = np.eye(self.ambient_dim)[:self.points.shape[1]]
        else:
            self.basis: Float[np.ndarray, "d+1 m"] = ortho_group.rvs(self.ambient_dim, random_state=self.rng)[:self.points.shape[1]]
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
        R = self.radius
        theta = distance/R         
        path = np.array([[R*np.cos(angle),R*np.sin(angle)]+[0. for _ in range(self.ambient_dim-2)] for angle in np.linspace(theta/2,-theta/2,num_steps)])
        return path@self.basis
    
    def evaluation_points(self) -> Float[np.ndarray, "1 m"]:
        return self.points[:1]