from typing import Tuple, Callable
from jaxtyping import Float, Integer
import numpy as np

class ColorspaceSphere:
    """
    Generates samples from the manifold characterized by a color sampled from the sphere within the cube of possible colors (0-255), where a single square block of this color can be anywhere in an otherwise black image.
    This is two-dimensional
    ambient_dim is width*height*3
    """
    def __init__(self,
        n_points: int,
        image_size: Tuple[int,int],
        radius: float=255/2.,
        noise: float=0.,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.image_size = image_size
        self.radius = radius
        self.noise = noise
        self.rng = rng

        # Generate image
        self.points = np.zeros((n_points,*self.image_size,3))
        self.colors: Float[np.ndarray, "N 3"] = self.rng.standard_normal((self.n_points, 3))
        self.colors = self.radius * self.colors / np.linalg.norm(self.colors, axis = -1, keepdims=True) + np.array([255/2.,255/2.,255/2.])
        self.colors = self.colors.astype(int)
        self.positions: Integer[np.ndarray, "N 2"] = np.stack([np.arange(self.n_points),self.rng.integers(0,self.image_size[0],size=self.n_points),self.rng.integers(0,self.image_size[1],size=self.n_points)],axis=1)
        self.points[self.positions[:,0],self.positions[:,1],self.positions[:,2]] = self.colors
        
        # Add noise
        self.points += (self.noise*self.rng.standard_normal((self.n_points, *self.image_size,3))/np.sqrt(np.prod(self.image_size)*3)).astype(int)

    def __len__(self) -> int:
        return self.n_points

    def __getitem__(self, idx: int) -> Float[np.ndarray, "m"]:
        return self.points[idx]
    
    def path(self,
        distance: float,
        num_steps: int=100
    ) -> Float[np.ndarray, "N w h 3"]:
        theta = distance/self.radius
        path = np.array([[self.radius*np.cos(angle),self.radius*np.sin(angle)]+[0. for _ in range(self.intrinsic_dim-1)] for angle in np.linspace(theta/2,-theta/2,num_steps)])
        return path@self.basis

    def evaluation_points(self) -> Float[np.ndarray, "1 w h 3"]:
        return self.points[:1]

def get_colorspace_embedding(
    dataset: Float[np.ndarray, "N 3"],
    image_size: Tuple[int,int],
    embedding_mode: str="pixel",
) -> Callable[[Float[np.ndarray, "N 3"]], Integer[np.ndarray, "N w h 3"]]:
    """Return a function to embed any manifold in 3-dimensions into the colorspace of an image"""
    if embedding_mode=="pixel":
        def colorspace_embedding(input_dataset: Float[np.ndarray, "N 3"], rng: np.random.Generator=np.random.default_rng()) -> Integer[np.ndarray, "N w h 3"]:
            n_points = input_dataset.shape[0]
            colors = (255*(input_dataset-dataset.min(axis=0))/(dataset.max(axis=0)-dataset.min(axis=0))).astype(int)
            points = np.zeros((n_points,*image_size,3))
            positions = np.stack([np.arange(n_points),rng.integers(0,image_size[0],size=n_points),rng.integers(0,image_size[1],size=n_points)],axis=1)
            points[positions[:,0],positions[:,1],positions[:,2]] = colors
            return points
        return colorspace_embedding
    else:
        raise ValueError(f"Embedding mode not supported (got {embedding_mode}).")