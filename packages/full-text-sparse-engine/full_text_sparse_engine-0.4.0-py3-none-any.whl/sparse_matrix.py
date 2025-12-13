import os
import numpy as np
from scipy.sparse import csr_matrix

def save_sparse_matrix(path, matrix):
    """Saves a csr_matrix to disk in a memory-mappable format."""
    np.save(os.path.join(path, "data.npy"), matrix.data)
    np.save(os.path.join(path, "indices.npy"), matrix.indices)
    np.save(os.path.join(path, "indptr.npy"), matrix.indptr)

def load_sparse_matrix(path):
    """Loads a csr_matrix from disk as a memory-mapped object."""
    data = np.load(os.path.join(path, "data.npy"), mmap_mode="r")
    indices = np.load(os.path.join(path, "indices.npy"), mmap_mode="r")
    indptr = np.load(os.path.join(path, "indptr.npy"), mmap_mode="r")
    return csr_matrix((data, indices, indptr))
