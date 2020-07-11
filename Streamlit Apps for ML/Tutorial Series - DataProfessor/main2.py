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
st.sidebar.subheader("User Input Parameters")
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

hyperparameter_names = ['n_estimators', 'max_depth', 'max_features']
hyperparameter_values = [[50, 1000, 200], [3, 10, 5], [["auto", "sqrt", "log2"], [0] ]]
def display_input_hyperparameters_dynamic():
    """
    Get user input as hyperparameters and display them
    """
    selected_hyperparameter_values = {}

    for idx, hyper_name_ in enumerate(hyperparameter_names):
        if idx < 2:
            value_ = st.sidebar.slider(label=hyper_name_, min_value=hyperparameter_values[idx][0], max_value=hyperparameter_values[idx][1], value=hyperparameter_values[idx][2])
        else:
            value_ = st.sidebar.selectbox(label=hyper_name_, options=hyperparameter_values[idx][0], index=hyperparameter_values[idx][1][0])
        selected_hyperparameter_values[hyper_name_] = value_
    return selected_hyperparameter_values
st.subheader("User input features")
selected_feature_values = display_input_features_dynamic()
st.write(selected_feature_values)
st.sidebar.markdown("---")
st.sidebar.subheader("User Input Hyperparameters for Random Forest Classifier")
selected_hyperparameter_values = display_input_hyperparameters_dynamic()
st.subheader("User input hyperparameters")
st.write(selected_hyperparameter_values)

button_value = st.sidebar.button(label="Submit user inputs")

def build_and_train_model(X, y, start_time, hyperparameters):
    clf = RandomForestClassifier(n_estimators=hyperparameters['n_estimators'], max_depth=hyperparameters['max_depth'], max_features=hyperparameters['max_features'])
    clf.fit(X, y)
    return clf, time()-start_time

def make_predictions(model, user_input):
    predicted_class = model.predict(np.array(user_input).reshape(1,-1))
    predicted_probability = model.predict_proba(np.array(user_input).reshape(1,-1))
    return predicted_class, predicted_probability




def main_block():
    ### train model
    with st.spinner(text='Model training...'):
        trained_model, time_to_train = build_and_train_model(X=iris['data'], y=iris['target'], start_time=time(), hyperparameters=selected_hyperparameter_values)
    st.write(f"Time to train the model is {np.round(time_to_train, decimals=2)}s")

    ### make prediction
    predicted_class, predicted_probability =  make_predictions(trained_model, list(selected_feature_values.values()))
    st.markdown(f"> The predicted class is **{iris['target_names'][predicted_class][0]}** with a probability of `{np.round(np.max(predicted_probability),decimals=4)*100}%`")

    ### display chart
    predicted_probability_chart_data = pd.DataFrame(data={'probabilities': predicted_probability[0], 'flower class': target_names})

    sns.barplot(x='flower class', y='probabilities', data=predicted_probability_chart_data)

    st.pyplot()

if button_value:
    main_block()