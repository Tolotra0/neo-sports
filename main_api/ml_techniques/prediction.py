#!/usr/bin/env python
# coding: utf-8

# In[42]:

import collections
import numpy as np
import pandas as pa

from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.externals.six import StringIO


def data_processing(data):
    df = data.drop(['Unnamed: 0', 'Team', 'Game', 'Date', 'Home', 'Opponent'], axis=1)
    features = df.values[:, 1:]
    classes  = df.values[:, 0]

    X = np.empty(features.shape, dtype=int)
    for index, line in enumerate(features):
        X[index] = line
        
    Y = [1 if item == 'W' else 0 for item in classes]

    data_df = pa.DataFrame(X)
    data_df.columns = df.columns[1:]
    data_df = data_df.assign(Decision=Y)

    return data_df

def build_classifier(data):
    X_data = data_df.values[:, :14]
    Y_data = data_df.values[:, 14]
    
    # split data into train and test set
    # 10%: test set | 90%: train set
    X_train, X_test, y_train, y_test = train_test_split(
        X_data, Y_data, test_size=0.1, random_state=100)

    classifier = DecisionTreeClassifier()
    classifier.fit(X_train, y_train)
    
    # evaluation
    y_pred = classifier.predict(X_test)

    report = classification_report(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    # evaluation
    
    return classifier

def predict(model, features):
    labels = np.array(['Win', 'Loss'])
    
    if model is not None and features is not None:
        classes = model.predict(features)
        return labels[classes]
    
    return None

def export_tree(classifier, feature_names):
    dot_data = StringIO()
    labels = np.array(['Win', 'Loss'])
    colors = ('#c2f9d2', '#f7eda0')
    
    export_graphviz(classifier, out_file=dot_data,
                    feature_names=feature_names,class_names=labels,
                    filled=True, rounded=True, proportion=True,
                    impurity=False, label='none', special_characters=True)

    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    edges = collections.defaultdict(list)

    for edge in graph.get_edge_list():
        edges[edge.get_source()].append(int(edge.get_destination()))

    for edge in edges:
        edges[edge].sort()
        for i in range(2):
            dest = graph.get_node(str(edges[edge][i]))[0]
            dest.set_fillcolor(colors[i])

    # graph.write_pdf('tree.pdf')
    # graph.write_png('tree.png')


# In[44]:


# main program

path = '/home/aina/Documents/PyNotebook/data/NBA 2014-2018 game stats.csv'
data = pa.read_csv(path)

# data processing and modeling
data_df = data_processing(data)
model = build_classifier(data_df)

# export model as file
# feature_names = data_df.columns[:14].values
# export_tree(model, feature_names)

# prediction
features = np.array([
                [102, 40, 80, 13, 22, 9, 17, 10, 42, 26, 6, 8, 17, 24],
                [102, 35, 69, 7, 20, 25, 33, 3, 37, 26, 10, 6, 12, 20],
                [92, 38, 92, 8, 25, 8, 11, 10, 37, 26, 14, 5, 13, 25],
                [119, 43, 93, 13, 33, 20, 26, 7, 38, 28, 8, 3, 19, 33],
                [103, 33, 81, 9, 22, 28, 36, 12, 41, 18, 10, 5, 8, 17]
            ])
decision = predict(model, features)
decision
