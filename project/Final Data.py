#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[ ]:


pwd=os.get.cwd()


# In[3]:


dataset =pd.read_excel(r'C:\Users\Sandhya\Desktop\Data - Survey Monkey Output.xlsx', sheet_name="edited_data")
dataset


# In[4]:


data_modified=dataset.copy()
dataset


# In[5]:


data_modified.columns


# In[6]:


columns_to_drop=['Start Date', 'End Date', 'Email Address',
       'First Name', 'Last Name', 'Custom Data 1']


# In[7]:


data_modified=data_modified.drop(columns=columns_to_drop,axis=1)
data_modified


# In[8]:


data_modified.columns


# In[9]:


id_vars=list(data_modified.columns)[:8]
value_vars=list(data_modified.columns)[8:]


# In[10]:


value_vars


# In[11]:


dataset_melted =data_modified.melt(id_vars=id_vars, value_vars=value_vars)
dataset_melted


# In[12]:


dataset_melted =data_modified.melt(id_vars=id_vars, value_vars=value_vars,var_name="Question+Subquestion",value_name="Answer")
dataset_melted


# In[13]:


questions_import = pd.read_excel(r'C:\Users\Sandhya\Desktop\Data - Survey Monkey Output.xlsx', sheet_name="Question")
questions_import


# In[14]:


question=questions_import.copy()
question.drop(columns=[" Raw Question","Raw Subquestion","SubQuestion"],inplace=True)
question


# In[15]:


question.dropna(inplace=True)
question


# In[16]:


dataset_merged=pd.merge(left=dataset_melted, right=question, how="left",left_on="Question+Subquestion",right_on="Question+Subquestion")


# In[17]:



print("original data",len(dataset_melted))
print("Merged Data",len(dataset_merged))
dataset_merged


# In[18]:


dataset_merged.columns


# In[25]:


respondents=dataset_merged[dataset_merged["Answer"].notna()]
respondents=respondents.groupby("Question")["Respondent ID"].nunique().reset_index()
respondents.rename(columns={"Respondent ID":"Respondents"},inplace=True)
respondents


# In[28]:


dataset_merged_two=pd.merge(left=dataset_merged, right=respondents, how="left",left_on="Question",right_on="Question")
print("original data",len(dataset_merged))
print("Merged Data",len(dataset_merged_two))
dataset_merged_two


# In[29]:


same_answer=dataset_merged#[dataset_merged["Answer"].notna()]
same_answer=same_answer.groupby(["Question+Subquestion","Answer"])["Respondent ID"].nunique().reset_index()
same_answer.rename(columns={"Respondent ID":"same_answer"},inplace=True)
same_answer


# In[32]:


dataset_merged_three=pd.merge(left=dataset_merged_two, right=same_answer, how="left",left_on=["Question+Subquestion","Answer"],right_on=["Question+Subquestion","Answer"])
dataset_merged_three["same_answer"].fillna(0,inplace=True)
print("original data",len(dataset_merged_two))
print("Merged Data",len(dataset_merged_three))
dataset_merged_three


# In[37]:


output=dataset_merged_three.copy()
output.rename(columns={"Identify which division you work in.-Response":"Division Primary","Identify which division you work in.-Other (please specify)":"Divison Secondary","Which of the following best describes your position level?-Response":"Position","Which generation are you apart of?-Response":"Generation","Please select the gender in which you identify.-Response":"Gender","Which duration range best aligns with your tenure at your company?-Response":"Tenure","Which of the following best describes your employment type?-Response":"mployment type"},inplace=True)
output


# In[43]:


output.to_excel(pwd+"\\final_output.xlsx",index=False)


# In[ ]:




