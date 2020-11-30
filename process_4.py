






# =========================
# title
# page_id
# SC
# idx:[s1,s2]
# idx:[s1,s2]
#    .
#    .
#    .
# idx:[s1,s2]
# =========================

# idx,....

# =========================





import pickle
with open('stock/contradictory_pair_sent.pickle', 'rb') as file:
    file_ =pickle.load(file)



pos_X = file_['pos_X']
contradictory_pair_sent = file_['contradictory_pair_sent']

with open('stock/contradictory_pair_sent.txt', 'w') as f:
    #title,page_id,SC,idx,[sa,sb]
    for i in range(len(contradictory_pair_sent)):
        contradictory_pair_sent_i = contradictory_pair_sent[i]
        if len(contradictory_pair_sent_i) != 0:
            title = contradictory_pair_sent_i[0]
            f.write('=========title :'+str(title)+ '+==============='+'\n')
            for j in range(len(contradictory_pair_sent_i)):
                info_ = contradictory_pair_sent_i[j]
                title = 'title: ' + info_[0] + '\n'
                page_id = 'page_id: ' + str(info_[1]) + '\n'
                if isinstance(info_[2],str):
                    SC = 'SC: ' + str(info_[2]) + '\n'
                else:
                    SC = ''
                    for k in range(len(info_[2])):
                        SC += str(info_[2][k])
                        SC += '-'
                idx = 'idx: ' + info_[3] + '\n'
                sa = 'sa: ' + info_[4][0] + '\n'
                sb = 'sb: ' + info_[4][1] + '\n'
                text = title + page_id + SC + idx + sa + sb
                f.write('------------------------------------------'+'\n')
                f.write(text)




