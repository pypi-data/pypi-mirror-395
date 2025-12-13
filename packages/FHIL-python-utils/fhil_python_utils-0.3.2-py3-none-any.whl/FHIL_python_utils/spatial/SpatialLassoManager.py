import matplotlib.pyplot as plt
import numpy as np

from matplotlib import colors as mcolors
from matplotlib import path
from matplotlib.collections import RegularPolyCollection
from matplotlib.widgets import Lasso


class SpatialLassoManager:
    """
    Interactive selection of points from a set of spatial coordinates

    Examples
    -----------
    >> %matplotlib widget # If in jupyter notebook
    >> fig, ax = plt.subplots(figsize=(6,6))
    >> manager = SpatialLassoManager(ax, objs['SG_SU9747'].obsm['spatial'], hex_size=5)
    >> plt.show() ## Circle cells on interactive plot

    >> ## points can then be retrieved from the manager as cell IDs
    >> objs['SG_SU9265'] = objs['SG_SU9265'][manager.selected, :]
    >> plt.close()
    """
    def __init__(self, ax, data, hex_size=5):
        self.data = data
        self.collection = RegularPolyCollection(
            6, sizes=(hex_size,), offset_transform=ax.transData,
            offsets=data, array=np.zeros(len(data)),
            clim=(0, 1), cmap=mcolors.ListedColormap(["tab:blue", "tab:red"]))
        ax.add_collection(self.collection)
        ax.set_aspect('equal')
        self.selected = np.zeros(len(data), dtype=bool)

        # Auto-scale axes based on data
        margin = 0.02  # add small padding around points
        x_min, x_max = np.min(data[:,0]), np.max(data[:,0])
        y_min, y_max = np.min(data[:,1]), np.max(data[:,1])
        ax.set_xlim(x_min - margin, x_max + margin)
        ax.set_ylim(y_min - margin, y_max + margin)

        canvas = ax.figure.canvas
        canvas.mpl_connect('button_press_event', self.on_press)
        canvas.mpl_connect('button_release_event', self.on_release)

    def callback(self, verts):
        p = path.Path(verts)
        self.selected = p.contains_points(self.data)
        self.collection.set_array(self.selected.astype(int))
        self.collection.figure.canvas.draw_idle()
        del self.lasso

    def on_press(self, event):
        canvas = self.collection.figure.canvas
        if event.inaxes is not self.collection.axes or canvas.widgetlock.locked():
            return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback)
        canvas.widgetlock(self.lasso)

    def on_release(self, event):
        canvas = self.collection.figure.canvas
        if hasattr(self, 'lasso') and canvas.widgetlock.isowner(self.lasso):
            canvas.widgetlock.release(self.lasso)
