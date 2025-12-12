from typing import Tuple, Union
from jaxtyping import Float
import numpy as np
# from opt_einsum import contract
from scipy.sparse import diags, coo_matrix, eye
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigh
from sklearn.neighbors import NearestNeighbors

class SFFDiffusionMap:
    """
    Second Fundamental Form is in terms of carre du champ operator, which can be obtained in terms of the Laplacian, which is estimated by Diffusion Maps.
    See Jones 2024 (https://arxiv.org/pdf/2411.04100)
    """
    @staticmethod
    def diffusion_map(
        manifold: Float[np.ndarray, "N m"],
        num_eigenfunctions: int = 60,
        c: float = 0,
        num_neighbors: int = 32,
        initial_bandwidth_num_neighbors: int = 8,
    ) -> Tuple[
        Float[np.ndarray,"N N"],
        Float[np.ndarray,"num_eigens N"],
        Float[np.ndarray,"N"],
    ]:
        num_points = manifold.shape[0]
        num_neighbors = min(num_neighbors,num_eigenfunctions)
        ####################################################################################################
        # 1. Setup
        ####################################################################################################
        
        # Find k nearest neighbours
        nbrs = NearestNeighbors(n_neighbors = num_neighbors, algorithm='auto').fit(manifold)
        neighbor_distances: Float[np.ndarray, "N k"]
        neighbor_distances, neighbor_indices = nbrs.kneighbors(manifold)

        # Compute the ad hoc bandwidth function initial_bandwidth
        initial_bandwidth: Float[np.ndarray, "N"] = np.sqrt((neighbor_distances[:,1:initial_bandwidth_num_neighbors]**2).mean(axis=1))
        
        ####################################################################################################
        # 2. Tune the initial parameters initial_epsilon and dim0 to use for density estimation.
        ####################################################################################################

        # Compute the pre_kernel with initial_bandwidth over a range of possible epsilons.
        candidate_epsilons = 2**np.arange(-30,10,step=0.25)
        pre_kernel_dist: Float[np.ndarray, "N k"] = neighbor_distances**2 / (initial_bandwidth[neighbor_indices] * initial_bandwidth.reshape(-1,1))
        pre_kernel: Float[np.ndarray, "N k e"] = np.exp(-pre_kernel_dist.reshape(num_points,num_neighbors,1) / (2*candidate_epsilons.reshape(1,1,-1)))
        pre_kernel_global = pre_kernel.mean(axis = (0,1))

        # Select the initial_epsilon that maximises the criterion and estimate dim0.
        initial_criterion = np.diff(np.log(pre_kernel_global))/np.diff(np.log(candidate_epsilons))
        initial_criterion_index = np.argmax(initial_criterion)
        initial_epsilon = candidate_epsilons[initial_criterion_index]
        dim0 = 2*initial_criterion[initial_criterion_index]

        ####################################################################################################
        # 3. Use initial_epsilon and dim0 to estimate the density density_est.
        ####################################################################################################

        # Compute the heat kernel matrix and symmetrise.
        int_kernel: Float[np.ndarray, "N k"] = np.exp(-pre_kernel_dist/(2*initial_epsilon)) / ((2*np.pi*initial_epsilon)**(dim0/2))
        int_kernel: Float[np.ndarray, "N N"] = coo_matrix((int_kernel.flatten(), (np.repeat(np.arange(num_points),num_neighbors), neighbor_indices.flatten())))
        int_kernel = (int_kernel + int_kernel.T)/2

        # Sum over the rows to get a density estimate.
        density_est = int_kernel.sum(axis=0) / (num_points * initial_bandwidth**dim0)
        density_est: Float[np.ndarray, "N"] = density_est.A[0]

        ####################################################################################################
        # 4. Define the true bandwidth function with the density_est.
        ####################################################################################################

        # Set alpha and beta in terms of the parameter c.
        alpha = 1/2 - c/2 - dim0/4
        beta = -1/2

        # Define bandwidth with density_est.
        bandwidth = density_est**beta
        bandwidth /= np.median(bandwidth)

        ####################################################################################################
        # 5. Tune the final paramters epsilon and dim.
        ####################################################################################################

        # Compute the tuned_kernel with bandwidth over a range of possible epsilons.
        tuned_kernel_distances = neighbor_distances**2 / (bandwidth[neighbor_indices] * bandwidth.reshape(-1,1))
        tuned_kernel: Float[np.ndarray, "N k"] = np.exp(-tuned_kernel_distances.reshape(num_points,num_neighbors,1) / (4*candidate_epsilons.reshape(1,1,-1)))
        tuned_kernel_global = tuned_kernel.mean(axis = (0,1))

        # Select the epsilon that maximizes the criterion and estimate dim.
        criterion = np.diff(np.log(tuned_kernel_global))/np.diff(np.log(candidate_epsilons))
        max_index = np.argmax(criterion)
        epsilon = candidate_epsilons[max_index]
        dim = 2*criterion[max_index]

        ####################################################################################################
        # 6. Define the final kernel matrix K and alpha-normalize.
        ####################################################################################################

        # Compute K with the final epsilon and dim (K is K_ep).
        K: Float[np.ndarray, "N k"] = np.exp(-tuned_kernel_distances/(4*epsilon))
        K: Float[np.ndarray, "N N"] = coo_matrix((K.flatten(), (np.repeat(np.arange(num_points),num_neighbors), neighbor_indices.flatten())))
        K = (K + K.T)/2

        # Normalise K with the 'alpha' normalisation (density is q_ep, K becomes K_{ep,al}).
        density = K.sum(axis=0).A[0] / (bandwidth**dim)
        alpha_normalisation = diags(density**(-alpha))
        K = alpha_normalisation @ K @ alpha_normalisation

        ####################################################################################################
        # 7. Solve the eigenproblem for K via symmetric normalization.
        ####################################################################################################

        # Compute the normalisations D and P.
        D = K.sum(axis=0).A[0]
        P2 = bandwidth**2

        # Compute the Laplacian as an operator.
        L = diags(1/P2) @ (eye(num_points) - diags(1/D) @ K) / epsilon

        # Form the symmetric normalisation of K.
        sample_density = D*P2
        S_normalisation = diags(sample_density**(-1/2))
        K = S_normalisation @ K @ S_normalisation - diags(1/P2)
        K /= epsilon

        # Find eigenvalues and eigenfunctions of K, un-normalize, and clean up data.
        eigenvalues, eigenvectors = eigsh(K, num_eigenfunctions, which = 'LA')
        eigenvectors = S_normalisation @ eigenvectors
        eigenvectors = eigenvectors[:,::-1].T
        eigenvalues = -eigenvalues[::-1]

        return L, eigenvectors, sample_density
    
    @staticmethod
    def tangent_bundle(
        manifold: Float[np.ndarray, "N m"],
        num_eigenfunctions: int = 100,
        c: float=0,
        num_neighbors: int=32,
        initial_bandwidth_num_neighbors: int=8,
        return_all: bool = False,
    ) -> Union[
        Float[np.ndarray, "N m m"],
        Tuple[
            Float[np.ndarray, "N m m"],
            Float[np.ndarray, "N m"],
            Float[np.ndarray,"N N"],
            Float[np.ndarray, "N m m"],
            Float[np.ndarray, "N m"],
            Float[np.ndarray,"num_eigens N"],
            Float[np.ndarray,"N"],
        ],
    ]:
        num_points = manifold.shape[0]

        # Compute the Laplacian.
        L, eigenvectors, sample_density = SFFDiffusionMap.diffusion_map(
            manifold=manifold,
            num_eigenfunctions=num_eigenfunctions,
            c=c,
            num_neighbors=num_neighbors,
            initial_bandwidth_num_neighbors=initial_bandwidth_num_neighbors,
        )

        # Bandlimit the data to the first n0 eigenfunctions (i.e. smooth it a bit).
        manifold_bandlimited: Float[np.ndarray, "N m"] = eigenvectors.T @ eigenvectors*sample_density @ manifold
        # Compute the carré du champ (Gamma) pointwise, i.e. metric in the tangent space for each x.
        XiLXj: Float[np.ndarray, "N m m"] = manifold_bandlimited.reshape(num_points,-1,1) * (L @ manifold_bandlimited).reshape(num_points,1,-1)
        coord_products = (manifold_bandlimited.reshape(num_points,-1,1) * manifold_bandlimited.reshape(num_points,1,-1))
        LXiXj = (L @ coord_products.reshape(num_points,-1)).reshape(coord_products.shape)
        Gamma: Float[np.ndarray, "N m m"] = (1/2)*(XiLXj + XiLXj.transpose((0,2,1)) - LXiXj)

        # Bandlimit Gamma to the first n0 eigenfunctions.
        Gamma_bandlimited = (eigenvectors.T @ eigenvectors*sample_density @ Gamma.reshape(num_points,-1)).reshape(Gamma.shape)
        
        # Diagonalise Gamma at each point to get an orthornomal basis for each tangent space.
        def pointwise_decomp(
            pointwise_matrices: Float[np.ndarray, "N m m"]
        ) -> Tuple[
            Float[np.ndarray, "N m"],
            Float[np.ndarray, "N m m"],
        ]:
            vals, vecs = [], []
            for m in pointwise_matrices:
                a, b = eigh(m)
                vals.append(a[::-1])
                vecs.append(b[:,::-1])
            return np.array(vals), np.array(vecs)
        pointwise_eigenvalues, tangent_bundle = pointwise_decomp(Gamma_bandlimited)
        if return_all:
            return tangent_bundle, pointwise_eigenvalues, L, Gamma, manifold_bandlimited, eigenvectors, sample_density, Gamma_bandlimited
        else:
            return tangent_bundle
        
    @staticmethod
    def sff_from_carre(
        tangent_bundle: Float[np.ndarray, "N m m"],
        intrinsic_dimension: int,
        L: Float[np.ndarray, "N N"],
        Gamma: Float[np.ndarray, "N m m"],
        manifold: Float[np.ndarray, "N m"],
    ) -> Float[np.ndarray, "N n d d"]:
        n, D = manifold.shape

        # Compute the iterated carré du champ \Gamma(x_1, \Gamma(x_2, x_3)).
        Gamma_iterated: Float[np.ndarray, "N d d d"] = manifold.reshape(n,D,1,1) * (L @ Gamma.reshape(n,-1)).reshape(n,1,D,D) # x_1 L(x_2)
        Gamma_iterated += Gamma.reshape(n,1,D,D) * (L @ manifold).reshape(n,D,1,1) # x_1 L(x_2) + x_2 L(x_1)
        Gamma_coord_products = manifold.reshape(n,D,1,1) * Gamma.reshape(n,1,D,D) # x_1x_2
        LGammaData = (L @ Gamma_coord_products.reshape(n,-1)).reshape(n,D,D,D) # L(x_1x_2)
        Gamma_iterated -= LGammaData # x_1 L(x_2) + x_2 L(x_1) - L(x_1x_2)
        Gamma_iterated /= 2

        # Compute the Hessian with the iterated Gamma term, with shape [n, D, D, D],
        # so that H[p,l,i,j] = H_p(x_l)(\nabla x_i, \nabla x_j)
        Hessian = (1/2)*(Gamma_iterated.transpose((0,3,1,2))
                        + Gamma_iterated.transpose((0,3,2,1))
                        - Gamma_iterated)

        # Compute the Hessian of the normals: the matrices H(n^l)(x_i,x_j) = (alpha^l_ij) for each l.
        # T is the basis for the tangent space and N is the basis for the normal space.
        T = tangent_bundle[:,:,:intrinsic_dimension]
        N = tangent_bundle[:,:,intrinsic_dimension:]
        alpha = np.einsum('pstu,psl,pti,puj->plij', Hessian, N, T, T)
        return alpha
    
    @staticmethod
    def scalar_curvature(
        manifold: Float[np.ndarray, "N m"],
        intrinsic_dimension: int,
        num_eigenfunctions: int=50,
        c: float=0,
        num_neighbors: int=32,
        initial_bandwidth_num_neighbors: int=8,
    ) -> float:
        # Compute the tangent bundle.
        tangent_bundle, pointwise_eigenvalues, L, Gamma, manifold_bandlimited, eigenvectors, sample_density, Gamma_bandlimited = SFFDiffusionMap.tangent_bundle(
            manifold=manifold,
            num_eigenfunctions=num_eigenfunctions,
            c=c,
            num_neighbors=num_neighbors,
            initial_bandwidth_num_neighbors=initial_bandwidth_num_neighbors,
            return_all=True,
        )

        # Rescale the carré du champ and Laplacian to the correct ambient geometry.
        scale_function: Float[np.ndarray, "N"] = np.mean(pointwise_eigenvalues[:,:intrinsic_dimension], axis = 1)
        average_scale = np.median(scale_function)
        Gamma /= average_scale
        L /= average_scale

        # Compute the Hessian of the normal vectors, with shape [n, D-d, d, d].
        alpha: Float[np.ndarray, "N n d d"] = SFFDiffusionMap.sff_from_carre(tangent_bundle, intrinsic_dimension, L, Gamma, manifold_bandlimited)

        # Compute Riemann curvature and bandlimit.
        Riemann = np.einsum('pLik,pLjl->pijkl',alpha,alpha) - np.einsum('pLjk,pLil->pijkl',alpha,alpha)
        Riemann: Float[np.ndarray, "N d d d d"] = (eigenvectors.T @ (eigenvectors*sample_density) @ Riemann.reshape(manifold.shape[0],-1)).reshape(Riemann.shape)

        # Compute Ricci curvature.
        Ricci: Float[np.ndarray, "N d d"] = np.einsum('pkikj->pij', Riemann)

        # Compute scalar curvature.
        scalar = np.einsum('pii->p', Ricci)
        
        return scalar