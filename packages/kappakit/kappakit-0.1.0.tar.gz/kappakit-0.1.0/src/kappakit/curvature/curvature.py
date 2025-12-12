from jaxtyping import Float
import numpy as np

def shape_from_sff(sff: Float[np.ndarray, "d d n"], n: Float[np.ndarray, "n"]) -> Float[np.ndarray, "d d"]:
    n /= np.linalg.norm(n)
    S = np.einsum('ijk,k->ij', sff, n)
    return S

def principal_from_shape(S: Float[np.ndarray, "d d"]) -> Float[np.ndarray, "d"]:
    eigenvalues, _ = np.linalg.eigh(S)
    k = eigenvalues.real
    return k

def gaussian_from_principal(k: Float[np.ndarray, "d"]) -> float:
    K = np.prod(k)
    return np.prod(K)

def mean_from_principal(k: Float[np.ndarray, "d"]) -> float:
    H = np.mean(k)
    return H

def normal_from_sff(sff: Float[np.ndarray, "d d n"], v: Float[np.ndarray, "d"]) -> float:
    v /= np.linalg.norm(v)
    k_N = np.sqrt(np.sum((np.einsum('ijk,i,j->k', sff, v, v))**2))
    return k_N

def riemannian_from_sff(sff: Float[np.ndarray, "d d n"]) -> Float[np.ndarray, "d d d d"]:
    R = np.einsum('ika,jla->ijkl', sff, sff) - np.einsum('ila,jka->ijkl', sff, sff)
    return R

def ricci_tensor_from_riemannian(R: Float[np.ndarray, "d d d d"]) -> Float[np.ndarray, "d d"]:
    Ric = np.einsum('ikjk->ij', R)
    return Ric

def ricci_from_ricci_tensor(Ric: Float[np.ndarray, "d d"], v: Float[np.ndarray, "d"]) -> float:
    return np.einsum('i,ij,j->', v, Ric, v)

def scalar_from_ricci_tensor(Ric: Float[np.ndarray, "d d"]) -> float:
    S = np.trace(Ric)
    return S

def sectional_from_riemannian(R: Float[np.ndarray, "d d d d"], x: Float[np.ndarray, "d"], y: Float[np.ndarray, "d"]) -> float:
    K = np.einsum('ijkl,i,j,k,l', R, x, y, y, x) / (np.dot(x, x) * np.dot(y, y) - np.dot(x, y)**2)
    return K


def gaussian_from_shape(S: Float[np.ndarray, "d d"]) -> float:
    return gaussian_from_principal(principal_from_shape(S))
def mean_from_shape(S: Float[np.ndarray, "d d"]) -> float:
    return mean_from_principal(principal_from_shape(S))
def gaussian_from_sff(sff: Float[np.ndarray, "d d n"], n: Float[np.ndarray, "n"]) -> float:
    return gaussian_from_principal(principal_from_shape(shape_from_sff(sff, n)))
def mean_from_sff(sff: Float[np.ndarray, "d d n"], n: Float[np.ndarray, "n"]) -> float:
    return mean_from_principal(principal_from_shape(shape_from_sff(sff, n)))
def principal_from_sff(sff: Float[np.ndarray, "d d n"], n: Float[np.ndarray, "n"]) -> Float[np.ndarray, "d"]:
    return principal_from_shape(shape_from_sff(sff, n))
def ricci_from_riemannian(R: Float[np.ndarray, "d d d d"], v: Float[np.ndarray, "d"]) -> float:
    return ricci_from_ricci_tensor(ricci_tensor_from_riemannian(R), v)
def scalar_from_riemannian(R: Float[np.ndarray, "d d d d"]) -> float:
    return scalar_from_ricci_tensor(ricci_tensor_from_riemannian(R))
def ricci_from_sff(sff: Float[np.ndarray, "d d d d"], v: Float[np.ndarray, "d"]) -> float:
    return ricci_from_ricci_tensor(ricci_tensor_from_riemannian(riemannian_from_sff(sff)), v)
def scalar_from_sff(sff: Float[np.ndarray, "d d n"]) -> float:
    return scalar_from_ricci_tensor(ricci_tensor_from_riemannian(riemannian_from_sff(sff)))
def ricci_tensor_from_sff(sff: Float[np.ndarray, "d d n"]) -> Float[np.ndarray, "d d"]:
    return ricci_tensor_from_riemannian(riemannian_from_sff(sff))
def sectional_from_sff(sff: Float[np.ndarray, "d d n"], u: Float[np.ndarray, "d"], v: Float[np.ndarray, "d"]) -> float:
    return sectional_from_riemannian(riemannian_from_sff(sff), u, v)