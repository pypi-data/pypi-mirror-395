from typing import Tuple
from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group

class Torus:
    """
    Generates uniform samples from :math:`S^1\\times S^1` embedded in :math:`\mathbb{R}^m`.
    """
    def __init__(self,
        n_points: int,
        ambient_dim: int,
        major_radius: float,
        minor_radius: float,
        noise: float=0.,
        skip_basis: bool=False,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.intrinsic_dim = 2
        self.normal_dim = ambient_dim-2
        self.ambient_dim = ambient_dim
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.noise = noise
        self.rng = rng

        # Generate torus (by rejection sampling)
        def sample_torus(R: float, r: float, num_samples: int, rng: np.random.Generator) -> Tuple[
            Float[np.ndarray, "N 3"], Float[np.ndarray, "N"]
        ]:
            phi = rng.uniform(0, 2*np.pi, num_samples) # Major circle
            theta = [] # Minor circle
            while len(theta) < num_samples:
                candidate_theta = rng.uniform(0, 2*np.pi) 
                if rng.uniform(0, 1) < (R + r * np.cos(candidate_theta)) / (R + r): # Rejection
                    theta.append(candidate_theta)
            theta = np.array(theta)
            x = (R + r * np.cos(theta)) * np.cos(phi)
            y = (R + r * np.cos(theta)) * np.sin(phi)
            z = r * np.sin(theta)
            true_sff = np.zeros((num_samples,2,2,1))
            true_sff[:,0,0] = -(np.cos(theta)/(R+r*np.cos(theta)))[:,None]
            true_sff[:,1,1] = -1./r
            tangent_basis = np.zeros((num_samples,2,3))
            tangent_basis[:,0,:] = np.array([
                -(R + r * np.cos(theta)) * np.sin(phi),
                (R + r * np.cos(theta)) * np.cos(phi),
                0*theta,
            ]).T # tangent vector to big circle
            tangent_basis[:,1,:] = np.array([
                -r * np.sin(theta) * np.cos(phi),
                -r * np.sin(theta) * np.sin(phi),
                r * np.cos(theta)
            ]).T # tangent vector to small circle
            # true_gaussian = np.cos(theta)/(r*(R+r*np.cos(theta)))
            return np.stack([x,y,z],axis=1), true_sff, tangent_basis
        self.points, self.true_sff, self.tangent_basis = sample_torus(self.major_radius, self.minor_radius, self.n_points, self.rng)


        # Embed in ambient dimension
        if skip_basis:
            self.basis: Float[np.ndarray, "3 m"] = np.eye(self.ambient_dim)[:self.points.shape[1]]
        else:
            self.basis: Float[np.ndarray, "3 m"] = ortho_group.rvs(self.ambient_dim, random_state=self.rng)[:self.points.shape[1]]
        self.points: Float[np.ndarray, "N m"] = self.points@self.basis
        self.tangent_basis = self.tangent_basis@self.basis

        # Add noise
        self.points += self.noise*self.rng.standard_normal((self.n_points, self.ambient_dim))/np.sqrt(self.ambient_dim)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, idx):
        return self.points[idx]

    def path(self,
        distance: float,
        mode: str="major_outer",
        num_steps: int=100,
    ) -> Float[np.ndarray, "N m"]:
        """
        Returns two points that are some specified distance apart. Mode is either "major_inner", "major_outer", "minor_inner", or "minor_outer"
        """
        if mode=="major_outer":
            R = self.major_radius+self.minor_radius
            theta = distance/R
            path = np.array([[R*np.cos(angle),R*np.sin(angle),0.] for angle in np.linspace(theta/2,-theta/2,num_steps)])          
        elif mode=="major_inner":
            R = self.major_radius-self.minor_radius
            theta = distance/R
            path = np.array([[R*np.cos(angle),R*np.sin(angle),0.] for angle in np.linspace(theta/2,-theta/2,num_steps)])          
        elif mode=="minor_outer":
            R = self.minor_radius
            theta = distance/R
            path = np.array([[self.major_radius+R*np.cos(angle),0.,R*np.sin(angle)] for angle in np.linspace(theta/2,-theta/2,num_steps)])          
        elif mode=="minor_inner":
            R = self.minor_radius
            theta = distance/R
            path = np.array([[self.major_radius+R*np.cos(np.pi+angle),0.,R*np.sin(np.pi+angle)] for angle in np.linspace(theta/2,-theta/2,num_steps)])          
        else:
            raise ValueError(f"Mode must be one of 'major_inner', 'major_outer', 'minor_inner', or 'minor_outer'. Got {mode}")
        return path@self.basis

    def evaluation_points(self) -> Float[np.ndarray, "3 m"]:
        """
        Returns three points: outside edge, inside edge, and on top
        """
        return np.stack([
            np.array([[self.major_radius+self.minor_radius,0.,0.]])@self.basis,
            np.array([[self.major_radius-self.minor_radius,0.,0.]])@self.basis,
            np.array([[self.major_radius,0.,self.minor_radius]])@self.basis,
        ],axis=0)
    
    def true_curvature(self) -> Float[np.ndarray, "N m"]:
        """
        Returns Gaussian curvature :math:`K=\\frac{\cos\theta}{r(R+r\cos\\theta)}`
        """
        return self.true_sff