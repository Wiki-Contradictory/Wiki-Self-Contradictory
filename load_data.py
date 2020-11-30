import pandas as pd
## csv part.
import pyprind 
import mwparserfromhell
def Format_csv2XY(path):
    X,Y,title,self_contradictory_template,revision_id_list = list(),list(),list(),list(),list()
    df = pd.read_csv(path)
    page_title = list(df['page_title'])
    revision_text = list(df['revision_text']) 
    revision_id = list(df['revision_id'])
    for i in pyprind.prog_bar(range(len(revision_text))):
        self_contradictory_template_i = list()
        text = revision_text[i]
        title_i = page_title[i]
        revision_id_i = revision_id[i]
        if isinstance(text,str) is True and len(text.split()) !=0:
            wikicode = mwparserfromhell.parse(text)
            templates = wikicode.filter_templates()
            is_pos = False
            for j in range(len(templates)):
                if 'Self-contradictory' in templates[j]:
                    is_pos = True
                    self_contradictory_template_i.append(templates[j])
            if is_pos:
                X.append(str(text))
                title.append(title_i)
                Y.append(1)
            else:
                X.append(str(text))
                title.append(title_i)
                Y.append(0)  
            self_contradictory_template.append(self_contradictory_template_i)    
            revision_id_list.append(revision_id_i)   
    return  X,Y,title,self_contradictory_template,revision_id_list

## jsonl part
import pyprind
import json


def Format_json2XY(path):
    with open(path, 'r') as jsonlfile:
        jsonlfile = list(jsonlfile)
    X,Y,title,self_contradictory_template,RID_list = list(),list(),list(),list(),list()
    for i in pyprind.prog_bar(range(len(jsonlfile))):
        self_contradictory_template_i_pov,self_contradictory_template_i_solvepov = list(),list()
        a = json.loads(jsonlfile[i])
        #print('revision ID:',a.keys())
        povVersionId = a['povVersionId']
        solvedpovVersionId = a['solvedpovVersionId']
        text = a['povVersion']
        solve_text = a['solvedpovVersion']
        pageTitle = a['pageTitle']
        wikicode = mwparserfromhell.parse(text)
        templates = wikicode.filter_templates()
        is_pos_1 = False
        for j in range(len(templates)):
            if 'Self-contradictory' in templates[j]: 
                is_pos_1 = True
                self_contradictory_template_i_pov.append(templates[j])
        wikicode = mwparserfromhell.parse(solve_text)
        templates = wikicode.filter_templates()
        is_pos_2 = False
        for j in range(len(templates)):
            if 'Self-contradictory' in templates[j]: 
                self_contradictory_template_i_solvepov.append(templates[j])
                is_pos_2 = True
        self_contradictory_template.append(self_contradictory_template_i_pov)
        self_contradictory_template.append(self_contradictory_template_i_solvepov)
        RID_list.append(povVersionId)
        RID_list.append(solvedpovVersionId)
        if is_pos_1 is True and len(text.split()) != 0:
            X.append(str(text))
            title.append(pageTitle)
            Y.append(1)
        else:
            X.append(str(text))
            title.append(pageTitle)
            Y.append(0)            
        if is_pos_2 is True and len(solve_text.split()) != 0:
            X.append(str(solve_text))
            title.append(pageTitle)
            Y.append(1)
        else:
            X.append(str(solve_text))
            title.append(pageTitle)
            Y.append(0)            
    return X,Y,title,self_contradictory_template,RID_list


main_path = '/home/hsucheng/wiki/'

json_path = 'dataset/' + 'solved.jsonl'
selfC_path = 'dataset/selfC.csv'
solvedSelfC_path = 'dataset/solvedSelfC.csv'

json_X,json_Y,json_title,json_SC_template,json_RID_list  = Format_json2XY(main_path+json_path)

selfC_X,selfC_Y,selfC_title,selfC_SC_template,selfC_RID_list = Format_csv2XY(main_path+selfC_path)
solvedSelfC_X,solvedSelfC_Y,solvedSelfC_title,solvedSelfC_SC_template,solvedSelfC_RID_list = Format_csv2XY(main_path+solvedSelfC_path)


X = json_X + selfC_X + solvedSelfC_X
Y = json_Y + selfC_Y + solvedSelfC_Y
title = json_title + selfC_title + solvedSelfC_title
self_contradictory_template = json_SC_template + selfC_SC_template + solvedSelfC_SC_template
Revision_ID = json_RID_list + selfC_RID_list + solvedSelfC_RID_list








import pickle

a_dict = {'X':X ,'Y':Y,'title':title,'revision_id':Revision_ID,'self-contradictory_template':self_contradictory_template}



file = open('stock/all_data.pickle', 'wb')
pickle.dump(a_dict, file)
file.close()