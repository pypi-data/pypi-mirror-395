from jaxtyping import Float
from typing import Optional
import os
import time
import re
import jsonargparse
import wandb
import PIL
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from diffusers import UNet2DModel, DDPMScheduler, DDPMPipeline
from datasets import Dataset, DatasetDict, load_dataset
from torchvision.transforms.v2 import Compose, Resize, ToImage, ToDtype, Normalize
from kappakit.plotting.log_utils import get_git_hash
from kappakit.estimation.diffusion_model.diffusion_tools import generate_diffusion_samples
device = "cuda" if torch.cuda.is_available() else "cpu"


def add_upsample_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--upsample.dataset", type=str, required=True, help="Dataset from create_dataset")
    parser.add_argument("--upsample.model", type=str, required=True, help="Trained diffusion model name")
    parser.add_argument("--upsample.x_0", type=str, required=True, help="Point to upsample from")
    parser.add_argument("--upsample.num_points", type=int, required=False, default=10000, help="Number of points to sample")
    parser.add_argument("--upsample.diffusion_distance", type=float, required=False, default=1., help="Distance to noise")
    parser.add_argument("--upsample.timestep", type=int, required=False, default=50, help="Number of timesteps away to denoise from")
    parser.add_argument("--upsample.batch_size", type=int, required=False, default=256, help="Batch size in upsampling")
    parser.add_argument("--upsample.save_name", type=str, required=True, help="Save name for upsampled")
    parser.add_argument("--upsample.upload_name", type=str, required=False, help="Upload to hub")

def add_device_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--device.seed", type=int, required=False, default=220, help="Random seed")

def add_wandb_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--wandb.enable", type=bool, required=False, default=False, help="Use wandb")
    parser.add_argument("--wandb.project", type=str, required=False, default="kappakit", help="Wandb project name")
    parser.add_argument("--wandb.team", type=str, required=False, default=None, help="Wandb team name")
    parser.add_argument("--wandb.git_hash", type=str, required=False, help="Git hash; will be overwritten if in git repo")

def main():
    start_total = time.perf_counter()
    parser = jsonargparse.ArgumentParser()
    parser.add_argument("--config", action="config")  
    parser.add_argument("--tag", type=str, required=False, help="If using default name, add more information of your choice")
    add_device_arguments(parser)
    add_wandb_arguments(parser)
    add_upsample_arguments(parser)
    args = parser.parse_args()
    rng = np.random.default_rng(args.device.seed)
    
    os.makedirs(args.upsample.save_name, exist_ok=True)
    args.wandb.git_hash = get_git_hash() if get_git_hash() else args.git_hash
    parser.save(args,f"{args.upsample.save_name}/args.yaml", overwrite=True)
    if args.wandb.enable:
        wandb.init(
            config=args,
            project=args.wandb.project,
            entity=args.wandb.team,
            name=os.path.basename(args.upsample.save_name),
        )

    train_dataset = DatasetDict.load_from_disk(args.upsample.dataset)["manifold"].shuffle(seed=args.device.seed)
    preprocess = Compose([
        ToImage(),
        ToDtype(torch.float32,scale=True),
        Normalize([0.5], [0.5]),
    ])
    def transform(examples):
        examples["points"] = [preprocess(image) for image in (examples["points"])]
        return examples
    train_dataset.set_transform(transform)
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=1, shuffle=False)

    if args.upsample.x_0=="random": # Get first sample
        x_0 = next(iter(train_dataloader))["points"]
    elif re.match(r"label_(.*)",args.upsample.x_0): # Interpret as first instance of specific label
        m = re.match(r"label_(.*)",args.upsample.x_0)
        for batch in train_dataloader:
            if str(batch["label"][0].item())==m.group(1):
                x_0 = batch["points"][0]
                break
    else: # Interpret as path
        x_0 = preprocess(PIL.Image.open(args.upsample.x_0))
    img_array = ((x_0*0.5+0.5).squeeze().numpy()*255).astype(np.uint8)
    if img_array.shape[0]==3:
        img_array = img_array.transpose(1,2,0)
    PIL.Image.fromarray(img_array).save(os.path.join(args.upsample.save_name,"x_0.png"))

    pipeline = DDPMPipeline(UNet2DModel.from_pretrained(args.upsample.model),DDPMScheduler.from_pretrained(args.upsample.model))
    samples = generate_diffusion_samples(
        eval_point=x_0,
        pipeline=pipeline,
        num_samples=args.upsample.num_points,
        diffusion_distance=args.upsample.diffusion_distance,
        diffusion_time=args.upsample.timestep,
        batch_size=args.upsample.batch_size,
        rng=rng,
    )
    samples = np.concatenate((x_0[None,...],samples),axis=0)
    samples = samples.reshape(samples.shape[0], -1)
    dataset_dict = DatasetDict({
        "manifold": Dataset.from_dict({"points":samples}),
    })
    dataset_dict.save_to_disk(args.upsample.save_name)
    if args.upsample.upload_name is not None:
        dataset_dict.push_to_hub(args.upsample.upload_name)

    end_total = time.perf_counter()
    print(f"- Creating {args.upsample.save_name} took {end_total-start_total} seconds.")

if __name__ == "__main__":
    main()