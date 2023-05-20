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

    viewer_options = st.sidebar.selectbox(
        label = "View",
        options = [
            "Volatility Surface", "Historical Z-Scores", "Historical PCs",
            "Bar Chart Richness / Cheapness", "Bar Chart Change in Z-Score"])
    
    swaption_pca = SwaptionVolPCA(
        verbose = verbose,
        log_on = logging,
        download = download_button,
        update_data = update_button)
    
    if viewer_options == "Volatility Surface":

        plot_output_options = st.sidebar.selectbox(
            label = "Plot Options",
            options = ["Plotly (Interactive)", "Matplotlib (JPEG)"])

        plot_resid = get_plot_resid()
    
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
                
    if viewer_options == "Historical Z-Scores":
        
        plot_type = st.sidebar.selectbox(
            label = "Plotting Type",
            options = ["Streamlit", "Matplotlib JPEG"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
        
            lookback_option = st.selectbox(
                label = "Lookback",
                options = ["Historical", "Custom"])
        
        if lookback_option == "Historical":
        
            rolling_z_score = swaption_pca.get_rolling_z_score()
            col1, col2, col3 = st.columns(3)
        
            
            for i, column in enumerate(rolling_z_score.columns):
                
                if plot_type == "Matplotlib JPEG":
                
                    fig, axes = plt.subplots(figsize = (8,3))
            
                    (rolling_z_score[
                        [column]].
                        plot(
                            ax = axes,
                            legend = False,
                            ylabel = "Z-Score",
                            title = column + " ATM Swaption Straddle from {} to {}".format(
                                rolling_z_score.index.min().date(), 
                                rolling_z_score.index.max().date())))
                    
                    if i % 3 == 0: 
                        with col1: st.pyplot(fig)
                        
                    if i % 3 == 1: 
                        with col2: st.pyplot(fig)
                        
                    if i % 3 == 2:
                        with col3: st.pyplot(fig)
                        
                if plot_type == "Streamlit":
                    
                    if i % 3 == 0:
                    
                        with col1: 
                            
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(rolling_z_score[[column]])
                    
                    if i % 3 == 1:
                        
                        with col2:
                            
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(rolling_z_score[[column]])
                            
                    if i % 3 == 2:
                        
                        with col3:
                            
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(rolling_z_score[[column]])
                    
        if lookback_option == "Custom":
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
            
                lookback_window = st.number_input(
                    label = "Lookback Days",
                    min_value = 30)
                
            rolling_z_score = swaption_pca.get_rolling_z_score().tail(lookback_window)
            col1, col2, col3 = st.columns(3)
            
            for i, column in enumerate(rolling_z_score.columns):
                
                fig, axes = plt.subplots(figsize = (8,3))
                
                if plot_type == "Matplotlib JPEG":
                
                    (rolling_z_score[
                        [column]].
                        plot(
                            ax = axes,
                            legend = False,
                            ylabel = "Z-Score",
                            title = column + " ATM Swaption Straddle from {} to {}".format(
                                rolling_z_score.index.min().date(), 
                                rolling_z_score.index.max().date())))
                    
                    if i % 3 == 0: 
                        with col1: st.pyplot(fig)
                        
                    if i % 3 == 1: 
                        with col2: st.pyplot(fig)
                        
                    if i % 3 == 2:
                        with col3: st.pyplot(fig)
                        
                if plot_type == "Streamlit":
                    
                    if i % 3 == 0:
                    
                        with col1: 
                            
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(rolling_z_score[[column]])
                    
                    if i % 3 == 1:
                        
                        with col2:
                            
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(rolling_z_score[[column]])
                            
                    if i % 3 == 2:
                        
                        with col3:
                            
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(rolling_z_score[[column]])
                            
    if viewer_options == "Bar Chart Richness / Cheapness":
        
        plotting_options = st.sidebar.selectbox(
            label = "Plotting Option",
            options = ["Matplotlib JPEG", "Streamlit"])
        
        if plotting_options == "Streamlit": 
        
            rolling_z_score = swaption_pca._make_z_score_bar_plot()
            st.bar_chart(rolling_z_score)
            
        if plotting_options == "Matplotlib JPEG":
            
            st.pyplot(swaption_pca.make_z_score_bar_plot())
            
    if viewer_options == "Bar Chart Change in Z-Score":
        
        plotting_options = st.sidebar.selectbox(
            label = "Plotting Option",
            options = ["Matplotlib JPEG", "Streamlit"])
        
        if plotting_options == "Streamlit":
            
            rolling_z_score_change = swaption_pca._make_z_score_change_plot(
                period = 1)
            
            st.write("1d Change")
            st.bar_chart(rolling_z_score_change)
            
            rolling_z_score_change = swaption_pca._make_z_score_change_plot(
                period = 5)
            
            st.write("5d Change (1wk)")
            st.bar_chart(rolling_z_score_change)
            
            rolling_z_score_change = swaption_pca._make_z_score_change_plot(
                period = 30)
            
            st.write("30d Change (1 month)")
            st.bar_chart(rolling_z_score_change)
            
        if plotting_options == "Matplotlib JPEG":
            
            col1, col2, col3 = st.columns(3)
            with col1:
                
                color = st.radio(
                    label = "Select Coloring",
                    options = ["By Change in Z Score", "By Z Score Value"])
                
                color_dict = {
                    "By Change in Z Score": "change",
                    "By Z Score Value": "z_score"}
            
            for i in [1, 5, 30]:
            
                rolling_z_score_change = swaption_pca.make_z_score_change_plot(
                    period = i,
                    color_by = color_dict[color])
                
                st.write(rolling_z_score_change)
            