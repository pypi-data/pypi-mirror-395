from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group

class S_Curve:
    """
    Generates uniform samples from S-curve (two 3/4 circles x linear) :math:`{(r\\sin\\theta,\sgn(\\theta)r(\cos(\\theta)-1)):\\theta\in[-\\frac{3\pi}{2},\\frac{3\pi}{2}]}\\times\mathbb{R}^{d-1}` embedded in :math:`\mathbb{R}^m`.
    """
    def __init__(self,
        n_points: int,
        intrinsic_dim: int,
        ambient_dim: int,
        radius: float,
        width: float,
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

        # Generate s-curve
        self.points = np.zeros((self.n_points, self.intrinsic_dim+1))
        thetas = rng.uniform(-1.5*np.pi,1.5*np.pi,size=self.n_points)
        self.points[:,0] = self.radius*np.sin(thetas)
        self.points[:,1] = self.radius*np.sign(thetas)*(np.cos(thetas)-1)
        self.points[:,2:] = rng.uniform(-width/2.,width/2.,size=(self.n_points,self.intrinsic_dim-1))

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
        center_theta: float=0,
        axis: int=0,
        num_steps: int=100
    ) -> Float[np.ndarray, "N m"]:
        theta = distance/self.radius
        if axis==0 or axis==1:
            path = np.zeros((num_steps,self.intrinsic_dim+1))
            delta_theta = distance/self.radius
            thetas = np.linspace(center_theta-delta_theta/2., center_theta+delta_theta/2., num_steps)
            path[:,0] = self.radius*np.sin(thetas)
            path[:,1] = self.radius*np.sign(thetas)*(np.cos(thetas)-1)
        else:
            path = np.zeros((num_steps,self.intrinsic_dim+1))
            path[:,0] = self.radius*np.sin(center_theta)
            path[:,1] = self.radius*np.sign(center_theta)*(np.cos(center_theta)-1)
            path[:,axis] = np.linspace(-distance/2.,distance/2.,num_steps)
        return path@self.basis
    
    def evaluation_points(self) -> Float[np.ndarray, "2 m"]:
        return np.stack([np.zeros(self.intrinsic_dim+1),[2*self.radius]+[0 for _ in range(self.intrinsic_dim)]],axis=0)