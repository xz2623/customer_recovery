#!/usr/bin/env python
# coding: utf-8

# # 机会表宽表变量选择与预处理

# In[1]:


import pandas as pd
import matplotlib as plt
import seaborn as sns


# In[2]:


df_merged = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/5-机会表 - v3/oppo_combined.csv', index_col=0,low_memory = False, encoding = "utf_8_sig")


# In[4]:


df_merged.columns.to_list()


# In[36]:


fp = open('columns.txt')


# In[37]:


importantColumns = list()
for i in fp.readlines():
    importantColumns.append(i[:-1])


# In[38]:


fp.close()


# In[39]:


importantColumns


# In[46]:


drop = [ 'jdealer',
 'vcusname',
 'vstate',
 'drivetype',
 'vseries',
 'vmodel',
 'intentvmodel',
 'intentvseries',
 'voriginvw',
 'vorigin',
 'kf_testdrivetime',
 'kf_testdrivedistance',
 'kf_testdrivecuscount',
 'jdealer','bcloseflag',
'blostflag',
'bmatch',
'bvip',
'dclose',
'dcreate',
'desticartime',
'dlost',
'dordercreate',
'uid',
'vbillno',
'vcardno',
'vlostreason',
'vmemo',
'vin',
'dinvoicedate',
'kf_deliver_time'
]


# In[41]:


importantColumns = set(importantColumns)


# In[47]:


importantColumnsList = list()
for i in importantColumns:
    if i not in drop:
        importantColumnsList.append(i)


# In[48]:


importantColumnsList


# In[46]:


keep1 =  ['vintentionlvl',
 'vexperience',
 'vplatetype',
 'vabandonrsn',
 'brecommend',
 'bislookvie',
 'bistryvie',
 'cartype',
 'vguanzhu','vcusmobile','ucusid','stayTime']


# In[28]:


df_merged_opportunity['vdissenttext'].unique()


# 'vdissenttext' 字段为字符串
# 
# 初步考虑分析nan的分布
# 

# In[31]:


df_merged_opportunity[ 'vabandonrsn'].unique()


# "01 无法按揭、02 没有现车、03 放弃购车、04 购买竞品、05 价格过高、06 颜色、07 配置"

# In[32]:


df_merged_opportunity['vguanzhutext'].unique()


# In[34]:


df_merged_opportunity['vguanzhutext'].nunique()


# In[33]:


df_merged_opportunity['vguanzhu'].unique()


# In[35]:


df_merged_opportunity['vguanzhu'].nunique()


# In[37]:


df_merged_opportunity['vexperience'].unique()


# In[38]:


df_merged_opportunity[ 'vvisitexperience'].unique()


# In[44]:


df_merged_opportunity[  'vcarbudget'].isna().sum()


# In[49]:


df_merged_opportunity[  'vcarbudget'].nunique()


# In[48]:


df_merged_opportunity[ 'fallprice'].unique()


# ## Needs to be processed

# In[2]:


df_merged_opportunity = pd.read_pickle("df_merged_opportunity_with_caruse.pkl")


# In[3]:


df_merged_opportunity = df_merged_opportunity.dropna(subset=['dbegin', 'dend'])


# In[4]:


import time
from datetime import datetime
time.mktime(datetime. strptime(df_merged_opportunity['dbegin'][0], '%Y-%m-%d %H:%M:%S').timetuple())


# In[ ]:


df_merged_opportunity


# In[ ]:


time.mktime(dtime.timetuple())


# In[5]:


def getTime(begin,end):
    return time.mktime(datetime. strptime(end, '%Y-%m-%d %H:%M:%S').timetuple()) - time.mktime(datetime.strptime(begin, '%Y-%m-%d %H:%M:%S').timetuple()) 


# In[6]:


df_merged_opportunity['stayTime'] = df_merged_opportunity.apply(lambda x: getTime(x['dbegin'], x['dend']), axis=1)


# In[20]:


df_merged_opportunity['stayTime']


# In[21]:


df_merged_opportunity.columns.tolist()


# In[ ]:


df_merged_opportunity[['p']]


# ## 正样本-DF
# 

# In[8]:


df_positive = df_merged_opportunity.loc[df_merged_opportunity['bcloseflag']==True]


# In[23]:


df_positive.to_pickle("df_opportunity_postive.pkl")


# In[47]:


df_positive = pd.read_pickle("df_opportunity_postive.pkl")


# In[24]:


df_positive['vcusmobile'].nunique()


# In[48]:


df_positive_select = df_positive[keep1]


# In[10]:


df_positive_select


# ## 负样本-DF

# In[11]:


df_negative = df_merged_opportunity[['vcusmobile','cabandon']]
df_negative


# In[12]:


def getNeg(row):
    if row['cabandon'] == 2:
        return True
    else:
        return False
df_negative['is_negative'] = df_negative.apply(lambda row: getNeg(row), axis=1)


# In[19]:


df_negative


# In[14]:


df_negative_grouped = df_negative.groupby(["vcusmobile"]).mean()
df_negative_grouped = df_negative_grouped.loc[df_negative_grouped['is_negative']==1].reset_index(level='vcusmobile')


# In[15]:


df_negative_grouped[['vcusmobile']]


# In[17]:


df_negative = df_negative_grouped[['vcusmobile']].merge(df_merged_opportunity, how = 'left', left_on='vcusmobile', right_on='vcusmobile',suffixes=('', '_y'))
df_negative.drop(list(df_negative.filter(regex='_y$')), axis=1, inplace=True) 


# In[18]:


df_negative['ucusid'].nunique()


# In[20]:


df_negative.to_pickle("df_opportunity_negative.pkl")


# In[49]:


df_negative= pd.read_pickle("df_opportunity_negative.pkl")


# In[50]:


df_negative_select = df_negative[keep1]


# In[51]:


import numpy as np
df_negative_select['category'] = np.zeros_like(df_negative_select['vintentionlvl'])


# In[52]:


df_positive_select['category'] = np.ones_like(df_positive_select['vintentionlvl'])


# In[53]:


df_select = pd.concat([df_positive_select,df_negative_select])


# In[27]:


df_positive_select['vcusmobile'].nunique()


# In[25]:


df_select 


# In[41]:


sns.pairplot(df_select, hue="category");


# In[32]:


for i in keep1:
    print(i)
    print(df_select[i].isna().sum())
    print('_____________________________')


# In[54]:


df_select[['vguanzhu',]] = df_select[['vguanzhu']].fillna(value='unknown')


# In[55]:


df_select = df_select.dropna(subset=['vintentionlvl'])


# In[56]:


df_select[['vplatetype','vabandonrsn','vexperience','cartype']] = df_select[['vplatetype','vabandonrsn','vexperience','cartype']].fillna(value=0)


# # NOTE: Treat these as categorical variables as well. 将以下变量也设置为类型变量

# In[19]:


df_select[[ 'fallprice']] = df_select[[ 'fallprice']].fillna(value=df_select[ 'fallprice'].mean())


# In[33]:


df_select['brecommend'].unique()


# In[57]:


import math
math.isnan(df_select['brecommend'].tolist()[0])


# In[58]:


brecommend = list()
for i in df_select['brecommend'].tolist():
    if type(i) != str:
        if math.isnan(i):
            brecommend.append(0)
        else:
            brecommend.append(i)
    else:
        if i == 'True':
            brecommend.append(1)
        else:
            brecommend.append(0)
            
df_select[['brecommend']] = brecommend 


# In[59]:



bislookvie = list()
for i in df_select['bislookvie'].tolist():
    if type(i) != str:
        bislookvie.append(i)
    else:
        if i == 'True':
            bislookvie.append(True)
        else:
            bislookvie.append(False)
            
df_select[['bislookvie']] = bislookvie


bistryvie = list()
for i in df_select['bistryvie'].tolist():
    if type(i) != str:
        bistryvie.append(i)
    else:
        if i == 'True':
            bistryvie.append(True)
        else:
            bistryvie.append(False)
            
df_select[['bistryvie']] = bistryvie


# In[38]:


brecommend 


# In[39]:


df_select


# In[16]:


keep1


# In[60]:


for i in keep1:
    print(i)
    print(df_select[i].isna().sum())
    print('_____________________________')


# 填补大量null的结果可能会是：如果之后出现较为明显的imbalanced positive/negative classes， 会导致此条目出现问题。例如：所有负样本均为fallprice为null，则模型会判断只要fallprice不是null就不为负样本。可能会产生问题，如有问题请删去相关条目

# In[61]:


check = ['vintentionlvl',
 'vexperience',
 'vplatetype',
 'vabandonrsn',
 'brecommend',
 'bislookvie',
 'bistryvie',
 'cartype',
 'vguanzhu']
for i in check:
    print(i)
    print(df_select[i].unique() )
    print('_____________________________')


# In[51]:


df_select.drop(columns = ['fallprice','vcarbudget'],inplace = True)


# In[41]:


df_select


# In[61]:


df_select.drop(columns = [ 'kf_potentialcuscount', 'kf_visitcount', 'kf_yhcount'],inplace = True)


# In[63]:


df_select.drop(columns = [ 'vguanzhutext'],inplace = True)


# In[65]:


df_select.drop(columns = [ 'vcaruse'],inplace = True)


# In[65]:


df_select


# In[76]:


df_select.to_pickle('df.select')


# In[59]:


df_select[['vdissenttext']].to_csv('word_count.csv')


# In[62]:


df_select['count'] = np.ones_like(df_select['ucusid'])


# In[78]:


df_most_frequent = df_select[['ucusid','cartype','vexperience','vplatetype','vabandonrsn']]


# In[80]:


df_sum = df_select[['ucusid','stayTime','bislookvie','bistryvie']]
df_concat = df_select[['ucusid','vguanzhu']]
df_largest = df_select[['ucusid','vintentionlvl','brecommend','category']]


# In[81]:


df_sum = df_sum.groupby(['ucusid']).sum()


# In[82]:


df_count = df_select[['ucusid','count']].groupby('ucusid').count()


# In[83]:


df_count


# In[76]:


df_sum['bislookvie'].unique() 


# In[77]:


df_sum['bistryvie'].unique() 


# In[85]:


df_most_frequent


# In[ ]:


df_most_frequent = df_most_frequent.groupby(['ucusid']).agg(lambda x:x.value_counts().index[0])


# In[72]:


df_most_frequent


# In[ ]:


df_concat = pd.DataFrame(df_concat.groupby('ucusid')['vguanzhu'].apply(list))


# In[90]:


df_concat 


# In[ ]:


df_largest = df_largest.groupby('ucusid').max()


# In[75]:


df_largest['category'].unique()


# In[ ]:





# In[ ]:


df_full = pd.concat([df_most_frequent, df_sum,df_concat,df_largest ], axis=1)


# In[ ]:


df_count.reset_index(level=['ucusid'], inplace= True)


# In[ ]:


df_full.reset_index(level=['ucusid'], inplace= True)


# In[95]:


df_full


# In[ ]:


def getGuanzhu0(vguanzhu):
    for i in vguanzhu:
        if '0' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu1(vguanzhu):
    for i in vguanzhu:
        if '1' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu2(vguanzhu):
    for i in vguanzhu:
        if '2' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu3(vguanzhu):
    for i in vguanzhu:
        if '3' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu4(vguanzhu):
    for i in vguanzhu:
        if '4' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu5(vguanzhu):
    for i in vguanzhu:
        if '5' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu6(vguanzhu):
    for i in vguanzhu:
        if '6' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu7(vguanzhu):
    for i in vguanzhu:
        if '7' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu8(vguanzhu):
    for i in vguanzhu:
        if '8' in i:
            return 1
        else:
            continue
    return 0

def getGuanzhu9(vguanzhu):
    for i in vguanzhu:
        if '9' in i:
            return 1
        else:
            continue
    return 0


# In[ ]:


df_full['Guanzhu0'] = df_full.apply(lambda x: getGuanzhu0(x['vguanzhu']), axis=1)
df_full['Guanzhu1'] = df_full.apply(lambda x: getGuanzhu1(x['vguanzhu']), axis=1)
df_full['Guanzhu2'] = df_full.apply(lambda x: getGuanzhu2(x['vguanzhu']), axis=1)
df_full['Guanzhu3'] = df_full.apply(lambda x: getGuanzhu3(x['vguanzhu']), axis=1)
df_full['Guanzhu4'] = df_full.apply(lambda x: getGuanzhu4(x['vguanzhu']), axis=1)
df_full['Guanzhu5'] = df_full.apply(lambda x: getGuanzhu5(x['vguanzhu']), axis=1)
df_full['Guanzhu6'] = df_full.apply(lambda x: getGuanzhu6(x['vguanzhu']), axis=1)
df_full['Guanzhu7'] = df_full.apply(lambda x: getGuanzhu7(x['vguanzhu']), axis=1)
df_full['Guanzhu8'] = df_full.apply(lambda x: getGuanzhu8(x['vguanzhu']), axis=1)
df_full['Guanzhu9'] = df_full.apply(lambda x: getGuanzhu9(x['vguanzhu']), axis=1)


# In[ ]:


df_full.drop(columns = ['vguanzhu'],inplace = True)


# In[ ]:


df_full = df_full.merge(df_count, how = 'left', left_on='ucusid', right_on='ucusid')


# In[ ]:


df_full.to_pickle('df_aggregated_Harry.pkl')


# In[111]:


df_full


# In[54]:


duplicateRowsDF = df_select[df_select.duplicated(['ucusid'],keep=False)]


# In[49]:


df_select.to_pickle('df_oppor_preprocessed.pkl')

