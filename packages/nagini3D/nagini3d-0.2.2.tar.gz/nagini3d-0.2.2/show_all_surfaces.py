import numpy as np
import napari 


path = "/home/qrapilly/Documents/Code/Results/test-pypi-nagini/results/surfaces.npz"

df = np.load(path)

points, facets, values, curv = df["points"], df["facets"], df["values"], -df["curvature"]

low = np.quantile(curv,0.05)
high = np.quantile(curv,0.95)
curv_ranged = curv*(curv>low)*(curv<high) + low*(curv<=low) + high*(curv>=high)
max_contrast = max(abs(low), abs(high))

viewer  = napari.view_surface((points,facets,values), ndisplay=3)
viewer.add_surface((points,facets,curv_ranged),contrast_limits=[-max_contrast,max_contrast],colormap="twilight_shifted")

napari.run( )