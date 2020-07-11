import streamlit as st
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from time import time
import seaborn as sns
sns.set(style="whitegrid")

st.write(
    """
    ## Simple Iris Flower Prediction App
    """
)

st.markdown("---")

st.sidebar.header("User Input Parameters")

iris = datasets.load_iris()

feature_names = ['sepal length', 'sepal width', 'petal length', 'petal width']
feature_stats = [None] * len(feature_names)
target_names = iris['target_names']

for x in range(iris['data'].shape[1]):
    feature_stats[x] = [None]*3
    feature_stats[x][0] = np.min(iris['data'][:, x])
    feature_stats[x][1] = np.max(iris['data'][:, x])
    feature_stats[x][2] = np.mean(iris['data'][:, x])

def display_input_features_dynamic():
    """
    display the user inputs and get the results
    """
    selected_feature_values = {}
    for idx, feature_name_ in enumerate(feature_names):
        value_ = st.sidebar.slider(label=feature_name_, min_value=feature_stats[idx][0], max_value=feature_stats[idx][1], value=feature_stats[idx][2])
        selected_feature_values[feature_name_] = value_
    return selected_feature_values
st.subheader("User input features")
selected_feature_values = display_input_features_dynamic()
st.write(selected_feature_values)

def build_and_train_model(X, y, start_time):
    clf = RandomForestClassifier(n_estimators=1000, max_depth=5)
    clf.fit(X, y)
    return clf, time()-start_time
with st.spinner(text='Model training...'):
    trained_model, time_to_train = build_and_train_model(X=iris['data'], y=iris['target'], start_time=time())
st.write(f"Time to train the model is {time_to_train}s")

def make_predictions(model, user_input):
    predicted_class = model.predict(np.array(user_input).reshape(1,-1))
    predicted_probability = model.predict_proba(np.array(user_input).reshape(1,-1))
    return predicted_class, predicted_probability

predicted_class, predicted_probability =  make_predictions(trained_model, list(selected_feature_values.values()))

print (predicted_class, predicted_probability)

st.write(iris['target_names'][predicted_class], predicted_probability)

predicted_probability_chart_data = pd.DataFrame(data={'probabilities': predicted_probability[0], 'flower class': target_names})

sns.barplot(x='flower class', y='probabilities', data=predicted_probability_chart_data)

st.pyplot()