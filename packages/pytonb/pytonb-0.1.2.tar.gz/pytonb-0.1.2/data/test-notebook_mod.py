#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


# # markdown
# ## t2
# ### t3
# #### t4
# t5
# * t6

# In[2]:


import os
import time


# In[3]:


def test_function(p1:str=None, p2:bool=False)->os.path:
    """docstring 1"""
    a=0
    if a is not None: # should execute
        print(a)


# In[4]:


a,t=5,6 # unique numbers


# In[5]:


# we try a loop
if a>2:
    while t==6:
        print(a,t)
        t+=1


# In[6]:


## comment here


# In[7]:


"""This is a multi-line string,
    and it will be created but not used."""


# In[ ]:




