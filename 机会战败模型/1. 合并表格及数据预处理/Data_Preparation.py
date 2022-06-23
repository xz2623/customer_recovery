#!/usr/bin/env python
# coding: utf-8

# ### 数据预处理

# ### 预备流程

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)


# In[4]:


pwd


# ### 合并试乘试驾表 Concatenating the test drive sheet

# #### 读取2019年与2020年数据, 并统一变量

# In[37]:


# 读取2019年表数据并查看表头字段
test_drive_1 = pd.read_excel('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/试乘试驾表2019-v3 all done 加密版2.xlsx', index_col=0, encoding = "utf_8_sig").reset_index(drop=True)
test_drive_1.columns


# In[40]:


# 查看某字段最小值
test_drive_1['dwd_jetta_sales_testdrive_dms_v1_t_d.kf_testdrivedistance'].min()


# In[ ]:


# 讲所有表头含‘dwd_jetta_sales_testdrive_dms_v1_t_d.’以下字段统统删除
col_1 = list(test_drive_1.columns) 
col_1 = [x.replace('dwd_jetta_sales_testdrive_dms_v1_t_d.', '') for x in col_1]
test_drive_1.columns = col_1
# 查看是否清理完成
test_drive_1.columns


# In[29]:


# 查看表格维度
test_drive_1.shape


# In[41]:


# 读取2020年数据，所有步骤同上
test_drive_2 = pd.read_excel('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/试乘试驾表2020-v3 all done 加密2.xlsx', index_col=0, encoding = "utf_8_sig").reset_index(drop=True)

col_2 = list(test_drive_2.columns) 
col_2 = [x.replace('dwd_jetta_sales_testdrive_dms_v1_t_d.', '') for x in col_2]
test_drive_2.columns = col_2

print(test_drive_2.columns)
test_drive_2.shape


# #### 合并2019与2020年数据

# In[39]:


# 将两表数据写进一个set并发现其相同变量
set_a = set(test_drive_1.columns)
set_b = set(test_drive_2.columns)


# In[41]:


# 验证47个字段相同
len(set_a.intersection(set_b))


# In[140]:


# 合并
test_drive_ttl = pd.concat([test_drive_1,test_drive_2],axis=0).reset_index(drop=True)


# In[70]:


# 查看表维度
test_drive_ttl.shape


# #### 检验试乘试驾表中的变量状况

# In[69]:


# 经验证以下字段几乎为空值
test_drive_ttl[['dappointbegin','dappointend','vsjno','vfromid','vfromtype','feedback','is_deleted']].isna().sum()


# In[ ]:


# 进行变量删除并及时留档为test_drive_ttl.csv
test_drive_ttl.drop(['dappointbegin','dappointend','vsjno','vfromid','vfromtype','feedback','is_deleted','ods_update_time','vstate','Y-备注','day_no'], axis=1, inplace=True)

# 为空值因此删除
# td_ttl.drop(131999, inplace=True)

# 保存试乘试驾合并表为 test_drive_ttl.csv
test_drive_ttl.to_csv('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/test_drive_ttl.csv', encoding='utf_8_sig', index=True)


# In[9]:


# 检查各变量unique值的情况
td_ttl.nunique()


# #### 将表保存成csv格式

# test_drive_ttl.to_csv('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/test_drive_ttl.csv', encoding='utf_8_sig', index=True)

# In[3]:


td_ttl = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/test_drive_ttl.csv', index_col=0,low_memory = False, encoding = "utf_8_sig")


# In[165]:


td_ttl.to_csv('C:/Users/lenovo/Automobile/机会战败模型/4-试乘试驾表-V3/test_drive_ttl.csv', encoding='utf_8_sig', index=True)


# #### 数据清理

# In[7]:


# 检查是驾照id, 发现单数值重复过多，因此该变量不可用 如6d1993e5-c4e4-47fd-bc62-dd93bb6ba904 出现 1549次
td_ttl['vdrivecarid'].value_counts()


# In[187]:


# 意向车系里 有 '0L', '0M', nan, 'L0'
td_ttl['vseries'].unique()


# In[183]:


# 车型有7 - 24种，与线现有信息不符合
td_ttl[['vseries','vmodel','intentvmodel','intentvseries']].nunique()


# In[74]:


# 是否预约值只有 nan 和 False
td_ttl['bappoint'].unique()


# ##### 去除drivetype为空值的行

# In[10]:


# 此步骤发现drivetype为空值的行
td_ttl = td_ttl[~td_ttl['drivetype'].isna()]


# ##### 去除试驾路线为空值的行

# In[108]:


td_ttl = td_ttl[~td_ttl['vtrycarpath'].isna()]


# ##### 清楚既无vcusid 也无手机号的数据

# In[125]:


td_ttl = td_ttl[~ td_ttl['vcusid'].isna() & td_ttl['vcusmobile'].isna()]


# In[132]:


# 检查以下字段
td_ttl[['concat_id','dtrybegin','dtryend','kf_testdrivetime','kf_testdrivedistance','drivetype']]


# In[ ]:


# 将'visit_day' 字段转化为 时间类型变量
td_ttl['visit_day'] = pd.to_datetime(td_ttl['dtrybegin']).dt.strftime('%Y-%m-%d')


# #### 检查表维度

# In[145]:


# 查看合并表前五行
td_ttl.head()


# In[36]:


# 以下可检测单变量/两变量之间的分布
sns.scatterplot(td_ttl['kf_testdrivetime'],td_ttl['kf_testdrivedistance'])
sns.distplot(td_ttl['kf_testdrivetime'])
# len(td_ttl[(td_ttl['kf_testdrivetime'] == 0)])


# ### 合并订单表

# In[ ]:


# 注意此处，两订单表已经完成.xlsx格式转.csv格式， 且两文件标头字段均为69列，因此可直接合并
df_order_19 = td_ttl = pd.read_csv('C:/Users/lenovo/Automobile/订单/df_order_2019.csv', index_col=0,low_memory = False, encoding = "utf_8_sig").reset_index(drop=True)
df_order_20 = td_ttl = pd.read_csv('C:/Users/lenovo/Automobile/订单/df_order_2020.csv', index_col=0,low_memory = False, encoding = "utf_8_sig").reset_index(drop=True)

print(df_order_19.shape)
df_order_20.shape


# In[ ]:


# 进行合并
df_order_ttl = pd.concat([df_order_19, df_order_20])

df_order_ttl = df_order_ttl.reset_index(drop=True)


# In[ ]:


#整理无效字段并进行删除
df_order_ttl.isna().sum().to_frame().sort_values(by=0, ascending = False)


# In[ ]:


df_order_ttl.drop(['is_deleted','vchangedealer','vparentno','vcusno','vspresmsg','Unnamed: 61','vappoint','vdress','nsubscription','vmemo','vpostal','desticartime','dlost','vlostreason'], axis=1, inplace = True )


# In[ ]:


# 将合并表保存为csv格式
df_order_ttl.to_csv('order_ttl.csv')


# ### 合并机会更新表

# #### 原文件预处理

# In[ ]:


# 读取全部22各文件, 在此时22个文件已经全部由.xlsx格式转化为.csv格式
oppo_fol_1 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_1.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_2 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_2.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_3 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_3.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_4 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_4.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_5 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_5.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_6 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_6.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_7 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_7.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_8 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_8.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_9 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_9.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_10 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_10.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_11 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_11.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_12 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_12.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_13 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_13.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_14 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_14.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_15 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_15.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_16 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_16.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_17 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_17.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_18 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_18.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_19 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_19.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_20 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_20.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_21 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_21.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")

oppo_fol_22 = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_22.csv',low_memory = False, index_col=0, encoding = "utf_8_sig")


# In[ ]:


# 修改每张数据表的表头，以确保合并不会出错
oppo_fol_1.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_2.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_3.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_4.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_5.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_6.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_7.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_8.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_9.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_10.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_11.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_12.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_13.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_14.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_15.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_16.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_17.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_18.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_19.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_20.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_21.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']

oppo_fol_22.columns = ['concat_id', 'concat_id_1', 'uid', 'ucusid', 'uprojectid', 'jdealer',
       'nbid', 'urelateid', 'vactiontype', 'dplanexec', 'drealexec',
       'vlinkresult', 'vcompleteflag', 'vnotes', 'vinfoback', 'vsubject',
       'bisapp', 'vowner', 'voldowner', 'dfirstdistribute', 'ddistribute',
       'utryid', 'createby', 'createon', 'updateby', 'updateon',
       'record_version', 'vactionmode', 'vseries', 'vmodel', 'voriginvw',
       'vorigin', 'kf_projecttrackcount', 'kf_projectunexceptedcount',
       'kf_projectrealexeccount', 'ods_update_time', 'is_deleted', 'day_no',
       'rownum', 'Y-备注']


# #### 合并表后并预处理

# In[ ]:


# 合并22张表为oppo_fol_ttl
oppo_fol_ttl = pd.concat([oppo_fol_1,oppo_fol_2,oppo_fol_3,oppo_fol_4,oppo_fol_5,oppo_fol_6,oppo_fol_7,oppo_fol_8,oppo_fol_9,oppo_fol_10,oppo_fol_11,oppo_fol_12,oppo_fol_13,oppo_fol_14,oppo_fol_15,oppo_fol_16,oppo_fol_17,oppo_fol_18,oppo_fol_19,oppo_fol_20,oppo_fol_21,oppo_fol_22]
, axis=0).reset_index(drop=True)

# 更新表索引
oppo_fol_ttl = oppo_fol_ttl.reset_index(drop=True)

# 去除'concat_id'为空值的记录
oppo_fol_ttl.dropna(subset=['concat_id'], inplace = True)

# 查看表维度
oppo_fol_ttl.shape


# #### 将表保存为csv格式

# In[ ]:


oppo_fol_ttl.to_csv('C:/Users/lenovo/Automobile/机会战败模型/6-机会跟进表/oppo_fol_ttl.csv', encoding='utf_8_sig', index=True)


# ### 读取合并并预处理机会表

# #### 合并机会表

# In[ ]:


确保所有文件都在同一个目录下,将所有相同表在一个目录下 然后设置working directory之后运行以下两段代码

以下代码仅仅确保 所有文件都在同一目录下 
get_ipython().run_line_magic('ls', '')
机会表_201907-201910.xlsx  机会表_202001.xlsx  机会表_202004.xlsx
机会表_201911.xlsx         机会表_202002.xlsx  机会表_202005.xlsx
机会表_201912.xlsx         机会表_202003.xlsx  机会表_202006.xlsx


# In[ ]:


# 统一表头 并将.xlsx格式改变为.csv
import os
for i in os.listdir():
    if i[-5:] == '.xlsx':
        df = pd.read_excel(i)
        try:
            df.rename(columns={'序号': 'dwd_jetta_sales_order_dms_v1_t_d.index_number'}, inplace=True)
            df.rename(columns=lambda x: x[33:], inplace=True)
            df.to_csv(i.replace('xlsx', 'csv'))
        except:
            continue


# In[ ]:


# 将每张表格都进行合并

import os
df = pd.DataFrame()
for i in os.listdir():
    if i[-4:] == '.csv':
        if df.empty:
            df = pd.read_csv(i,low_memory=False)
        else:
            try:
                df = pd.concat([df,pd.read_csv(i,low_memory=False)])
            except:
                print("An exception occurred during merging. Check columns.")
df = df.drop(columns = ['Unamed: 0']
df.to_csv('oppo_combined.csv')


# In[152]:


# 此处 oppo_combined文件由Harry完成
df_oppo_ttl = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/5-机会表 - v3/oppo_combined.csv', index_col=0,low_memory = False, encoding = "utf_8_sig").iloc[:, 1:]


# In[109]:


df_oppo_ttl.shape


# #### 预处理

# In[158]:


# oppo_trial_1 = df_oppo_ttl.isna().sum().to_frame().reset_index()


# In[168]:


# 删除无效字段

df_oppo_ttl.drop(['mkid', 'vinfosourcevw', 'vinfosource', 'fwin', 'vexperiencetext', 'vcarintention', 'vcarintentiontext', 'vvisitexperience',
 'from_id', 'from_type', 'staflag', 'loanway', 'brepeatflag', 'is_deleted'], axis=1, inplace = True)


# In[ ]:


# 删除所有与表关联相关的空值字段
oppo_ttl.dropna(subset = ['psg_uid','uid','ucusid'], inplace = True)

oppo_ttl.reset_index(drop=True)


# #### 将已处理的表保存为csv格式

# In[171]:


df_oppo_ttl.to_csv('C:/Users/lenovo/Automobile/机会战败模型/5-机会表 - v3/oppo_combined.csv', encoding='utf_8_sig', index=True)


# ### 读取合并并预处理的客流表

# #### 合并客流表

# 确保所有文件都在同一个目录下,将所有相同表在一个目录下 然后设置working directory之后运行以下两段代码
# 
# 以下代码仅仅确保 所有文件都在同一目录下 
# %ls
# 客流表201907-V3（all done）加密完成版.xlsx
# 客流表201908-V3（all done）-加密完成版.xlsx
# 客流表201909-V3 加密完成版.xlsx
# 客流表201910-V3 加密完成版.xlsx
# 客流表201911-V3 加密完成版.xlsx
# 客流表201912-V3 加密完成版.xlsx
# 客流表202001-202002-V3 加密完成版.xlsx
# 客流表202003-V3 加密完成版.xlsx
# 客流表202004-V3 加密完成版.xlsx
# 客流表202005-V3 加密完成版.xlsx
# 客流表202006-V3 加密完成版.xlsx

# In[ ]:


# 统一表头 并将.xlsx格式改变为.csv
import os
for i in os.listdir():
    if i[-5:] == '.xlsx':
        df = pd.read_excel(i)
        try:
            df.rename(columns={'序号': 'dwd_jetta_sales_order_dms_v1_t_d.index_number'}, inplace=True)
            df.rename(columns=lambda x: x[33:], inplace=True)
            df.to_csv(i.replace('xlsx', 'csv'))
        except:
            continue


# In[ ]:


# 将每张表格都进行合并

import os
df = pd.DataFrame()
for i in os.listdir():
    if i[-4:] == '.csv':
        if df.empty:
            df = pd.read_csv(i,low_memory=False)
        else:
            try:
                df = pd.concat([df,pd.read_csv(i,low_memory=False)])
            except:
                print("An exception occurred during merging. Check columns.")
df = df.drop(columns = ['Unamed: 0']
df.to_csv('customer_flow_total.csv')


# In[191]:


# 运行已经合并好的客流表
df_customer_flow_ttl = pd.read_csv('C:/Users/lenovo/Automobile/机会战败模型/3-客流表-v3/customer_flow_total.csv', index_col=0, low_memory=False, encoding = "utf_8_sig")


# #### 预处理

# In[192]:


df_customer_flow_ttl.head()


# In[195]:


df_customer_flow_ttl.shape


# ##### 数据清理 - 去空

# In[ ]:


# 删除绝大多数为空值的字段
cf_trial_1 = df_customer_flow_ttl.isna().sum().to_frame().reset_index().rename(columns={'index': 'attributes',0: 'counts'})

# print(list(cf_trial_1[cf_trial_1['counts'] > 450000]['attributes']))

df_customer_flow_ttl.drop(['arrivetype',  'vfrom',  'bisdistribute',  'dfirstdis', 'ddistribute',  'vdistributeman',  'bisconfirm',
 'vinvalidrsn',  'vinvalidrsntext',  'is_deleted'], axis=1, inplace = True)


# In[200]:


# 此处发现很多时间变量均为异常值
# df_customer_flow_ttl[~df_customer_flow_ttl['ddistribute'].isna()]['ddistribute']


# ##### 去除所有数据均相同的行数

# In[ ]:


sample_cf.drop_duplicates(inplace=True)


# ##### 去除所有uid均为空值的行数

# In[ ]:


sample_cf.dropna(subset=['uid'],inplace = True)

