import os
import time
import jsonargparse
import wandb
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
from kappakit.estimation.diffusion_model.architectures import FullyConnectedNetwork, FCNConfig
from diffusers import UNet2DModel, DDPMScheduler, DDPMPipeline
from datasets import DatasetDict, load_dataset
from torchvision.transforms.v2 import Compose, Resize, ToImage, ToDtype, Normalize
from tqdm import tqdm
import matplotlib.pyplot as plt
from kappakit.plotting.log_utils import get_git_hash
device = "cuda" if torch.cuda.is_available() else "cpu"


def add_dataset_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--dataset.name", type=str, required=True, help="Either a path to an existing numpy file or a name from the manifold library")
    parser.add_argument("--dataset.num_points", type=int, required=False, help="Number of points to train on")

def add_train_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--train.num_epochs", type=int, required=False, default=50, help="Number of epochs to train")
    parser.add_argument("--train.batch_size", type=int, required=False, default=256, help="Batch size")
    parser.add_argument("--train.lr", type=float, required=False, default=0.001, help="Learning rate")
    parser.add_argument("--train.model_architecture", type=str, required=False, default="FCN", help="Model architecture (FCN or UNet)")
    parser.add_argument("--train.ambient_dim", type=int, required=False, help="Ambient dim, if model architecture set to FCN")
    parser.add_argument("--train.num_layers", type=int, required=False, help="Number of layers in FCN, if model architecture set to FCN")
    parser.add_argument("--train.width", type=int, required=False, help="Width of FCN, if model architecture set to FCN")
    parser.add_argument("--train.time_emb_dim", type=int, required=False, default=128, help="Time embed dim, if model architecture set to FCN")
    parser.add_argument("--train.dropout", type=float, required=False, default=0., help="Dropout of FCN, if model architecture set to FCN")

    parser.add_argument("--train.image_size", type=int, required=False, help="Image size, if model architecture set to UNet")
    parser.add_argument("--train.image_channels", type=int, required=False, help="Image channels, if model architecture set to UNet")
    parser.add_argument("--train.layers_per_block", type=int, required=False, default=2, help="ResNet layers per UNet block")
    parser.add_argument("--train.block_out_channels", type=list[int], required=False, default=[64,128,256], help="ResNet layers per UNet block")
    parser.add_argument("--train.save_name", type=str, required=True, help="Save name")
    parser.add_argument("--train.upload_name", type=str, required=False, help="Upload name")

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
    add_dataset_arguments(parser)
    add_train_arguments(parser)
    args = parser.parse_args()
    
    os.makedirs(args.train.save_name, exist_ok=True)
    args.wandb.git_hash = get_git_hash() if get_git_hash() else args.git_hash
    parser.save(args,f"{args.train.save_name}/args.yaml", overwrite=True)
    if args.wandb.enable:
        wandb.init(
            config=args,
            project=args.wandb.project,
            entity=args.wandb.team,
            name=os.path.basename(args.train.save_name),
        )

    if os.path.exists(args.dataset.name):
        train_dataset = DatasetDict.load_from_disk(args.dataset.name)["manifold"].shuffle(seed=args.device.seed)
    else:
        train_dataset = load_dataset(args.dataset.name, split="manifold").shuffle(seed=args.device.seed)
    if args.dataset.num_points:
        train_dataset = train_dataset.select(range(args.dataset.num_points))

    # Create a model
    if args.train.model_architecture=="FCN":
        preprocess = Compose([
            ToDtype(torch.float32,scale=True),
        ])

        def transform(examples):
            examples["points"] = torch.tensor([preprocess(pt) for pt in (examples["points"])])
            return examples
        train_dataset.set_transform(transform)

        train_dataloader = DataLoader(train_dataset, batch_size=args.train.batch_size, shuffle=True)
        
        def compute_mean_std(dataloader):
            """
            Numerically-stable streaming mean/std over [B, D] tensors.
            Uses Chan's parallel/Welford update; applies Bessel's correction (ddof=1).
            """
            n = 0
            mean = None
            M2 = None

            with torch.no_grad():
                for batch in dataloader:
                    x = batch["points"]
                    if not torch.is_tensor(x):
                        x = torch.tensor(x)
                    x = x.to(dtype=torch.float64)

                    # Ensure shape [B, D]
                    if x.ndim > 2:
                        x = x.view(x.shape[0], -1)

                    m = x.shape[0]
                    if m == 0:
                        continue

                    # Per-batch stats
                    batch_mean = x.mean(dim=0)                    # [D]
                    batch_M2   = ((x - batch_mean) ** 2).sum(dim=0)  # [D]

                    if n == 0:
                        mean = batch_mean
                        M2 = batch_M2
                        n = m
                    else:
                        delta = batch_mean - mean                 # [D]
                        tot = n + m
                        mean = mean + delta * (m / tot)
                        M2 = M2 + batch_M2 + (delta ** 2) * (n * m / tot)
                        n = tot
            if n < 2:
                raise ValueError("Need at least 2 samples to compute an unbiased std (n < 2).")
            mean = mean.to(dtype=torch.float32)
            var = (M2 / (n - 1)).to(dtype=torch.float32)
            std = torch.sqrt(torch.clamp(var, min=1e-12))
            return mean, std
        data_mean, data_std = compute_mean_std(train_dataloader)

        model = FullyConnectedNetwork(
            FCNConfig(
                input_dim=args.train.ambient_dim,
                output_dim=args.train.ambient_dim,
                num_layers=args.train.num_layers,
                width=args.train.width,
                time_emb_dim=args.train.time_emb_dim,
                dropout=args.train.dropout,
                data_mean=data_mean.tolist(),
                data_std=data_std.tolist(),
            ),
        )

    elif args.train.model_architecture=="UNet":
        preprocess = Compose([
            ToImage(),
            ToDtype(torch.float32,scale=True),
            Normalize([0.5], [0.5]),
        ])

        def transform(examples):
            examples["points"] = [preprocess(image) for image in (examples["points"])]
            return examples
        train_dataset.set_transform(transform)

        # Create a dataloader from the dataset to serve up the transformed images in batches
        train_dataloader = DataLoader(train_dataset, batch_size=args.train.batch_size, shuffle=True)

        model = UNet2DModel(
            sample_size=args.train.image_size,  # the target image resolution
            in_channels=args.train.image_channels,  # the number of input channels, 3 for RGB images
            out_channels=args.train.image_channels,  # the number of output channels
            layers_per_block=args.train.layers_per_block,  # how many ResNet layers to use per UNet block
            block_out_channels=args.train.block_out_channels,  # the number of output channes for each UNet block
            down_block_types=(
                "DownBlock2D",  # a regular ResNet downsampling block
                "AttnDownBlock2D",  # a ResNet downsampling block with spatial self-attention
                "DownBlock2D",
            ),
            up_block_types=(
                "UpBlock2D",  # a regular ResNet upsampling block
                "AttnUpBlock2D",  # a ResNet upsampling block with spatial self-attention
                "UpBlock2D"
            ),
        )
    else:
        raise ValueError(f"Expected train.model_architecture to be FCN or UNet but got {args.train.model_architecture}")
    model.to(device)

    # Set the noise scheduler
    noise_scheduler = DDPMScheduler(
        num_train_timesteps=1000, beta_schedule="squaredcos_cap_v2", clip_sample=False,
    )

    # Training loop
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.train.lr)
    scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=20, T_mult=1)
    losses = []

    for epoch in range(args.train.num_epochs):
        for step, batch in tqdm(enumerate(train_dataloader),desc=f'Epoch {epoch}',total=len(train_dataloader)):
            clean_images = batch["points"].to(device)
            # Sample noise to add to the images
            noise = torch.randn(clean_images.shape).to(clean_images.device)
            bs = clean_images.shape[0]

            # Sample a random timestep for each image
            timesteps = torch.randint(
                0, noise_scheduler.num_train_timesteps, (bs,), device=clean_images.device
            ).long()

            # Add noise to the clean images according to the noise magnitude at each timestep
            noisy_images = noise_scheduler.add_noise(clean_images, noise, timesteps)

            # Get the model prediction
            if args.train.model_architecture=="FCN":
                noise_pred = model(noisy_images, timesteps, return_dict=False)
            elif args.train.model_architecture=="UNet":
                noise_pred = model(noisy_images, timesteps, return_dict=False)[0]

            # Calculate the loss
            loss = F.mse_loss(noise_pred, noise)
            loss.backward()
            losses.append(loss.item())

            # Update the model parameters with the optimizer
            optimizer.step()
            optimizer.zero_grad()
            scheduler.step(epoch + step / len(train_dataloader))

        if (epoch + 1) % 1 == 0:
            loss_last_epoch = sum(losses[-len(train_dataloader) :]) / len(train_dataloader)
            print(f"Epoch:{epoch+1}, loss: {loss_last_epoch}")
    
    noise_scheduler.save_pretrained(args.train.save_name)
    model.save_pretrained(args.train.save_name)
    if args.train.upload_name is not None:
        model.push_to_hub(args.train.upload_name)

    plt.figure()
    plt.plot()

    pipeline = DDPMPipeline(unet=model,scheduler=noise_scheduler)
    if args.train.model_architecture=="UNet":
        example_generations = pipeline(16).images
        for i,image in enumerate(example_generations):
            image.save(os.path.join(args.train.save_name,f"sample_{i}.png"))

    end_total = time.perf_counter()
    print(f"- Creating {args.train.save_name} took {end_total-start_total} seconds.")

if __name__ == "__main__":
    main()