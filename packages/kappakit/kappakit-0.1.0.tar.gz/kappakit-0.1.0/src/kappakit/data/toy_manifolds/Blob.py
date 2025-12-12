from typing import Tuple
from jaxtyping import Float
import numpy as np
from scipy.stats import multivariate_normal
from ...plotting.image_utils import normalize

class Blob:
    """
    Generates samples from the image blob synthetic dataset from Stanczuk et al. 2023 (https://arxiv.org/pdf/2212.12611).
    Note this is a linear manifold
    intrinsic_dim is the number of blobs
    ambient_dim is width*height
    blob_size is the range of blob sizes uniformly sampled
    """
    def __init__(self,
        n_points: int,
        num_blobs: int,
        blob_type: str,
        image_size: Tuple[int,int],
        blob_size_range: Tuple[float,float],
        noise: float=0.,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.num_blobs = num_blobs
        self.blob_type = blob_type
        self.image_size = image_size
        self.blob_size_range = blob_size_range
        self.noise = noise
        self.rng = rng

        # Generate image
        self.points = np.zeros((n_points,*self.image_size))
        self.blob_centers = np.stack([self.rng.integers(0,image_size[0],size=self.num_blobs),self.rng.integers(0,image_size[1],size=self.num_blobs)],axis=1)
        if self.blob_type=="square":
            self.blob_sizes = self.rng.integers(*self.blob_size_range,endpoint=True,size=self.num_blobs)
            self.representations = self.rng.uniform(0,1,size=(self.n_points,self.num_blobs))
            self.points = np.stack([Blob.create_square_blob_image(
                blob_values=self.representations[i],
                blob_centers=self.blob_centers,
                blob_sizes=self.blob_sizes,
                image_size=self.image_size,
            ) for i in range(self.n_points)],axis=0)
        elif self.blob_type=="gaussian":
            self.representations = self.rng.uniform(*self.blob_size_range,size=(self.n_points,self.num_blobs))
            self.points = np.stack([Blob.create_gaussian_blob_image(
                blob_values=self.representations[i],
                blob_centers=self.blob_centers,
                image_size=self.image_size,
            ) for i in range(self.n_points)],axis=0)
        else:
            raise ValueError(f"Expected blob_type to be 'square' or 'gaussian' (got {self.blob_type}).")
        
        # Add noise
        self.points += (self.noise*self.rng.standard_normal((self.n_points, *self.image_size))/np.sqrt(np.prod(self.image_size))).astype(int)

    def __len__(self) -> int:
        return self.n_points

    def __getitem__(self, idx: int) -> Float[np.ndarray, "m"]:
        return self.points[idx]
    
    def path(self,
        distance: float,
        blob: int=0,
        num_steps: int=100
    ) -> Float[np.ndarray, "N w h"]:
        if self.blob_type=="square":
            return np.stack([Blob.create_square_blob_image(
                blob_values=self.representations[0]+step*np.eye(self.num_blobs,M=1,k=-blob),
                blob_centers=self.blob_centers,
                blob_sizes=self.blob_sizes,
                image_size=self.image_size,
            ) for step in np.linspace(distance/2.,-distance/2.,num_steps)],axis=0)
        elif self.blob_type=="gaussian":
            return np.stack([Blob.create_gaussian_blob_image(
                blob_values=self.representations[0]+step*np.eye(self.num_blobs,M=1,k=-blob),
                blob_centers=self.blob_centers,
                blob_sizes=self.blob_sizes,
                image_size=self.image_size,
            ) for step in np.linspace(distance/2.,-distance/2.,num_steps)],axis=0)
        else:
            raise ValueError(f"Expected blob_type to be 'square' or 'gaussian' (got {self.blob_type}).")

    def evaluation_points(self) -> Float[np.ndarray, "d w h"]:
        return self.points[self.blob_centers]
    
    @staticmethod
    def create_square_blob_image(blob_values: Float[np.ndarray, "d"], blob_centers: Float[np.ndarray, "d 2"], blob_sizes: Float[np.ndarray, "d"], image_size: Tuple[int,int]):
        image = np.zeros(image_size)
        xx, yy = np.meshgrid(np.arange(image_size[0]), np.arange(image_size[1]))
        for i in range(blob_centers.shape[0]):
            mask = (blob_centers[i][0] - np.floor((blob_sizes[i]-1)/2.) <= xx) & (xx < blob_centers[i][0] + np.ceil((blob_sizes[i]-1)/2.)) & (blob_centers[i][1] - np.floor((blob_sizes[i]-1)/2.) <= yy) & (yy < blob_centers[i][1] + np.ceil((blob_sizes[i]-1)/2.))
            image += blob_values[i]*mask
        return normalize(image)

    @staticmethod
    def create_gaussian_blob_image(blob_values: Float[np.ndarray, "d"], blob_centers: Float[np.ndarray, "d 2"], image_size: Tuple[int,int]):
        image = np.zeros(image_size)
        xx, yy = np.meshgrid(np.arange(image_size[0]), np.arange(image_size[1]))
        for i in range(blob_centers.shape[0]):
            blob = multivariate_normal(blob_centers[i],np.identity(2)*blob_values[i])
            image += blob.pdf(np.stack((xx,yy),axis=2))
        return normalize(image)