#!/usr/bin/env python
# coding: utf-8

# ### 构建全新变量及宽表 及 外部数据提取 3万样本 

# ### 预备流程

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)


# In[3]:


#载入宽表 次宽表由Harry整理
df = pd.read_pickle('df_aggregated.pkl')


# In[4]:


# 检查表维度 并去除重复ucusid
print(df[['vcusmobile','ucusid']].nunique())

df.drop_duplicates(subset = 'ucusid', keep = 'first', inplace = True)

df[['vcusmobile','ucusid']].nunique()


# #### 保留更新后的宽表

# In[12]:


df.to_pickle('df_aggregated.pkl')


# ### 合并宽表 与客流表与机会跟进表

# #### 读取客流表与机会跟进表并与宽表合并

# In[7]:


# 读取客流表 
df_cf = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/3-客流表-v3/customer_flow_total.csv', index_col=0, low_memory=False, encoding = "utf_8_sig").reset_index(drop=True)
# 读取机会跟进表
oppo_fol = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_ttl.csv', low_memory = False, encoding='utf_8_sig', index_col=0)


# In[8]:


# 准备用以连表的dataframe df_merge 只是用宽表的手机号与正负样本标识
df_merge = df[['vcusmobile', 'category']]

# 输出只含有宽表种正负样本的手机号
sample_mobile = list(set(df['vcusmobile']))


# In[9]:


# 输出dataframe df_cf_sample 为只含正负样本数据的客流表

df_cf_sample = df_cf.loc[df_cf['vcusmobile'].isin(sample_mobile)]


# In[31]:


# 合并df_merge 与 df_cf_sample, 并挑选连接机会跟进表的字段并从上到下排序

merge_1_sample_cf = pd.merge(df_merge, df_cf_sample, on = 'vcusmobile', how = 'left')

merge_1_sample_cf = merge_1_sample_cf[['vcusmobile','category','uid']]

merge_1_sample_cf = merge_1_sample_cf.sort_values(by=['vcusmobile','uid'], ascending = [True, True])


# In[41]:


merge_1_sample_cf


# ### 合并机会表

# In[12]:


# 读取机会表
df_oppo_ttl = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/5-机会表 - v3/oppo_combined.csv', index_col=0,low_memory = False, encoding = "utf_8_sig")
df_oppo_ttl.head()


# In[62]:


# 合并表, 获取机会表中所需字段
merge_1_sample_cf_oppo = pd.merge(merge_1_sample_cf, df_oppo_ttl, left_on = 'uid', right_on = 'psg_uid', how = 'left')

merge_1_sample_cf_oppo.columns


# In[63]:


# 获取连表字段并去空值
merge_1_sample_cf_oppo = merge_1_sample_cf_oppo[['vcusmobile', 'category','psg_uid','ucusid']]

merge_1_sample_cf_oppo.dropna(inplace = True)


# In[32]:


merge_1_sample_cf_oppo.nunique()


# In[39]:


# 连接机会跟进表
merge_1_sample_cf_oppo_fol = pd.merge(merge_1_sample_cf_oppo, oppo_fol, on ='ucusid', how = 'left')


# In[112]:


# 获取3万外部数据手机号
for_sample_1 = merge_1_sample_cf_oppo_fol[['vcusmobile','category','drealexec']]

pd.to_datetime(for_sample_1.loc[:,'drealexec'])

for_sample_1 = for_sample_1.sort_values(by=['vcusmobile', 'drealexec'], ascending = [True, False])

for_sample_1.drop_duplicates(subset = 'vcusmobile', keep = 'first', inplace = True)

for_sample_2 = for_sample_1[for_sample_1['drealexec'] > '2020-05-07 00:00:00']

for_sample_2_pos = for_sample_2[for_sample_2['category'] == 1]

for_sample_2_neg = for_sample_2[for_sample_2['category'] == 0]

pos = for_sample_2_pos.sample(n=10000, replace = False).reset_index(drop=True)

neg = for_sample_2_neg.sample(n=20000, replace = False).reset_index(drop=True)

sample_for_external = pd.concat([pos,neg])

sample_for_external.to_csv('sample_for_external.csv')


# ### 修改全量宽表并增加新模型变量
# 

# In[443]:


kb = pd.read_excel('机会战败概率打分宽表及下发字段.xlsx')


# In[7]:


kb = pd.read_excel('机会战败概率打分宽表及下发字段.xlsx')
df = pd.read_pickle('df_aggregated.pkl')


# In[8]:


kb.drop(['Unnamed: 0'], axis=1, inplace = True)
kb


# In[13]:


# 使用之前所用到的 只含正负样本的客流表并与机会表左连接 
merge_1_sample_cf_oppo = pd.merge(merge_1_sample_cf, df_oppo_ttl, left_on = 'uid', right_on = 'psg_uid', how = 'left')


# In[ ]:


# 获取最晚执行时间的经销商用以下发并去重
merge_1_sample_cf_oppo_fol = pd.merge(merge_1_sample_cf_oppo, oppo_fol, on ='ucusid', how = 'left')

for_sample_1 = merge_1_sample_cf_oppo_fol[['vcusmobile','drealexec','jdealer']]
pd.to_datetime(for_sample_1.loc[:,'drealexec'])

for_sample_1 = for_sample_1.sort_values(by=['vcusmobile', 'drealexec'], ascending = [True, False])

for_sample_1.drop_duplicates(subset = 'vcusmobile', keep = 'first', inplace = True)


# #### 新增试驾/试驾试乘率，即顾客总到店次数中试驾/试乘试驾比例

# In[ ]:


df['test_testdrive_rate'] = df['bistryvie'] / df_agg['count']
df['test_testdrive_rate'].unique()


# #### 下发字段 - 增加机会跟进表字段最晚执行时间 'drealexec'及 下发经销商'jdealer_for_xiafa'

# In[50]:


# 合并表为df_1 并重命名表头
df_1 = pd.merge(df, for_sample_1, left_on = 'vcusmobile', right_on = 'vcusmobile')

df_1.columns = ['vcusmobile', 'ucusid', 'cartype', 'vexperience', 'vplatetype',
       'vabandonrsn', 'stayTime', 'bislookvie', 'bistryvie', 'vintentionlvl',
       'category', 'count', 'Guanzhu0', 'Guanzhu1', 'Guanzhu2', 'Guanzhu3',
       'Guanzhu4', 'Guanzhu5', 'Guanzhu6', 'Guanzhu7', 'Guanzhu8', 'Guanzhu9',
       'is_test', 'test_count', 'ttl_test', 'cleaned_time_ttl_test',
       'cleaned_distance_ttl_test', 'is_test_drive', 'testdrive_count',
       'ttl_testdrive', 'cleaned_time_ttl_testdrive',
       'cleaned_distance_ttl_testdrive', 'vtrycarpath_test_TryDriveRoute1',
       'vtrycarpath_test_TryDriveRoute2', 'vtrycarpath_test_TryDriveRoute3',
       'vtrycarpath_testdrive_TryDriveRoute1',
       'vtrycarpath_testdrive_TryDriveRoute2',
       'vtrycarpath_testdrive_TryDriveRoute3', 'b_recommend',
       'test_testdrive_rate', 'drealexec','jdealer_for_xiafa']


# ####  增加上午下午 火 工作日与双休日到店次数

# In[ ]:


# 摘取客流表中顾客到店时间
df_cf_sample_arrival = df_cf_sample[['vcusmobile','dbegin']]

df_cf_sample_arrival.loc[:,'dbegin'] = pd.to_datetime(df_cf_sample_arrival['dbegin'], errors='coerce').to_frame()

df_cf_sample_arrival


# In[ ]:


# 将顾客到店时间换算成 周几与上下午时间
df_cf_sample_arrival['weekday'] = df_cf_sample_arrival['dbegin'].dt.dayofweek

df_cf_sample_arrival['morning'] = df_cf_sample_arrival['dbegin'].dt.hour


# In[ ]:


# 看其分布并将空值设定为0
print(df_cf_sample_arrival['morning'].unique())

df_cf_sample_arrival['morning'] = df_cf_sample_arrival.fillna(0)

df_cf_sample_arrival['weekday'].unique()


# In[ ]:


# 分别为顾客分类其到店时间按 indicator 为周六周日 indicator_1为早晨与夜晚
df_cf_sample_arrival['indicator'] = [1 if row == 5.0 or row == 6.0 else 0 for row in df_cf_sample_arrival.loc[:,'weekday']]

list_hour = [0,1,2,3,4,5,6,7,8,9,10,11,12]

df_cf_sample_arrival['indicator_1'] = [1 if row in  list_hour else 0 for row in df_cf_sample_arrival.loc[:,'morning']]


# In[ ]:


# 为每位用户计算其 周末到店次数 与 早上到店次数
c = df_cf_sample_arrival.groupby(['vcusmobile'])['indicator','indicator_1'].sum().reset_index()

df_2 = pd.merge(df_1, c, left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left')

df_2.columns = ['vcusmobile', 'ucusid', 'cartype', 'vexperience', 'vplatetype',
       'vabandonrsn', 'stayTime', 'bislookvie', 'bistryvie', 'vintentionlvl',
       'category', 'count', 'Guanzhu0', 'Guanzhu1', 'Guanzhu2', 'Guanzhu3',
       'Guanzhu4', 'Guanzhu5', 'Guanzhu6', 'Guanzhu7', 'Guanzhu8', 'Guanzhu9',
       'is_test', 'test_count', 'ttl_test', 'cleaned_time_ttl_test',
       'cleaned_distance_ttl_test', 'is_test_drive', 'testdrive_count',
       'ttl_testdrive', 'cleaned_time_ttl_testdrive',
       'cleaned_distance_ttl_testdrive', 'vtrycarpath_test_TryDriveRoute1',
       'vtrycarpath_test_TryDriveRoute2', 'vtrycarpath_test_TryDriveRoute3',
       'vtrycarpath_testdrive_TryDriveRoute1',
       'vtrycarpath_testdrive_TryDriveRoute2',
       'vtrycarpath_testdrive_TryDriveRoute3', 'b_recommend',
       'test_testdrive_rate', 'drealexec', 'jdealer_for_xiafa', 'weekend_tag',
       'morning_tag']


# #### 增加到店最多的经销商大区/小区
# 

# In[13]:


# 选取相应字段
df_cf_sample_jdealer = df_cf_sample[['vcusmobile','jdealer']]
df_cf_sample_jdealer


# In[14]:


# 获取经销商次数
jdealer_number = df_cf_sample_jdealer.drop_duplicates(subset=['vcusmobile','jdealer'], keep = 'first')

jdealer_number = jdealer_number.groupby(['vcusmobile'])['jdealer'].count().reset_index()


# In[27]:


# 获取去得最多得经销商
jdealer_counts = df_cf_sample_jdealer.groupby(['vcusmobile']).agg(
    { 'jdealer' : lambda x:x.value_counts().index[0]
    }
).reset_index()

jdealer_counts


# In[18]:


# 读取经销商对应区域文件 并 合并 去重 更改字段名称
section = pd.read_excel('附件1：经销商对应区域清单（md5).xlsx')

jdealer_seciont = pd.merge(jdealer_counts, section, left_on='jdealer', right_on = '销售代码', how='left')

df_7.drop_duplicates(subset=['vcusmobile'],keep='first', inplace=True)

jdealer_seciont = jdealer_seciont[['vcusmobile','销售大区','销售小区']]
jdealer_seciont.columns = ['vcusmobile','Section_Macro','Section_Micro']


# In[176]:


# 合并获取到店次数，与最多到点经销商 并进行规范化字段值
df_3 = pd.merge(df_2, jdealer_number, left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left')

df_3 = pd.merge(df_3, jdealer_seciont, left_on='vcusmobile', right_on = 'vcusmobile', how = 'left')

df_3['Section_Micro']  = [row[:3] for row in df_3.loc[:,'Section_Micro']]

df_3['Section_Macro'] = [row[:3] for row in df_3.loc[:,'Section_Macro']]


# In[487]:


plt.figure(figsize=(20,10))
ax_2 = sns.countplot(x="Section_Macro", hue="category", data=df_3)


# In[113]:


plt.figure(figsize=(20,10))
ax_1 = sns.countplot(x="Section_Micro", hue="category", data=a)


# #### 增加单次到店人数

# In[203]:


# 选取相应字段
df_cf_sample_peer = df_cf_sample[['vcusmobile','vpeernum']]

b.vpeernum = b.vpeernum.fillna(1)


# In[218]:


# 观察到店人数分布
b = df_cf_sample_peer.groupby(['vcusmobile'])['vpeernum'].max().reset_index()


# In[222]:


# 算出平均到店人数为1.5人/次
(1*121495 + 2 * 33261 + 3 * 14666 + 4 * 6007 + 5 * 1607 + 6 * 344 + 7 *97 + 8 * 24 + 9 * 9 + 10 * 10) / (121495 + 33261 + 14666 + 6007 +  1607 + 344 + 97 +  24 +  9 +  100)


# In[223]:


# 将异常到店人数更改为平均值（四舍五入）
b.vpeernum = [2 if row > 10 else row for row in b.vpeernum]


# In[227]:


# 合并
df_4 = pd.merge(df_3, b, left_on = 'vcusmobile', right_on='vcusmobile', how='left')
df_4.head()


# #### 增加第一次/最后一次到店是否试驾

# In[ ]:


# 选取相应字段
df_cf_sample_peer = df_cf_sample[['vcusmobile','dbegin']]

merge_1_sample_cf_oppo = pd.merge(merge_1_sample_cf, df_oppo_ttl, left_on = 'uid', right_on = 'psg_uid', how = 'left')

merge_1_sample_cf_oppo.columns


# In[334]:


d = merge_1_sample_cf_oppo[['vcusmobile','dbegin','bistryvie']]


# In[342]:


# 更改字段为事件类型字段
d[['dbegin']] = pd.to_datetime(d['dbegin'])

# 并从早到晚排序
d = d.sort_values(by=['vcusmobile','dbegin'], ascending = [True, True])

# 去重
d = d.drop_duplicates(subset = ['vcusmobile'],keep='first')

# 补空值
d = d.fillna(0).reset_index(drop=True)


# In[349]:


# 因为机会表为顾客第一次到点意愿，因此 1为第一次到点试驾 0 为无
d.bistryvie = [1 if row == True else 0 for row in d.loc[:,'bistryvie']]

d.bistryvie


# In[350]:


df_5 = pd.merge(df_4, d[['vcusmobile','bistryvie']], left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left')


# In[351]:


df_5.head()


# In[352]:


df_5.columns = ['vcusmobile', 'ucusid', 'cartype', 'vexperience', 'vplatetype',
       'vabandonrsn', 'stayTime', 'bislookvie', 'bistryvie', 'vintentionlvl',
       'category', 'count', 'Guanzhu0', 'Guanzhu1', 'Guanzhu2', 'Guanzhu3',
       'Guanzhu4', 'Guanzhu5', 'Guanzhu6', 'Guanzhu7', 'Guanzhu8', 'Guanzhu9',
       'is_test', 'test_count', 'ttl_test', 'cleaned_time_ttl_test',
       'cleaned_distance_ttl_test', 'is_test_drive', 'testdrive_count',
       'ttl_testdrive', 'cleaned_time_ttl_testdrive',
       'cleaned_distance_ttl_testdrive', 'vtrycarpath_test_TryDriveRoute1',
       'vtrycarpath_test_TryDriveRoute2', 'vtrycarpath_test_TryDriveRoute3',
       'vtrycarpath_testdrive_TryDriveRoute1',
       'vtrycarpath_testdrive_TryDriveRoute2',
       'vtrycarpath_testdrive_TryDriveRoute3', 'b_recommend',
       'test_testdrive_rate', 'drealexec',  'jdealer_for_xiafa'， 'weekend_tag',
       'morning_tag', 'max_visited_jdealer', 'num_visitors', '1st_tryvie_tag']


# #### 增加最后一次到店是否试驾

# In[278]:


# 读取客流表
td = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/test_drive_ttl.csv', low_memory = False, index_col=0)

# 获取客流表中的正负样本以及所对应字段
td_sample = td.loc[td['vcusmobile'].isin(sample_mobile)]

td_sample_1 = td_sample[['vcusmobile','dtrybegin']]


# In[357]:


# 将开始试驾时间改为时间变量 并从晚到早排序/用户
td_sample_1.loc[:,'dtrybegin'] = pd.to_datetime(td_sample_1['dtrybegin']).to_frame()

td_sample_1.sort_values(by=['vcusmobile','dtrybegin'], ascending = [True, False])


# In[358]:


# 去除重复值，只保留最后一次试驾时间
td_sample_1 = td_sample_1.drop_duplicates(subset='vcusmobile',keep='first')


# In[359]:


#同时找到客流表中，用户最后一次到店记录，并去重
df_cf_sample_testdrive = df_cf_sample[['vcusmobile','dbegin']]

df_cf_sample_testdrive.loc[:,'dbegin'] = pd.to_datetime(df_cf_sample_testdrive['dbegin']).to_frame()

df_cf_sample_testdrive = df_cf_sample_testdrive.sort_values(by=['vcusmobile','dbegin'], ascending = [True, False])

df_cf_sample_testdrive = df_cf_sample_testdrive.drop_duplicates(subset=['vcusmobile'], keep='first')


# In[362]:


# 各表合并, 如若客户在最后一次到店时间中并未试驾，则会有空值，因此判断
e = pd.merge(df_cf_sample_testdrive, td_sample_1, left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left')

e.loc[:,'dbegin'] = pd.to_datetime(e.dbegin).to_frame()
e.loc[:,'dtrybegin'] = pd.to_datetime(e.dtrybegin).to_frame()


# In[365]:


e.head()


# In[395]:


# 以防万一，将变量全部重新调整为时间变量
e['dbegin_date'] = e.dbegin.dt.date

e['dtrybegin_date'] = e.dtrybegin.dt.date

e['dtrybegin_date'] = pd.to_datetime(e['dtrybegin_date'])
e['dbegin_date'] = pd.to_datetime(e['dbegin_date'])

e['dtrybegin_date'] = e['dtrybegin_date'].fillna('1970-0-01')


# In[390]:


e.index


# In[388]:


# 进行时间之间的对比
def date_comparison(a, b):
    if a > b:
        return 1
    else:
        return 0
    
e['indicator'] = e.apply(lambda row:date_comparison(row['dbegin_date'],row['dtrybegin_date']), axis = 1)


# In[402]:


df_6 = pd.merge(df_5, e[['vcusmobile','indicator']], left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left')

# df_6.drop(['drealexec'], axis=1,inplace=True)


# #### 增加平均每次试驾与试乘试驾时间

# In[423]:


df_6['avg_test'] = df_6['cleaned_time_ttl_test'] / df['ttl_test']
df_6['avg_testdrive'] = df_6['cleaned_time_ttl_testdrive'] / df['ttl_testdrive']


# In[425]:


df_6[['cleaned_time_ttl_testdrive']]


# #### 下发字段 - 意向车系/型

# In[444]:


# 选取相应表
merge_1_sample_cf_oppo_fol = pd.merge(merge_1_sample_cf_oppo, oppo_fol, on ='ucusid', how = 'left')


# In[ ]:


# 截取最进一次执行时间的意向车系

for_sample_2 = merge_1_sample_cf_oppo_fol[['vcusmobile','vseries','vmodel'，'drealexec']]

pd.to_datetime(for_sample_1.loc[:,'drealexec'])

for_sample_2 = for_sample_1.sort_values(by=['vcusmobile', 'drealexec'], ascending = [True, False])

for_sample_2.drop_duplicates(subset = 'vcusmobile', keep = 'first', inplace = True)


# In[ ]:


# 修正所有 -1 以及 nan的意向车系
a = ['0L', '0M', 'L0']
for_sample_2['vseries'] = ['unknown' if row == 'unknown' or row == -1 else row for row in for_sample_2.vseries]

b = ['0L12PV','0L12PY','0L13PV','0L13PY','0L14PY','0L22PV','0L22PY','0L23PV','0L23PY','0L24PY','0M22EV','0M23EV','0M23EY','0M24EV','0M24EY','L022PV','L022PY','L023PV','L023PY','L024PY'
]
for_sample_2['vmodel_y'] = [row if row in b else 'unknown' for row in for_sample_2['vmodel_y'] ]


# In[454]:


for_sample_2.vseries.unique()


# In[455]:


df_7 = pd.merge(df_6, for_sample_2, left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left')


# In[458]:


# 无发连接的null值改为'unknown'
df_7.vseries = df_7.vseries.replace(pd.NA, 'unknown')


# In[465]:


df_7.columns


# #### 下发字段 - 线索创建时间

# In[ ]:


merge_1_sample_cf_oppo_fol = pd.merge(merge_1_sample_cf_oppo, oppo_fol, on ='ucusid', how = 'left')

# 截取最小一次线索执行时间

for_sample_3 = merge_1_sample_cf_oppo_fol[['vcusmobile','createon_y']]

for_sample_3.loc['createon_y'] = pd.to_datetime(for_sample_3['createon_y'])

for_oppo = for_oppo.sort_values(by=['vcusmobile', 'createon_y'], ascending = [True, True])

for_sample_2.drop_duplicates(subset = 'vcusmobile', keep = 'first', inplace = True)

for_oppo.drop_duplicates(subset='vcusmobile', keep = 'first', inplace = True)

df_8 = pd.merge(df_7, for_oppo, on='vcusmobile', how = 'left')


# #### 增加该顾客最长到店时间

# In[48]:


df_cf_time = df_cf_sample[['vcusmobile','dbegin','dend']]


# In[49]:


# 截取相应字段
df_cf_time['dbegin'] = pd.to_datetime(df_cf_time['dbegin'])

df_cf_time['dend'] = pd.to_datetime(df_cf_time['dend'])

df_cf_time['duration'] = df_cf_time['dend'] - df_cf_time['dbegin']


# In[51]:


# 获取每个客户的最长到店时间
h = df_cf_time.groupby(['vcusmobile'])['duration'].max().reset_index()


# In[52]:


h.head()


# In[53]:


# 将该事件提取出小时与分钟并进行计算
h['duration_hours'] = h['duration'].dt.components['hours']
h['duration_minutes'] = h['duration'].dt.components['minutes']  
h['duration_in_minutes'] = h['duration_hours']  * 60 + h['duration_minutes']


# In[54]:


g = h.groupby(['vcusmobile'])['duration_in_minutes'].max().reset_index()


# In[545]:


g.head()


# In[55]:


df_10 = pd.merge(df_8, g, left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left' )


# In[56]:


# 计算平均看车时间并将其与总看车时间换算成分钟
df_10['avg_kanche'] = df_10['stayTime'] / df_8['count']
df_10['avg_kanche'] = df_10['avg_kanche'] / 60

df_10['stayTime'] = df_10['stayTime'] / 60


# #### 增加渠道

# In[59]:


import numpy as np


# In[61]:


# 清理渠道数据
i = df_cf_sample[['vcusmobile','voriginvw']].fillna('unknown')

i['voriginvw'].unique()


# In[62]:


#寻找渠道的众数
k = i.groupby(['vcusmobile']).agg({'voriginvw':lambda x: x.value_counts().index[0]}).reset_index()


# In[63]:


# 合并渠道
df_11 = pd.merge(df_10, k, left_on = 'vcusmobile', right_on = 'vcusmobile', how = 'left')


# In[64]:


df_11.head()


# ### 增加GAP字段, 即正样本顾客中, 最后一次到店时间与订单成交时间之差

# In[ ]:


# 读取订单表
order = pd.read_csv('C:/Users/lenovo/Automobile/订单/order_ttl.csv', index_col=0,low_memory = False, encoding = "utf_8_sig")

# 并解渠所需字段
order['dclose'] = pd.to_datetime(order['dclose'])
order_vcus = order[['vcusmobile', 'dclose']]


# In[ ]:


df_dummy_order = pd.merge(df_11, order_vcus, on ='vcusmobile', how = 'left')


# In[ ]:


cust_flow_entry = df_cf_sample[['vcusmobile','dbegin']].reset_index(drop=True).sort_values(by=['vcusmobile','dbegin'],ascending=[True,True])

verify = cust_flow_entry.copy()


# In[ ]:


cust_flow_entry.drop_duplicates(subset='vcusmobile', keep='first', inplace = True)

cust_flow_entry.reset_index(drop=True, inplace = True)


# In[ ]:


merge = pd.merge(df_dummy_order, cust_flow_entry, on = 'vcusmobile', how = 'left')


# In[ ]:


# 此处可验证，我们的负样本无订单完成时间
merge[merge['category'] == 0.0]['dclose'].isna().sum()


# In[ ]:


# 由此，我们可算出正样本的gap
merge['dclose'] = pd.to_datetime(merge['dclose'])
merge['dbegin'] = pd.to_datetime(merge['dbegin'])

merge['gap'] = round((merge['dclose'] - merge['dbegin']) / np.timedelta64(1, 'D'), 4)


# In[ ]:


df_12 = merge.copy()


# In[65]:


# 形成最终宽表，包括所有新增变量以及 dclose, dbegin 及 gap
df_12.to_pickle('df_final_attributes.pkl')

# 备份
#df_12.to_pickle('df_final_attributes_1.pkl')

