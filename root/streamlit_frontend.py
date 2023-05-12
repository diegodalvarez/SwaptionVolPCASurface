# -*- coding: utf-8 -*-
"""
Created on Sun May  7 19:24:11 2023

@author: Diego
"""

import streamlit as st
from SwaptionVolPCA import *


st.set_page_config(
    page_title = "Swaption IV Surface",
    layout = "wide")

st.header("Swaption IV Surface PCA")
st.write("Made by Diego Alvarez")

col1, col2, col3 = st.columns(3)

with col1:
    
    st.subheader("Data Options")
    download_button = st.radio(
        label = "Download Data (from Bloomberg Terminal if none is found)",
        options = ["On", "Off"])
    
    if download_button == "Off": download_button = False
    else: download_button = True
    
    update_button = st.radio(
        label = "Update New Data (from Bloomberg Terminal)",
        options = ["Off", "On"])
    
    if update_button == "Off": update_button = False,
    else: update_button = True
    
with col2:
    
    st.subheader("Output Options")
    
    output_options = st.radio(
        label = "Save output to file",
        options = ["Off", "On"])
    
    if output_options == "Off": output_options = False
    else: output_options = True
    
with col3:
    
    st.subheader("Backend Options")
    
    verbose = st.radio(
        label = "Output Logging to Console",
        options = ["Off", "On"])
    
    if verbose == "Off": verbose = False,
    else: verbose = True
    
    logging = st.radio(
        label = "Save logs to file",
        options = ["Off", "On"])
    
    if logging == "Off": logging = False,
    else: logging = True

st.subheader("Run Button")

run_button = st.radio(
    label = "Run Button",
    options = ["Off", "On"])

@st.cache_data
def get_plot_resid(): 
    
    return(swaption_pca.plot_resid_zscore())

if run_button == "On":

    swaption_pca = SwaptionVolPCA(
        verbose = verbose,
        log_on = logging,
        download = download_button,
        update_data = update_button)
    
    plot_resid = get_plot_resid()

    plot_output_options = st.sidebar.selectbox(
        label = "Plot Options",
        options = ["Matplotlib (JPEG)", "Plotly (Interactive)"])
    
    if plot_output_options == "Matplotlib (JPEG)":
        st.pyplot(plot_resid)
        
    if plot_output_options == "Plotly (Interactive)":
        
        col1, col2 = st.columns(2)

        with col1:
            
            current_grid, max_date = swaption_pca.make_current_surface_plotly()
            st.subheader("Swaption Surface as of {}".format(max_date))
            st.plotly_chart(current_grid, theme = "streamlit")

            ratio_grid = swaption_pca.make_current_ratio_plotly()
            st.subheader("Swaption Surface Difference using 30d Window")
            st.plotly_chart(ratio_grid)

        with col2:
            
            ratio_grid = swaption_pca.make_current_difference_plotly()
            st.subheader("Swaption Surface Difference using 30d Window")
            st.plotly_chart(ratio_grid)

            st.subheader("Swaption PCA Z-scores Richness and Cheapness")
            st.plotly_chart(swaption_pca.make_pca_z_score_plotly())