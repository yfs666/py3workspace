import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

digits = datasets.load_iris()

X = digits.data.astype(np.float32)
Y = digits.target.reshape(-1,1).astype(np.float32)


# 分隔训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=1 / 3., random_state=8)

from sklearn.preprocessing import StandardScaler  # 对数据归一化

scaler = StandardScaler()
X_std_train = scaler.fit_transform(X_train)
X_std_test = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

# penalty:正则化 l2/l1
# C ：正则化强度
# multi_class:多分类时使用 ovr: one vs rest
lor = LogisticRegression(penalty='l1', C=100, multi_class='ovr')
lor.fit(X_std_train, y_train)
y_pred = lor.predict(X_std_test)
print(lor.score(X_std_test, y_test))

sgdv = SGDClassifier(penalty='l1')
sgdv.fit(X_std_train, y_train)
print(sgdv.score(X_std_test, y_test))
