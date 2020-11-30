



import torch

import pyprind



import pickle
with open('stock/test_X_Y.pickle', 'rb') as file:
    test_X_Y =pickle.load(file)

X = test_X_Y['X']
Y = test_X_Y['Y']

X_pos = X[:int(len(X)/2)]
X_neg = X[int(len(X)/2):]
Y_pos = Y[:int(len(X)/2)]
Y_neg = Y[int(len(X)/2):]


import random

new_X_pos_index = random.sample([i for i in range(len(X_pos))],len(X_pos))
new_X_pos = [X_pos[new_X_pos_index[i]] for i in range(len(X_pos))]
new_Y_pos = [Y_pos[new_X_pos_index[i]] for i in range(len(X_pos))]

new_X_neg_index = random.sample([i for i in range(len(X_neg))],len(X_neg))
new_X_neg = [X_neg[new_X_neg_index[i]] for i in range(len(X_neg))]
new_Y_neg = [Y_neg[new_X_neg_index[i]] for i in range(len(X_neg))]

new_X_pos_train = new_X_pos[:int(len(new_X_pos)*0.8)]
new_Y_pos_train = new_Y_pos[:int(len(new_Y_pos)*0.8)]
new_X_pos_test = new_X_pos[int(len(new_X_pos)*0.8):]
new_Y_pos_test = new_Y_pos[int(len(new_Y_pos)*0.8):]

new_X_neg_train = new_X_neg[:int(len(new_X_neg)*0.8)]
new_Y_neg_train = new_Y_neg[:int(len(new_Y_neg)*0.8)]
new_X_neg_test = new_X_neg[int(len(new_X_neg)*0.8):]
new_Y_neg_test = new_Y_neg[int(len(new_Y_neg)*0.8):]

train_X = new_X_pos_train + new_X_neg_train
train_Y = new_Y_pos_train + new_Y_neg_train
test_X = new_X_pos_test + new_X_neg_test
test_Y = new_Y_pos_test + new_Y_neg_test

train_index = random.sample([i for i in range(len(train_X))],len(train_X))
train_X = [train_X[train_index[i]] for i in range(len(train_index))]
train_Y = [train_Y[train_index[i]] for i in range(len(train_index))]


train_Y = torch.tensor(train_Y).cuda()
#test_Y = torch.tensor(test_Y).cuda()

from backup_tool import Train_Eval_Process_Layer
Train_Eval_Process_Layer(train_X,train_Y,test_X,test_Y)