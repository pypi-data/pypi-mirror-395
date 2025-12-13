import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def ridge_plot(objs, metric, x_label, table='obs'):
    plotdata = pd.concat(
        {name: getattr(obj, table) for name, obj in objs.items()},
        names=["sample"]
    ).reset_index(level="sample")

    # sns.set_theme(style="white", rc={"axes.facecolor": (0n_genes_by_counts, 0, 0, 0)})
    g = sns.FacetGrid(
        plotdata,
        row="sample",
        hue="sample",
        aspect=15,
        height=0.5,
        #     palette=pal
    )
    # Disable tight_layout to prevent warnings with negative spacing
    g.figure.set_tight_layout(False)

    g.map(sns.kdeplot, metric,
        bw_adjust=0.5,
        clip_on=False,
        fill=True,
        alpha=1,
        linewidth=1)
    # g.map(sns.kdeplot, metric,
    #     bw_adjust=0.5,
    #     clip_on=False,
    #     color="w",
    #     lw=1.1)

    # g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)
    # g.refline(x=20, linewidth=1, linestyle='--', color='red')

    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, 0.2, label, color=color, ha='right', va='center', transform=ax.transAxes)
    g.map(label, metric)

    # Use subplots_adjust instead of tight_layout to control overlap
    g.figure.subplots_adjust(hspace=-0.25)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="", xlabel=x_label)
    g.despine(bottom=True, left=True)
    return g