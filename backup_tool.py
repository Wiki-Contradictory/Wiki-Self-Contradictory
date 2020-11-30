#Evaluation

#accuracy
# PA
# TP(PP)
# FP(PN)
# FN(NP)    
# TN(NN)

import torch
import torch.nn as nn
import torch.optim as optim
def Evaluation(Y_hat,Y):
    print(Y_hat)
    print(Y)
    from sklearn.metrics import f1_score
    TP,FP,FN,TN = 0,0,0,0
    for i in range(len(Y_hat)):
        if int(Y_hat[i]) == 1 and int(Y[i]) ==1:
            TP+=1
        elif int(Y_hat[i]) == 1 and int(Y[i]) ==0:
            FP +=1
        elif int(Y_hat[i]) == 0 and int(Y[i]) ==1:
            FN +=1
        elif int(Y_hat[i]) == 0 and int(Y[i]) ==0:
            TN +=1
        else:
            print('[ERROR]')
    Accuracy = (TP+TN)/(TP+FP+FN+TN)
    Precision = (TP)/(TP+FP)
    Recall = (TP)/(TP+FN)
    F1 = f1_score(Y, Y_hat)

    print('Accuracy:',Accuracy)
    print('Precision:',Precision)
    print('Recall:',Recall)
    print('F1:',F1)



def Train_Eval_Process_Layer(train_X,train_Y,test_X,test_Y):
    # RetaGNN + Self Attention
    import pyprind
    import pickle
    epoch_num =10
    input_dim = 8
    hidden_dim = 8
    model = double_LSTM_model().cuda()
    optimizer = optim.Adam(model.parameters())
    criterion = nn.BCELoss()
    for epoch_  in range(epoch_num):
        model.train() 
        for i in pyprind.prog_bar(range(len(train_X))):
            batch_X,batch_Y = train_X[i],train_Y[i] #(b,l,d) ,(b,)
            batch_Y_hat = model(batch_X).squeeze(dim=-1)
            loss = criterion(batch_Y_hat, batch_Y.float())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            #print('loss:',loss)
        model.eval()
        pred_Y = list()
        for i in range(len(test_X)):
            pred_Y.append(model(test_X[i]).view(1,-1))
        test_Y_hat = torch.cat(pred_Y,0).cpu().data.numpy()
        test_Y_hat_list = list()
        for i in range(test_Y_hat.shape[0]):
            if test_Y_hat[i,0] >= 0.5:
                test_Y_hat_list.append(1)
            else:
                test_Y_hat_list.append(0)
        Evaluation(test_Y_hat_list,test_Y)









#single2batch layer for RetaGNN + Self Attention 
import numpy as np
def Single2Batch_Layer_v2(X,Y,X_text):
    train_rate = 0.8
    batch_size = 32
    train_size = int(train_rate * len(X))
    import random
    data_index = [i for i in range(len(X))]
    shuffle_data_index = random.sample(data_index,len(data_index))
    train_data_index = shuffle_data_index[:train_size]
    test_data_index = shuffle_data_index[train_size:]
    if train_size % batch_size != 0 :
        batch_num = int(train_size / batch_size) + 1 
    else:
        batch_num = int(train_size / batch_size) 
    train_X,train_Y = list(),list()
    X_virtual,Y_virtual = list(),list()
    for i in range(len(train_data_index)):
        X_i,Y_i = X[train_data_index[i]],Y[train_data_index[i]]        
        Y_i = np.array([Y_i])
        X_virtual.append(X_i)
        Y_virtual.append(Y_i.reshape(1,1))
        if len(X_virtual) >= batch_size :
            Y_virtual = np.concatenate(Y_virtual)
            Y_virtual = torch.tensor(Y_virtual)
            train_X.append(X_virtual)
            train_Y.append(Y_virtual)
            X_virtual,Y_virtual = list(),list()
        elif len(train_X) == batch_num - 1 and i == len(train_data_index)-1:
            Y_virtual =  np.concatenate(Y_virtual)
            Y_virtual = torch.tensor(Y_virtual)
            train_X.append(X_virtual)
            train_Y.append(Y_virtual)
    test_X,test_Y,test_X_text = list(),list(),list()
    for i in range(len(test_data_index)):
        X_i,Y_i = X[test_data_index[i]],Y[test_data_index[i]]
        X_i_text = X_text[test_data_index[i]]
        test_X.append(X_i)
        test_Y.append(Y_i)
        test_X_text.append(X_i_text)
    return train_X,train_Y,test_X,test_Y,test_X_text



import torch.nn as nn
class LSTM_model(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(LSTM_model,self).__init__()
        self.input_dim,self.hidden_dim = input_dim,hidden_dim
        self.lstm = nn.LSTM(input_dim, hidden_dim)
        self.attention_weight = nn.Linear(hidden_dim, 1)
        self.fc = nn.Linear(hidden_dim, hidden_dim)
        self.sigmoid_layer = nn.Sigmoid()
        
    def Attention_Layer(self,hidden_vec):
        self.attn = self.attention_weight(hidden_vec)
        out = torch.sum(hidden_vec * self.attn,1)
        return out

    def forward(self, X,sent_type=False):
        hidden_vec, (h_n, c_n) = self.lstm(X)
        attn_layer_out = self.Attention_Layer(hidden_vec)
        out = self.fc(attn_layer_out)
        #out = self.sigmoid_layer(out)
        return out

class double_LSTM_model(nn.Module):
    def __init__(self):
        super(double_LSTM_model,self).__init__()  
        self.lstm_layer = LSTM_model(1024,128).cuda()
        self.fc = nn.Linear(128, 1)
        self.sigmoid_layer = nn.Sigmoid()
    def forward(self,X):
        sent_emd_list = list()
        for i in range(len(X)):
            X_i = X[i]
            sent_embbeding = self.lstm_layer(X_i.view(1,-1,1024),sent_type=True).cuda()
            sent_emd_list.append(sent_embbeding.view(1,-1))
        sent_emd = torch.cat(sent_emd_list,0)
        sent_emd = torch.sum(sent_emd,0).cuda()
        pred_Y = self.fc(sent_emd)
        pred_Y = self.sigmoid_layer(pred_Y)
        return pred_Y
        
