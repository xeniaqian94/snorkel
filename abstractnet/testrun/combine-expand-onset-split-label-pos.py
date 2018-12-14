# coding: utf-8

# In this notebook, we gather two pieces of annotation: one csv is the 2K groundtruth, one is our snorkel gen output. See how the PP precision goes.
#     
#     

# In[1]:


import pathlib
import pandas as pd

'''
combine the generative onset df_gen
python combine-expand-onset-split-label-pos.py --onset_split_dir data/annotations_2k/largest-s2/onset_split_with_pos/ --originally_null_as_zero
python combine-expand-onset-split-label-pos.py --onset_split_dir data/annotations_2k/largest-s2/cscw50/ --originally_null_as_zero

THe combined .csv treats 0-PP, 1-MN, 2-PP which will be used by another script in BiLSTM-tagger/ directory, make-tagging-data-with-pos.py


'''
import os

import argparse

parser = argparse.ArgumentParser(description='Input, output and other configurations')
parser.add_argument('--onset_split_dir', type=str, default="data/annotations_2k/largest-s2/")
parser.add_argument('--onset_split_file_prefix', type=str, default="onset_split_gz")

parser.add_argument('--originally_null_as_zero', dest='null_as_zero', action='store_true', default=True)
parser.add_argument('--originally_null_as_two', dest='null_as_zero', action='store_false')

args = parser.parse_args()
print("args dictionary", args.__dict__)

expansion = False
sub_dfs = []
onset_split_dir = args.onset_split_dir

for filename in os.listdir(onset_split_dir):
    if args.onset_split_file_prefix in filename:
        sub_dfs += [pd.read_csv(open(onset_split_dir + filename, "r"))]

df = pd.concat(sub_dfs)
print("df concatenated! ")
df = df.drop(columns=['Unnamed: 0'])
df2 = df.copy()

mapping = [2, 0, 1]
if args.null_as_zero:
    df2['winningHighlight'] = df2['winningHighlight'].apply(lambda x: mapping[int(x)])

unexpanded_path = onset_split_dir + "onset_joint_split.csv"
df2.to_csv(open(unexpanded_path, "w"))
print("df combined and one-hottified success!")

# # In[ ]:
# # In[22]:
#
# '''
# validTypesMapping
# '''
#
# import numpy as np
# import re
# from collections import defaultdict
# from sklearn.metrics import precision_recall_fscore_support
#
# validTypes = set(['Method', 'Background', 'Findings', 'Mechanism', 'Purpose'])
# validTypesMapping=defaultdict(lambda:2)
# validTypesMapping["Method"]=2
# validTypesMapping["Background"]=2
# validTypesMapping["Findings"]=2
# validTypesMapping["Mechanism"]=1
# validTypesMapping["Purpose"]=0
#
#
# # In[35]:
#
#
# count_PP_MN=0
# count_PP=0
# count_MN=0
# count_none=0
# # print(df2.groupby('paperID').size())
# for paperID, paperData in df2.groupby('paperID'):
#     paperData = paperData.sort_values(by="globalPsn")
# #     print(paperData)
#     aspects=paperData['winningHighlight'].tolist()
#
#     hasPP=False
#     hasMN=False
#     for aspect in aspects:
#         # aspect=np.argmax(ast.literal_eval(aspect))
#         aspect=int(aspect)
#         if aspect==0:
#             hasPP=True
#         if aspect==1:
#             hasMN=True
#
#     if hasPP and hasMN:
#         count_PP_MN+=1
#     elif hasPP:
#         count_PP+=1
#     elif hasMN:
#         count_MN+=1
#     else:
#         count_none+=1
# print("onset percentage PP AND/OR MN", count_PP_MN,count_PP,count_MN,count_none)
#
# import pandas as pd
# import pathlib
# import numpy as np
# import csv
# import ast
# from IPython.core.display import display, HTML
#
#
# def render_text(text,labels,label_mapping=None):
#     assert len(text)==len(labels)
#     html_string=""
#     for idx in range(len(text)):
#         html_string+="<font style='background-color: "+str(label_mapping[labels[idx]])+";' color='black'>"+text[idx]+" </font>"
#     display(HTML(html_string))
#
#
#
# df_gen = df2
# df_list=[]
# count=0
# for paperID, paperData in df_gen.groupby('paperID'):
# #     newID=actual_paperID[int(paperID.split("2K_dev_")[1])]
# #     docID=paperID_docID_mapping[newID]
# #     print(newID)
#
#     paperData = paperData.sort_values(by="globalPsn")
#
#     contents_gen=paperData['content'].tolist()
#     aspects_gen=paperData['winningHighlight'].tolist()
#     sequences_gen=[]
#     current_aspect=2
#     hasMN=False
#     hasPP=False
#     for pair in zip(contents_gen,aspects_gen):
#         content=re.sub(r"\s+","",str(pair[0]))
#         if len(content)==0:
#             continue
#         # gen_label=ast.literal_eval(pair[1])
#         # aspect=np.argmax(gen_label)
#         aspect=pair[1]
#
#         if content=="'":
#             continue
#
#         if expansion:
#             if aspect!=2 and current_aspect!=aspect:
#                 if aspect==1:
#                     hasMN=True
#                 if aspect==0:
#                     hasPP=True
#                 current_aspect=aspect
#             sequences_gen+=[(content,current_aspect)]
#
#             if content==".":
#                 current_aspect=2
#         else:
#             if aspect!=2:
#                 if aspect==1:
#                     hasMN=True
#                 if aspect==0:
#                     hasPP=True
#             sequences_gen+=[(content,aspect)]
#
#
#     if not hasMN or not hasPP:
#         continue
#     else:
#         count+=1
#
#     for idx,pair in enumerate(sequences_gen):
#
#         winningHighlight=[0,0,0]
#         winningHighlight[pair[1]]=1
#
#         df_list+=[[winningHighlight,paperID,idx+1,pair[0]]]
#
# print("Total number of weakly training doc", count)
#
# df=pd.DataFrame(df_list,columns=['winningHighlight', 'paperID', 'globalPsn','content'])
# df.to_csv(open(str(unexpanded_path).replace(".csv","_expanded_"+str(expansion)+".csv"),"w"))   # in the spreadsheet, punctuations are splitted
#
#
