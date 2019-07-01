#!/usr/bin/env python
# coding: utf-8

# In[35]:


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


# In[36]:


#Explore Data
player_file_path='Data/nba_2014_2018_game_stats.csv'
team_data=pd.read_csv(player_file_path)
team_data.describe()


# In[37]:


team_data.head()


# In[38]:


# Choose target and features
y = team_data.Win
player_features = ['TeamId','Game','GameLocationTypeId', 'OpponentId','PTS','FGM','FGA','TPM','TPA','FTM','FTA','OREB','TREB','AST','STL','BLK','TOV','TF']
X = team_data[player_features]


# In[39]:


#Cross validation
my_pipeline = Pipeline(steps=[('preprocessor', SimpleImputer()),
                              ('model', RandomForestRegressor(n_estimators=75,
                                                              random_state=0))
                             ])


# In[40]:


#fit estimator
my_pipeline.fit(X,y)

#Serialize estimator
with open('my_pipeline.pkl','wb') as fid:
    pickle.dump(my_pipeline,fid)


# In[41]:


# Multiply by -1 since sklearn calculates *negative* MAE
scores = -1 * cross_val_score(my_pipeline, X, y,
                              cv=10,
                              scoring='neg_mean_absolute_error')

print("MAE scores:\n", scores)
print("Average MAE score (across experiments):")
print(scores.mean())


# In[42]:


val_predict =cross_val_predict(my_pipeline, X, y,cv=5)
print("Values predicted:\n",val_predict)


# In[43]:


#data frame 
true_salary=team_data.Win
plot_data2=pd.DataFrame(data = {'true_victory':true_salary,'predicted_victory':val_predict})

# Set the width and height of the figure
plt.figure(figsize=(18,8))

# Add title
plt.title("NBA players'salary stats 2017_2018")

# Line chart showing true salary'
sns.lineplot(data=plot_data2['true_victory'], label="true_victory")

# Line chart showing predicted salary'
sns.lineplot(data=plot_data2['predicted_victory'], label="predicted_victory")


# In[44]:


#Cross validation one row to predict
num=5000
Xnew=[X.iloc[num]]
ynew=my_pipeline.predict(Xnew)

def victory(y):
    if(y>0.5):
        return 1
    else:
        return 0
    
print("True victory: ",true_salary.iloc[num],"\nPredicted victory : ",victory(ynew))

