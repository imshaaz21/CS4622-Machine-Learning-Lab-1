# -*- coding: utf-8 -*-
"""label3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lfZ_5xQ_qZqjZotozzhpNPXPPjLti5xO
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

"""##Label 03"""

train3 = train[FEATURES + ['label_3']].dropna()
valid3 = valid[FEATURES + ['label_3']]

train3.head()

from sklearn import svm

from sklearn.preprocessing import StandardScaler

"""##  without any feature engineering"""

scaler = StandardScaler()

_x_train3 = train3.drop('label_3',axis=1)
y_train3 = train3['label_3']

_x_valid3 = valid3.drop('label_3',axis=1)
y_valid3 = valid3['label_3']

x_train3 = pd.DataFrame(scaler.fit_transform(_x_train3),columns=FEATURES)
x_valid3 = pd.DataFrame(scaler.transform(_x_valid3),columns=FEATURES)

clf = svm.SVC(kernel='linear')
clf.fit(x_train3,y_train3)

y_pred = clf.predict(x_valid3)

from sklearn import metrics

def find_accuracy(Y_pred,Y_valid):
  print(f"accuracy_score {metrics.accuracy_score(Y_valid,Y_pred)}")
  print(f"precision_score {metrics.precision_score(Y_valid,Y_pred,average='weighted')}")
  print(f"recall_score {metrics.recall_score(Y_valid,Y_pred,average='weighted')}")

find_accuracy(y_pred,y_valid3)

"""## Feature selection

### Mutual Information Feature selection
"""

from sklearn.feature_selection import SelectKBest, mutual_info_classif
import numpy as np

for k in [50,200,250]:
  mutual_info_selector = SelectKBest(mutual_info_classif, k=k)
  x_train_mutual_info = mutual_info_selector.fit_transform(x_train3, y_train3)
  print(f"Selected featured: ", x_train_mutual_info.shape[1])

  clf = svm.SVC(kernel='linear')
  clf.fit(x_train_mutual_info,y_train3)
  y_pred = clf.predict(mutual_info_selector.transform(x_valid3))

  print(f"Accuracies for k={k}: ")
  find_accuracy(y_pred,y_valid3)

"""k = 230"""

mutual_info_selector = SelectKBest(mutual_info_classif, k=200)
x_train_mutual_info = mutual_info_selector.fit_transform(x_train3, y_train3)
print(f"Selected featured: ", x_train_mutual_info.shape[1])

clf = svm.SVC(kernel='linear')
clf.fit(x_train_mutual_info,y_train3)
y_pred = clf.predict(mutual_info_selector.transform(x_valid3))

print(f"Accuracies for k={200}: ")
find_accuracy(y_pred,y_valid3)

"""### PCA"""

from sklearn.decomposition import PCA

for n in [0.95,0.99]:
  pca = PCA(n_components=n, svd_solver='full')
  pca.fit(x_train3)
  x_train_pca = pd.DataFrame(pca.transform(x_train3))
  x_valid_pca = pd.DataFrame(pca.transform(x_valid3))
  print(f"Selected featured: ", x_train_pca.shape[1])

  clf = svm.SVC(kernel='linear')
  clf.fit(x_train_pca,y_train3)
  y_pred = clf.predict(x_valid_pca)
  print(f"Accuracies for n_components={n}: ")
  find_accuracy(y_pred,y_valid3)

"""### Mutual Information Feature selection + PCA k=200, n_components=0.99"""

mutual_info_selector = SelectKBest(mutual_info_classif, k=200)
x_train_mutual_info = mutual_info_selector.fit_transform(x_train3, y_train3)
x_valid_mutual_info = mutual_info_selector.transform(x_valid3)
print(f"Selected featured for k=200: ", x_train_mutual_info.shape[1])

pca = PCA(n_components=0.95, svd_solver='full')
pca.fit(x_train_mutual_info)
x_train_pca = pd.DataFrame(pca.transform(x_train_mutual_info))
x_valid_pca = pd.DataFrame(pca.transform(x_valid_mutual_info))
print(f"Selected featured: ", x_train_pca.shape[1])

clf_selected = svm.SVC(kernel='linear')
clf_selected.fit(x_train_pca,y_train3)
y_pred = clf_selected.predict(x_valid_pca)
print(f"Accuracies for n_components={0.95}: ")
find_accuracy(y_pred,y_valid3)

"""### Correlation Co-efficient"""

corr_matrix3 = x_train3.corr()

upper_triangle3 = corr_matrix3.where(np.triu(np.ones(corr_matrix3.shape), k=1).astype(np.bool))
correlated_features_to_drop3 = [column for column in upper_triangle3.columns if any(upper_triangle3[column] > 0.5)]

print("Correlated features to drop:", correlated_features_to_drop3)
print("Number of features to drop:", len(correlated_features_to_drop3))
print("Number of features left:", 256 - len(correlated_features_to_drop3))

clf_cc = svm.SVC(kernel='linear')
clf_cc.fit(x_train3[x_train3.columns.difference(correlated_features_to_drop3)],y_train3)
y_pred = clf_cc.predict(x_valid3[x_valid3.columns.difference(correlated_features_to_drop3)])
print(f"Accuracy: ")
find_accuracy(y_pred,y_valid3)

"""## Y_Test"""

mutual_info_selector = SelectKBest(mutual_info_classif, k=200)
x_train_mutual_info = mutual_info_selector.fit_transform(x_train3, y_train3)
x_valid_mutual_info = mutual_info_selector.transform(x_valid3)

print(f"Selected featured for k=200: ", x_train_mutual_info.shape[1])

pca = PCA(n_components=0.95, svd_solver='full')
pca.fit(x_train_mutual_info)
x_train_pca = pd.DataFrame(pca.transform(x_train_mutual_info))
x_valid_pca = pd.DataFrame(pca.transform(x_valid_mutual_info))
print(f"Selected featured: ", x_train_pca.shape[1])

clf_selected = svm.SVC(kernel='linear')
clf_selected.fit(x_train_pca,y_train3)
y_pred = clf_selected.predict(x_valid_pca)
print(f"Accuracies for n_components={0.95}: ")
find_accuracy(y_pred,y_valid3)

test_df = test.drop(['label_1','label_2','label_3','label_4'],axis=1)

x_test3 = pd.DataFrame(scaler.transform(test_df),columns=FEATURES)

x_test_mutual_info = mutual_info_selector.transform(x_test3)

x_test_pca = pd.DataFrame(pca.transform(x_test_mutual_info))

test_pred = clf_selected.predict(x_test_pca)

x_test_pca

new_column_names = [f'new_feature_{i+1}' for i in range(x_test_pca.shape[1])]

x_test_pca.columns = new_column_names

x_test_pca.head()

pred_df =  pd.DataFrame(test_pred, columns=["Predicted label_3 after feature engineering"])

clf = svm.SVC(kernel='linear')
clf.fit(x_train3,y_train3)

_y_pred_before = clf.predict(x_test3)

pred_df_before =  pd.DataFrame(_y_pred_before, columns=["Predicted label_3 before feature engineering"])

merged_df = pd.concat([x_test_pca, pred_df, pred_df_before], axis=1)

merged_df.head()

merged_df.to_csv('190023G label 3.csv', index=False)





