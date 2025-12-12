from typing import Tuple
from jaxtyping import Float
import math
import numpy as np
import torch
from diffusers import DDPMPipeline
from kappakit.estimation.diffusion_model.diffusion_tools import step_deterministic
device = "cuda" if torch.cuda.is_available() else "cpu"

class FSInterpolationPath:
    """
    Draws interpolation paths from trained diffusion model and computes Frenet-Serret curvatures
    """
    @staticmethod
    def interpolate(
        pipeline: DDPMPipeline,
        eval_point: Float[np.ndarray, "m"],
        tangent: Float[np.ndarray, "m"],
        distance: float,
        num_interpolants: int,
        diffusion_time: int,
    ) -> Tuple[
        Float[np.ndarray,"m-1"],
        Float[np.ndarray,"N m"],
    ]:
        tangent = tangent/np.linalg.norm(tangent)
        x_t = torch.tensor(np.tile(eval_point,(num_interpolants,1)) + distance*np.linspace(-1,1,num_interpolants)[:,None]*np.tile(tangent,(num_interpolants,1))).float()
        for timestep in range(diffusion_time,0,-1):
            residuals = pipeline.unet(x_t.to(device),torch.LongTensor([timestep]).to(device)).detach().cpu()
            x_t = step_deterministic(pipeline.scheduler,residuals,torch.LongTensor([timestep]),x_t)[2]
        fs_curvatures = frenet_serret_by_finite_diff(x_t)
        fs_curvatures = np.nanmean(fs_curvatures[0,math.floor(num_interpolants*0.25):math.ceil(num_interpolants*0.75)])
        return fs_curvatures, x_t

def frenet_serret_by_finite_diff(curve: Float[np.ndarray, "N d"]) -> Float[np.ndarray, "N d-1"]:
    # Gradients is (T,dth derivative,d) 
    T = np.cumsum(np.linalg.norm(np.gradient(curve,axis=0),axis=1))
    gradients = [np.gradient(curve,T,axis=0)]
    for dim in range(curve.shape[1]-1):
        gradients.append(np.gradient(gradients[-1],T,edge_order=1,axis=0))
    gradients = np.array(gradients).transpose((1,0,2))

    # Gram-Schmidt
    frame = np.zeros_like(gradients)
    normalized_frame = np.zeros_like(gradients)
    for dim in range(curve.shape[1]):
        frame[:,dim,:] = gradients[:,dim,:]-np.sum([np.einsum("ti,ti->t",gradients[:,dim,:],frame[:,i,:])[:,None]*frame[:,i,:]for i in range(dim)],axis=0)
        normalized_frame[:,dim,:] = frame[:,dim,:]/np.linalg.norm(frame[:,dim,:],axis=1)[:,None]

    curvature = np.array([np.einsum("ti,ti->t",np.gradient(normalized_frame[:,i],T,edge_order=1,axis=0),normalized_frame[:,i+1]) for i in range(curve.shape[1]-1)])
    return curvature