import numpy as np
import squidpy as sq
import matplotlib.pyplot as plt
from anndata import AnnData
from typing import Dict, List, Optional

def multiObjectSpatialScatter(
    objs: Dict[str, AnnData],
    color_by: List[str],
    spatial_key: str = 'spatial',
    shape: Optional[str] = None,
    figsize: int = 4,
    wspace: float = 0.5,
) -> plt.Figure:
    """
    Plot spatial scatter plots for multiple objects.
    """
    nrows = len(objs)
    ncols = len(color_by)

    # Main figure containing subfigures (one per object)
    fig = plt.figure(figsize=(ncols * figsize + figsize * wspace * (ncols - 1),
                              nrows * figsize))

    subfigs = fig.subfigures(nrows=nrows, ncols=1)

    # If there's only one object, enforce a list for consistent indexing
    if nrows == 1:
        subfigs = [subfigs]

    for (obj_name, adata), subfig in zip(objs.items(), subfigs):
        # Title for the entire row
        subfig.suptitle(obj_name, fontsize=14)

        # Create row of axes inside the subfigure
        axs = subfig.subplots(1, ncols)
        subfig.subplots_adjust(wspace=wspace)

        # Handle axs shape for the single-feature case
        if ncols == 1:
            axs = [axs]

        for ax, feature in zip(axs, color_by):
            sq.pl.spatial_scatter(
                adata,
                color=feature,
                shape=shape,
                spatial_key=spatial_key,
                return_ax=True,
                ax=ax,
            )
            ax.set_title(feature)

    return fig
