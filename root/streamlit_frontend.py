# -*- coding: utf-8 -*-
"""
Created on Sun May  7 19:24:11 2023

@author: Diego
"""

import altair as alt
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
        options = ["Off", "On"])

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
        label = "Verbose",
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
            "Volatility Surface", "Historical Volatility", "Historical Z-Scores", 
            "Historical PCs", "Bar Chart Richness / Cheapness", 
            "Bar Chart Change in Z-Score"])

    swaption_pca = SwaptionVolPCA(
        verbose = verbose,
        log_on = logging,
        download = download_button,
        update_data = update_button)
    
    if viewer_options == "Historical Volatility":
        
        df_plot = (swaption_pca.df_prep.sort_values(["tenor_year", "expiry_month"]).
            assign(name = lambda x: "Swap Year: " + x.tenor_year.astype(str) + ", Option Months: " + x.expiry_month.astype(str))
            [["date", "name", "value"]].
            pivot(index = "date", columns = "name", values = "value"))
        
        plot_type = st.sidebar.selectbox(
            label = "Plot Options",
            options = ["Streamlit (Interactive)", "Matplotlib (JPEG)"])
    
        col1, col2, col3 = st.columns(3)
        
        with col1: 
            
            lookback_option = st.selectbox(
                label = "Lookback",
                options = ["Historical", "Custom"])
            
        col1, col2, col3 = st.columns(3)
        
        if lookback_option == "Historical":
        
            for i, column in enumerate(df_plot.columns):
                
                if plot_type == "Matplotlib (JPEG)":
    
                    fig, axes = plt.subplots(figsize = (8,3))                
                    title = "{} from {} to {}".format(
                        column, 
                        df_plot.index.min().date(), 
                        df_plot.index.max().date())
                    
                    (df_plot[
                        [column]].
                        plot(
                            ax = axes,
                            legend = False,
                            title = title,
                            ylabel = "ATM Implied Volatility"))
    
                    if i % 3 == 0:
                        with col1: st.pyplot(fig)
    
                    if i % 3 == 1:
                        with col2: st.pyplot(fig)
    
                    if i % 3 == 2:
                        with col3: st.pyplot(fig)
    
                if plot_type == "Streamlit (Interactive)":
    
                    if i % 3 == 0:
    
                        with col1:
    
                            st.write(column + " ATM Swaption Straddle")

                            min_, max_ = df_plot[column].min(), df_plot[column].max()
                            min_, max_ = min_ * 0.9, max_ * 1.1

                            altair_chart = (alt.Chart(
                                df_plot[[column]].reset_index().rename(
                                    columns = {column: "Implied Volatility"})).
                                mark_line().
                                encode(
                                    x = "date",
                                    y = alt.Y(
                                        "Implied Volatility", 
                                        scale = alt.Scale(domain = [min_, max_]))))
                            
                            st.altair_chart(altair_chart, use_container_width = True)

                    if i % 3 == 1:
    
                        with col2:
    
                            st.write(column + " ATM Swaption Straddle")

                            min_, max_ = df_plot[column].min(), df_plot[column].max()
                            min_, max_ = min_ * 0.9, max_ * 1.1

                            altair_chart = (alt.Chart(
                                df_plot[[column]].reset_index().rename(
                                    columns = {column: "Implied Volatility"})).
                                mark_line().
                                encode(
                                    x = "date",
                                    y = alt.Y(
                                        "Implied Volatility", 
                                        scale = alt.Scale(domain = [min_, max_]))))
                            
                            st.altair_chart(altair_chart, use_container_width = True)
                            
                    if i % 3 == 2:
    
                        with col3:

                            st.write(column + " ATM Swaption Straddle")
                            
                            min_, max_ = df_plot[column].min(), df_plot[column].max()
                            min_, max_ = min_ * 0.9, max_ * 1.1
                            
                            altair_chart = (alt.Chart(
                                df_plot[[column]].reset_index().rename(
                                    columns = {column: "Implied Volatility"})).
                                mark_line().
                                encode(
                                    x = "date",
                                    y = alt.Y(
                                        "Implied Volatility", 
                                        scale = alt.Scale(domain = [min_, max_]))))
                            
                            st.altair_chart(altair_chart, use_container_width = True)
                            
        if lookback_option == "Custom":
            
            col1, col2, col3 = st.columns(3)
    
            with col1:
    
                lookback_window = st.number_input(
                    label = "Lookback Days",
                    min_value = 30)
                
            
            col1, col2, col3 = st.columns(3)
            for i, column in enumerate(df_plot.columns):
                
                df_plot = df_plot.tail(lookback_window)
                
                if plot_type == "Matplotlib (JPEG)":
    
                    fig, axes = plt.subplots(figsize = (8,3))                
                    title = "{} from {} to {}".format(
                        column, 
                        df_plot.index.min().date(), 
                        df_plot.index.max().date())
                    
                    (df_plot[
                        [column]].
                        plot(
                            ax = axes,
                            legend = False,
                            title = title,
                            ylabel = "ATM Implied Volatility"))
    
                    if i % 3 == 0:
                        with col1: st.pyplot(fig)
    
                    if i % 3 == 1:
                        with col2: st.pyplot(fig)
    
                    if i % 3 == 2:
                        with col3: st.pyplot(fig)
    
                if plot_type == "Streamlit (Interactive)":
    
                    if i % 3 == 0:
    
                        with col1:
    
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(df_plot[
                                [column]].
                                rename(columns = {column: "Implied Volatility"}))
    
                    if i % 3 == 1:
    
                        with col2:
    
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(df_plot[
                                [column]].
                                rename(columns = {column: "Implied Volatility"}))
                            
                    if i % 3 == 2:
    
                        with col3:
    
                            st.write(column + " ATM Swaption Straddle")
                            st.line_chart(df_plot[
                                [column]].
                                rename(columns = {column: "Implied Volatility"}))

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

    if viewer_options == "Historical PCs":

        col1, col2, col3 = st.columns(3)

        with col1:

            plotting_options = st.sidebar.selectbox(
                label = "Select Plotting Options",
                options = ["Streamlit (Interactive)", "Matplotlib (JPEG)"])

        if plotting_options == "Matplotlib (JPEG)":

            explained_variance = swaption_pca.get_pca_exp_variances()
            col1, col2 = st.columns(2)

            with col1:

                df_single = (explained_variance[
                    ["single_component"]].
                    rename(columns = {"single_component": "variance"}).
                    assign(variance = lambda x: x.variance * 100))

                fig, axes = plt.subplots(figsize = (12,6))
                (df_single.plot(
                    ax = axes, kind = "bar",
                    legend = False, title = "Single PC Explained Variance",
                    ylabel = "Explained Variance (%)"))

                st.pyplot(fig)

                pcs = swaption_pca.get_pca_fit_transform()
                fig, axes = plt.subplots(figsize = (16,6))
                (pcs.plot(
                    ax = axes, title = "Historical PCs from {} to {}".format(
                        pcs.index.min().date(), pcs.index.max().date())))

                st.pyplot(fig)

            with col2:

                df_single = (explained_variance[
                    ["cum_component"]].
                    rename(columns = {"cum_component": "variance"}).
                    assign(variance = lambda x: x.variance * 100))

                fig, axes = plt.subplots(figsize = (12,6))
                (df_single.plot(
                    ax = axes, kind = "bar",
                    legend = False, title = "Cumulative PC Explained Variance",
                    ylabel = "Explained Variance (%)"))

                st.pyplot(fig)

                pcs_scaled = swaption_pca.get_pca_fit_transform_scale_plot(
                    figsize = (16,6))
                st.pyplot(pcs_scaled)


        if plotting_options == "Streamlit (Interactive)":

            explained_variance = swaption_pca.get_pca_exp_variances()
            col1, col2 = st.columns(2)

            with col1:

                st.write("Single PC Explained Variance")
                df_single = (explained_variance[
                    ["single_component"]].
                    rename(columns = {"single_component": "variance"}).
                    assign(variance = lambda x: x.variance * 100))

                st.bar_chart(df_single)

                pcs = swaption_pca.get_pca_fit_transform()
                title = "Historical PCs from {} to {}".format(
                    pcs.index.min().date(), pcs.index.max().date())

                st.write(title)
                st.line_chart(pcs)

            with col2:

                st.write("Cumulative PC Explained Variance")
                df_cum = (explained_variance[
                    ["cum_component"]].
                    rename(columns = {"cum_component": "variance"}).
                    assign(variance = lambda x: x.variance * 100))

                st.bar_chart(df_cum)

                pcs_scaled = swaption_pca.get_pca_fit_transform_scale()
                title = "Historical PCs from {} to {} scaled by explained variance".format(
                    pcs_scaled.index.min().date(), pcs_scaled.index.max().date())

                st.write(title)
                st.line_chart(pcs_scaled)