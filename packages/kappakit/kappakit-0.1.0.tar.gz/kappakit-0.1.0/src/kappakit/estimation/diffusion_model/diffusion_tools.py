from jaxtyping import Float
from typing import Tuple
import numpy as np
import torch
from tqdm import tqdm
from diffusers import DDPMPipeline
from diffusers.models.unets.unet_2d import UNet2DOutput
from diffusers.utils.torch_utils import randn_tensor
from sklearn.decomposition import PCA
device = "cuda" if torch.cuda.is_available() else "cpu"

def step_deterministic(
    scheduler,
    model_output: torch.Tensor,
    timestep: int,
    sample: torch.Tensor,
    generator=None,
):
    t = timestep

    prev_t = scheduler.previous_timestep(t)

    if model_output.shape[1] == sample.shape[1] * 2 and scheduler.variance_type in ["learned", "learned_range"]:
        model_output, predicted_variance = torch.split(model_output, sample.shape[1], dim=1)
    else:
        predicted_variance = None

    # 1. compute alphas, betas
    alpha_prod_t = scheduler.alphas_cumprod[t]
    alpha_prod_t_prev = scheduler.alphas_cumprod[prev_t] if prev_t >= 0 else scheduler.one
    beta_prod_t = 1 - alpha_prod_t
    beta_prod_t_prev = 1 - alpha_prod_t_prev
    current_alpha_t = alpha_prod_t / alpha_prod_t_prev
    current_beta_t = 1 - current_alpha_t

    # 2. compute predicted original sample from predicted noise also called
    # "predicted x_0" of formula (15) from https://arxiv.org/pdf/2006.11239.pdf
    if scheduler.config.prediction_type == "epsilon":
        pred_original_sample = (sample - beta_prod_t ** (0.5) * model_output) / alpha_prod_t ** (0.5)
    elif scheduler.config.prediction_type == "sample":
        pred_original_sample = model_output
    elif scheduler.config.prediction_type == "v_prediction":
        pred_original_sample = (alpha_prod_t**0.5) * sample - (beta_prod_t**0.5) * model_output
    else:
        raise ValueError(
            f"prediction_type given as {scheduler.config.prediction_type} must be one of `epsilon`, `sample` or"
            " `v_prediction`  for the DDPMScheduler."
        )

    # 3. Clip or threshold "predicted x_0"
    if scheduler.config.thresholding:
        pred_original_sample = scheduler._threshold_sample(pred_original_sample)
    elif scheduler.config.clip_sample:
        pred_original_sample = pred_original_sample.clamp(
            -scheduler.config.clip_sample_range, scheduler.config.clip_sample_range
        )

    # 4. Compute coefficients for pred_original_sample x_0 and current sample x_t
    # See formula (7) from https://arxiv.org/pdf/2006.11239.pdf
    pred_original_sample_coeff = (alpha_prod_t_prev ** (0.5) * current_beta_t) / beta_prod_t
    current_sample_coeff = current_alpha_t ** (0.5) * beta_prod_t_prev / beta_prod_t

    # 5. Compute predicted previous sample µ_t
    # See formula (7) from https://arxiv.org/pdf/2006.11239.pdf
    pred_prev_sample = pred_original_sample_coeff * pred_original_sample + current_sample_coeff * sample

    # 6. Add noise
    variance = 0
    if t > 0:
        device = model_output.device
        variance_noise = randn_tensor(
            model_output.shape, generator=generator, device=device, dtype=model_output.dtype
        )
        if scheduler.variance_type == "fixed_small_log":
            variance = scheduler._get_variance(t, predicted_variance=predicted_variance) * variance_noise
        elif scheduler.variance_type == "learned_range":
            variance = scheduler._get_variance(t, predicted_variance=predicted_variance)
            variance = torch.exp(0.5 * variance) * variance_noise
        else:
            variance = (scheduler._get_variance(t, predicted_variance=predicted_variance) ** 0.5) * variance_noise

    return (
        pred_prev_sample+variance,
        pred_original_sample,
        pred_prev_sample,
    )

def denoise(x_t: Float[np.ndarray, "N m"], pipeline: DDPMPipeline, diffusion_time: int, deterministic: bool) -> Float[np.ndarray, "N m"]:
    x = torch.tensor(x_t).float().to(device)
    for t in range(diffusion_time-1,-1,-1):
        t_tensor = torch.full((x.shape[0],), t, dtype=torch.int64, device=x.device)
        with torch.no_grad():
            noise_pred = pipeline.unet(x, t_tensor)
            if isinstance(noise_pred, UNet2DOutput) or isinstance(noise_pred, tuple):
                noise_pred = noise_pred[0]
        if deterministic:
            x = step_deterministic(pipeline.scheduler, noise_pred, t, x)[2]
        else:
            x = pipeline.scheduler.step(noise_pred, t, x).prev_sample
    return x.cpu().numpy()

def generate_diffusion_samples(eval_point: Float[np.ndarray, "m"], pipeline: DDPMPipeline, num_samples: int, diffusion_distance: float, diffusion_time: int, batch_size: int, rng: np.random.Generator=np.random.default_rng()) -> Float[np.ndarray, "N m"]:
    pipeline.to(device)
    samples = []
    with torch.no_grad():
        for i in range(0,num_samples,batch_size):
            x_0 = np.tile(eval_point[None], (min(batch_size,num_samples-i), *([1] * eval_point.ndim)))
            noise = rng.standard_normal(size=x_0.shape)
            noise /= np.linalg.norm(noise, axis = -1, keepdims=True)
            noise *= rng.uniform(0, diffusion_distance, (noise.shape[0],*([1] * eval_point.ndim)))**(1./np.prod(x_0.shape[1:]))
            x_T = x_0 + noise
            x_denoised = denoise(x_t=x_T, pipeline=pipeline, diffusion_time=diffusion_time, deterministic=True)
            samples.append(x_denoised)
    final_samples = np.concatenate(samples, axis=0)
    return final_samples

def generate_diffusion_samples_basis(eval_point: Float[np.ndarray, "m"], pipeline: DDPMPipeline, basis: Float[np.ndarray, "d m"], num_samples: int, diffusion_distance: float, diffusion_time: int, batch_size: int, rng: np.random.Generator=np.random.default_rng()) -> Float[np.ndarray, "N m"]:
    samples = []
    with torch.no_grad():
        for i in range(0,num_samples,batch_size):
            x_0 = np.tile(eval_point,(min(batch_size,num_samples-i),1))
            noise = rng.standard_normal(size=(x_0.shape[0],basis.shape[0]))
            noise /= np.linalg.norm(noise, axis = -1, keepdims=True)
            noise *= rng.uniform(0, diffusion_distance, (noise.shape[0],1))**(1./basis.shape[0])
            noise = noise @ basis
            x_T = x_0 + noise
            x_denoised = denoise(x_t=x_T, pipeline=pipeline, diffusion_time=diffusion_time, deterministic=True)
            samples.append(x_denoised)
    final_samples = np.concatenate(samples, axis=0)
    return final_samples

def select_elbow(
    singular_values: Float[np.ndarray, "m"],
    method: str = "kneedle",
) -> int: # number of dimensions to keep
    if method=="gap":
        estimated_dimension = np.argmax(np.abs(singular_values[1:]-singular_values[:-1]))+1
    elif method=="derivative":
        explained_variances = np.cumsum(np.square(singular_values),0)/np.sum(np.square(singular_values))
        second_derivative = np.diff(explained_variances,2)
        estimated_dimension = np.argmax(np.abs(second_derivative)[2:])+2+1
    elif method=="kneedle":
        from kneed import KneeLocator
        explained_variances = np.cumsum(np.square(singular_values),0)/np.sum(np.square(singular_values))
        estimated_dimension = round(KneeLocator(range(1,len(explained_variances)+1),explained_variances).knee)
    return estimated_dimension

def obtain_basis(
    manifold: Float[np.ndarray, "N m"],
    intrinsic_dim: int=None,
    method: str = "kneedle",
) -> Tuple[Float[np.ndarray, "m m"], int]:
    pca = PCA().fit(manifold)
    if intrinsic_dim is None:
        intrinsic_dim = select_elbow(pca.singular_values_, method=method)
    return pca.components_, intrinsic_dim