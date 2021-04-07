mport numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

good_events = np.array([list(element.values()) for element in json.load(open('dataset_real_good_uniq.json'))])
bad_events = np.array([list(element.values()) for element in json.load(open('dataset_real_bad_uniq.json'))])
events = np.concatenate((good_events, bad_events), axis=0)
x = events[:, :11]
y = events[:, 11]

x2 = StandardScaler().fit_transform(x)
pca = PCA(n_components=2)
pc = pca.fit_transform(x2)
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('PCA 1', fontsize = 15)
ax.set_ylabel('PCA 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
colors = ['r', 'b']
targets = ['good', 'bad']
ax.scatter(pc[:750,0], pc[:750,1], c=colors[1], s = 50)
ax.scatter(pc[750:,0], pc[750:,1], c=colors[0], s = 50)
ax.legend(targets)
ax.grid()
plt.show()
