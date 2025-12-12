from jaxtyping import Float
import numpy as np
from datasets import load_dataset
import torchvision.transforms as transforms

class MNIST:
    """
    Generates samples from MNIST
    """
    def __init__(self,
        n_points: int=None,
        image_size: int=None,
        rng: np.random.Generator=np.random.default_rng(),
    ):
        self.n_points = n_points
        self.rng = rng
        self.dataset = load_dataset("ylecun/MNIST",split="train").rename_column("image","points").shuffle(generator=rng)
        if n_points is not None:
            self.dataset = self.dataset.select(range(n_points))
        if image_size is not None:
            resize_transform = transforms.Compose([
                transforms.Resize((image_size, image_size)),
            ])
            def resize_image(example):
                image = example["points"]
                image = resize_transform(image)
                example["points"] = image
                return example
            self.dataset = self.dataset.map(resize_image)
