from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group

class Sphere:
    """
    Generates uniform samples from :math:`S^d` embedded in :math:`\mathbb{R}^m`.
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

        # Generate sphere
        self.points: Float[np.ndarray, "N d+1"] = self.rng.standard_normal((self.n_points, self.intrinsic_dim+1))
        self.points = self.radius * self.points / np.linalg.norm(self.points, axis = -1, keepdims=True)

        # Embed in ambient dimension
        if skip_basis:
            self.basis: Float[np.ndarray, "d+1 m"] = np.eye(self.ambient_dim)[:self.points.shape[1]]
        else:
            self.basis: Float[np.ndarray, "d+1 m"] = ortho_group.rvs(self.ambient_dim, random_state=self.rng)[:self.points.shape[1]]

        def tangent_basis(point: Float[np.ndarray, "m"]) -> Float[np.ndarray, "m"]:
            A = np.random.randn(point.shape[0], point.shape[0]-1)
            A_proj = A - np.outer(point, point @ A)
            Q, _ = np.linalg.qr(A_proj)
            return Q.T
        self.tangent_basis: Float[np.ndarray, "N m"] = (np.stack([tangent_basis(point) for point in self.points]))@self.basis[None,:,:]   
       
        self.points: Float[np.ndarray, "N m"] = self.points@self.basis

        # Add noise
        self.points += self.noise*self.rng.standard_normal((self.n_points, self.ambient_dim))/np.sqrt(self.ambient_dim)
        
        self.true_sff = np.zeros((self.n_points,self.intrinsic_dim,self.intrinsic_dim,1))
        self.true_sff[:,0,0,0] = -1./self.radius
        self.true_sff[:,1,1,0] = -1./self.radius

    def __len__(self) -> int:
        return self.n_points

    def __getitem__(self, idx: int) -> Float[np.ndarray, "m"]:
        return self.points[idx]
    
    def path(self,
        distance: float,
        num_steps: int=100
    ) -> Float[np.ndarray, "N m"]:
        theta = distance/self.radius
        path = np.array([[self.radius*np.cos(angle),self.radius*np.sin(angle)]+[0. for _ in range(self.intrinsic_dim-1)] for angle in np.linspace(theta/2,-theta/2,num_steps)])
        return path@self.basis
    
    def evaluation_points(self) -> Float[np.ndarray, "1 m"]:
        return self.points[:1]