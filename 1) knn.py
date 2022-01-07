from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np 

#initialization
X_Red = [
    [0.5, 3.0],
    [1.0, 4.25],
    [1.5, 2.0],
    [2.0, 2.75],
    [2.5, 1.65],
    [3.0, 2.7],
    [3.5, 1.0],
    [4.0, 2.5],
    [4.5, 2.1],
    [5.0, 2.75]
]

X_Blue = [
    [0.5, 1.75],
    [1.5, 1.5],
    [2.5, 4.0],
    [2.5, 2.1],
    [3.0, 1.5],
    [3.5, 1.85],
    [4.0, 3.5],
    [5.0, 1.45]
]

#labels for reference for red and blue
Y_Red = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Y_Blue = [0, 0, 0, 0, 0, 0, 0, 0]

X = np.array(X_Red + X_Blue)
Y = np.array(Y_Red + Y_Blue)

k = 3   # number of neighbors, here k = 3
h = 0.02    # step size in mesh

#create color maps for classifiers
map_light = ListedColormap(['#FFC4C5', '#C4FFC5', '#89FFFE'])
map_bold = ListedColormap(['#E60001', '#00E601', '#0000CD'])

classifier = KNeighborsClassifier(n_neighbors=k)

# training phase
classifier.fit(X, Y)

X_min, X_max = X[:, 0].min() - 1, X[:, 0].max() + 1
Y_min, Y_max = X[:, 0].min() - 1, X[:, 0].max() + 1

# convert coordinate vectors into coordinate matrices
XX, yy = np.meshgrid(np.arange(X_min, X_max, h), np.arange(Y_min, Y_max, h))  

# predict
Z = classifier.predict(np.c_[XX.ravel(), yy.ravel()])

# plot
Z = Z.reshape(XX.shape)
plt.figure()
plt.pcolormesh(XX, yy, Z, cmap=map_light)
plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=map_bold)
plt.xlim(XX.min(), XX.max())
plt.ylim(yy.min(), yy.max())
plt.title("k = {}, Decision boundary".format(k))
plt.show()
