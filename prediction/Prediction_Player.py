#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pickle
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict

print("Setup Complete")


# In[2]:


#Explore Data
player_file_path='Data/nba_players_stats_salary_2017_2018.csv'
player_data=pd.read_csv(player_file_path)
player_data.describe()


# In[3]:


# Choose target and features
y = player_data.SALARY
player_features = ['FTM','AGE', 'GP','STL', 'FTA', 'W','3PM','FGA','DREB','FGM','MIN', 'TOV','AST','3PA','PTS','OREB','BLK','L' ]
X = player_data[player_features]


# In[4]:


#Cross validation
my_pipeline = Pipeline(steps=[('preprocessor', SimpleImputer()),
                              ('model', RandomForestRegressor(n_estimators=75,
                                                              random_state=0))
                             ])


# In[5]:


#fit estimator
my_pipeline.fit(X,y)
#Serialize estimator
with open('my_pipeline.pkl','wb') as fid:
    pickle.dump(my_pipeline,fid)


# In[6]:


# Multiply by -1 since sklearn calculates *negative* MAE
scores = -1 * cross_val_score(my_pipeline, X, y,
                              cv=10,
                              scoring='neg_mean_absolute_error')

print("MAE scores:\n", scores)
print("Average MAE score (across experiments):")
print(scores.mean())


# In[7]:


val_predict =cross_val_predict(my_pipeline, X, y,cv=5)
print("Values predicted:\n",val_predict)


# In[8]:


#data frame 
true_salary=player_data.SALARY
plot_data2=pd.DataFrame(data = {'true_salary':true_salary,'predicted_salary':val_predict})

# Set the width and height of the figure
plt.figure(figsize=(18,8))

# Add title
plt.title("NBA players'salary stats 2017_2018")

# Line chart showing true salary'
sns.lineplot(data=plot_data2['true_salary'], label="true_salary")

# Line chart showing predicted salary'
sns.lineplot(data=plot_data2['predicted_salary'], label="predicted_salary")


# In[9]:


#Cross validation one row to predict
num=50
Xnew=[X.iloc[num]]
ynew=my_pipeline.predict(Xnew)

print("True salary: ",true_salary.iloc[num],"\nPredicted salary ",ynew)


# In[10]:


#To deserialize estimator later
with open('my_pipeline.pkl','wb') as fid:
    pickle.dump(my_pipeline,fid)

