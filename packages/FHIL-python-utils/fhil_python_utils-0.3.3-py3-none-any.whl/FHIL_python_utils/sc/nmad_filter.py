from scipy.stats import median_abs_deviation
import numpy as np

def nmad_filter(x, nmad=5):
    """Return a boolean mask for values outside nmad * MAD from the median
    
    Parameters
    ----------
    x : array-like
        Input array
    nmad : float, default=5
        Number of MADs from median to use as threshold
    
    Returns
    -------
    np.ndarray
        Boolean mask where True indicates outliers
    """
    mad = median_abs_deviation(x)
    median = np.median(x)
    return (x < median - nmad * mad) | (x > median + nmad * mad)