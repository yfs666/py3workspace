print(__doc__)

# Author: Phil Roth <mr.phil.roth@gmail.com>
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
import pandas as pd


data = pd.read_csv('C:\\Users\\41620\\Desktop\\大数据\\大数据第六阶段'
                   '\\1807机器学习\\算法第二天\\算法后两天课前资料\\consumption_data.csv',encoding='gb18030')



# data_onehot = pd.get_dummies(data)
# data_onehot = data_onehot.fillna(0)
data = data[['R', 'F', 'M']]

data.R = (data.R-data.R.min())/(data.R.max()-data.R.min())
data.F = (data.F-data.F.min())/(data.F.max()-data.F.min())
data.M = (data.M-data.M.min())/(data.M.max()-data.M.min())

kmeans = KMeans(n_clusters = 3, max_iter=1000)
kmeans.fit(data)

label_pred = kmeans.labels_

X = data.values
x0 = X[label_pred == 0]
x1 = X[label_pred == 1]
x2 = X[label_pred == 2]
plt.scatter(x0[:, 0], x0[:, 1], c = "red", marker='o', label='label0')
plt.scatter(x1[:, 0], x1[:, 1], c = "green", marker='*', label='label1')
plt.scatter(x2[:, 0], x2[:, 1], c = "blue", marker='+', label='label2')
plt.xlabel('petal length')
plt.ylabel('petal width')
plt.legend(loc=2)
plt.show()
