from tqdm import tqdm
from typing import Union
from jaxtyping import Float, Integer
import numpy as np
from scipy.stats import ortho_group, semicircular

"""
Dataset Conventions:
- d is intrinsic, n is normal, m is ambient: d+n=m
- Dataset classes will ask for d,m and compute n itself
- Noise is added to the final manifold by adding + s*N(0,I_m)/sqrt(d)
(so will be on average be s away, as mean of chi-distribution is like sqrt(n)
- N is the number of points
- k is the rank
- Generator is a numpy generator, we always generate in numpy then cast to torch

anchor_points gives two points for interpolation curves and the perfect interpolation between the two
evaluation_points gives good landmark points to evaluate curvature at
"""

class Paraboloid:
    """
    Generates samples around a paraboloid described by second fundamental form at the vertex.
    This is uniform in the ball spanned by the intrinsic dimension but not in the normal dimensions.

    General equation of a paraboloid is :math:`y=x^THx`. H is the second fundamental form.

    SFF can be given in any of the following forms:
    - Float[np.ndarray, "d d n"]: the full SFF
    - Float[np.ndarray, "d n"]: list of d eigenvalues for each n normal direction; 
        since SFF symmetric, orthogonal eigenvectors are randomly generated uniformly over O(N)
        and created via diagonalization SFF=UDU^T.
    - Integer[np.ndarray, "n"]: list of ranks for each n normal direction;
        eigenvalues are generated according to the Wigner semicirclular distribution with support [-3,3]
        (limiting eigenvalue distribution of random symmetric matrices)
    - int: one rank for all n normal dimensions
    """
    def __init__(self,
        n_points: int,
        intrinsic_dim: int,
        ambient_dim: int,
        sff: Union[
            Float[np.ndarray, "d d n"],
            Float[np.ndarray, "d n"],
            Integer[np.ndarray, "n"],
            int,
        ],
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

        if isinstance(sff, int): # one rank for all n normal dimensions
            rank = sff
            eigenvalues: Float[np.ndarray, "d n"] = np.stack([np.concatenate((
                semicircular.rvs(scale=3,size=rank,random_state=self.rng),
                np.zeros(self.intrinsic_dim-rank)
            )) for _ in range(self.normal_dim)], axis=0)
            D: Float[np.ndarray, "d d n"] = np.stack([np.diag(eigens) for eigens in eigenvalues], axis=-1)
            U: Float[np.ndarray, "d d n"] = np.stack([ortho_group.rvs(self.intrinsic_dim,random_state=self.rng) for _ in range(self.normal_dim)], axis=-1)
            self.sff: Float[np.ndarray, "d d n"] = np.einsum("ijn,jkn,lkn->iln",U,D,U)
        elif sff.shape==(self.normal_dim,): # rank per normal dimension
            rank = sff
            eigenvalues: Float[np.ndarray, "d n"] = np.array([np.concatenate((
                semicircular.rvs(scale=3,size=rank[i],random_state=self.rng),
                np.zeros(self.intrinsic_dim-rank[i])
            )) for i in range(self.normal_dim)])
            D: Float[np.ndarray, "d d n"] = np.stack([np.diag(eigenvalues[:,i]) for i in range(eigenvalues.shape[1])], axis=-1)
            U: Float[np.ndarray, "d d n"] = np.stack([ortho_group.rvs(self.intrinsic_dim,random_state=self.rng) for _ in range(self.normal_dim)], axis=-1)
            self.sff: Float[np.ndarray, "d d n"] = np.einsum("ijn,jkn,lkn->iln",U,D,U)
        elif sff.shape==(self.intrinsic_dim, self.normal_dim): # eigenvalues per normal dim
            eigenvalues = sff
            D: Float[np.ndarray, "d d n"] = np.stack([np.diag(eigenvalues[:,i]) for i in range(eigenvalues.shape[1])], axis=-1)
            U: Float[np.ndarray, "d d n"] = np.stack([ortho_group.rvs(self.intrinsic_dim,random_state=self.rng) for _ in range(self.normal_dim)], axis=-1)
            self.sff: Float[np.ndarray, "d d n"] = np.einsum("ijn,jkn,lkn->iln",U,D,U)
        elif sff.shape==(self.intrinsic_dim, self.intrinsic_dim, self.normal_dim): # sff
            self.sff = sff
        else:
            raise ValueError(f"SFF input format not recognized (got {sff}).")
        # Generate ball on intrinsic dimensions
        self.points: Float[np.ndarray, "N d"] = self.rng.standard_normal((self.n_points-1, self.intrinsic_dim))
        self.points /= np.linalg.norm(self.points, axis = -1, keepdims=True)
        self.points *= (self.rng.uniform(0, self.radius, self.n_points-1)**(1./self.intrinsic_dim)).reshape(-1,1)
        self.points = np.concatenate([np.zeros((1,self.intrinsic_dim)),self.points],axis=0)

        # Use SFF to generate paraboloid in normal dimensions
        paraboloid = np.zeros((self.n_points,self.normal_dim))
        batch_size = 100000
        for offset in tqdm(range(0, self.n_points, batch_size)):
            paraboloid[offset:offset+batch_size] = np.einsum('Ni,ijn,Nj->Nn', self.points[offset:offset+batch_size], self.sff/2., self.points[offset:offset+batch_size])
        self.points = np.concatenate((self.points,paraboloid),axis=1)

        # Embed in ambient dimension
        if skip_basis:
            self.basis: Float[np.ndarray, "m m"] = np.eye(self.ambient_dim)[:self.points.shape[1]]
        else:
            self.basis: Float[np.ndarray, "m m"] = ortho_group.rvs(self.ambient_dim, random_state=self.rng)[:self.points.shape[1]]
        self.points: Float[np.ndarray, "N m"] = self.points@self.basis
        self.tangent_basis = np.tile(self.basis,(self.n_points,1))

        # Add noise
        self.points += self.noise*self.rng.standard_normal((self.n_points, self.ambient_dim))/np.sqrt(self.ambient_dim)
        print(self.points[0])

    def __len__(self) -> int:
        return self.n_points

    def __getitem__(self, idx: int) -> Float[np.ndarray, "m"]:
        return self.points[idx]
    
    def path(self,
        distance: float,
        axis: int=0,
        intrinsic_axis: int=None,
        normal_axis: int=None,
        num_steps: int=100,
    ) -> Float[np.ndarray, "N m"]:
        if intrinsic_axis is not None and normal_axis is not None:
            eigenvectors: Float[np.ndarray, "d d n"] = np.linalg.eigh(self.sff.transpose(2,0,1))[1].transpose(1,2,0)
            path = np.stack([eigenvectors[:,intrinsic_axis,normal_axis]*step for step in np.linspace(distance/2.,-distance/2.,num_steps)],axis=0)
        else:
            path = np.concatenate([np.eye(self.intrinsic_dim,M=1,k=-axis).T*step for step in np.linspace(distance/2.,-distance/2.,num_steps)],axis=0)
        path = np.concatenate([path,np.einsum('Ni,ijn,Nj->Nn', path, self.sff, path)],axis=1)
        return path@self.basis
    
    def evaluation_points(self) -> Float[np.ndarray, "1 m"]:
        return np.zeros((1,self.ambient_dim))