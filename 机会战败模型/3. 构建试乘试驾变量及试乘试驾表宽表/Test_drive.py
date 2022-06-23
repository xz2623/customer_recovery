#!/usr/bin/env python
# coding: utf-8

# ### 构建变量及宽表

# ### 预备流程

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)


# ### 检查试乘试驾表变量维度及宽表

# In[3]:


# 读取试乘试驾合并表: test_drive_ttl.csv
td_ttl = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/test_drive_ttl.csv', index_col=0,low_memory = False, encoding = "utf_8_sig")


# In[3]:


# 检查表中vucsmobile 及 vcusid 无重复值数 分别为 117540, 119714
td_ttl[['vcusmobile','vcusid']].nunique()


# In[4]:


# 检查表头字段名称
td_ttl.columns


# td_ttl.to_csv('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/test_drive_ttl.csv', encoding='utf_8_sig', index=True)

# In[4]:


# 检查表行数列数
td_ttl.shape


# In[5]:


# 检查表各字段非重复值量级
td_ttl.nunique()


# In[51]:


# 检查表各字段空值数
td_ttl.isna().sum()


# ### 构建试乘试驾表变量

# #### 清理字段'kf_testdrivedistance', 及 'kf_testdrivetime'
# 

# In[154]:


# 新建dtaframe distance, 选取试乘试驾表里程频次出现最高的前35里程数
distance = td_ttl['kf_testdrivedistance'].value_counts().to_frame().iloc[:35,].reset_index().sort_values(by=['index'],ascending = True)
distance.columns = ['testdrive_distance','counts']
distance

# 前35里程数已覆盖近99%的数据，且已基本不包括异常值 131790
# td_ttl['kf_testdrivedistance'].value_counts().to_frame().iloc[:35,].reset_index()['kf_testdrivedistance'].sum()


# In[157]:


# 计算平均每人试乘试驾里程数 答案为7.7公里/每人 
distance['multiple'] = distance['testdrive_distance'] * distance['counts']
avg_distance = round(distance['multiple'].sum() / distance['testdrive_distance'].sum(),1)
avg_distance


# In[ ]:


# 新建drivetime dataframe, 选取试乘试驾表里程频次出现最高的前35试乘试驾时长
drivetime = td_ttl['kf_testdrivetime'].value_counts().to_frame().iloc[:800,].reset_index().sort_values(by=['index'],ascending = True)
distance.columns = ['testdrive_time','counts']
drivetime

# 前35里程数已覆盖近91%的数据，且已基本不包括异常值 119781
td_ttl['kf_testdrivetime'].value_counts().to_frame().iloc[:800,].reset_index()['kf_testdrivetime'].sum()


# In[ ]:


# 计算平均每人试乘试驾时长 答案为14.53分钟/每人
drivetime['multiple'] = drivetime['testdrive_time'] * drivetime['counts']
avg_time = round(drivetime['multiple'].sum() / drivetime['testdrive_time'].sum(), 2)
avg_time


# #### 制造出模型变量 'cleaned_distance', 'cleaned_time'

# In[ ]:


# 分别将模型种的试乘试驾里程数/时长的异常值 用刚刚计算的平均值取代
td_ttl['cleaned_time'] = [avg_time if row < 0 or row > 60 else row for row in td_ttl.loc[:,'kf_testdrivetime']]

td_ttl['cleaned_distance'] = [avg_distance if row < 0 or row > 50 else row for row in td_ttl.loc[:,'kf_testdrivedistance']]


# In[166]:


# 此处我们可发现之前的异常值 如- 26555861.77 已经被正常的平均值取代
td_ttl[['kf_testdrivetime','cleaned_time']].sort_values(by=['kf_testdrivetime'])


# #### 清理并制造模型新变量

# In[261]:


# 删除无效字段并生成新dataframe td_ttl_1
td_ttl_1 = td_ttl.drop(['concat_id','vmemo','bappoint','pk','vorigin','kf_testdrivetime','kf_testdrivedistance','kf_testdrivecuscount','kf_testdrivecount'], axis=1)


# In[197]:


# 检查新模型变量的相关性
sns.scatterplot(td_ttl['cleaned_distance'],td_ttl['cleaned_time'])


# In[4]:


# 同上
np.corrcoef(td_ttl['cleaned_distance'],td_ttl['cleaned_time'])


# In[263]:


td_ttl_1.head(5)


# In[28]:


cf_ttl.columns


# In[226]:


a.nunique()


# #### 生成符合构建模型的试乘试驾宽表

# In[24]:


# 提取手机号并去重去空值
driver_mobile = td_ttl[['vcusmobile']]

driver_mobile.shape


# In[27]:


driver_mobile = driver_mobile.dropna()

driver_mobile = driver_mobile.drop_duplicates(keep='first')

# 去重去空的结果
driver_mobile.shape


# In[37]:


# 制造仅含试驾数据的dataframe a(drivetype = 1）, 及仅含试乘试驾数据的dataframe b(drivetype = 2)
a = td_ttl[td_ttl['drivetype'] == 1.].reset_index(drop=True)

b = td_ttl[td_ttl['drivetype'] == 2.].reset_index(drop=True)


# In[40]:


a.columns


# In[127]:


# 合并dataframe a 第一步
a_agg = a.groupby(['vcusmobile','drivetype','visit_day']).agg(
    {
        'vprojectid': "count",
        'cleaned_distance': 'sum',
        'cleaned_time': 'sum',
        'vtrycarpath': lambda x:x.value_counts().index[0]
    }
).reset_index()

agg_a = a_agg.copy()
agg_a


# In[128]:


# 合并dataframe a 第二步
agg_a_1 = agg_a.groupby(['vcusmobile','drivetype']).agg(
    {
        'visit_day' : 'count',
        'vprojectid' : 'sum',
        'cleaned_time': 'sum',
        'cleaned_distance':'sum',
        'vtrycarpath' : lambda x:x.value_counts().index[0]
    }
).reset_index()


# In[129]:


# 合并dataframe b 第一步
b_agg = b.groupby(['vcusmobile','drivetype','visit_day']).agg(
    {
        'vprojectid': "count",
        'cleaned_distance': 'sum',
        'cleaned_time': 'sum',
        'vtrycarpath': lambda x:x.value_counts().index[0]
    }
).reset_index()

agg_b = b_agg.copy()


# In[130]:


# 合并dataframe b 第二步
agg_b_1 = agg_b.groupby(['vcusmobile','drivetype']).agg(
    {
        'visit_day' : 'count',
        'vprojectid' : 'sum',
        'cleaned_time': 'sum',
        'cleaned_distance':'sum',
        'vtrycarpath' : lambda x:x.value_counts().index[0]
    }
).reset_index()


# ##### 表连接, 并新生成模型变量 
# 'is_test', 'test_count', 'ttl_test',
# 'cleaned_time_ttl_test', 'cleaned_distance_ttl_test',  'is_test_drive',
# 'testdrive_count', 'ttl_testdrive', 'cleaned_time_ttl_testdrive', 'cleaned_distance_ttl_testdrive', 'vtrycarpath_testdrive' , 'vtrycarpath_test',

# In[133]:


# 将代表试乘的agg_a_1与代表试乘试驾的agg_b_1 与手机号依次相连
to_merge = pd.merge(driver_mobile, agg_a_1, on = 'vcusmobile', how = 'left')

to_merge_final = pd.merge(to_merge, agg_b_1, on = 'vcusmobile', how = 'left')

to_merge_final


# In[136]:


# 模型变量重命名
to_merge_final.columns = ['vcusmobile', 'is_test', 'test_count', 'ttl_test',
       'cleaned_time_ttl_test', 'cleaned_distance_ttl_test', 'vtrycarpath_test', 'is_test_drive',
       'testdrive_count', 'ttl_testdrive', 'cleaned_time_ttl_testdrive', 'cleaned_distance_ttl_testdrive',
       'vtrycarpath_testdrive']

# 由于空值即该顾客未试乘试驾，因此用零填补
to_merge_final.fillna(0, inplace = True)


# ##### 保存试乘试驾宽表

# In[154]:


to_merge_final.to_csv('test_drive_agg_final.csv')

# 与客流表/机会表的宽表由 ucusid vcusid联接, 并完成于文件 df_aggregated.pkl

