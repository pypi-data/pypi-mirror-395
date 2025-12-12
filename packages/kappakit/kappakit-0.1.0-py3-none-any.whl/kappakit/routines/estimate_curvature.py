import os
import time
from typing import Union
from itertools import product
import jsonargparse
import wandb
import numpy as np
from tqdm import tqdm
import torch
from datasets import load_dataset, DatasetDict, Dataset
from diffusers import UNet2DModel, DDPMScheduler, DDPMPipeline
from kappakit.estimation.regression import SFFRegressor
from kappakit.estimation.diffusion_map import SFFDiffusionMap
from kappakit.estimation.interpolation import FSInterpolationPath
from kappakit.estimation.diffusion_model.diffusion_tools import generate_diffusion_samples, generate_diffusion_samples_basis, select_elbow, obtain_basis
from kappakit.estimation.diffusion_model.architectures import FullyConnectedNetwork
from kappakit.curvature import *
from kappakit.plotting.visualize import visualize_2d, visualize_3d, visualize_image_grid
from kappakit.plotting.log_utils import get_git_hash, clean_filename
device = "cuda" if torch.cuda.is_available() else "cpu"

def add_dataset_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--dataset.name", type=str, required=True, help="Dataset name")
    parser.add_argument("--dataset.num_samples", type=int, required=False, help="Number of data points to take from the dataset")
    parser.add_argument("--dataset.eval_mode", type=str, required=False, help="Evaluation mode: 'all' for all points, integer n for first n points, str filepath to numpy, or unspecified for dataset's default")

    parser.add_argument("--output.name", type=str, required=False, help="Output results path")
    parser.add_argument("--output.tag", type=str, required=False, help="Tag to append to default output path")

def add_method_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--method.name", type=str, required=True, help="Name of curvature estimation method")

    parser.add_argument("--regression.num_neighbors", type=Union[list[int],int], required=False, help="Number of points to get quadratic neighborhood")
    parser.add_argument("--regression.radius", type=Union[list[float],float], required=False, help="Radius to get quadratic neighborhood")
    parser.add_argument("--regression.intrinsic_dim", type=int, required=False, help="Intrinsic dimension of manifold")
    parser.add_argument("--regression.compute_basis", type=bool, required=False, default=True, help="Whether to compute basis change")
    parser.add_argument("--regression.pca_num_neighbors", type=Union[list[int],int], required=False, help="Number of points to get linear neighborhood")
    parser.add_argument("--regression.pca_radius", type=Union[list[float],float], required=False, help="Radius to get linear neighborhood")
    parser.add_argument("--regression.num_tangents", type=int, required=False, help="Number of tangent dimensions to compute sff for")
    parser.add_argument("--regression.num_normals", type=int, required=False, help="Number of normal dimensions to compute sff for")
    parser.add_argument("--regression.method", type=str, required=False, default="numpy", help="Regression method")
    parser.add_argument("--regression.eval_split", type=float, required=False, default=0., help="Eval split proportion")
    parser.add_argument("--regression.rank", type=int, required=False, help="Low rank assumption (defaults to full rank)")
    parser.add_argument("--regression.num_trials", type=int, required=False, default=1, help="Number of trials for gradient descent")
    parser.add_argument("--regression.num_epochs", type=int, required=False, default=300, help="Number of epochs to fit for")
    parser.add_argument("--regression.manopt_iters", type=int, required=False, default=8000, help="Max number of iterations to fit manopt for")
    parser.add_argument("--regression.learning_rate", type=float, required=False, default=0.1, help="Learning rate")
    parser.add_argument("--regression.batch_size", type=int, required=False, help="Evaluation batch size")
    parser.add_argument("--regression.batch_normal", type=int, required=False, help="Batch size to compute several normal dimensions at once")

    parser.add_argument("--regression.pca_batch_size", type=int, required=False, default=1, help="PCA batch size")
    parser.add_argument("--regression.min_pca_points", type=int, required=False, help="PCA min points")
    parser.add_argument("--regression.min_pca_radius", type=float, required=False, help="PCA min radius")
    parser.add_argument("--regression.max_pca_points", type=int, required=False, help="PCA max points")
    parser.add_argument("--regression.max_pca_radius", type=float, required=False, help="PCA max radius")
    parser.add_argument("--regression.pca_bandwidth", type=float, required=False, help="PCA bandwidth")
    parser.add_argument("--regression.reg_batch_size", type=int, required=False, default=1, help="Regression batch size")
    parser.add_argument("--regression.min_reg_points", type=int, required=False, help="Regression min points")
    parser.add_argument("--regression.min_reg_radius", type=float, required=False, help="Regression min radius")
    parser.add_argument("--regression.max_reg_points", type=int, required=False, help="Regression max points")
    parser.add_argument("--regression.max_reg_radius", type=float, required=False, help="Regression max radius")

    parser.add_argument("--regression.model_path", type=str, required=False, help="Path to trained diffusion model")
    parser.add_argument("--regression.model_type", type=str, required=False, help="Model type; FCN or UNet")
    parser.add_argument("--regression.diffusion_distance", type=float, required=False, help="Magnitude of noise to add")
    parser.add_argument("--regression.diffusion_time", type=int, required=False, default=100, help="Number of timesteps to denoise")
    parser.add_argument("--regression.num_interpolants", type=int, required=False, default=100, help="Number of points to generate")

    parser.add_argument("--diffusion_map.intrinsic_dim", type=int, required=False, help="Intrinsic dimension of manifold")
    parser.add_argument("--diffusion_map.num_eigenfunctions", type=int, required=False, default=50, help="Number of eigenfunctions to preserve in diffusion map")
    parser.add_argument("--diffusion_map.c", type=float, required=False, default=0, help="Diffusion map c parameter")
    parser.add_argument("--diffusion_map.num_neighbors", type=int, required=False, default=32, help="Number of neighbors for KNN")
    parser.add_argument("--diffusion_map.initial_bandwidth_num_neighbors", type=int, required=False, default=8, help="Number of neighbors to compute initial bandwidth")

    parser.add_argument("--interpolation.model_path", type=str, required=False, help="Path to trained diffusion model")
    parser.add_argument("--interpolation.model_type", type=str, required=False, help="Model type; FCN or UNet")
    parser.add_argument("--interpolation.distance", type=float, required=False, help="Distance of geodesic")
    parser.add_argument("--interpolation.use_true_tangents", type=bool, required=False, help="Use principal directions given by ground truth SFF")
    parser.add_argument("--interpolation.num_interpolants", type=int, required=False, default=100, help="Number of interpolation steps")
    parser.add_argument("--interpolation.diffusion_time", type=int, required=False, default=100, help="Number of timesteps to denoise")
    parser.add_argument("--interpolation.num_neighbors", type=int, required=False, help="Number of neighbors for local PCA")
    parser.add_argument("--interpolation.radius", type=float, required=False, help="Radius for local PCA")
    parser.add_argument("--interpolation.intrinsic_dim", type=int, required=False, help="Radius for local PCA")

def add_device_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--device.seed", type=int, required=False, default=220, help="Random seed")

def add_wandb_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--wandb.enable", type=bool, required=False, default=False, help="Use wandb")
    parser.add_argument("--wandb.project", type=str, required=False, default="kappakit", help="Wandb project name")
    parser.add_argument("--wandb.team", type=str, required=False, default=None, help="Wandb team name")
    parser.add_argument("--wandb.git_hash", type=str, required=False, help="Git hash; will be overwritten if in git repo")

def main():
    start_total = time.perf_counter()
    ####################################################################################################
    # 0. SETUP
    ####################################################################################################
    parser = jsonargparse.ArgumentParser()
    parser.add_argument("--config", action="config")  
    add_device_arguments(parser)
    add_wandb_arguments(parser)
    add_dataset_arguments(parser)
    add_method_arguments(parser)
    args = parser.parse_args()
    rng = np.random.default_rng(args.device.seed)
    
    if args.output.name is None:
        args.output.name = clean_filename(
            (f"{args.dataset.name}__{args.method.name}") + 
            (f"__tag={args.output.tag}" if args.output.tag is not None else "")
        )
        args.output.name = os.path.join("results", args.output.name)

    os.makedirs(args.output.name, exist_ok=True)
    args.wandb.git_hash = get_git_hash() if get_git_hash() else args.git_hash
    parser.save(args,f"{args.output.name}/args.yaml", overwrite=True)
    if args.wandb.enable:
        wandb.init(
            config=args,
            project=args.wandb.project,
            entity=args.wandb.team,
            name=os.path.basename(args.experiment_name),
        )
    ####################################################################################################
    # 1. LOAD DATASET
    ####################################################################################################
    print("Loading Data")
    start = time.perf_counter()

    if os.path.exists(args.dataset.name):
        dataset_dict = DatasetDict.load_from_disk(args.dataset.name)
    else:
        dataset_dict = load_dataset(args.dataset.name)
    
    manifold = dataset_dict["manifold"].with_format("numpy")["points"] if args.dataset.num_samples is None else dataset_dict["manifold"].select(range(args.dataset.num_samples)).with_format("numpy")["points"]
    all_tangent_basis = dataset_dict["tangent_basis"].with_format("numpy")["points"] if "tangent_basis" in dataset_dict else None
    # geodesic = dataset_dict["geodesic"].with_format("numpy")["points"]

    if args.dataset.eval_mode is None:
        eval_points = dataset_dict["eval_points"].with_format("numpy")["points"] if "eval_points" in dataset_dict else manifold
    elif args.dataset.eval_mode=="all":
        eval_points = manifold
    elif args.dataset.eval_mode.isdigit():
        eval_points = manifold[:int(args.dataset.eval_mode)]
    elif os.path.exists(args.dataset.eval_mode):
        eval_points = np.load(args.dataset.eval_mode)
    
    if manifold.ndim>2:
        manifold = manifold.reshape(manifold.shape[0],-1)
        eval_points = eval_points.reshape(eval_points.shape[0],-1)
    
    end = time.perf_counter()
    print(f"- Dataset loading took {end-start} seconds.")
    ####################################################################################################
    # 2. COMPUTE CURVATURE
    ####################################################################################################
    print("Computing Curvature")
    start = time.perf_counter()

    if args.method.name=="regression":
        sffs = []
        metrics = []
        nbhds = []
        pcs = []
        preds = []
        hyperparam_grid = [
            dict(
                num_neighbors=nn,
                radius=r,
                pca_num_neighbors=pn,
                pca_radius=pr,
            )
            for nn, r, pn, pr in product(
                args.regression.num_neighbors if isinstance(args.regression.num_neighbors,list) else [args.regression.num_neighbors],
                args.regression.radius if isinstance(args.regression.radius,list) else [args.regression.radius],
                args.regression.pca_num_neighbors if isinstance(args.regression.pca_num_neighbors,list) else [args.regression.pca_num_neighbors],
                args.regression.pca_radius if isinstance(args.regression.pca_radius,list) else [args.regression.pca_radius],
            )
        ]
        for i,eval_point in enumerate(tqdm(eval_points)):
            best_sff = None
            best_r2 = -float("inf")
            best_mse = float("inf")
            best_nbhd = None
            best_pc = None
            for hparams in hyperparam_grid:
                sff, r2, mse, nbhd, pc, pred = SFFRegressor.regress_sff(
                    eval_point=eval_point,
                    manifold=manifold,
                    **hparams,
                    # num_neighbors=args.regression.num_neighbors,
                    # radius=args.regression.radius,
                    intrinsic_dim=args.regression.intrinsic_dim,
                    compute_basis=args.regression.compute_basis,
                    # pca_num_neighbors=args.regression.pca_num_neighbors,
                    # pca_radius=args.regression.pca_radius,
                    num_tangents=args.regression.num_tangents,
                    num_normals=args.regression.num_normals,
                    method=args.regression.method,
                    eval_split=args.regression.eval_split,
                    rng=rng,
                    num_trials=args.regression.num_trials,
                    num_epochs=args.regression.num_epochs,
                    learning_rate=args.regression.learning_rate,
                    rank=args.regression.rank,
                    manopt_iters=args.regression.manopt_iters,
                    batch_size=args.regression.batch_size,
                    batch_normal=args.regression.batch_normal,
                    return_stats=True,
                    verbose=(i==len(eval_points)-1),
                )
                if r2 >= best_r2:
                    best_sff = sff
                    best_r2 = r2
                    best_mse = mse
                    best_nbhd = nbhd
                    best_pc = pc
                    best_pred = pred
            sffs.append(best_sff)
            metrics.append([best_r2,best_mse])
            nbhds.append(best_nbhd)
            pcs.append(best_pc)
            preds.append(best_pred)
        result = Dataset.from_dict({"points": eval_points,"sffs": sffs, "regression_metrics": metrics})
        result.save_to_disk(args.output.name)
        if manifold.ndim==2 and manifold.shape[1]==2:
            visualize_2d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                ],
                marker_size=[2,8],
                save_name=f"{args.output.name}/curvature",
            )
        elif manifold.ndim==2 and manifold.shape[1]==3:
            visualize_3d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                    ("Local",nbhds[-1]),
                    ("PC",pcs[-1]),
                    ("Pred",preds[-1]),
                ],
                marker_size=[2,8,2,2,2],
                save_name=f"{args.output.name}/curvature",
            )
    elif args.method.name=="regression_auto":
        sffs = []
        metrics = []
        nbhds = []
        pcs = []
        preds = []
        for i,eval_point in enumerate(tqdm(eval_points)):
            sff, r2, mse, nbhd, pc, pred = SFFRegressor.regress_sff_auto(
                eval_point=eval_point,
                manifold=manifold,
                intrinsic_dim=args.regression.intrinsic_dim,
                compute_basis=args.regression.compute_basis,
                pca_batch_size=args.regression.pca_batch_size,
                min_pca_points=args.regression.min_pca_points,
                min_pca_radius=args.regression.min_pca_radius,
                max_pca_points=args.regression.max_pca_points,
                max_pca_radius=args.regression.max_pca_radius,
                pca_bandwidth=args.regression.pca_bandwidth,
                reg_batch_size=args.regression.reg_batch_size,
                min_reg_points=args.regression.min_reg_points,
                min_reg_radius=args.regression.min_reg_radius,
                max_reg_points=args.regression.max_reg_points,
                max_reg_radius=args.regression.max_reg_radius,
                eval_split=args.regression.eval_split,
                rng=rng,
                return_stats=True,
                verbose=(i==len(eval_points)-1),
            )
            sffs.append(sff)
            metrics.append([r2,mse])
            nbhds.append(nbhd)
            pcs.append(pc)
            preds.append(pred)
        result = Dataset.from_dict({"points": eval_points,"sffs": sffs, "regression_metrics": metrics})
        result.save_to_disk(args.output.name)
        if manifold.ndim==2 and manifold.shape[1]==2:
            visualize_2d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                ],
                marker_size=[2,8],
                save_name=f"{args.output.name}/curvature",
            )
        elif manifold.ndim==2 and manifold.shape[1]==3:
            visualize_3d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                    ("Local",nbhds[-1]),
                    ("PC",pcs[-1]),
                    ("Pred",preds[-1]),
                ],
                marker_size=[2,8,2,2,2],
                save_name=f"{args.output.name}/curvature",
            )
    elif args.method.name=="regression_diffusion":
        if args.regression.model_type=="FCN":
            model = FullyConnectedNetwork.from_pretrained(args.regression.model_path).to(device)
        elif args.regression.model_type=="UNet":
            model = UNet2DModel.from_pretrained(args.regression.model_path).to(device)
        else:
            raise NotImplementedError(f"Model '{args.model}' is not supported.")
        noise_scheduler = DDPMScheduler.from_pretrained(args.regression.model_path)
        pipeline = DDPMPipeline(unet=model,scheduler=noise_scheduler)
        sffs = []
        metrics = []
        nbhds = []
        pcs = []
        preds = []
        hyperparam_grid = [
            dict(
                num_neighbors=nn,
                radius=r,
                pca_num_neighbors=pn,
                pca_radius=pr,
            )
            for nn, r, pn, pr in product(
                args.regression.num_neighbors if isinstance(args.regression.num_neighbors,list) else [args.regression.num_neighbors],
                args.regression.radius if isinstance(args.regression.radius,list) else [args.regression.radius],
                args.regression.pca_num_neighbors if isinstance(args.regression.pca_num_neighbors,list) else [args.regression.pca_num_neighbors],
                args.regression.pca_radius if isinstance(args.regression.pca_radius,list) else [args.regression.pca_radius],
            )
        ]
        for i,eval_point in enumerate(tqdm(eval_points)):
            best_sff = None
            best_r2 = -float("inf")
            best_mse = float("inf")
            best_nbhd = None
            best_pc = None
            submanifold = generate_diffusion_samples(
                eval_point=eval_point,
                pipeline=pipeline,
                num_samples=args.regression.num_interpolants,
                diffusion_distance=args.regression.diffusion_distance,
                diffusion_time=args.regression.diffusion_time,
                batch_size=256,
                rng=rng,
            )
            basis, intrinsic_dim = obtain_basis(submanifold,intrinsic_dim=args.regression.intrinsic_dim,method="gap")
            tangent_basis = basis[:intrinsic_dim]
            submanifold = generate_diffusion_samples_basis(
                eval_point=eval_point,
                pipeline=pipeline,
                basis=tangent_basis,
                num_samples=args.regression.num_interpolants,
                diffusion_distance=args.regression.diffusion_distance,
                diffusion_time=args.regression.diffusion_time,
                batch_size=256,
                rng=rng,
            )
            for hparams in hyperparam_grid:
                sff, r2, mse, nbhd, pc, pred = SFFRegressor.regress_sff(
                    eval_point=eval_point,
                    manifold=submanifold,
                    **hparams,
                    # num_neighbors=args.regression.num_neighbors,
                    # radius=args.regression.radius,
                    intrinsic_dim=args.regression.intrinsic_dim,
                    compute_basis=args.regression.compute_basis,
                    # pca_num_neighbors=args.regression.pca_num_neighbors,
                    # pca_radius=args.regression.pca_radius,
                    num_tangents=args.regression.num_tangents,
                    num_normals=args.regression.num_normals,
                    method=args.regression.method,
                    eval_split=args.regression.eval_split,
                    rng=rng,
                    num_trials=args.regression.num_trials,
                    num_epochs=args.regression.num_epochs,
                    learning_rate=args.regression.learning_rate,
                    rank=args.regression.rank,
                    manopt_iters=args.regression.manopt_iters,
                    batch_size=args.regression.batch_size,
                    batch_normal=args.regression.batch_normal,
                    return_stats=True,
                    verbose=(i==len(eval_points)-1),
                )
                # sffs.append(sff)
                # metrics.append([r2,mse])
                if r2 >= best_r2:
                    best_sff = sff
                    best_r2 = r2
                    best_mse = mse
                    best_nbhd = nbhd
                    best_pc = pc
                    best_pred = pred
            sffs.append(best_sff)
            metrics.append([best_r2,best_mse])
            nbhds.append(best_nbhd)
            pcs.append(best_pc)
            preds.append(best_pred)
        result = Dataset.from_dict({"points": eval_points,"sffs": sffs, "regression_metrics": metrics})
        result.save_to_disk(args.output.name)
        if manifold.ndim==2 and manifold.shape[1]==2:
            visualize_2d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                    ("Submanifold",submanifold),
                ],
                marker_size=[2,8,2],
                save_name=f"{args.output.name}/curvature",
            )
        elif manifold.ndim==2 and manifold.shape[1]==3:
            visualize_3d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                    ("Submanifold",submanifold),
                    ("Local",nbhds[-1]),
                    ("PC",pcs[-1]),
                    ("Pred",preds[-1]),
                ],
                marker_size=[2,8,2,2,2,2],
                save_name=f"{args.output.name}/curvature",
            )
    elif args.method.name=="regression_diffusion_auto":
        if args.regression.model_type=="FCN":
            model = FullyConnectedNetwork.from_pretrained(args.regression.model_path).to(device)
        elif args.regression.model_type=="UNet":
            model = UNet2DModel.from_pretrained(args.regression.model_path).to(device)
        else:
            raise NotImplementedError(f"Model '{args.model}' is not supported.")
        noise_scheduler = DDPMScheduler.from_pretrained(args.regression.model_path)
        pipeline = DDPMPipeline(unet=model,scheduler=noise_scheduler)
        sffs = []
        metrics = []
        nbhds = []
        pcs = []
        preds = []
        for i,eval_point in enumerate(tqdm(eval_points)):
            submanifold = generate_diffusion_samples(
                eval_point=eval_point,
                pipeline=pipeline,
                num_samples=args.regression.num_interpolants,
                diffusion_distance=args.regression.diffusion_distance,
                diffusion_time=args.regression.diffusion_time,
                batch_size=256,
                rng=rng,
            )
            basis, intrinsic_dim = obtain_basis(submanifold,intrinsic_dim=args.regression.intrinsic_dim,method="gap")
            tangent_basis = basis[:intrinsic_dim]
            submanifold = generate_diffusion_samples_basis(
                eval_point=eval_point,
                pipeline=pipeline,
                basis=tangent_basis,
                num_samples=args.regression.num_interpolants,
                diffusion_distance=args.regression.diffusion_distance,
                diffusion_time=args.regression.diffusion_time,
                batch_size=256,
                rng=rng,
            )
            sff, r2, mse, nbhd, pc, pred = SFFRegressor.regress_sff_auto(
                eval_point=eval_point,
                manifold=submanifold,
                intrinsic_dim=args.regression.intrinsic_dim,
                compute_basis=args.regression.compute_basis,
                pca_batch_size=args.regression.pca_batch_size,
                min_pca_points=args.regression.min_pca_points,
                min_pca_radius=args.regression.min_pca_radius,
                max_pca_points=args.regression.max_pca_points,
                max_pca_radius=args.regression.max_pca_radius,
                pca_bandwidth=args.regression.pca_bandwidth,
                reg_batch_size=args.regression.reg_batch_size,
                min_reg_points=args.regression.min_reg_points,
                min_reg_radius=args.regression.min_reg_radius,
                max_reg_points=args.regression.max_reg_points,
                max_reg_radius=args.regression.max_reg_radius,
                eval_split=args.regression.eval_split,
                rng=rng,
                return_stats=True,
                verbose=(i==len(eval_points)-1),
            )
            sffs.append(sff)
            metrics.append([r2,mse])
            nbhds.append(nbhd)
            pcs.append(pc)
            preds.append(pred)
        result = Dataset.from_dict({"points": eval_points,"sffs": sffs, "regression_metrics": metrics})
        result.save_to_disk(args.output.name)
        if manifold.ndim==2 and manifold.shape[1]==2:
            visualize_2d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                    ("Submanifold",submanifold),
                ],
                marker_size=[2,8,2],
                save_name=f"{args.output.name}/curvature",
            )
        elif manifold.ndim==2 and manifold.shape[1]==3:
            visualize_3d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([eval_points,[[scalar_from_sff(sff)] for sff in sffs]],axis=1)),
                    ("Submanifold",submanifold),
                    ("Local",nbhds[-1]),
                    ("PC",pcs[-1]),
                    ("Pred",preds[-1]),
                ],
                marker_size=[2,8,2,2,2,2],
                save_name=f"{args.output.name}/curvature",
            )
    elif args.method.name=="diffusion_map":
        scalars = SFFDiffusionMap.scalar_curvature(
            manifold=manifold,
            intrinsic_dimension=args.diffusion_map.intrinsic_dim,
            num_eigenfunctions=args.diffusion_map.num_eigenfunctions,
            c=args.diffusion_map.c,
            num_neighbors=args.diffusion_map.num_neighbors,
            initial_bandwidth_num_neighbors=args.diffusion_map.initial_bandwidth_num_neighbors,
        )
        result = Dataset.from_dict({"points": manifold, "scalars": scalars})
        result.save_to_disk(args.output.name)
        if manifold.ndim==2 and manifold.shape[1]==2:
            visualize_2d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([manifold,scalars[:,None]],axis=1)),
                ],
                marker_size=[2,8],
                save_name=f"{args.output.name}/curvature",
            )
        elif manifold.ndim==2 and manifold.shape[1]==3:
            visualize_3d(
                pointsets=[
                    ("Manifold",manifold),
                    ("Scalar Curvature",np.concatenate([manifold,scalars[:,None]],axis=1)),
                ],
                marker_size=[2,8],
                save_name=f"{args.output.name}/curvature",
            )
            
    elif args.method.name=="interpolation":
        if args.interpolation.model_type=="FCN":
            model = FullyConnectedNetwork.from_pretrained(args.interpolation.model_path).to(device)
        elif args.interpolation.model_type=="UNet":
            model = UNet2DModel.from_pretrained(args.interpolation.model_path).to(device)
        else:
            raise NotImplementedError(f"Model '{args.model}' is not supported.")
        noise_scheduler = DDPMScheduler.from_pretrained(args.interpolation.model_path)
        pipeline = DDPMPipeline(unet=model,scheduler=noise_scheduler)

        tangents_all = []
        curvatures_all = []
        geodesics_all = []
        for i,eval_point in enumerate(tqdm(eval_points)):
            submanifold = generate_diffusion_samples(
                eval_point=eval_point,
                pipeline=pipeline,
                num_samples=args.interpolation.num_interpolants,
                diffusion_distance=args.interpolation.distance,
                diffusion_time=args.interpolation.diffusion_time,
                batch_size=256,
                rng=rng,
            )
            if args.interpolation.use_true_tangents:
                tangent_basis = all_tangent_basis[i]
            else:
                basis, intrinsic_dim = obtain_basis(submanifold,intrinsic_dim=args.interpolation.intrinsic_dim,method="gap")
                tangent_basis = basis[:intrinsic_dim]
            fs_curvatures = []
            geodesics = []
            for tangent in tangent_basis:
                fs_curvature, geodesic = FSInterpolationPath.interpolate(
                    pipeline=pipeline,
                    eval_point=eval_point,
                    tangent=tangent,
                    distance=args.interpolation.distance,
                    num_interpolants=args.interpolation.num_interpolants,
                    diffusion_time=args.interpolation.diffusion_time,
                )
                fs_curvatures.append(fs_curvature)
                geodesics.append(geodesic)
            tangents_all.append(tangent_basis)
            curvatures_all.append(fs_curvatures)
            geodesics_all.append(geodesics)
        tangents_all = np.array(tangents_all)
        curvatures_all = np.array(curvatures_all)
        geodesics_all = np.array(geodesics_all)
        
        result = Dataset.from_dict({"points": eval_points, "tangents": tangents_all, "fs_curvatures": curvatures_all, "geodesics": geodesics_all})
        result.save_to_disk(args.output.name)
        if manifold.ndim==2 and manifold.shape[1]==2:
            visualize_2d(
                pointsets=[
                    ("Manifold",manifold),
                ]+[
                    (f"Osculating Curvature {i}",np.concatenate([eval_points,curvatures_all[:,i][:,None]],axis=1)) for i in range(curvatures_all.shape[1])
                ],
                marker_size=[2]+[8 for i in range(curvatures_all.shape[1])],
                paths=[
                    (f"Tangent {i}",geodesic) for i,geodesic in enumerate(geodesics)
                ],
                save_name=f"{args.output.name}/curvature",
            )
        elif manifold.ndim==2 and manifold.shape[1]==3:
            visualize_3d(
                pointsets=[
                    ("Manifold",manifold),
                ]+[
                    (f"Osculating Curvature {i}",np.concatenate([eval_points,curvatures_all[:,i][:,None]],axis=1)) for i in range(curvatures_all.shape[1])
                ],
                marker_size=[2]+[8 for i in range(curvatures_all.shape[1])],
                paths=[
                    (f"Tangent {i}",geodesic) for i,geodesic in enumerate(geodesics)
                ],
                save_name=f"{args.output.name}/curvature",
            )
    else:
        raise ValueError(f"Estimation method not recognized (got {args.method.name}).")

    end = time.perf_counter()
    print(f"- Curvature computation took {end-start} seconds.")
    ####################################################################################################
    end_total = time.perf_counter()
    print(f"- Experiment {args.output.name} took {end_total-start_total} seconds.")

if __name__ == "__main__":
    main()