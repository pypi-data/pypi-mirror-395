import numpy as np
def correct_pvalues_for_multiple_testing(pvalues, correction_type = "Benjamini-Hochberg"):                
    """                                                                                                   
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    p = np.asarray(pvalues, dtype=float)
    orig_shape = p.shape
    p1d = p.ravel()
    n = p1d.size

    # Track finite entries; leave NaNs untouched
    finite = np.isfinite(p1d)
    out = np.full_like(p1d, np.nan, dtype=float)
    from numpy import array, empty                                                                        
    pvalues = array(pvalues) 
    n = int(pvalues.shape[0])                                                                           
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":                                                                   
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":                                                            
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]                                      
        values.sort()
        for rank, vals in enumerate(values):                                                              
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue                                                            
    elif correction_type == "Benjamini-Hochberg":                                                         
        # BH FDR step-up on finite p-values
        idx = np.flatnonzero(finite)
        pfin = p1d[idx]
        order = np.argsort(pfin)                # ascending by p
        ranks = np.arange(1, order.size + 1)    # 1..m
        bh = pfin[order] * order.size / ranks
        bh = np.minimum.accumulate(bh[::-1])[::-1]
        bh = np.clip(bh, 0.0, 1.0)
        adj = np.empty_like(pfin)
        adj[order] = bh
        out[idx] = adj                                                                                                                  
    return new_pvalues
