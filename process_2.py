









 

import pickle
with open('stock/title_2_Y_2_id_2_X_SC.pickle', 'rb') as file:
    title_2_Y_2_id_2_X_SC =pickle.load(file)

title_2_Y_2_id_2_X_SC = title_2_Y_2_id_2_X_SC['title_2_Y_2_id_2_X_SC']
title_list = list(title_2_Y_2_id_2_X_SC.keys())
Y1_X,Y1_X_title,Y1_X_id,Y1_X_SC = list(),list(),list(),list()
Y0_X,Y0_X_title,Y0_X_id,Y0_X_SC = list(),list(),list(),list()

for i in range(len(title_list)):
    if 'Y==1' in title_2_Y_2_id_2_X_SC[title_list[i]]:
        title_Y1 = title_2_Y_2_id_2_X_SC[title_list[i]]['Y==1']
        demo_id = list(title_Y1.keys())##
        for j in range(len(demo_id)):
            demo_X_SC = title_Y1[demo_id[j]]
            demo_X = demo_X_SC[0]
            demo_SC = demo_X_SC[1]
            Y1_X.append(demo_X)
            Y1_X_title.append(title_list[i])
            Y1_X_id.append(demo_id[j])
            Y1_X_SC.append(demo_SC)
    elif 'Y==0' in title_2_Y_2_id_2_X_SC[title_list[i]]:
        title_Y0 = title_2_Y_2_id_2_X_SC[title_list[i]]['Y==0']
        demo_id = list(title_Y0.keys())[0]
        demo_X_SC = title_Y0[demo_id]
        demo_X = demo_X_SC[0]
        demo_SC = demo_X_SC[1]
        Y0_X.append(demo_X)
        Y0_X_title.append(title_list[i])
        Y0_X_id.append(demo_id)
        Y0_X_SC.append(demo_SC)
        
print(len(Y1_X))
print(len(Y0_X))
pos_num = len(Y1_X)
import random
neg_idx_sample = random.sample([i for i in range(len(Y0_X))],pos_num)


new_Y0_X,new_Y0_X_title,new_Y0_X_id,new_Y0_X_SC = list(),list(),list(),list()
for i in range(len(neg_idx_sample)):
    new_Y0_X.append(Y0_X[neg_idx_sample[i]])
    new_Y0_X_title.append(Y0_X_title[neg_idx_sample[i]])
    new_Y0_X_id.append(Y0_X_id[neg_idx_sample[i]])
    new_Y0_X_SC.append(Y0_X_SC[neg_idx_sample[i]])


Y0_X,Y0_X_title,Y0_X_id,Y0_X_SC  = new_Y0_X,new_Y0_X_title,new_Y0_X_id,new_Y0_X_SC 

import re
import calendar
import mwparserfromhell
import spacy
import pyprind

def Parsing2Sent(Y1_X_1,Y1_X_title_i):
    nlp = spacy.load("en_core_web_lg")
    wikicode = mwparserfromhell.parse(Y1_X_1) 
    templates = wikicode.filter_templates()
    for i in range(len(templates)):
        if 'Infobox' in templates[i]:
            templates_i = templates[i].split('\n')
            infobox = dict()
            for j in range(len(templates_i)):
                if '=' in templates_i[j]:
                    head_dirty = templates_i[j].split('=')[0].replace('| ','')
                    tail_dirty = '='.join(templates_i[j].split('=')[1:])
                    ## head clean
                    head_clean = ' '.join(head_dirty.split('_')).lstrip().rstrip()
                    ## tail clean
                    # ] and [
                    tail_dirty = tail_dirty.replace('[','').replace(']','')
                    # birth date
                    if 'birth' in head_dirty and 'date' in head_dirty:
                        if '|' in tail_dirty:
                            tail_dirty = tail_dirty.replace('{','').replace('}','')
                            date_dirty = tail_dirty.split('|')
                            date = list()
                            for k in range(len(date_dirty)):
                                if date_dirty[k].lstrip().rstrip().isdigit():
                                    date.append(date_dirty[k])
                            if len(date) ==3:
                                if int(date[1]) in [k+1 for k in range(12)]:
                                    month = calendar.month_name[int(date[1])]
                                    date = month + ',' + date[2] + ',' + date[0]
                                    tail_dirty = date
                    # <br>
                    if '<br>'in tail_dirty :
                        tail_dirty = ' and '.join(tail_dirty.split('<br>'))
                    # unknown sign
                    if 'birth_date' not in head_dirty:
                        tail_clean = ' '.join(re.sub('[^a-zA-Z0-9.– -]',' ',tail_dirty).split())
                    else:
                        tail_clean = tail_dirty
                    if len(tail_clean) !=0:
                        infobox[head_clean] = tail_clean
            infobox_text = str(templates[i])
            new_infobox_text = ''
            infobox_keys = list(infobox.keys())
            if 'name' in infobox:
                infobox_name = infobox['name']
            else:
                infobox_name = Y1_X_title_i
            infobox_keys = list(infobox.keys())
            for j in range(len(infobox_keys)):
                if 'name' not in infobox_keys[j] :
                    tail = infobox[infobox_keys[j]]
                    triple = 'The '+infobox_keys[j]+' of '+ infobox_name + ' is ' + tail
                    new_infobox_text = new_infobox_text + triple + '.' +'\n'
            new_infobox_text = new_infobox_text + '\n'
            Y1_X_1 = Y1_X_1.replace(infobox_text,new_infobox_text)
    new_Y1_X_1 = list()
    Y1_X_1_split = Y1_X_1.split('\n')#
    for i in range(len(Y1_X_1_split)):
        token_ = Y1_X_1_split[i]
        doc = nlp(token_)
        for sent in doc.sents:
            sent = sent.text
            ## clean article
            # clean ] and [ 
            sent = sent.replace('[','').replace(']','')
            # clean template
            wikicode = mwparserfromhell.parse(sent)
            templates = wikicode.filter_templates()
            str_wikicode = str(wikicode)
            for j in range(len(templates)):
                str_wikicode = str_wikicode.replace(str(templates[j]),' ')
            #str_wikicode = str_wikicode#.replace('<ref name','.').replace('/>','.')
            sent = str_wikicode
            if 'See also' in sent or 'References' in sent or \
                'External links' in sent or 'Books' in sent or \
                'Further reading' in sent:
                break
            else:
                if sent.isspace() == False and len(sent) !=0:
                    new_Y1_X_1.append(sent)
    return new_Y1_X_1








len1_list = list()
len0_list = list()
import pyprind
new_Y1_X_1_list = list()
for i in pyprind.prog_bar(range(len(Y1_X))):
    Y1_X_1 = Y1_X[i]
    Y1_X_title_i = Y1_X_title[i]
    new_Y1_X_1 = Parsing2Sent(Y1_X_1,Y1_X_title_i)
    new_Y1_X_1_list.append(new_Y1_X_1)
    len1_list.append(len(new_Y1_X_1))
new_Y0_X_1_list = list()
for i in pyprind.prog_bar(range(len(Y0_X))):
    Y0_X_1 = Y0_X[i]
    Y0_X_title_i = Y0_X_title[i]
    new_Y0_X_1 = Parsing2Sent(Y0_X_1,Y0_X_title_i)
    new_Y0_X_1_list.append(new_Y0_X_1)
    len0_list.append(len(new_Y0_X_1))



neg_X = new_Y0_X_1_list
neg_title = Y0_X_title
neg_id = Y0_X_id
neg_SC = Y0_X_SC

new_neg_X,new_neg_title,new_neg_id,new_neg_SC = list(),list(),list(),list()
for i in range(len(neg_X)):
    if len(neg_X[i]) > 1:
        new_neg_X.append(neg_X[i])
        new_neg_title.append(neg_title[i])
        new_neg_id.append(neg_id[i])
        new_neg_SC.append(neg_SC[i])
print(len(pos_X))
print(len(new_neg_X))

import pickle

a_dict = {'pos_X':new_Y1_X_1_list,'neg_X':new_neg_X,'pos_title':Y1_X_title,'neg_title':new_neg_title,'pos_id':Y1_X_id,'neg_id':new_neg_id,'pos_SC':Y1_X_SC,'neg_SC':new_neg_SC}



file = open('stock/pair_sent_and_DATA.pickle', 'wb')
pickle.dump(a_dict, file)
file.close()

    




import spacy

# nlp = spacy.load("en_core_web_lg")
# doc = nlp(Y1_X[1])
# new_Y1_X = list()
# for sent in doc.sents:
#     sent = sent.text
#     if 'See also' in sent or 'References' in sent or 'External links' in sent or 'Books' in sent or 'Further reading' in sent:
#         break
#     else:
#         new_Y1_X.append(sent)


# for i in range(len(new_Y1_X)):
#     print(new_Y1_X[i])
#     print('==========')

'''
==See also==
==References==
==External links==
===Books===
==Further reading==
'''


