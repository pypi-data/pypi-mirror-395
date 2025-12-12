from jaxtyping import Float, Integer
import numpy as np

def image_type(image: Integer[np.ndarray, "w h ..."]) -> str:
    if image.ndim==2 or (image.ndim==3 and image.shape[2]==1):
        return "grayscale"
    elif image.ndim==3 and image.shape[-1]==3:
        return "rgb"
    elif image.ndim==3 and image.shape[-1]==4:
        return "rgba"
    else:
        raise ValueError(f"Unrecognized image shape: {image.shape}")

def normalize(image: Float[np.ndarray, "w h"]) -> Integer[np.ndarray, "w h"]:
    if image_type(image)=="grayscale":
        normalized_image = (255 * (image - image.min()) / (image.max() - image.min())).astype(int)
        return normalized_image
    else:
        raise ValueError("Expected grayscale image.")

def to_color(image: Integer[np.ndarray, "w h"]) -> Integer[np.ndarray, "w h c"]:
    if image_type(image)=="grayscale":
        return np.repeat(image[:,:,None],3,axis=2) if image.ndim==3 else np.repeat(image[:,:,None],3,axis=2)
    else:
        return image