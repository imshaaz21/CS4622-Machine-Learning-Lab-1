# -*- coding: utf-8 -*-
"""label4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_dC3b6eNyAIF38_soOIDJDqDq7uBE3db
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

train = pd.read_csv('/content/drive/MyDrive/CS4622 - Machine Learning/Lab 01/train.csv')
valid = pd.read_csv('/content/drive/MyDrive/CS4622 - Machine Learning/Lab 01/valid.csv')
test = pd.read_csv('/content/drive/MyDrive/CS4622 - Machine Learning/Lab 01/test.csv')

train.describe()

valid.describe()

FEATURES = [f'feature_{i}' for i in range(1,257)]

"""## Preprocessing"""

from sklearn.preprocessing import StandardScaler

"""##Label 04"""

train4 = train[FEATURES + ['label_4']].dropna()
valid4 = valid[FEATURES + ['label_4']]

train4.head()

from sklearn import svm

from sklearn.preprocessing import StandardScaler

"""##  without any feature engineering"""

scaler = StandardScaler()

_x_train4 = train4.drop('label_4',axis=1)
y_train4 = train4['label_4']

_x_valid4 = valid4.drop('label_4',axis=1)
y_valid4 = valid4['label_4']

x_train4 = pd.DataFrame(scaler.fit_transform(_x_train4),columns=FEATURES)
x_valid4 = pd.DataFrame(scaler.transform(_x_valid4),columns=FEATURES)

clf = svm.SVC(kernel='linear')
clf.fit(x_train4,y_train4)

y_pred = clf.predict(x_valid4)

from sklearn import metrics

def find_accuracy(Y_pred,Y_valid):
  print(f"accuracy_score {metrics.accuracy_score(Y_valid,Y_pred)}")
  print(f"precision_score {metrics.precision_score(Y_valid,Y_pred,average='weighted')}")
  print(f"recall_score {metrics.recall_score(Y_valid,Y_pred,average='weighted')}")

find_accuracy(y_pred,y_valid4)

"""## Feature selection

### Mutual Information Feature selection
"""

from sklearn.feature_selection import SelectKBest, mutual_info_classif
import numpy as np

for k in [50,100,150,200,250]:
  mutual_info_selector = SelectKBest(mutual_info_classif, k=k)
  x_train_mutual_info = mutual_info_selector.fit_transform(x_train4, y_train4)
  print(f"Selected featured: ", x_train_mutual_info.shape[1])

  clf = svm.SVC(kernel='linear')
  clf.fit(x_train_mutual_info,y_train4)
  y_pred = clf.predict(mutual_info_selector.transform(x_valid4))

  print(f"Accuracies for k={k}: ")
  find_accuracy(y_pred,y_valid4)

"""k = 230"""

for k in [225,230,240]:
  mutual_info_selector = SelectKBest(mutual_info_classif, k=k)
  x_train_mutual_info = mutual_info_selector.fit_transform(x_train4, y_train4)
  print(f"Selected featured: ", x_train_mutual_info.shape[1])

  clf = svm.SVC(kernel='linear')
  clf.fit(x_train_mutual_info,y_train4)
  y_pred = clf.predict(mutual_info_selector.transform(x_valid4))

  print(f"Accuracies for k={k}: ")
  find_accuracy(y_pred,y_valid4)

mutual_info_selector = SelectKBest(mutual_info_classif, k=225)
x_train_mutual_info = mutual_info_selector.fit_transform(x_train4, y_train4)
print(f"Selected featured: ", x_train_mutual_info.shape[1])

clf = svm.SVC(kernel='linear')
clf.fit(x_train_mutual_info,y_train4)
y_pred = clf.predict(mutual_info_selector.transform(x_valid4))

print(f"Accuracies for k={225}: ")
find_accuracy(y_pred,y_valid4)

"""### PCA"""

from sklearn.decomposition import PCA

for n in [0.95,0.99]:
  pca = PCA(n_components=n, svd_solver='full')
  pca.fit(x_train4)
  x_train_pca = pd.DataFrame(pca.transform(x_train4))
  x_valid_pca = pd.DataFrame(pca.transform(x_valid4))
  print(f"Selected featured: ", x_train_pca.shape[1])

  clf = svm.SVC(kernel='linear')
  clf.fit(x_train_pca,y_train4)
  y_pred = clf.predict(x_valid_pca)
  print(f"Accuracies for n_components={n}: ")
  find_accuracy(y_pred,y_valid4)

"""### Mutual Information Feature selection + PCA k=225, n_components=0.99"""

mutual_info_selector = SelectKBest(mutual_info_classif, k=225)
x_train_mutual_info = mutual_info_selector.fit_transform(x_train4, y_train4)
x_valid_mutual_info = mutual_info_selector.transform(x_valid4)
print(f"Selected featured for k=225: ", x_train_mutual_info.shape[1])

pca = PCA(n_components=0.99, svd_solver='full')
pca.fit(x_train_mutual_info)
x_train_pca = pd.DataFrame(pca.transform(x_train_mutual_info))
x_valid_pca = pd.DataFrame(pca.transform(x_valid_mutual_info))
print(f"Selected featured: ", x_train_pca.shape[1])

clf_selected = svm.SVC(kernel='linear')
clf_selected.fit(x_train_pca,y_train4)
y_pred = clf_selected.predict(x_valid_pca)
print(f"Accuracies for n_components={0.99}: ")
find_accuracy(y_pred,y_valid4)

"""### Correlation Co-efficient"""

corr_matrix4 = x_train4.corr()

upper_triangle4 = corr_matrix4.where(np.triu(np.ones(corr_matrix4.shape), k=1).astype(np.bool))
correlated_features_to_drop4 = [column for column in upper_triangle4.columns if any(upper_triangle4[column] > 0.5)]

print("Correlated features to drop:", correlated_features_to_drop4)
print("Number of features to drop:", len(correlated_features_to_drop4))
print("Number of features left:", 256 - len(correlated_features_to_drop4))

clf_cc = svm.SVC(kernel='linear')
clf_cc.fit(x_train4[x_train4.columns.difference(correlated_features_to_drop4)],y_train4)
y_pred = clf_cc.predict(x_valid4[x_valid4.columns.difference(correlated_features_to_drop4)])
print(f"Accuracy: ")
find_accuracy(y_pred,y_valid4)

"""## Y_Test"""

mutual_info_selector = SelectKBest(mutual_info_classif, k=225)
x_train_mutual_info = mutual_info_selector.fit_transform(x_train4, y_train4)
x_valid_mutual_info = mutual_info_selector.transform(x_valid4)

print(f"Selected featured for k=230: ", x_train_mutual_info.shape[1])

pca = PCA(n_components=0.99, svd_solver='full')
pca.fit(x_train_mutual_info)
x_train_pca = pd.DataFrame(pca.transform(x_train_mutual_info))
x_valid_pca = pd.DataFrame(pca.transform(x_valid_mutual_info))
print(f"Selected featured: ", x_train_pca.shape[1])

clf_selected = svm.SVC(kernel='linear')
clf_selected.fit(x_train_pca,y_train4)
y_pred = clf_selected.predict(x_valid_pca)
print(f"Accuracies for n_components={0.99}: ")
find_accuracy(y_pred,y_valid4)

test_df = test.drop(['label_1','label_2','label_3','label_4'],axis=1)

x_test4 = pd.DataFrame(scaler.transform(test_df),columns=FEATURES)

x_test_mutual_info = mutual_info_selector.transform(x_test4)

x_test_pca = pd.DataFrame(pca.transform(x_test_mutual_info))

test_pred = clf_selected.predict(x_test_pca)

x_test_pca

new_column_names = [f'new_feature_{i+1}' for i in range(x_test_pca.shape[1])]

x_test_pca.columns = new_column_names

x_test_pca.head()

pred_df =  pd.DataFrame(test_pred, columns=["Predicted labels after feature engineering"])

clf = svm.SVC(kernel='linear')
clf.fit(x_train4,y_train4)

_y_pred_before = clf.predict(x_test4)

pred_df_before =  pd.DataFrame(_y_pred_before, columns=["Predicted labels before feature engineering"])

merged_df = pd.concat([x_test_pca, pred_df, pred_df_before], axis=1)

merged_df.head()

merged_df.to_csv('190023G_label_4.csv', index=False)

