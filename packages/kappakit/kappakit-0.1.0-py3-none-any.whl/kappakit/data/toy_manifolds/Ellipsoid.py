from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group
from scipy.integrate import quad
from scipy.optimize import root_scalar

class Ellipsoid:
    """
    Generates uniform samples from distorted :math:`S^d` embedded in :math:`\mathbb{R}^m`.
    """
    def __init__(self,
        n_points: int,
        intrinsic_dim: int,
        ambient_dim: int,
        radii: Float[np.ndarray, "d+1"],
        noise: float=0.,
        skip_basis: bool=False,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.intrinsic_dim = intrinsic_dim
        self.normal_dim = ambient_dim-intrinsic_dim
        self.ambient_dim = ambient_dim
        self.radii = radii
        self.noise = noise
        self.rng = rng

        # Generate ellipsoid via rejection sampling
        def sample_ellipsoid(num_samples: int, radii: Float[np.ndarray, "d+1"], rng: np.random.Generator) -> Float[np.ndarray, "N d+1"]:
            samples = []
            inv_radii = radii**-2
            max_scale_factor = np.sqrt(np.sum(inv_radii))
            while len(samples) < num_samples:
                point = rng.standard_normal(self.intrinsic_dim+1)
                point /= np.linalg.norm(point)
                scale_factor = np.sqrt(np.sum((point**2)*inv_radii))
                if rng.uniform(0, 1) < max_scale_factor / scale_factor: # Rejection
                    samples.append(point*radii)
            return np.stack(samples,axis=0)
        self.points = sample_ellipsoid(self.n_points, self.radii, self.rng)

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
        center_axis: int=0,
        path_axis: int=1,
        num_steps: int=100
    ) -> Float[np.ndarray, "N m"]:
        def ellipse_arc_length(a, b, theta0, l):
            """
            Finds the angle range around theta0 that gives an arc length of l.
            """
            # Function to compute arc length from theta0 - delta to theta0 + delta
            def arc_length(delta):
                def integrand(theta):
                    return np.sqrt(a**2 * np.sin(theta)**2 + b**2 * np.cos(theta)**2)
                return quad(integrand, theta0 - delta, theta0 + delta)[0]
            # Solve for delta using a numerical solver
            delta_theta = root_scalar(lambda delta: arc_length(delta) - l, bracket=[0, np.pi / 2]).root
            return theta0 - delta_theta, theta0 + delta_theta
        theta_start, theta_end = ellipse_arc_length(self.radii[center_axis],self.radii[path_axis],0,distance)
        path = np.zeros((num_steps,self.intrinsic_dim+1))
        path[:,center_axis] = self.radii[center_axis]*np.cos(np.linspace(theta_start,theta_end,num_steps))
        path[:,path_axis] = self.radii[path_axis]*np.sin(np.linspace(theta_start,theta_end,num_steps))
        return path@self.basis
    
    def evaluation_points(self) -> Float[np.ndarray, "d+1 m"]:
        return np.stack([np.eye(self.intrinsic_dim+1,M=1,k=-axis)*self.radii[axis] for axis in range(self.intrinsic_dim+1)],axis=0)@self.basis