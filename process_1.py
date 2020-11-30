





import pickle
with open('stock/all_data.pickle', 'rb') as file:
    all_data =pickle.load(file)



X = all_data['X']
Y = all_data['Y']
title = all_data['title']
revision_id = all_data['revision_id']
SC_template = all_data['self-contradictory_template']




'''
title {
    Y=1:{
        id:{X,SC_template}
        id:
    }
    Y=0:{

    }
}
'''
print(len(X))
print(len(Y))
print('len check!!')
if len(X) != len(Y):
    print('ERROR1')
if len(X) != len(title):
    print('ERROR2')    
if len(X) != len(revision_id):
    print(len(revision_id))
    print('ERROR3')   
if len(X) != len(SC_template):
    print(len(SC_template))
    print('ERROR4')   
print('len cjheck finish!')

title2data = dict()
for i in range(len(title)):
    if title[i] not in title2data:
        title2data[title[i]] = dict()
        if Y[i] == 1:
            title2data[title[i]]['Y==1'] = dict()
        elif Y[i] == 0:
            title2data[title[i]]['Y==0'] = dict()
        else:
            print('[ERROR]: there is non-define Y!!')
    if 'Y=='+str(Y[i]) not in title2data[title[i]]:
        title2data[title[i]]['Y=='+str(Y[i])] = dict()
    title2data[title[i]]['Y=='+str(Y[i])][revision_id[i]] = [X[i],SC_template[i]]


import pickle

a_dict = {'title_2_Y_2_id_2_X_SC':title2data}



file = open('stock/title_2_Y_2_id_2_X_SC.pickle', 'wb')
pickle.dump(a_dict, file)
file.close()
