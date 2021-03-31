import os
import streamlit as st
import numpy as np
import pandas as pd
import time

def expensive_computation(model_selected, weeks_selceted):
    st.warning('Intensive computation')
    time.sleep(5)
    return [model_selected, weeks_selceted]


if __name__ == "__main__":

    model_options = ['model_A', 'model_B', 'model_C']
    weeks_options = list(range(1, 11))
    sku_options = ['1212','132132','3223', '78498', '77392']


    model_selected = st.sidebar.selectbox(label='Select model', options=model_options, index=0)
    weeks_selected = st.sidebar.selectbox(label='Select weeks to inspect', options=['all'] + weeks_options, index=0)

    st.header('Main page')

    computation_result = expensive_computation(model_selected, weeks_selected)

    st.write(computation_result)


    skus_selected = st.selectbox(label='Select skus', options=sku_options)
    

    computation_result = expensive_computation(model_selected, weeks_selected)

    st.write(skus_selected)
    st.write(computation_result)