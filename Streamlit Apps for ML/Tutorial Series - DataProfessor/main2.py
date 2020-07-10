import streamlit as st
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.write(
    """
    ## Simple Iris Flower Prediction App
    """
)

st.sidebar.header("User Input Parameters")

iris = datasets.load_iris()

print (iris['data'].shape)

feature_names = ['sepal length', 'sepal width', 'petal length', 'petal width']
feature_stats = [None] * len(feature_names)
target_names = iris['target_names']

for x in range(iris['data'].shape[1]):
    print (f"min: {np.min(iris['data'][:, x])}, max: {np.max(iris['data'][:, x])}, mean: {np.mean(iris['data'][:, x])}")
    feature_values[x] = [None]*3
    feature_stats[x][0] = np.min(iris['data'][:, x])
    feature_stats[x][1] = np.max(iris['data'][:, x])
    feature_stats[x][2] = np.mean(iris['data'][:, x])

print (feature_stats)

def display_input_features_dynamic():
    """
    display the user inputs and get the results
    """
    selected_feature_values = {}