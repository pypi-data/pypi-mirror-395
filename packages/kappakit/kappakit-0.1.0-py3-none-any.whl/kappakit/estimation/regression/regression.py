from copy import deepcopy
from typing import Union, Tuple
from jaxtyping import Float
import time
from tqdm import tqdm
import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from sklearn.decomposition import PCA, IncrementalPCA
from scipy.spatial.distance import cdist
from scipy.stats import ortho_group
import pymanopt
from kappakit.estimation.diffusion_model.diffusion_tools import select_elbow
from kappakit.curvature.curvature import scalar_from_sff
device = "cuda" if torch.cuda.is_available() else "cpu"

class SFFRegressor:
    """
    Second Fundamental Form is solution to hT=N where T is quadratic term matrix and N is normal space coords.
    See Cao et al. 2020 (https://arxiv.org/pdf/1905.10725) and Sritharan et al. 2021 (https://www.pnas.org/doi/10.1073/pnas.2100473118)
    """
    @staticmethod
    def regress_sff(
        eval_point: Float[np.ndarray, "m"],
        manifold: Float[np.ndarray, "N m"],

        num_neighbors: int = None,
        radius: float = None,
        intrinsic_dim: int = None,
        compute_basis: bool = True,
        pca_num_neighbors: int = None,
        pca_radius: float = None,

        num_tangents: int = None,
        num_normals: int = None,

        eval_split: float = 0.,
        rng: np.random.Generator = np.random.default_rng(),
        method: str = "numpy",

        num_trials: int = 1,
        num_epochs: int = 300,
        learning_rate: float = 1e-1,
        rank: int = None,
        manopt_iters: int = 8000,

        batch_size: int = None,
        batch_normal: int = None,

        verbose: bool = False,
        return_stats: bool = False,
    ) -> Union[
        Float[np.ndarray, "d d n"],
        Tuple[
            Float[np.ndarray, "d d n"],
            
        ],
    ]:
        if verbose:
            print(f"Calculating Curvature at {eval_point} via Regression...")
        ####################################################################################################
        # Step 1: Obtain Local Quadratic Neighborhood
        ####################################################################################################
        local_manifold, sorted_points, sorted_distances = SFFRegressor.obtain_neighborhood(
            eval_point=eval_point,
            manifold=manifold,
            num_neighbors=num_neighbors,
            radius=radius,
            return_sorted=True,
            verbose=verbose,
        )
        if verbose:
            print("Local Quadratic Neighborhood Size:",local_manifold.shape[0])
        if local_manifold.shape[0]<30:
            print(f"WARNING: N={local_manifold.shape[0]} is very low! Please adjust your quadratic neighborhood!")
        ###################################################################################################
        # Step 2: Obtain Basis for Tangent and Normal Spaces
        ###################################################################################################
        if intrinsic_dim is None and not compute_basis:
            raise ValueError("Intrinsic dimension must be specified if not computing basis.")
        if compute_basis:
            linear_manifold = SFFRegressor.obtain_neighborhood(
                sorted_points=sorted_points,
                sorted_distances=sorted_distances,
                num_neighbors=pca_num_neighbors,
                radius=pca_radius,
                verbose=verbose,
            )
            if verbose:
                print("Local Linear Neighborhood Size:",linear_manifold.shape[0])
            if linear_manifold.shape[0]<30:
                print(f"WARNING: N={linear_manifold.shape[0]} is very low! Please adjust your linear neighborhood!")
            # kernel = np.exp(-0.5*((sorted_distances/1)**2))
            # kernel /= np.sum(kernel)
            # pca = PCA().fit(linear_manifold*kernel[:linear_manifold.shape[0],None])
            pca = PCA().fit(linear_manifold)
            local_coords = pca.transform(local_manifold)#-pca.transform(eval_point.reshape(1,-1))
            # pca_deviation = measure_pca_deviation(pca.components_,intrinsic_dimension)
        else:
            local_coords = local_manifold#-eval_point
        if intrinsic_dim is None:
            intrinsic_dim = select_elbow(singular_values=pca.singular_values_, method="gap")

        local_coords_tangent = local_coords[:,:intrinsic_dim]
        local_coords_normal = local_coords[:,intrinsic_dim:][:,:num_normals]

        if num_tangents is not None:
            local_coords_tangent = local_coords_tangent[:,:num_tangents]
        if num_normals is not None:
            local_coords_normal = local_coords_normal[:,:num_normals]
        
        num_points = local_coords_tangent.shape[0]
        intrinsic_dim = local_coords_tangent.shape[1]
        normal_dim = local_coords_normal.shape[1]
        ambient_dim = intrinsic_dim+normal_dim
        ###################################################################################################
        # Step 3: Perform the Regression
        ###################################################################################################
        batch_size = num_points if batch_size is None else batch_size
        batch_normal = normal_dim if batch_normal is None else batch_normal

        if eval_split>0:
            random_indices = rng.permutation(np.arange(num_points))
            train_indices = random_indices[:int(num_points*(1-eval_split))]
            val_indices = random_indices[int(num_points*(1-eval_split)):]
        else:
            train_indices = np.arange(num_points)
        
        betas = []
        for normal_offset in range(0,normal_dim,batch_normal):
            local_coords_normal_batch = local_coords_normal[:,normal_offset:normal_offset+batch_normal]
            if method=="numpy":
                beta = SFFRegressor.regress_w_numpy(
                    local_coords_tangent[train_indices],
                    local_coords_normal_batch[train_indices],
                )
            elif method=="gradient_descent":
                beta = SFFRegressor.regress_w_grad_descent(
                    local_coords_tangent[train_indices],
                    local_coords_normal[train_indices],
                    num_trials=num_trials,
                    num_epochs=num_epochs,
                    learning_rate=learning_rate,
                    batch_size=batch_size,
                    verbose=verbose,
                )
            elif method=="low_rank":
                beta = SFFRegressor.regress_w_low_rank(
                    local_coords_tangent[train_indices],
                    local_coords_normal[train_indices],
                    rank=rank,
                    num_trials=num_trials,
                    num_epochs=num_epochs,
                    learning_rate=learning_rate,
                    batch_size=batch_size,
                    rng=rng,
                    verbose=verbose,
                )
            elif method=="manopt":
                beta = SFFRegressor.regress_w_manopt(
                    local_coords_tangent[train_indices],
                    local_coords_normal[train_indices],
                    rank=rank,
                    manopt_iters=manopt_iters,
                    batch_normal=batch_normal,
                    verbose=verbose,
                )
            else:
                raise ValueError(f"Unrecognized method: {method}.")
            betas.append(beta)
        beta = np.concatenate(betas,axis=1)
        ###################################################################################################
        # Step 4: Evaluate the Regression
        ###################################################################################################
        if eval_split>0:
            train_r2, train_mse = SFFRegressor.evaluate_regression(
                local_coords_tangent=local_coords_tangent[train_indices],
                local_coords_normal=local_coords_normal[train_indices],
                beta=beta,
                batch_size=1,
            )
            val_r2, val_mse = SFFRegressor.evaluate_regression(
                local_coords_tangent=local_coords_tangent[val_indices],
                local_coords_normal=local_coords_normal[val_indices],
                beta=beta,
                batch_size=1,
            )
            if verbose:
                print("Train R2",train_r2)
                print("Train MSE",train_mse)
                print("Val R2",val_r2)
                print("Val MSE",val_mse)
            r2, mse = train_r2, train_mse
        else:
            r2, mse, pred = SFFRegressor.evaluate_regression(
                local_coords_tangent=local_coords_tangent,
                local_coords_normal=local_coords_normal,
                beta=beta,
                batch_size=batch_size,
            )
            if verbose:
                print("R^2:",r2)
                print("MSE:",mse)
        ###################################################################################################
        # Step 5: Return the SFF
        ###################################################################################################
        hessmats = np.zeros((len(beta) - 1, normal_dim))
        hessmats[:, :normal_dim] = beta[1:, :] # Ignore constant term
        sff = hessmats.reshape(intrinsic_dim,intrinsic_dim,normal_dim)*2 # Double to account for power rule
        if verbose:
            print("Scalar:",scalar_from_sff(sff))
        if return_stats:
            return sff, r2, mse, local_manifold, pca.inverse_transform(np.concatenate([scale*np.eye(manifold.shape[1])[:intrinsic_dim] for scale in np.linspace(0,0.5,20)],axis=0)), pca.inverse_transform(np.concatenate((local_coords_tangent,pred),axis=1))
        else:
            return sff

    @staticmethod
    def regress_sff_auto(
        eval_point: Float[np.ndarray, "m"],
        manifold: Float[np.ndarray, "N m"],

        intrinsic_dim: int = None,
        compute_basis: bool = True,

        pca_batch_size: int = 1,
        min_pca_points: int = None,
        min_pca_radius: float = None,
        max_pca_points: int = None,
        max_pca_radius: float = None,
        pca_bandwidth: float = None,

        reg_batch_size: int = 1,
        min_reg_points: int = None,
        min_reg_radius: float = None,
        max_reg_points: int = None,
        max_reg_radius: float = None,

        eval_split: float = 0.,
        rng: np.random.Generator = np.random.default_rng(),

        verbose: bool = False,
        return_stats: bool = False,
    ) -> Union[
        Float[np.ndarray, "d d n"],
        Tuple[
            Float[np.ndarray, "d d n"],
            
        ],
    ]:
        if verbose:
            print(f"Calculating Curvature at {eval_point} via Regression...")
        ####################################################################################################
        # Step 1: Tangent Space Estimation
        ####################################################################################################
        ambient_dim = manifold.shape[1]
        if intrinsic_dim is None and not compute_basis:
            raise ValueError("Intrinsic dimension must be specified if not computing basis.")
        if compute_basis:
            distances = cdist(eval_point.reshape(1,-1),manifold,"euclidean").flatten()
            sorted_distances = np.sort(distances)
            sorted_points = manifold[np.argsort(distances)]

            if min_pca_points is None:
                if min_pca_radius is None:
                    min_pca_points = max(30,ambient_dim)
                else:
                    min_pca_points = np.searchsorted(sorted_distances,np.array(min_pca_radius),side="right")
            if max_pca_points is None:
                if max_pca_radius is None:
                    max_pca_points = manifold.shape[0]
                else:
                    max_pca_points = np.searchsorted(sorted_distances,np.array(max_pca_radius),side="right")
            
            if verbose:
                print(f"Min PCA: {min_pca_points}, {sorted_distances[min_pca_points-1]}")
                print(f"Max PCA: {max_pca_points}, {sorted_distances[max_pca_points-1]}")

            best_pca = {
                "explained_variance_ratio": np.NINF,
                "num_points": None,
                "pca": None,
            }

            # if pca_bandwidth is None:
            #     kernel = np.ones_like(sorted_distances)
            # else:
            #     kernel = np.exp(-0.5*((sorted_distances/pca_bandwidth)**2))
            #     kernel /= np.sum(kernel)
            
            pca = IncrementalPCA()
            pca.partial_fit(sorted_points[:min_pca_points])
            for offset in tqdm(range(min_pca_points, max_pca_points, pca_batch_size),desc="PCA") if verbose else range(min_pca_points, max_pca_points, pca_batch_size):
                pca.partial_fit(sorted_points[offset:offset+pca_batch_size])
                explained_variance_ratio = pca.explained_variance_[intrinsic_dim]-pca.explained_variance_[intrinsic_dim-1]
                # explained_variance_ratio = pca.explained_variance_ratio_[:intrinsic_dim].sum()
                if verbose:
                    print(f"PCA @ {min(len(sorted_points),offset+pca_batch_size)}, {sorted_distances[min(len(sorted_points),offset+pca_batch_size)-1]}: {explained_variance_ratio}")
                if explained_variance_ratio>best_pca["explained_variance_ratio"]:
                    best_pca["explained_variance_ratio"] = explained_variance_ratio
                    best_pca["num_points"] = min(len(sorted_points),offset+pca_batch_size)
                    best_pca["pca"] = deepcopy(pca)
            pca = best_pca["pca"]
            if verbose:
                print("Local Linear Neighborhood Size:",best_pca["num_points"],sorted_distances[best_pca["num_points"]-1])
                print("Local Linear Neighborhood Explained Variance Ratio:",best_pca["explained_variance_ratio"])
        else:
            distances = None
        if intrinsic_dim is None:
            intrinsic_dim = select_elbow(singular_values=pca.singular_values_, method="gap")
        normal_dim = ambient_dim-intrinsic_dim
        ####################################################################################################
        # Step 2: Quadratic Regression
        ####################################################################################################
        if distances is None:
            distances = cdist(eval_point.reshape(1,-1),manifold,"euclidean").flatten()
            sorted_distances = np.sort(distances)
            sorted_points = manifold[np.argsort(distances)]
        if eval_split>0:
            random_indices = rng.permutation(np.arange(manifold.shape[0]))
            train_indices = np.sort(random_indices[:int(manifold.shape[0]*(1-eval_split))])
            val_indices = np.sort(random_indices[int(manifold.shape[0]*(1-eval_split)):])
        else:
            train_indices = np.arange(manifold.shape[0])

        if compute_basis:
            local_coords = pca.transform(sorted_points)
        else:
            local_coords = sorted_points

        if min_reg_points is None:
            if min_reg_radius is None:
                min_reg_points = max(30,ambient_dim)
            else:
                min_reg_points = np.searchsorted(sorted_distances[train_indices],np.array(min_reg_radius),side="right")
        if max_reg_points is None:
            if max_reg_radius is None:
                max_reg_points = manifold.shape[0]
            else:
                max_reg_points = np.searchsorted(sorted_distances[train_indices],np.array(max_reg_radius),side="right")

        if verbose:
            print(f"Min Reg: {min_reg_points}, {sorted_distances[min_reg_points-1]}")
            print(f"Max Reg: {max_reg_points}, {sorted_distances[max_reg_points-1]}")

        best_reg = {
            "r2": np.NINF,
            "num_points": None,
            "regressor": None,
        }

        def prepare_batch_for_reg(batch):
            quad_terms = (batch[:,:intrinsic_dim,None] * batch[:,None,:intrinsic_dim]).reshape(batch.shape[0],-1)
            return quad_terms
        
        regressor = RLSRegressor()
        initial_batch = prepare_batch_for_reg(local_coords[train_indices][:min_reg_points])
        regressor.partial_fit(initial_batch,local_coords[train_indices][:min_reg_points,intrinsic_dim:])
        for offset in tqdm(range(min_reg_points, max_reg_points, reg_batch_size),desc="REG") if verbose else range(min_reg_points, max_reg_points, reg_batch_size):
            batch = prepare_batch_for_reg(local_coords[train_indices][offset:offset+reg_batch_size])
            regressor.partial_fit(batch,local_coords[train_indices][offset:offset+reg_batch_size,intrinsic_dim:])
            r2 = regressor.r2_
            if verbose:
                print(f"REG @ {min(len(sorted_points),offset+reg_batch_size)}, {sorted_distances[min(len(sorted_points),offset+reg_batch_size)-1]}: {r2}")
            if r2>best_reg["r2"]:
                best_reg["r2"] = r2
                best_reg["num_points"] = min(len(local_coords[train_indices]),offset+reg_batch_size)
                best_reg["regressor"] = deepcopy(regressor)
        regressor = best_reg["regressor"]
        if verbose:
            print("Local Quadratic Neighborhood Size:",best_reg["num_points"],sorted_distances[best_reg["num_points"]-1])
            print("Local Quadratic Neighborhood R2:",best_reg["r2"])
        ####################################################################################################
        # Step 3: Evaluate
        ####################################################################################################
        if eval_split>0:
            train_r2, train_mse = SFFRegressor.evaluate_regression(
                local_coords_tangent=local_coords[train_indices][:best_reg["num_points"],:intrinsic_dim],
                local_coords_normal=local_coords[train_indices][:best_reg["num_points"],intrinsic_dim:],
                beta=regressor.beta_,
                batch_size=1,
            )
            val_r2, val_mse = SFFRegressor.evaluate_regression(
                local_coords_tangent=local_coords[val_indices][:best_reg["num_points"],:intrinsic_dim],
                local_coords_normal=local_coords[val_indices][:best_reg["num_points"],intrinsic_dim:],
                beta=regressor.beta_,
                batch_size=1,
            )
            if verbose:
                print("Train R2",train_r2)
                print("Train MSE",train_mse)
                print("Val R2",val_r2)
                print("Val MSE",val_mse)
            r2, mse = train_r2, train_mse
        else:
            r2, mse, pred = SFFRegressor.evaluate_regression(
                local_coords_tangent=local_coords[:best_reg["num_points"],:intrinsic_dim],
                local_coords_normal=local_coords[:best_reg["num_points"],intrinsic_dim:],
                beta=regressor.beta_,
                batch_size=1,
            )
            if verbose:
                print("R^2:",r2)
                print("MSE:",mse)
        ###################################################################################################
        # Step 4: Return the SFF
        ###################################################################################################
        sff = regressor.beta_[1:,:].reshape(intrinsic_dim,intrinsic_dim,normal_dim)*2 # Double to account for power rule
        if verbose:
            print("Scalar:",scalar_from_sff(sff))
        if return_stats:
            return sff, r2, mse, sorted_points[:best_reg["num_points"]], pca.inverse_transform(np.concatenate([scale*np.eye(manifold.shape[1])[:intrinsic_dim] for scale in np.linspace(0,0.5,20)],axis=0)), pca.inverse_transform(np.concatenate((local_coords[:best_reg["num_points"],:intrinsic_dim],pred),axis=1))
        else:
            return sff

    @staticmethod
    def obtain_neighborhood(
        eval_point: Float[np.ndarray, "m"] = None,
        manifold: Float[np.ndarray, "N m"] = None,
        sorted_points: Float[np.ndarray, "N m"] = None,
        sorted_distances: Float[np.ndarray, "N"] = None,
        num_neighbors: int = None,
        radius: float = None,
        return_sorted: bool = False,
        verbose: bool = False,
    ) -> Union[
        Float[np.ndarray, "N m"],
        Tuple[
            Float[np.ndarray, "N m"],
            Float[np.ndarray, "N m"], # Sorted points
            Float[np.ndarray, "N"], # Sorted distances
        ],
    ]:
        start = time.perf_counter()
        if verbose:
            print(f"\tObtaining neighborhood...")
        if not ((num_neighbors is None) ^ (radius is None)):
            raise ValueError("Must specify exactly one of nbhd_size or radius")
        if sorted_points is None and sorted_distances is None:
            distances = cdist(eval_point.reshape(1,-1),manifold,"euclidean").flatten()
            sorted_distances = np.sort(distances)
            sorted_points = manifold[np.argsort(distances)]
        if radius is not None:
            num_points = np.searchsorted(sorted_distances,np.array(radius),side="right")
            # if num_points<64:
                # if len(sorted_points)//10>=50:
                #     print(f"Radius deemed insufficient ({num_points}), using num_neighbors={len(sorted_points)//10}")
                #     num_points = len(sorted_points)//10
                # else:
                # print(f"Radius deemed insufficient ({num_points}), using num_neighbors={50}")
                # num_points = 64
            # if num_points<50 and num_neighbors is not None:
            #     print(f"Radius deemed insufficient ({num_points}), using num_neighbors={num_neighbors}")
            #     num_points = num_neighbors
        elif num_neighbors is not None:
            num_points = num_neighbors
        if num_points<64:
            print(f"Radius deemed insufficient ({num_points}), using num_neighbors={num_neighbors}")
            num_points=64
        neighborhood = sorted_points[:num_points]
        
        # if num_neighbors is not None:
        #     neighborhood = sorted_points[:num_neighbors]
        # elif radius is not None:
        #     neighborhood = sorted_points[:np.searchsorted(sorted_distances,np.array(radius),side="right")]
        end = time.perf_counter()
        if verbose:
            print(f"\tObtaining neighborhood took {end-start:.2f} seconds")
        if return_sorted:
            return neighborhood, sorted_points, sorted_distances
        else:
            return neighborhood
    
    @staticmethod
    def regress_w_numpy(
        local_coords_tangent: Float[np.ndarray, "N d"],
        local_coords_normal: Float[np.ndarray, "N n"],
    ) -> Float[np.ndarray, "d**2+1 n"]:
        num_points = local_coords_tangent.shape[0]
        quad_terms = (local_coords_tangent[:,:,None] * local_coords_tangent[:,None,:]).reshape(num_points,-1)
        beta, _, _, _ = np.linalg.lstsq(np.column_stack([np.ones((num_points, 1)), quad_terms]), local_coords_normal, rcond=None)
        return beta
    
    @staticmethod
    def regress_w_grad_descent(
        local_coords_tangent: Float[np.ndarray, "N d"],
        local_coords_normal: Float[np.ndarray, "N n"],
        num_trials: int=1,
        num_epochs: int=300,
        learning_rate: float=0.1,
        batch_size: int=1,
        verbose: bool=False,
    ) -> Float[np.ndarray, "d**2+1 n"]:
        x_data = torch.from_numpy(local_coords_tangent).float().to(device)
        y_data = torch.from_numpy(local_coords_normal).float().to(device)
        class QuadraticRegression(nn.Module):
            def __init__(self, beta, constant):
                super(QuadraticRegression, self).__init__()
                self.beta = nn.Parameter(beta)
                self.constant = nn.Parameter(constant)
            def forward(self, x):
                out = torch.einsum('ni,kij,nj->nk', x, self.beta, x) + self.constant # quadratic form
                return out
        best_loss = float("Inf")
        for trial in range(num_trials):
            beta_init = torch.zeros(y_data.shape[1],x_data.shape[1],x_data.shape[1])
            constant_init = torch.zeros(y_data.shape[1])
            model = QuadraticRegression(beta_init, constant_init).to(device)
            criterion = nn.MSELoss()
            optimizer = Adam(model.parameters(), lr=learning_rate)
            for epoch in range(num_epochs):
                total_loss = 0
                for offset in range(0, x_data.shape[0], batch_size):
                    outputs = model(x_data[offset:offset+batch_size])
                    loss = criterion(outputs, y_data[offset:offset+batch_size])
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    total_loss+=loss.item()
                if verbose and (epoch % 100 == 0):
                    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss/x_data.shape[0]:.8f}')
            if total_loss<best_loss:
                best_loss = total_loss
                beta = model.beta.data.cpu().detach().numpy()
        beta = beta.transpose((1,2,0))
        beta = beta.reshape(-1,beta.shape[-1])
        beta = np.concatenate((model.constant.data.cpu().detach().numpy().reshape(1,-1),beta),axis=0)
        return beta

    @staticmethod
    def regress_w_low_rank(
        local_coords_tangent: Float[np.ndarray, "N d"],
        local_coords_normal: Float[np.ndarray, "N n"],
        rank: int=None,
        num_trials: int=1,
        num_epochs: int=300,
        learning_rate: float=0.1,
        batch_size: int=1,
        rng: np.random.Generator=np.random.default_rng(),
        verbose: bool=False,
    ) -> Float[np.ndarray, "d**2+1 n"]:
        rank = local_coords_tangent.shape[1] if rank is None else rank
        x_data = torch.tensor(local_coords_tangent).float().to(device)
        y_data = torch.tensor(local_coords_normal).float().to(device)
        def eig_to_mat(eig, bases):
            out = torch.einsum('ab,acb->abc', eig, bases)
            return torch.einsum('abc,acd->abd', bases, out )
        class QuadraticFormModel(nn.Module):
            def __init__(self, bases, eigenvalues, constant):
                super(QuadraticFormModel, self).__init__()
                self.bases = nn.Parameter(bases)
                self.eigenvalues = nn.Parameter(eigenvalues) # not actual eigenvalues given we do not enforce unitarity
                self.constant = nn.Parameter(constant)
            def forward(self, x):
                out = torch.einsum('abc,db->dac',self.bases, x) # get x in terms of dim-r eigenbasis -> z, and have a diff eigenbasis for each normal dimension
                out = torch.einsum('abc,bc,abc->ab', out, self.eigenvalues, out) + self.constant # for each normal dim, compute z^2 dot lambda
                return out
        best_loss = float("Inf")
        for trial in range(num_trials):
            bases = torch.stack([torch.from_numpy(ortho_group.rvs(dim=x_data.shape[1], random_state=rng)[:,:rank]).float() for _ in range(y_data.shape[1])])
            eigenvalues = torch.zeros(y_data.shape[1], rank)
            constant = torch.zeros(y_data.shape[1])
            model = QuadraticFormModel(bases, eigenvalues, constant).to(device)
            criterion = nn.MSELoss()
            optimizer = Adam(model.parameters(), lr=learning_rate)
            for epoch in range(num_epochs):
                total_loss = 0
                for offset in range(0, x_data.shape[0], batch_size):
                    outputs = model(x_data[offset:offset+batch_size])
                    loss = criterion(outputs, y_data[offset:offset+batch_size])
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    total_loss+=loss.item()
                if verbose and (epoch % 100 == 0):
                    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss/x_data.shape[0]:.8f}')
            if total_loss<best_loss:
                best_loss = total_loss
                learned_bases = model.bases.data
                learned_eigenvalues = model.eigenvalues.data
                beta = eig_to_mat(learned_eigenvalues,learned_bases).cpu().detach().numpy()
        beta = beta.transpose((1,2,0))
        beta = beta.reshape(-1,beta.shape[-1])
        beta = np.concatenate((model.constant.data.cpu().detach().numpy().reshape(1,-1),beta),axis=0)
        return beta

    @staticmethod
    def regress_w_manopt(
        local_coords_tangent: Float[np.ndarray, "N d"],
        local_coords_normal: Float[np.ndarray, "N n"],
        rank: int=None,
        manopt_iters: int=8000,
        batch_normal: int=1,
        verbose: bool=False,
    ) -> Float[np.ndarray, "d**2+1 n"]:
        rank = local_coords_tangent.shape[1] if rank is None else rank
        beta = []
        def quadratic_form(x,M):
            return torch.sum((x@M)*x, dim = -1)
        for normal_dim in range(batch_normal):
            x_data = torch.from_numpy(local_coords_tangent).float()
            y_data = torch.from_numpy(local_coords_normal[:,normal_dim].flatten())
            manifold = pymanopt.manifolds.fixed_rank.FixedRankEmbedded(local_coords_tangent.shape[1], local_coords_tangent.shape[1], rank)
            manifold = pymanopt.manifolds.product.Product([manifold,pymanopt.manifolds.euclidean.Euclidean(1)])
            @pymanopt.function.pytorch(manifold)
            def cost(u,s,vt,c):
                point = u.float() @ torch.diag(s.float()) @ vt.float()
                return (torch.square(y_data - (quadratic_form(x_data, point + point.T)+c))).mean()
            problem = pymanopt.Problem(manifold, cost)
            optimizer = pymanopt.op1timizers.SteepestDescent(verbosity=2 if verbose else 0,max_iterations=manopt_iters)
            result = optimizer.run(problem)
            M,c = result.point
            u,s,vt = M
            out = u @ np.diag(s) @ vt
            out = out + out.T
            beta.append(np.concatenate((c,out.flatten())))
        beta = np.stack(beta,axis=-1)
        return beta

    @staticmethod
    def evaluate_regression(
        local_coords_tangent: Float[np.ndarray, "N d"],
        local_coords_normal: Float[np.ndarray, "N n"],
        beta: Float[np.ndarray, "d**2+1 n"],
        batch_size: int = None,
        device: str = None,
    ) -> Tuple[int,int]:
        num_points = local_coords_tangent.shape[0]
        intrinsic_dim = local_coords_tangent.shape[1]
        normal_dim = local_coords_normal.shape[1]
        rss = np.zeros(normal_dim)
        tss = np.zeros(normal_dim)
        mse = 0
        y_mean = np.average(local_coords_normal, axis=0)
        prediction = []
        if device=="cuda":
            beta = torch.from_numpy(beta).to(device).float()
        batch_size = num_points if batch_size is None else batch_size
        for offset in range(0, num_points, batch_size):
            actual_batch_size = local_coords_tangent[offset:offset+batch_size].shape[0]
            quad_terms = (local_coords_tangent[offset:offset+batch_size,:,None] * local_coords_tangent[offset:offset+batch_size,None,:]).reshape(actual_batch_size,-1).astype(np.float32)
            quad_terms = np.concatenate([np.ones((actual_batch_size, 1)), quad_terms], axis=1, dtype=np.float32)
            if device=="cuda":
                quad_terms = torch.from_numpy(quad_terms).to(device)
                pred = (quad_terms@beta).cpu().detach().numpy()
            else:
                pred = np.dot(quad_terms, beta)
            prediction.append(pred)
            rss += np.square(local_coords_normal[offset:offset+batch_size]-pred).sum(axis=0)
            tss += np.square(local_coords_normal[offset:offset+batch_size]-y_mean).sum(axis=0)
        if device=="cuda":
            beta = beta.cpu().detach().numpy()
        def r2_manual(numerator,denominator):
            nonzero_denominator = denominator != 0
            nonzero_numerator = numerator != 0
            # Default = Zero Numerator = perfect predictions. Set to 1.0
            # (note: even if denominator is zero, thus avoiding NaN scores)
            output_scores = np.ones([numerator.shape[0]])
            # Non-zero Numerator and Non-zero Denominator: use the formula
            valid_score = nonzero_denominator & nonzero_numerator
            output_scores[valid_score] = 1 - (
                numerator[valid_score] / denominator[valid_score]
            )
            # Non-zero Numerator and Zero Denominator:
            # arbitrary set to 0.0 to avoid -inf scores
            output_scores[nonzero_numerator & ~nonzero_denominator] = 0.0
            return np.average(output_scores)
        r2 = r2_manual(rss,tss)
        mse = (rss/num_points).mean()
        return r2, mse, np.concatenate(prediction,axis=0)


from sklearn.base import BaseEstimator, RegressorMixin

class RLSRegressor(BaseEstimator, RegressorMixin):
    """
    Recursive Least Squares with forgetting (lambda) and optional ridge (alpha),
    supporting multi-output targets and a running R^2 computed *after* updates.

    After T updates (exact arithmetic), solves:
        min_B  sum_{t=1..T} lambda**(T-t) * || y_t - x_t^T B ||_2^2  +  alpha * ||B_no_intercept||_F^2

    Parameters
    ----------
    fit_intercept : bool, default=True
    forgetting_factor : float in (0,1], default=1.0
        lambda=1 gives ordinary LS; <1 exponentially forgets older data.
    alpha : float, default=0.0
        Ridge strength; if >0, initializes P_ = I / alpha.
    p0_scale : float, default=1e6
        Initial covariance scale when alpha == 0 (uninformative prior).
    dtype : np.dtype, default=np.float64
    warm_start : bool, default=False
    r2_multioutput : {'uniform_average','raw_values','variance_weighted'}, default='uniform_average'
        Aggregation across targets.

    Attributes
    ----------
    coef_ : (n_targets, n_features) or (n_features,)
    intercept_ : (n_targets,) or float
    r2_ : float or (n_targets,)
        Running R^2 computed using *post-update* predictions on each batch (with same forgetting/weights as training).
    """

    def __init__(
        self,
        fit_intercept: bool = True,
        forgetting_factor: float = 1.0,
        alpha: float = 0.0,
        p0_scale: float = 1e6,
        dtype=np.float64,
        warm_start: bool = False,
        r2_multioutput: str = "uniform_average",
    ):
        self.fit_intercept = fit_intercept
        self.forgetting_factor = forgetting_factor
        self.alpha = alpha
        self.p0_scale = p0_scale
        self.dtype = dtype
        self.warm_start = warm_start
        self.r2_multioutput = r2_multioutput

        # model state
        self.P_ = None              # (D_aug, D_aug)
        self.beta_ = None           # (D_aug, n_targets)
        self.n_features_in_ = None
        self.n_targets_ = None
        self._fitted = False

        # running R^2 state (weighted/forgotten)
        self.weight_sum_ = 0.0      # scalar W
        self.y_mean_ = None         # (n_targets,)
        self.y_M2_ = None           # (n_targets,)  -- sum w*(y-mean)^2 (population)
        self.sse_ = None            # (n_targets,)  -- sum w*(y - yhat_post)^2

        # sklearn-exposed
        self.coef_ = None
        self.intercept_ = None
        self.r2_ = None

    # ---------------- utilities ----------------

    def _augment(self, X: np.ndarray) -> np.ndarray:
        if self.fit_intercept:
            ones = np.ones((X.shape[0], 1), dtype=self.dtype)
            return np.hstack([ones, X])
        return X

    def _ensure_init(self, X: np.ndarray, y: np.ndarray):
        n_features = X.shape[1]
        n_targets = 1 if y.ndim == 1 else y.shape[1]
        if self._fitted and self.n_features_in_ == n_features and self.n_targets_ == n_targets:
            return

        self.n_features_in_ = n_features
        self.n_targets_ = n_targets
        D_aug = n_features + (1 if self.fit_intercept else 0)

        if self.alpha > 0:
            self.P_ = np.eye(D_aug, dtype=self.dtype) / self.alpha
        else:
            self.P_ = np.eye(D_aug, dtype=self.dtype) * self.p0_scale

        self.beta_ = np.zeros((D_aug, n_targets), dtype=self.dtype)

        # reset running stats
        self.weight_sum_ = 0.0
        self.y_mean_ = np.zeros(n_targets, dtype=self.dtype)
        self.y_M2_ = np.zeros(n_targets, dtype=self.dtype)
        self.sse_ = np.zeros(n_targets, dtype=self.dtype)

        self._fitted = True

    # ---------------- core math ----------------

    def _block_update(self, Xb_aug: np.ndarray, Yb: np.ndarray):
        """Block RLS parameter update (matrix inversion lemma)."""
        lam = float(self.forgetting_factor)
        PXT = self.P_ @ Xb_aug.T
        S = lam * np.eye(Xb_aug.shape[0], dtype=self.dtype) + Xb_aug @ PXT
        K = np.linalg.solve(S, PXT.T).T
        resid = Yb - Xb_aug @ self.beta_
        self.beta_ = self.beta_ + K @ resid
        self.P_ = (self.P_ - K @ (Xb_aug @ self.P_)) / lam
        # Optional: symmetrize tiny drift
        # self.P_ = 0.5 * (self.P_ + self.P_.T)

    def _update_running_r2_post(self, Yb: np.ndarray, Yhat_post: np.ndarray, w: np.ndarray):
        """
        Update running R^2 using *post-update* predictions on this batch.
        Weighted + forgetting: decay previous stats by lam**m, then merge batch stats via Chan.
        """
        m = Yb.shape[0]
        lam = float(self.forgetting_factor)
        decay = lam ** m

        # ensure shapes
        if Yb.ndim == 1:      Yb = Yb.reshape(-1, 1)
        if Yhat_post.ndim == 1: Yhat_post = Yhat_post.reshape(-1, 1)
        if w is None:
            w = np.ones((m, 1), dtype=self.dtype)
        else:
            w = w.reshape(-1, 1).astype(self.dtype, copy=False)

        # batch totals
        Wb = float(np.sum(w))
        if Wb <= 0:
            return

        # batch mean and population M2 of y (for SST)
        num_b = (w * Yb).sum(axis=0)                       # (n_targets,)
        mu_b  = num_b / Wb
        M2_b  = (w * (Yb - mu_b) ** 2).sum(axis=0)         # (n_targets,)

        # batch SSE using *post-update* predictions
        SSE_b = (w * (Yb - Yhat_post) ** 2).sum(axis=0)    # (n_targets,)

        # decay old aggregates
        W_old  = decay * self.weight_sum_
        M2_old = decay * self.y_M2_
        SSE_old= decay * self.sse_

        if W_old == 0.0:
            self.weight_sum_ = Wb
            self.y_mean_ = mu_b
            self.y_M2_ = M2_b
            self.sse_ = SSE_b
        else:
            mu_old = self.y_mean_
            W_new = W_old + Wb
            delta = mu_b - mu_old
            self.y_mean_ = (W_old * mu_old + Wb * mu_b) / W_new
            self.y_M2_   = M2_old + M2_b + (delta ** 2) * (W_old * Wb / W_new)
            self.sse_    = SSE_old + SSE_b
            self.weight_sum_ = W_new

        self._refresh_r2_attr()

    def _refresh_r2_attr(self):
        """Compute running R^2 (sklearn multioutput styles)."""
        eps = 1e-12
        if self.weight_sum_ <= 0:
            self.r2_ = np.nan if self.n_targets_ != 1 else float("nan")
            return
        sst = self.y_M2_                      # = W * var
        sse = self.sse_

        r2_raw = np.empty(self.n_targets_, dtype=self.dtype)
        for j in range(self.n_targets_):
            if sst[j] <= eps:
                r2_raw[j] = 1.0 if sse[j] <= eps else 0.0
            else:
                r2_raw[j] = 1.0 - (sse[j] / sst[j])

        if self.r2_multioutput == "raw_values":
            self.r2_ = r2_raw if self.n_targets_ > 1 else float(r2_raw[0])
        elif self.r2_multioutput == "variance_weighted":
            w = sst / (np.sum(sst) + eps)
            self.r2_ = float(np.sum(w * r2_raw))
        else:  # 'uniform_average'
            self.r2_ = float(np.mean(r2_raw)) if self.n_targets_ > 1 else float(r2_raw[0])

    # ---------------- sklearn API ----------------

    def partial_fit(self, X, y, sample_weight=None):
        """
        Incremental fit on a batch (or single sample).

        This computes the R^2 using *post-update* predictions on the batch.
        """
        X = np.asarray(X, dtype=self.dtype)
        y = np.asarray(y, dtype=self.dtype)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        if y.ndim == 1:
            y = y.reshape(-1, 1)
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of samples.")

        self._ensure_init(X, y)

        # Parameter update first (RLS). For sample weights, scale rows by sqrt(w).
        Xb = self._augment(X)
        Yb = y
        w = None
        if sample_weight is not None:
            w = np.asarray(sample_weight, dtype=self.dtype)
            sw = np.sqrt(w).reshape(-1, 1)
            Xb = Xb * sw
            Yb = Yb * sw
        self._block_update(Xb, Yb)

        # Post-update predictions on the *unweighted* batch
        if self.fit_intercept:
            coef = self.beta_[1:, :]          # (n_features, n_targets)
            intercept = self.beta_[0, :]      # (n_targets,)
        else:
            coef = self.beta_
            intercept = np.zeros(self.n_targets_, dtype=self.dtype)

        yhat_post = X @ coef + intercept       # (m, n_targets)

        # Update running R^2 AFTER the update
        self._update_running_r2_post(y, yhat_post, w)

        # expose coef_/intercept_
        if self.fit_intercept:
            coef_out = self.beta_[1:, :].T
            intercept_out = self.beta_[0, :].copy()
        else:
            coef_out = self.beta_.T
            intercept_out = np.zeros(self.n_targets_, dtype=self.dtype)

        self.coef_ = coef_out[0] if self.n_targets_ == 1 else coef_out
        self.intercept_ = float(intercept_out[0]) if self.n_targets_ == 1 else intercept_out
        return self

    def fit(self, X, y, sample_weight=None):
        """Fit on (X, y). Resets state unless warm_start=True."""
        if not self.warm_start:
            self._fitted = False
            self.P_ = None
            self.beta_ = None
            self.n_features_in_ = None
            self.n_targets_ = None
            self.weight_sum_ = 0.0
            self.y_mean_ = None
            self.y_M2_ = None
            self.sse_ = None
            self.r2_ = None
        return self.partial_fit(X, y, sample_weight=sample_weight)

    def predict(self, X):
        """Predict with shape (n_samples,) for single target or (n_samples, n_targets)."""
        if not self._fitted:
            raise RuntimeError("Model is not fitted yet.")
        X = np.asarray(X, dtype=self.dtype)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"Expected {self.n_features_in_} features, got {X.shape[1]}.")

        if self.fit_intercept:
            coef = self.beta_[1:, :]
            intercept = self.beta_[0, :]
        else:
            coef = self.beta_
            intercept = np.zeros(self.n_targets_, dtype=self.dtype)

        Y = X @ coef + intercept
        return Y if self.n_targets_ > 1 else Y.ravel()
