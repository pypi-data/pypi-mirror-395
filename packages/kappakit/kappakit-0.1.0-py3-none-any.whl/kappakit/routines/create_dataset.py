from typing import Union
import os
import time
import jsonargparse
import wandb
import numpy as np
from datasets import Dataset, DatasetDict, load_dataset
from kappakit.data.toy_manifolds import Ball, Blob, ColorspaceSphere, Cylinder, Ellipsoid, MobiusStrip, Paraboloid, Roll, S_Curve, Sphere, Torus
from kappakit.data.real_manifolds import MNIST, KMNIST, FMNIST, StanfordBunny
from kappakit.plotting.log_utils import get_git_hash


def add_dataset_arguments(parser: jsonargparse.ArgumentParser):
    parser.add_argument("--dataset.name", type=str, required=True, help="Either a path to an existing numpy file or a name from the manifold library")
    parser.add_argument("--dataset.save_name", type=str, required=True, help="Dataset name")
    parser.add_argument("--dataset.upload_name", type=str, required=False, help="Dataset upload name; if specified, will upload to HF Hub")
    parser.add_argument("--dataset.eval_points_name", type=str, required=False, help="Path to an existing numpy file for evaluation points")
    parser.add_argument("--dataset.geodesic_name", type=str, required=False, help="Path to an existing numpy file for geodesic points")
    parser.add_argument("--dataset.num_points", type=int, required=True, help="Number of data points")
    parser.add_argument("--dataset.noise", type=float, required=False, default=0., help="Number of data points")
    parser.add_argument("--dataset.skip_basis", type=bool, required=False, default=False, help="Number of data points")
    parser.add_argument("--dataset.geodesic_distance", type=float, required=False, default=1., help="Length of geodesic")
    parser.add_argument("--dataset.geodesic_num_steps", type=int, required=False, default=100, help="Geodesic num steps")

    parser.add_argument("--ball.intrinsic_dim", type=int, required=False, help="Intrinsic dimension")
    parser.add_argument("--ball.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--ball.radius", type=float, required=False, help="Radius")

    parser.add_argument("--blob.num_blobs", type=int, required=False, help="Number of blobs")
    parser.add_argument("--blob.blob_type", type=str, required=False, help="Type of blob")
    parser.add_argument("--blob.image_size", type=tuple[int,int], required=False, help="Image width and height")
    parser.add_argument("--blob.blob_size_range", type=tuple[float,float], required=False, help="Range of blob sizes")

    parser.add_argument("--colorspace_sphere.image_size", type=tuple[int,int], required=False, help="Image width and height")
    parser.add_argument("--colorspace_sphere.radius", type=float, required=False, help="Radius")
    
    parser.add_argument("--cylinder.sphere_dim", type=int, required=False, help="Dimension of sphere part")
    parser.add_argument("--cylinder.linear_dim", type=int, required=False, help="Dimension of linear part")
    parser.add_argument("--cylinder.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--cylinder.radius", type=float, required=False, help="Radius")
    parser.add_argument("--cylinder.width", type=float, required=False, help="Width")

    parser.add_argument("--ellipsoid.intrinsic_dim", type=int, required=False, help="Intrinsic dimension")
    parser.add_argument("--ellipsoid.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--ellipsoid.radii", type=list[float], required=False, help="List of radii")

    parser.add_argument("--mobius_strip.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--mobius_strip.radius", type=float, required=False, help="Radius")
    parser.add_argument("--mobius_strip.width", type=float, required=False, help="Width")
    parser.add_argument("--mobius_strip.turn_count", type=float, required=False, help="Number of turns")

    parser.add_argument("--paraboloid.intrinsic_dim", type=int, required=False, help="Intrinsic dimension")
    parser.add_argument("--paraboloid.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--paraboloid.sff", type=Union[int,list[int],list[list[float]],list[list[list[float]]]], required=False, help="Second fundamental form")
    parser.add_argument("--paraboloid.radius", type=float, required=False, help="Radius")

    parser.add_argument("--roll.intrinsic_dim", type=int, required=False, help="Intrinsic dimension")
    parser.add_argument("--roll.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--roll.spiral_coef", type=float, required=False, help="Spiral coefficient")
    parser.add_argument("--roll.theta_max", type=float, required=False, help="Maximum theta")
    parser.add_argument("--roll.width", type=float, required=False, help="Width")

    parser.add_argument("--s_curve.intrinsic_dim", type=int, required=False, help="Intrinsic dimension")
    parser.add_argument("--s_curve.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--s_curve.radius", type=float, required=False, help="Radius")
    parser.add_argument("--s_curve.width", type=float, required=False, help="Width")

    parser.add_argument("--sphere.intrinsic_dim", type=int, required=False, help="Intrinsic dimension")
    parser.add_argument("--sphere.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--sphere.radius", type=float, required=False, help="Radius")

    parser.add_argument("--torus.ambient_dim", type=int, required=False, help="Ambient dimension")
    parser.add_argument("--torus.major_radius", type=float, required=False, help="Major radius")
    parser.add_argument("--torus.minor_radius", type=float, required=False, help="Minor radius")

    parser.add_argument("--mnist.image_size", type=int, required=False, help="MNIST image size")
    parser.add_argument("--kmnist.image_size", type=int, required=False, help="KMNIST image size")
    parser.add_argument("--fmnist.image_size", type=int, required=False, help="FMNIST image size")

    parser.add_argument("--bunny.rescale", type=float, required=False, default=10, help="Rescale factor for bunny point cloud")

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
    args = parser.parse_args()
    
    os.makedirs(args.dataset.save_name, exist_ok=True)
    args.wandb.git_hash = get_git_hash() if get_git_hash() else args.git_hash
    parser.save(args,f"{args.dataset.save_name}/args.yaml", overwrite=True)
    if args.wandb.enable:
        wandb.init(
            config=args,
            project=args.wandb.project,
            entity=args.wandb.team,
            name=os.path.basename(args.args.dataset.save_name),
        )

    if os.path.exists(args.dataset.name):
        dataset = Dataset.from_dict({"points": np.load(args.dataset.name)})
        dataset_dict = DatasetDict({"manifold":dataset})
        if os.path.exists(args.dataset.eval_points_name):
            eval_points = Dataset.from_dict({"points":np.load(args.dataset.eval_points_name)})
            dataset_dict["eval_points"] = eval_points
        if os.path.exists(args.dataset.geodesic_name):
            geodesic = Dataset.from_dict({"points":np.load(args.dataset.geodesic_name)})
            dataset_dict["geodesic"] = geodesic
    elif args.dataset.name=="Ball":
        dataset = Ball(
            n_points=args.dataset.num_points,
            intrinsic_dim=args.ball.intrinsic_dim,
            ambient_dim=args.ball.ambient_dim,
            radius=args.ball.radius,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
        })
    elif args.dataset.name=="Blob":
        dataset = Blob(
            n_points=args.dataset.num_points,
            num_blobs=args.blob.num_blobs,
            blob_type=args.blob.blob_type,
            image_size=args.blob.image_size,
            blob_size_range=args.blob.blob_size_range,
            noise=args.dataset.noise,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
        })
    elif args.dataset.name=="ColorspaceSphere":
        dataset = ColorspaceSphere(
            n_points=args.dataset.num_points,
            image_size=args.colorspace_sphere.image_size,
            radius=args.colorspace_sphere.radius,
            noise=args.dataset.noise,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
        })
    elif args.dataset.name=="Cylinder":
        dataset = Cylinder(
            n_points=args.dataset.num_points,
            sphere_dim=args.cylinder.sphere_dim,
            linear_dim=args.cylinder.linear_dim,
            ambient_dim=args.cylinder.ambient_dim,
            radius=args.cylinder.radius,
            width=args.cylinder.width,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
        })
    elif args.dataset.name=="Ellipsoid":
        dataset = Ellipsoid(
            n_points=args.dataset.num_points,
            intrinsic_dim=args.ellipsoid.intrinsic_dim,
            ambient_dim=args.ellipsoid.ambient_dim,
            radii=args.ellipsoid.radii,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
        })
    elif args.dataset.name=="MobiusStrip":
        dataset = MobiusStrip(
            n_points=args.dataset.num_points,
            ambient_dim=args.mobius_strip.ambient_dim,
            radius=args.mobius_strip.radius,
            width=args.mobius_strip.width,
            turn_count=args.mobius_strip.turn_count,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
        })
    elif args.dataset.name=="Paraboloid":
        if args.paraboloid.sff is not None and isinstance(args.paraboloid.sff,list):
            args.paraboloid.sff = np.array(args.paraboloid.sff)
        dataset = Paraboloid(
            n_points=args.dataset.num_points,
            intrinsic_dim=args.paraboloid.intrinsic_dim,
            ambient_dim=args.paraboloid.ambient_dim,
            sff=args.paraboloid.sff,
            radius=args.paraboloid.radius,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "true_curvature":Dataset.from_dict({"points":[dataset.sff]}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
            "tangent_basis":Dataset.from_dict({"points":dataset.tangent_basis}),
        })
    elif args.dataset.name=="Roll":
        dataset = Roll(
            n_points=args.dataset.num_points,
            intrinsic_dim=args.roll.intrinsic_dim,
            ambient_dim=args.roll.ambient_dim,
            spiral_coef=args.roll.spiral_coef,
            theta_max=args.roll.theta_max,
            width=args.roll.width,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
            "true_curvature":Dataset.from_dict({"points":dataset.true_sff}),
            "tangent_basis":Dataset.from_dict({"points":dataset.tangent_basis}),
        })
    elif args.dataset.name=="S_Curve":
        dataset = S_Curve(
            n_points=args.dataset.num_points,
            intrinsic_dim=args.s_curve.intrinsic_dim,
            ambient_dim=args.s_curve.ambient_dim,
            radius=args.s_curve.radius,
            width=args.s_curve.width,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
        })
    elif args.dataset.name=="Sphere":
        dataset = Sphere(
            n_points=args.dataset.num_points,
            intrinsic_dim=args.sphere.intrinsic_dim,
            ambient_dim=args.sphere.ambient_dim,
            radius=args.sphere.radius,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
            "true_curvature":Dataset.from_dict({"points":dataset.true_sff}),
            "tangent_basis":Dataset.from_dict({"points":dataset.tangent_basis}),
        })
    elif args.dataset.name=="Torus":
        dataset = Torus(
            n_points=args.dataset.num_points,
            ambient_dim=args.torus.ambient_dim,
            major_radius=args.torus.major_radius,
            minor_radius=args.torus.minor_radius,
            noise=args.dataset.noise,
            skip_basis=args.dataset.skip_basis,
            rng=np.random.default_rng(args.device.seed),
        )
        eval_points = dataset.evaluation_points()
        geodesic = dataset.path(
            distance=args.dataset.geodesic_distance,
            num_steps=args.dataset.geodesic_num_steps
        )
        dataset_dict = DatasetDict({
            "manifold":Dataset.from_dict({"points":dataset}),
            "eval_points":Dataset.from_dict({"points":eval_points}),
            "geodesic":Dataset.from_dict({"points":geodesic}),
            "true_curvature":Dataset.from_dict({"points":dataset.true_sff}),
            "tangent_basis":Dataset.from_dict({"points":dataset.tangent_basis}),

        })
    elif args.dataset.name=="MNIST":
        dataset = MNIST(n_points=args.dataset.num_points, image_size=args.mnist.image_size, rng=np.random.default_rng(args.device.seed)).dataset
        dataset_dict = DatasetDict({
            "manifold": dataset
        })
    elif args.dataset.name=="KMNIST":
        dataset = KMNIST(n_points=args.dataset.num_points, image_size=args.kmnist.image_size, rng=np.random.default_rng(args.device.seed)).dataset
        dataset_dict = DatasetDict({
            "manifold": dataset
        })
    elif args.dataset.name=="FMNIST":
        dataset = FMNIST(n_points=args.dataset.num_points, image_size=args.fmnist.image_size, rng=np.random.default_rng(args.device.seed)).dataset
        dataset_dict = DatasetDict({
            "manifold": dataset
        })
    elif args.dataset.name=="StanfordBunny":
        dataset = StanfordBunny(n_points=args.dataset.num_points, rescale=args.bunny.rescale, rng=np.random.default_rng(args.device.seed)).dataset
        dataset_dict = DatasetDict({
            "manifold": Dataset.from_dict({"points":dataset}),
        })
    else:
        raise ValueError(f"Dataset name not recognized (got {args.dataset.name})")
    
    dataset_dict.save_to_disk(args.dataset.save_name)
    if args.dataset.upload_name is not None:
        dataset_dict.push_to_hub(args.dataset.upload_name)

    end_total = time.perf_counter()
    print(f"- Creating {args.dataset.name} took {end_total-start_total} seconds.")

if __name__ == "__main__":
    main()