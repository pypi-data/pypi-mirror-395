from jaxtyping import Float
import numpy as np
from scipy.stats import ortho_group
from scipy.integrate import quad
from scipy.optimize import root_scalar

def arc_length(t_start: float, t_end: float, spiral_coef: float) -> float:
    """Computes the arc length of the spiral from t_start to t_end."""
    return quad(lambda tau: spiral_coef * np.sqrt(1 + tau**2), t_start, t_end)[0]

class Roll:
    """
    Generates uniform samples from a Swiss Roll (Archimidean spiral x linear) :math:`{(a\\theta\cos\\theta,a\\theta\sin\\theta):\\theta\in[0,\\theta_{max}]}\\times\mathbb{R}^{d-1}` embedded in :math:`\mathbb{R}^m`.
    """
    def __init__(self,
        n_points: int,
        intrinsic_dim: int,
        ambient_dim: int,
        spiral_coef: float,
        theta_max: float,
        width: float,
        noise: float=0.,
        skip_basis: bool=False,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.intrinsic_dim = intrinsic_dim
        self.normal_dim = ambient_dim-self.intrinsic_dim
        self.ambient_dim = ambient_dim
        self.spiral_coef = spiral_coef
        self.theta_max = theta_max
        self.width = width
        self.noise = noise
        self.rng = rng

        # Generate spiral
        def sample_spiral(num_samples: int, spiral_coef: float, theta_max: float, rng: np.random.Generator) -> Float[np.ndarray, "N 2"]:
            def inverse_arc_length(length: float, spiral_coef: float, theta_max: float) -> float:
                """Finds the t corresponding to a given arc length."""
                result = root_scalar(lambda t: arc_length(0, t, spiral_coef) - length, bracket=[0, theta_max])
                return result.root
            total_arc_length = arc_length(t_start=0, t_end=theta_max, spiral_coef=spiral_coef)
            lengths = rng.uniform(0, total_arc_length, num_samples)
            spiral_theta = np.stack([inverse_arc_length(length=length, spiral_coef=spiral_coef, theta_max=theta_max) for length in lengths],axis=0)

            true_sff = np.zeros((num_samples,2,2,1))
            true_sff[:,0,0] = ((spiral_theta**2+2)/(spiral_coef*(spiral_theta**2+1)**(3/2)))[:,None]

            tangent_basis = np.zeros((num_samples,1,2))
            tangent_basis[:,0,:] = spiral_coef*np.array([
                np.cos(spiral_theta)-spiral_theta*np.sin(spiral_theta),
                np.sin(spiral_theta)+spiral_theta*np.cos(spiral_theta),
            ]).T
            return np.stack([spiral_coef*spiral_theta*np.cos(spiral_theta),spiral_coef*spiral_theta*np.sin(spiral_theta)],axis=1), true_sff, tangent_basis
        self.points, self.true_sff, tangent_basis = sample_spiral(num_samples=self.n_points, spiral_coef=self.spiral_coef, theta_max=self.theta_max, rng=self.rng)
        
        # Generate linear
        self.points = np.concatenate((self.points,self.rng.uniform(-self.width/2.,self.width/2.,size=(self.n_points,self.intrinsic_dim-1))),axis=1)
        self.tangent_basis = np.zeros((self.n_points,self.intrinsic_dim,self.ambient_dim))
        self.tangent_basis[:,0,:2] = tangent_basis[:,0]
        self.tangent_basis[:,1:,2:self.intrinsic_dim+1] = np.tile(np.eye(self.intrinsic_dim-1),(self.n_points,1,1))

        # Embed in ambient dimension
        if skip_basis:
            self.basis: Float[np.ndarray, "d+1 m"] = np.eye(self.ambient_dim)[:self.points.shape[1]]
        else:
            self.basis: Float[np.ndarray, "d+1 m"] = ortho_group.rvs(self.ambient_dim, random_state=self.rng)[:self.points.shape[1]]
        self.points: Float[np.ndarray, "N m"] = self.points@self.basis
        self.tangent_basis = self.tangent_basis@self.basis[None,:,:]

        # Add noise
        self.points += self.noise*self.rng.standard_normal((self.n_points, self.ambient_dim))/np.sqrt(self.ambient_dim)

    def __len__(self) -> int:
        return self.n_points

    def __getitem__(self, idx: int) -> Float[np.ndarray, "m"]:
        return self.points[idx]
    
    def path(self,
        distance: float,
        center_theta: float=np.pi,
        axis: int=0,
        num_steps: int=100,
    ) -> Float[np.ndarray, "N m"]: 
        if axis==0 or axis==1:
            def find_delta(center_theta: float, length: float, spiral_coef: float) -> float:
                """Finds delta such that the arc length between theta - delta and theta + delta equals L."""
                result = root_scalar(lambda delta: arc_length(center_theta-delta, center_theta+delta, spiral_coef) - length, bracket=[0, self.theta_max], method='brentq')
                return result.root
            delta_theta = find_delta(center_theta=center_theta, length=distance, spiral_coef=self.spiral_coef)
            path = np.zeros((num_steps,self.intrinsic_dim+1))
            thetas = np.linspace(center_theta-delta_theta, center_theta+delta_theta, num_steps)
            path[:,0] = self.spiral_coef*thetas*np.cos(thetas)
            path[:,1] = self.spiral_coef*thetas*np.sin(thetas)
        else:
            path = np.zeros((num_steps,self.intrinsic_dim+1))
            path[:,0] = self.spiral_coef*center_theta*np.cos(center_theta)
            path[:,1] = self.spiral_coef*center_theta*np.sin(center_theta)
            path[:,axis] = np.linspace(-distance/2.,distance/2.,num_steps)
        return path@self.basis
    
    def evaluation_points(self) -> Float[np.ndarray, "1 m"]:
        return np.array([[self.spiral_coef*self.theta_max/2.*np.cos(self.theta_max/2.),self.spiral_coef*self.theta_max/2.*np.sin(self.theta_max/2.)]+[0 for _ in range(self.intrinsic_dim-1)]])@self.basis