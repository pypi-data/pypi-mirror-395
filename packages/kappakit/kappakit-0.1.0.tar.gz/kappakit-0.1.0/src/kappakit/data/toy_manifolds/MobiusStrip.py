from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group

class MobiusStrip:
    """
    Generates uniform samples from the Mobius Strip embedded in :math:`\mathbb{R}^m`.

    Follows the parameterization :math:`((r+w\cos(ct))\cos(t),(r+w\cos(ct))\sin(t),w\sin(ct))`
    for radius :math:`r`, turn count :math:`c`, angle around the circle :math:`t`, 
    and position widthwise along the strip :math:`w`
    """
    def __init__(self,
        n_points: int,
        ambient_dim: int,
        radius: float,
        width: float,
        turn_count: float,
        noise: float=0.,
        skip_basis: bool=False,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.intrinsic_dim = 2
        self.normal_dim = ambient_dim-2
        self.ambient_dim = ambient_dim
        self.radius = radius
        self.width = width
        self.turn_count = turn_count
        self.noise = noise
        self.rng = rng

        # Generate Mobius strip
        theta = rng.uniform(0,2*np.pi,size=self.n_points)
        offset = rng.uniform(-width/2.,width/2.,size=self.n_points)
        self.points = np.zeros((self.n_points,3))
        self.points[:,0] = (self.radius+offset*np.cos(self.turn_count*theta))*np.cos(theta)
        self.points[:,1] = (self.radius+offset*np.cos(self.turn_count*theta))*np.sin(theta)
        self.points[:,2] = offset*np.sin(self.turn_count*theta)

        # Embed in ambient dimension
        if skip_basis:
            self.basis: Float[np.ndarray, "3 m"] = np.eye(self.ambient_dim)[:self.points.shape[1]]
        else:
            self.basis: Float[np.ndarray, "3 m"] = ortho_group.rvs(self.ambient_dim, random_state=self.rng)[:self.points.shape[1]]
        self.points: Float[np.ndarray, "N m"] = self.points@self.basis

        # Add noise
        self.points += self.noise*self.rng.standard_normal((self.n_points, self.ambient_dim))/np.sqrt(self.ambient_dim)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, idx):
        return self.points[idx]

    def path(self,
        distance: float,
        offset: float=0,
        axis: int=0,
        num_steps: int=100,
    ) -> Float[np.ndarray, "N m"]:
        if axis==0:
            theta = np.linspace(0,distance/self.radius,num_steps)
            path = np.zeros((num_steps,3))
            path[:,0] = (self.radius+offset*np.cos(self.turn_count*theta))*np.cos(theta)
            path[:,1] = (self.radius+offset*np.cos(self.turn_count*theta))*np.sin(theta)
            path[:,2] = offset*np.sin(self.turn_count*theta)
        elif axis==1:
            path = np.zeros((num_steps,3))
            path[:,0] = np.linspace(self.radius-distance/2.,self.radius+distance/2.,num_steps)
        else:
            raise ValueError(f"Axis should be 0 (circular) or 1 (width-wise), but got {axis}.")
        return path@self.basis

    def evaluation_points(self) -> Float[np.ndarray, "3 m"]:
        """
        Returns three points: outside edge, center, inside edge
        """
        return np.stack([
            np.array([[self.radius-self.width/2.,0.,0.]])@self.basis,
            np.array([[self.radius,0.,0.]])@self.basis,
            np.array([[self.radius+self.width/2.,0.,0.]])@self.basis,
        ],axis=0)