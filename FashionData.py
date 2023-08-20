#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.cluster import KMeans
from sklearn import datasets


# In[6]:


df = pd.read_csv("styles.csv")


# In[8]:


df.columns


# In[9]:


df["gender"].unique()


# In[10]:


df["masterCategory"].unique()


# In[11]:


df["subCategory"].unique()


# In[12]:


df["articleType"].unique()


# In[13]:


df["baseColour"].unique()


# In[14]:


df["season"].unique()


# In[15]:


df["year"].unique()


# In[16]:


df["usage"].unique()


# In[17]:


df["productDisplayName"].unique()


# In[ ]:




