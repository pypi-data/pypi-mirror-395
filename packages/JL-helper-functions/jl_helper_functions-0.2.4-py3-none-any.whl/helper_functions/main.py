import numpy as np
import sys
import json
import subprocess
import os
import scanpy as sc
import pandas as pd
import warnings
import scipy as sp

def print_to_json(obj, obj_name):
        """output a json file in the working directory, containing the object"""
        # conver entries to strings
        if type(obj) == dict:
            obj_string = {}
            for item in obj.items():
                key = str(item[0])
                value = str(item[1])
                obj_string[key] = value
        if type(obj) == list:
            obj_string = [None for i in range(len(obj))]
            for i in range(len(obj)):
                obj_string[i] = str(obj[i])
        with open(f"{obj_name}.json", "w") as f:
            json.dump(obj_string, f, indent=2)

def make_vprint(verbose):
    """ 
    Return a function that prints if verbose, the argument of this function, is true.
    This is supposed to be called once at the beginning of a function definition.

    Parameters
    ----------
    verbose : bool
        Whether to print the output or not

    Returns
    -------
    function
        A lambda function that prints if verbose is true

    Example
    -------
    >>> vprint = make_vprint(verbose)
    >>> vprint("Hello world")
    """
    return lambda *a, **k: print(*a, **k) if verbose else None 
    # lambda notation: lambda argument1, arugment2: return value (so here we return a function that prints if verbose is true)
    # *a is a tuple of positional arguments, **k is a dictionary of keyword arguments
    # eg in function(a,b,c, d=1, e=2) *a = (a,b,c) and **k = {"d":1, "e":2}


def matrix_to_anndata(adata, matrix_key):
    """Creates a new anndata object with the given matrix (any layer, obsm, or X) as adata.X and returns it.
       preserves obs annotations and row identity, only preserves var annotations and column identity if
       the var_names of adata.X and the matrix match exactly in order, values and length (for obsm matrices, this can only be 
       verified if the obs matrix is a pandas dataframe with index and columns set).
       
       DOES NOT MODIFY ORIGINAL ADATA"""

    # check if matrix_key is unique among adata.layers, adata.obsm, and adata.X
    keys = list(adata.layers.keys()) + list(adata.obsm.keys()) + ["X"]
    if keys.count(matrix_key) > 1:
        raise ValueError(f"Matrix key '{matrix_key}' is not unique among layers, obsm, and X")
    
    # assign correct matrix to a pandas dataframe (so varnames and obs names are implicit to the object)
    if matrix_key == "X":
        adata.X = adata.X.toarray() if (hasattr(adata.X, "toarray") and sp.sparse.issparse(adata.X)) else adata.X # turn scipy sparse matrices into array
        assert type(adata.X) == np.ndarray # make sure it is an array (maybe it did not have the "toarray" attribute and wasn't a numpy array)
        mat = pd.DataFrame( # assign to dataframe and keep known row and column identities
            adata.X,
            index=adata.obs_names,
            columns=adata.var_names
        )
    elif matrix_key in adata.layers:
        adata.layers[matrix_key] = adata.layers[matrix_key].toarray() if (hasattr(adata.layers[matrix_key], "toarray") and sp.sparse.issparse(adata.layers[matrix_key])) else adata.layers[matrix_key]
        assert type(adata.layers[matrix_key]) == np.ndarray
        mat = pd.DataFrame(
            adata.layers[matrix_key],
            index=adata.obs_names,
            columns=adata.var_names
        )
    elif matrix_key in adata.obsm:
        if type(adata.obsm[matrix_key]) == pd.DataFrame: # if the matrix is already a dataframe, just use as is
            mat = adata.obsm[matrix_key].copy()
        elif hasattr(adata.obsm[matrix_key], "toarray") and sp.sparse.issparse(adata.obsm[matrix_key]): # if the matrix is scipy sparse
            adata.obsm[matrix_key] = adata.obsm[matrix_key].toarray() # make into np.ndarray
            assert type(adata.obsm[matrix_key]) == np.ndarray # make sure the conversion worked
            mat = pd.DataFrame(adata.obsm[matrix_key], index=adata.obs_names) # assign to dataframe, without column identities (we cannot be sure that the order was the same, even if length would match adata.varnames; obs names must match by anndata design so we keep them)
        else: # if it is not scipy sparse, or a dataframe
            assert type(adata.obsm[matrix_key]) == np.ndarray # it could be anything so we make sure it is an np.ndarray
            mat = pd.DataFrame(adata.obsm[matrix_key], index=adata.obs_names) # keep obs names, skip var names for above mentioned reason
    else:
        raise ValueError(f"Key '{matrix_key}' not found in X, layers, or obsm")
    
    # assign obs and var
    obs = adata.obs.copy()
    var = adata.var.copy()

    # create new anndata, assign var if possible
    if np.array_equal(var.index, mat.columns): # check if var names and var names in matrix match exaclty
        print(f"{matrix_key} feature count and feature names and order matches adata.var, assigning var and obs to {matrix_key}_adata...")
        matrix_adata = sc.AnnData(X=mat, obs=obs, var=var)
    else:
        print(f"Obsm matrix feature count does not match adata.var, only assigning obs to {matrix_key}_adata...")
        warnings.warn(
            "IMPORTANT:\n\n"
            "This AnnData object can ONLY be used for purposes where column identity "
            "(i.e. which gene corresponds to which column) is unimportant, such as UMAP plots.\n\n"
            "Since the var_names of the provided matrix and those in adata.var_names do not "
            "match exactly in order, values, and length, they cannot be reliably transferred "
            "to the new AnnData object.\n\n"
            "As a result, this object must NOT be used for downstream analyses requiring "
            "precise var_name identity (e.g. differential expression or gene regulatory "
            "network inference).",
            UserWarning
        )
        matrix_adata = sc.AnnData(X=mat, obs=obs)

    return matrix_adata

# check if data is alrdy normalized
def is_normalized(adata, layer: str = None, verbose: bool = False):

    """
    Check if adata is already normalized. Checks for the given layer, which can be in adata.layers or adata.obsm.

    Parameters
    ----------
    adata : anndata.AnnData
        Input data object.
    layer : str, optional
        Which layer to check for normalization. If None, defaults to adata.X.
    verbose : bool, optional
        Whether to print additional information. Defaults to False.

    Returns
    -------
    bool
        Whether the data is normalized.

    Notes
    -----
    Checks if the sum of counts per cell is the same for all cells in the layer.
    If verbose, prints the number of barcodes, median UMIs per barcode, and maximum UMIs per barcode.
    """
    
    vprint = make_vprint(verbose) # function to print if verbose

    # sum of counts per cell for first 100 cells
    if layer == None:
        counts_per_cell = np.array(adata.X[:100].sum(axis=1)).flatten()
    elif layer in adata.layers.keys():
        counts_per_cell = np.array(adata.layers[layer][:100].sum(axis=1)).flatten()
    elif layer in adata.obsm.keys():
        counts_per_cell = np.array(adata.obsm[layer][:100].sum(axis=1)).flatten()

    if verbose == True:
        vprint(f"   Number of barcodes: {adata.n_obs}")
        vprint(f"   Median UMIs per barcode: {np.median(counts_per_cell):.1f}")
        vprint(f"   Max UMIs per barcode: {np.max(counts_per_cell):.0f}")

    # check if all counts are equal
    if np.allclose(counts_per_cell, counts_per_cell[0]): # verify that all entries are equal (integer precision, not useful for comparing floats)
        if verbose == True:
            vprint("adata is normalized")
        return True
    else:
        if verbose == True:
            vprint("adata is NOT normalized")
            vprint(f"Sums of counts per cell for first 100 rows of adata.X:\n{counts_per_cell}")
        return False


def import_cmd_args(constant_count):
    """
    Returns input data path, output data path and each element of a list of python objects received
    from `execute_subprocess` as command line arguments. Set `constant_count` to the number of
    variables you expect to receive as command line arguments.

    Example
    -------

    >>> input_data_path, output_data_path, annotations_list, verbose,  = import_cmd_args(4)
    """

    if constant_count < 2:
        raise ValueError("Please provide at least 2 constant names to import_cmd_args. The first one is the input data path, the second one is the output data path.")

    # assign python objects list
    if constant_count > 2 and sys.argv[3] != "":
        python_objects = sys.argv[3]
    elif constant_count > 2 and sys.argv[3] == "":
        raise ValueError("Trying to assign python objects, but no python objects list was provided. Please provide a list with python objects to execute_subprocess.")
    elif constant_count == 2 and sys.argv[3] != "":
        raise ValueError("Trying to assign python objects, but no constant_names for them where provided in the subprocess. Please provide constant_names for the expected python objects to impor_cmd_args.")

    # import python objects
    if constant_count > 2:
        python_objects = python_objects.split("\n")
        for object in python_objects:
            python_objects[python_objects.index(object)] = json.loads(object.strip())
    else:
        python_objects = []

    return sys.argv[1], sys.argv[2], *python_objects # * unpacks the list into separate elements


def execute_subprocess(subprocess_path: str, inputadata_path: str, output_dir_path: str,
                       python_objects: list = None) -> str:
    """Run a Python subprocess, forward arguments and optional JSON objects, return output file path."""

    # Prepare stdin payload if needed
    stdin_data = "" # must be empty string, so that it can be passed to subprocess. If it were None, then an error would occur
    if python_objects != None:
        for object in python_objects:
            print(f"Forwarding python object to subprocess: Object at index {python_objects.index(object)} of type {type(object)}: {python_objects[python_objects.index(object)]}")
        stdin_data = "\n".join(json.dumps(obj) for obj in python_objects)

    args = ["python", "-u", subprocess_path, inputadata_path, output_dir_path, stdin_data] # u means unbuffered mode -> directly print when print statement


    # Run subprocess, capture stdout + stderr
    # in args: "python" and "-u" in args are swallowed by the function, everthing else is acutally passed to the subprocess
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Parse every line of stdout
    output_file_path = None
    for line in proc.stdout:
        if line.strip().startswith("Output: "):
            output_file_path = line.split("Output:", 1)[1].strip()
            print(f"execute_subprocess: received output: {output_file_path}")
        else:
            print(f"Subprocess {os.path.basename(subprocess_path)}: {line}")

    # Wait for subprocess to finish and collect stderr
    stdout, stderr = proc.communicate(input=stdin_data)

    # if there was an error, raise RntimeError and print stderr
    if proc.returncode != 0:
        raise RuntimeError(f"Subprocess {os.path.basename(subprocess_path)} failed with exit code {proc.returncode}:\n{stderr}")

    # if output file path was not printed to stdout by the subprocess, raise RuntimeError
    if output_file_path is None:
        raise RuntimeError(f"Output file path not found in subprocess {os.path.basename(subprocess_path)} stdout")

    return output_file_path