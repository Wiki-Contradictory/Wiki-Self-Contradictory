






import pyprind



import pickle
with open('stock/pair_sent_and_DATA.pickle', 'rb') as file:
    pair_sent_and_DATA =pickle.load(file)

pos_X = pair_sent_and_DATA['pos_X']
neg_X = pair_sent_and_DATA['neg_X']
pos_title = pair_sent_and_DATA['pos_title']
neg_title = pair_sent_and_DATA['neg_title']
pos_id = pair_sent_and_DATA['pos_id']
neg_id = pair_sent_and_DATA['neg_id']
pos_SC = pair_sent_and_DATA['pos_SC']
neg_SC = pair_sent_and_DATA['neg_SC']





print('pos X len:',len(pos_X))
print('neg X len:',len(neg_X))




def Sent2Pair_Sent(X,filter_or_not=False):
    X_pair_sent = list()
    for i in pyprind.prog_bar(range(len(X))):
        X_pair_sent_i = list()
        X_i = X[i]
        for j in range(len(X_i)):
            for k in range(len(X_i)):
                if j < k:
                    if filter_or_not is True:
                        idx = str(i) + '-' + str(j) + '-' + str(k)
                        X_pair_sent_i.append([X_i[j],X_i[k],idx])
                    else:
                        X_pair_sent_i.append([X_i[j],X_i[k]])
        X_pair_sent.append(X_pair_sent_i)   
    return X_pair_sent


#pos_X_pair = Sent2Pair_Sent(pos_X,filter_or_not=True)
#neg_X_pair = Sent2Pair_Sent(neg_X_sample)



# pair_pos_X = list()

import torch
# Download RoBERTa already finetuned for MNLI
roberta = torch.hub.load('pytorch/fairseq', 'roberta.large.mnli')
roberta.cuda()
roberta.eval()  # disable dropout for evaluation
from fairseq.data.data_utils import collate_tokens





def NLI_model(semantic_pair_sent):
    batch_of_pairs = semantic_pair_sent
    tokens = list()
    for pair in batch_of_pairs:
        tokens.append(roberta.encode(pair[0], pair[1]))
    if len(tokens) !=0:
        batch = collate_tokens(
            tokens, pad_idx=1
        ) 
        logprobs = roberta.predict('mnli', batch)
        #max_value = torch.max(softmax_layer(logprobs))
        return logprobs.argmax(dim=1)

def X_list2batch(X_list,batch_size=32,filter_or_not=False):
    batch_num = int(len(X_list)/batch_size)+1
    batch_list,batch_idx = list(),list()
    idx_list = list()
    for i in range(len(X_list)):
        idx_list.append(X_list[i][-1])
    for i in range(batch_num):
        X_list_batch = X_list[i*batch_size:(i*batch_size)+batch_size]
        idx_batch = idx_list[i*batch_size:(i*batch_size)+batch_size]
        if len(X_list_batch) != 0:
            if filter_or_not is True:
                batch_list.append(X_list_batch)
                batch_idx.append(idx_batch)
            else:
                batch_list.append(X_list_batch)
    if filter_or_not is True:
        return batch_list,batch_idx
    else:
        return batch_list

def Prediction(X_pair):
    pred_Y = list()
    import torch.nn as nn
    softmax_layer = nn.Softmax(dim=1)
    for i in pyprind.prog_bar(range(len(X_pair))):
        Y_ = 0
        X_pair_i = X_pair[i]
        batch_list = X_list2batch(X_pair_i)
        for j in range(len(batch_list)):
            tensor_output = NLI_model(batch_list[j])
            if tensor_output is not None:
                array_outtput = tensor_output.cpu().data.numpy()
                for k in range(array_outtput.shape[0]):
                    if array_outtput[k] == 0 and max_value >=0.9:
                        Y_ = 1
        pred_Y.append(Y_)
    return pred_Y
    
def Filter_BY_NLI(X_pair,pos_title,pos_id,pos_SC):
    contradictory_pair_sent = list()#title,page_id,SC,idx,[sa,sb]
    for i in pyprind.prog_bar(range(len(X_pair))):
        contradictory_pair_sent_i = list()
        X_pair_i = X_pair[i]
        if len(X_pair_i) <= 10000:
            print(1)
            title = pos_title[i]
            page_id = pos_id[i]
            SC = pos_SC[i]
            batch_list,batch_idx = X_list2batch(X_pair_i,filter_or_not=True)
            for j in range(len(batch_list)):
                #print('2-'+str(j))
                tensor_output = NLI_model(batch_list[j])
                if tensor_output is not None:
                    array_outtput = tensor_output.cpu().data.numpy()
                    for k in range(array_outtput.shape[0]):
                        if array_outtput[k] == 0:
                            pair_sent = batch_list[j][k]
                            info_ = [title,page_id,SC,batch_idx[j][k],pair_sent]
                            contradictory_pair_sent_i.append(info_)
        contradictory_pair_sent.append(contradictory_pair_sent_i)
    return contradictory_pair_sent




# #title,page_id,SC,idx,[sa,sb]
# contradictory_pair_sent = Filter_BY_NLI(pos_X_pair,pos_title,pos_id,pos_SC)
# import pickle

# a_dict = {'pos_X':pos_X,'contradictory_pair_sent':contradictory_pair_sent}



# file = open('stock/contradictory_pair_sent.pickle', 'wb')
# pickle.dump(a_dict, file)
# file.close()








import re
X,Y = list(),list()
for i in pyprind.prog_bar(range(len(pos_X))):
    pos_X_i = pos_X[i]
    X_i = list()
    if len(pos_X_i) != 0:
        for j in range(len(pos_X_i)):
            sent_ = pos_X_i[j]
            sent_ = ' '.join(re.sub('[^a-zA-Z0-9.%]',' ',sent_).split())
            if sent_.isalpha():
                doc = roberta.extract_features_aligned_to_words(sent_)
                sent_vector_ = list()
                for tok in doc:
                    sent_vector_.append(tok.vector.view(1,-1))
                sent_vector_ = torch.cat(sent_vector_,0)
        X_i.append(sent_vector_)
    if len(X_i) != 0:
        X.append(X_i)
        Y.append(1)

for i in pyprind.prog_bar(range(len(neg_X))):
    neg_X_i = neg_X[i]
    X_i = list()
    if len(neg_X_i) !=0:
        for j in range(len(neg_X_i)):
            sent_ = neg_X_i[j]
            sent_ = ' '.join(re.sub('[^a-zA-Z0-9.%]',' ',sent_).split())
            if sent_.isalpha():
                doc = roberta.extract_features_aligned_to_words(sent_)
                sent_vector_ = list()
                for tok in doc:
                    sent_vector_.append(tok.vector.view(1,-1))
                sent_vector_ = torch.cat(sent_vector_,0)
        X_i.append(sent_vector_)
    if len(X_i) != 0:
        X.append(X_i)
        Y.append(0)


print('===============')

import pickle

a_dict = {'X':X,'Y':Y}



file = open('stock/test_X_Y.pickle', 'wb')
pickle.dump(a_dict, file)
file.close()

import random

new_X_index = random.sample([i for i in range(len(X))],len(X))
new_X = [X[new_X_index[i]] for i in range(len(X))]
new_Y = [Y[new_X_index[i]] for i in range(len(X))]

train_X = new_X[:int(len(new_X)*0.8)]
test_X = new_X[int(len(new_X)*0.8):]
train_Y = new_Y[:int(len(new_Y)*0.8)]
test_Y = new_Y[int(len(new_Y)*0.8):]
train_Y = torch.tensor(train_Y).cuda()
test_Y = torch.tensor(test_Y).cuda()

from backup_tool import Train_Eval_Process_Layer
Train_Eval_Process_Layer(train_X,train_Y,test_X,test_Y)