This package contains 2 functions:



-make\_vprint(verbose): returns a print function that only prints if verbose = True; useful for creating optional print statements in long pipelines



-is\_normalized(): checks if the matrix in a specific (X / layer / obsm) layer has already been normalized for an AnnData object from scanpy (numeric check, not guaranteed to work, if further processing has been done after normalization, eg log1p)



-matrix\_to\_anndata(): returns an anndata object with the specified matrix (from adata.X, adata.layer or adata.obsm) as adata.X. Keeps obs annotations, tries to preserve var annotations of column identity can be guaranteed.



-execute\_subprocess(): runs a python subprocess, with given inputs and outputs. Passes arguments to subprocess including a list of arbitrary python objects.



-import\_cmd\_args(): (used in python subprocesses) imports command line arguments received from execute\_subprocess via stdin





Scanpy is not directly required by the function, but it assumes adata is an AnnData object so the function is useless without scanpy or at least AnnData installed. 

