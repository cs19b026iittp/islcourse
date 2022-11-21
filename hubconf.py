# -*- coding: utf-8 -*-
"""hubconf

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dcKskcQS7Pgm6sCrtwFJGBRQ-qg7rVIp
"""

from sklearn.datasets import make_blobs, make_circles, load_digits
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import homogeneity_score, completeness_score, v_measure_score
import torch
from torch import nn
import torch.optim as optim


def get_data_blobs(n_points=100):
  X, y = make_blobs(n_samples=n_points, centers=3, 
                    n_features=2,random_state=0)
  return X,y

def get_data_circles(n_points=100):
  X, y = make_circles(n_samples=n_points, shuffle=True,  
                      factor=0.3, noise=0.05, random_state=0)
  return X,y

def get_data_mnist():
  digits = load_digits()
  X=digits.data
  y=digits.target
  return X,y

def build_kmeans(X=None,k=10):
  # k is a variable, calling function can give a different number
  # Refer to sklearn KMeans method
  km = KMeans(n_clusters=k, random_state=0).fit(X)
  return km

def assign_kmeans(km=None,X=None):
  ypred = km.predict(X)
  return ypred

def compare_clusterings(ypred_1=None,ypred_2=None):
  pass
  # refer to sklearn documentation for homogeneity, completeness and vscore
  h = "%.6f" % homogeneity_score(ypred_1, ypred_2)
  c = "%.6f" % completeness_score(ypred_1, ypred_2)
  v = "%.6f" % v_measure_score(ypred_1, ypred_2)
 
  return h,c,v

# X_b , y_b = get_data_blobs()
# X_c, y_c = get_data_circles()
# km = build_kmeans(X = X_b, k = 10)
# y_b_pred = assign_kmeans(km, X_b)
# print(y_b_pred)

# km = build_kmeans(X = X_c, k = 10)
# y_c_pred = assign_kmeans(km, X_c)
# print(y_c_pred)

# print(compare_clusterings(y_b_pred, y_c_pred))

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import GridSearchCV

def build_lr_model(X=None, y=None):
  # Build logistic regression, refer to sklearn
  lr_model = LogisticRegression(solver="liblinear",fit_intercept=False)
  lr_model.fit(X,y)
  return lr_model

def build_rf_model(X=None, y=None):
  # Build Random Forest classifier, refer to sklearn
  rf_model = RandomForestClassifier(random_state=400)
  rf_model.fit(X,y)
  return rf_model

def get_metrics(model1=None,X=None,y=None):
  acc, prec, rec, f1, auc = 0,0,0,0,0
  y_pred = model1.predict(X)
  acc = accuracy_score(y, y_pred)
  prec = precision_score(y, y_pred, average='micro')
  rec =  recall_score(y, y_pred , average='micro')
  f1 =  f1_score(y, y_pred, average='micro' )
  auc = roc_auc_score(y, model1.predict_proba(X), multi_class='ovr' )
  return acc, prec, rec, f1, auc

# from sklearn.model_selection import train_test_split
# X, y = get_data_mnist()
# Xtrain,Xtest,ytrain,ytest = train_test_split(X,y,test_size=0.3)

# lr_model = build_lr_model(Xtrain, ytrain)
# rf_model = build_rf_model(Xtrain, ytrain)

# print(get_metrics(lr_model, Xtest, ytest))
# print(get_metrics(rf_model, Xtest, ytest))

import warnings
warnings.filterwarnings('ignore')

def get_paramgrid_lr():
  lr_param_grid = {"C": np.logspace(-3, 3, 7), "penalty": ["l1", "l2"]}
  return lr_param_grid

def get_paramgrid_rf(): 
  rf_param_grid = {
        'max_depth': [1, 10, None],
        'n_estimators': [1, 10, 100],
        'criterion': ['gini', 'entropy']
    }
  return rf_param_grid

def perform_gridsearch_cv_multimetric(model1=None, param_grid=None, cv=5, X=None, y=None, metrics=['accuracy','roc_auc']):
  
  grid_search_cv = GridSearchCV(model1, param_grid, cv=cv)
  grid_search_cv.fit(X, y)
  params = grid_search_cv.best_params_
  acc, prec, rec, f1, auc = 0, 0, 0, 0, 0
  if 'criterion' in params.keys():
    rfc1 = RandomForestClassifier(random_state=42, n_estimators=params['n_estimators'], max_depth=params['max_depth'], criterion=params['criterion'])
    rfc1.fit(X,y)
    acc, prec, rec, f1, auc = get_metrics(rfc1, X, y)
  else:
    lg1 = LogisticRegression(C=params['C'], penalty=params['penalty'],solver = "liblinear")
    lg1.fit(X, y)
    acc, prec, rec, f1, auc = get_metrics(lg1, X, y)
  
  top1_scores = []
  for k in metrics:
      if k == 'accuracy':
          top1_scores.append(acc)
      elif k == 'recall':
          top1_scores.append(rec)
      elif k == 'roc_auc':
          top1_scores.append(auc)
      elif k == 'precision':
          top1_scores.append(prec)
      else:
          top1_scores.append(f1)
        

  return top1_scores

# param_grid = get_paramgrid_lr()
# print(perform_gridsearch_cv_multimetric(model1=LogisticRegression(), param_grid=param_grid, cv=5, X=X, y=y, metrics=['accuracy']))

# param_grid = get_paramgrid_rf()
# print(perform_gridsearch_cv_multimetric(model1=RandomForestClassifier(), param_grid=param_grid, cv=5, X=X, y=y, metrics=['accuracy']))

class MyNN(nn.Module):
  def __init__(self,inp_dim=64,hid_dim=13,num_classes=10):
    super(MyNN,self).__init__()
    
    self.fc_encoder = nn.Linear(inp_dim,hid_dim) 
    self.fc_decoder = nn.Linear(hid_dim,inp_dim) 
    self.fc_classifier = nn.Linear(hid_dim,num_classes) 
    
    self.relu = nn.ReLU() #write your code - relu object
    self.softmax = nn.Softmax() #write your code - softmax object
    
  def forward(self,x):
    x = torch.flatten(x) # write your code - flatten x
    x = torch.nn.functional.normalize(x, p=2.0, dim=0)
    x_enc = self.fc_encoder(x)
    x_enc = self.relu(x_enc)
    
    y_pred = self.fc_classifier(x_enc)
    y_pred = self.softmax(y_pred)
    
    x_dec = self.fc_decoder(x_enc)
    
    return y_pred, x_dec
  
  # This a multi component loss function - lc1 for class prediction loss and lc2 for auto-encoding loss
  def loss_fn(self,x,yground,y_pred,xencdec):
    lc1 = -(torch.nn.functional.one_hot(yground,num_classes=y_pred.shape[-1])*torch.log(y_pred)) # write your code for cross entropy between yground and y_pred, advised to use torch.mean()
    lc1=torch.mean(lc1)
    lc2 = torch.mean((x - xencdec)**2)
    return lc1+lc2
    
def get_mynn(inp_dim=64,hid_dim=13,num_classes=10):
  mynn = MyNN(inp_dim,hid_dim,num_classes)
  mynn.double()
  return mynn

def get_mnist_tensor():
  X,y = load_digits(return_X_y=True)
  X_tensor=torch.tensor(X)
  y_tensor=torch.tensor(y)
  return X_tensor,y_tensor

def get_loss_on_single_point(mynn,x0,y0):
  y_pred, xencdec = mynn(x0)
  lossval = mynn.loss_fn(x0,y0,y_pred,xencdec)
  return lossval

def train_combined_encdec_predictor(mynn,X,y, epochs=11):
  # X, y are provided as tensor
  # perform training on the entire data set (no batches etc.)
  # for each epoch, update weights
  
  optimizer = optim.SGD(mynn.parameters(), lr=0.01)
  
  for i in range(epochs):
    for j in range(X.shape[0]):
      try:
        optimizer.zero_grad()
        ypred, Xencdec = mynn(X[j])
        lval = mynn.loss_fn(X[j],y,ypred,Xencdec)
        lval.backward()
        optimizer.step()
      except:
        pass
  return mynn