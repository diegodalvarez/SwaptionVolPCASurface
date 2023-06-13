# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:45:33 2023

@author: Diego
"""

import os
import sys
import time
import pdblp
import logging
import pandas as pd
import seaborn as sns
import datetime as dt
import plotly.express as px
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

import streamlit as st

class SwaptionVolPCA:
    
    def __init__(
            self, verbose = True, log_on = True, download = False, 
            update_data = False):
        
        # path management
        self.parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.data_path = os.path.join(self.parent_path, "data")
        self.out_path = os.path.join(self.parent_path, "out")
        self.file_path = os.path.join(self.data_path, "svols.parquet")
        
        if os.path.exists(self.data_path) == False: os.makedirs(self.data_path)
        if os.path.exists(self.out_path) == False: os.makedirs(self.out_path)
        if os.path.exists(self.file_path) == False: os.makedirs(self.file_path)
        
        self.today_date = dt.date.today()
        self.verbose = verbose
        self.log_on = log_on
        self.download = download
        
        if self.log_on == True:
            self.log_on_path = os.path.join(self.out_path, "logs")
            
            if os.path.exists(self.log_on_path) == False:
                os.makedirs(self.log_on_path)
                
            logging.basicConfig(
                level = logging.INFO,
                filename = os.path.join(
                    self.log_on_path, 
                    "{}.txt".format(str(time.time()).replace(".", "_"))),
                format = "%(levelname)s: %(asctime)s %(message)s",
                datefmt = "%m/%d/%Y %I:%M:%S")

        if self._locate_data() == False:
            
            if download == False:
                
                if self.verbose == True:
                    sys.exit("[ALERT] Data not found, run svols_pull.py from root directory")
                 
                if self.verbose == False:
                    sys.exit()
                    
            if download == True:
                self._download_swaption_bbg()
                
        if (self.today_date - self.df.date.max().date()).days > 3:
            
            if self.verbose == True:
                print("[ALERT] Data Needs to be updated")
            
            if self.log_on == True:
                logging.info("Data Needs to be updated")
                
            if update_data == True:
                self._download_swaption_bbg()   
             
        self._prep_data()
        self._make_pca()

        self.tenor_join = pd.DataFrame({
            "tenor_year": [5, 7, 1, 2, 10, 30],
            "Swap Tenor Year": ["5y", "7y", "1y", "2y", "10y", "30y"]})
        
        self.expiry_join = pd.DataFrame({
            "expiry_month": [120, 3, 12, 1, 60, 24],
            "Option Expiry Month": ["10y", "3m", "1y", "1m", "5y", "2y"]})
        
        self.column_renamer = {
            "USSN011": "1y1y",
            "USSN0110": "1y10y",
            "USSN012": "1y2y",
            "USSN0130": "1y30y",
            "USSN015": "1y5y",
            "USSN017": "1y7y",
            "USSN021": "2y1y",
            "USSN0210": "2y10y",
            "USSN022": "2y2y",
            "USSN0230": "2y30",
            "USSN025": "2y5y",
            "USSN027": "2y7y", 
            "USSN051": "5y1y",
            "USSN0510": "5y10y",
            "USSN052": "5y2y", 
            "USSN0530": "5y30y",
            "USSN055": "5y5y",
            "USSN057": "5y7y",
            "USSN0A1": "1m1y", 
            "USSN0A10": "1m10y",
            "USSN0A2": "1m2y",
            "USSN0A30": "1m30y",
            "USSN0A5": "1m5y",
            "USSN0A7": "1m7y",
            "USSN0C1": "3m1y",
            "USSN0C10": "3m10y",
            "USSN0C2": "3m2y",
            "USSN0C30": "3m30y",
            "USSN0C5": "3m5y",
            "USSN0C7": "3m7y",
            "USSN101": "10y1y",
            "USSN1010": "10y10y",
            "USSN102": "10y2y",
            "USSN1030": "10y30y",
            "USSN105": "10y5y",
            "USSN107": "10y7y"}
        
    # looks for data returns bool, saves data as self.df if it can find it  
    def _locate_data(self) -> bool:
        
        try:
            
            if self.verbose == True:
                st.write("[INFO] Trying to locate Swaption Volatility Data")
                
            if self.log_on == True:
                logging.info("Attempting to read data")
            
            self.df = pd.read_parquet(
                path  = self.file_path,
                engine = "pyarrow")
            
            if self.verbose == True:
                st.write("[INFO] Swaption Volatility Data Found")
                
            if self.log_on == True:
                logging.info("Data Found")
            
            return True
        
        except:
            
            if self.verbose == True:
                st.write("[ALERT] Swaption Volatility Data Not Found, select Download")
                
            if self.log_on == True:
                logging.error("Data Not Found")
            
            return False
    
    # downloads data, saves it as self.df, appends to new
    def _download_swaption_bbg(self) -> bool:
        
        try:
            
            if self.verbose == True:
                print("[INFO] Establishing connection to BBG")

            if self.log_on == True:
                logging.info("Establishing Bloomberg Connection")
            
            con = pdblp.BCon(debug = False, port = 8194, timeout = 5_000)
            con.start()
            
            if self.verbose == True:
                print("[INFO] Connection Established")

            if self.log_on == True:
                logging.info("Connection Established")
            
            EXPIRY_LIST = ["0A", "0C", "01", "02", "05", "10"]
            TENOR_LIST = ["1", "2", "5", "7", "10", "30"]
            flds = ["PX_LAST"]
            
            # we need to check if we already have our data
            if self._locate_data() == False:
            
                if self.verbose == True:
                    print("[ALERT] No Existing data found")
                    
                if self.log_on == True:
                    logging.info("No Existing data found")
            
                end_date = self.today_date
                start_date = dt.date(
                    year = self.today_date.year - 10,
                    month = self.today_date.month,
                    day = self.today_date.day)
                
            else:
                
                if self.verbose == True:
                    print("[INFO] Found existing data")
                    
                if self.log_on == True:
                    logging.info("Existing data found")
                
                end_date = self.today_date
                start_date = self.df.date.max().date()
                
                if self.verbose == True:
                    print("[INFO] Updating data from {}".format(start_date))
                    
                if self.log_on == True:
                    logging.info("Updating data from {}".format(start_date))
                
            end_date_input  = end_date.strftime("%Y%m%d")
            start_date_input = start_date.strftime("%Y%m%d")
            security_list = []
            
            for expiry in EXPIRY_LIST:
                for tenor in TENOR_LIST:
                    
                    security_input = "USSN{}{} BBIR Curncy".format(expiry, tenor)
                    security_list.append(security_input)
            
            if self.verbose == True:
                print("[INFO] Attempting to download data")
                
            if self.log_on == True:
                logging.info("Attempting to download data")
            
            if self._locate_data() == False:
                        
                print("Collecting data")
                self.df = (con.bdh(
                    tickers = security_list,
                    flds = flds,
                    start_date = start_date_input,
                    end_date = end_date_input).
                    reset_index().
                    melt(id_vars = "date"))
                
            else:
                
                print("Collecting Data")
                df_tmp = (con.bdh(
                    tickers = security_list,
                    flds = flds,
                    start_date = start_date_input,
                    end_date = end_date_input).
                    reset_index().
                    melt(id_vars = "date"))
                
                self.df = pd.concat([self.df, df_tmp])
                
            con.stop()   
                
            self.df = self.df.drop_duplicates()
                
            self.df.to_parquet(os.path.join(self.data_path, "svols.parquet"))
                
            if self.verbose == True:
                print("[INFO] Data Was Successfullly Collected from Bloomberg")
                
            if self.log_on == True:
                logging.info("Data was collected from Bloomberg")
            
            return True
            
        except:
            
            if self.verbose == True:
                print("[ALERT] There was a problem at the previous step")
                
            if self.log_on == True:
                logging.error("There was a problem at the previous step")
            
            return False
        
    def _prep_data(self) -> None:
        
        try:
        
            df_expiry = (self.df.assign(
                first_val = lambda x: x.ticker.str.split(" ").str[0].str.replace("USSN", ""),
                expiry = lambda x: x.first_val.str[0:2],
                ticker_len = lambda x: x.ticker.str.len()))
            
            df_expiry_single, df_expiry_double = df_expiry.query("ticker_len == 19"), df_expiry.query("ticker_len == 20")
            
            df_expiry_single_tenor = (df_expiry_single.assign(
                tenor = lambda x: x.first_val.str[-1]))
            
            df_expiry_double_tenor = (df_expiry_double.assign(
                tenor = lambda x: x.first_val.str[-2:]))
            
            df_expiry_tenor = (pd.concat([
                df_expiry_single_tenor, 
                df_expiry_double_tenor]).
                drop(columns = ["ticker_len"]).
                assign(tenor = lambda x: x.tenor.astype("int")))
            
            expiry_fix = (pd.DataFrame(
                {"expiry": ["0C", "10", "01", "05", "0A", "02"],
                 "expiry_month": [3, 10 * 12, 1 * 12, 5 * 12, 1, 2 * 12]}))
            
            self.df_prep = (df_expiry_tenor.merge(
                expiry_fix, 
                how = "inner",
                on = ["expiry"]).
                drop(columns = ["expiry", "first_val"]).
                rename(columns = {"tenor": "tenor_year"}))
            
        except:
            
            if self.verbose == True:
                sys.exit("[ALERT] There was a problem prepping the data")
                
            if self.log_on == True:
                logging.error("There was a problem prepping the data")
                sys.exit()
            
            else:
                sys.exit()
            
    def _make_pca(self) -> None:
        
        try:
        
            date_max = self.df_prep.date.max()
            date_cutoff = dt.date(year = date_max.year - 2, month = date_max.month, day = date_max.day)
            self.df_wider_raw_value = (self.df_prep.drop_duplicates().query(
                "date >= @date_cutoff").
                assign(ticker = lambda x: x.ticker.str.split(" ").str[0])
                [["date", "ticker", "value"]].
                pivot(index = "date", columns = "ticker", values = "value"))
            
            self.pca_raw = PCA(n_components = 3)
            self.pca_raw_fit = self.pca_raw.fit(self.df_wider_raw_value)
            
            if self.verbose == True:
                print("[INFO] Made PCA model")
                
            if self.log_on == True:
                logging.info("Made PCA model")
                
        except:
            
            if self.verbose == True:
                sys.exit("[ALERT] There was a problem making the PCA model")
                
            if self.log_on == True:
                logging.error("There was a problem generating the PCA model")
                sys.exit()
                
            else:
                sys.exit()

    def get_pca_exp_variances(self) -> pd.DataFrame:
        
        try:
        
            if self.verbose == True:
                print("[INFO] Generating Explained Variance Ratio DataFrame")
            
            if self.log_on == True:
                logging.info("Generating Explained Variance Ratio DataFrame")
            
            return(pd.DataFrame({
                "single_component": self.pca_raw_fit.explained_variance_ratio_},
                index = ["comp1", "comp2", "comp3"]).
                assign(cum_component = lambda x: x.single_component.cumsum()))
        
        except:
            
            if self.verbose == True:
                sys.exit("[ALERT] There was a problem with generating explained variance ratio dataframe")
                
            if self.log_on == True:
                logging.error("There was a problem with generating explained variance ratio dataframe")
                sys.exit()
                
            else:
                sys.exit()
    
    def plot_pca_exp_variances(self, figsize = (20,6)) -> plt.Figure:
        
        try:
            
            if self.verbose == True:
                print("[INFO] Generating Variance Plots")
                
            if self.log_on == True:
                logging.info("Generating Variance Plots")
        
            fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = figsize)
            pca_variances_df = self.get_pca_exp_variances()
            
            (pca_variances_df[
                ["single_component"]].
                rename(columns = {"single_component": "Single Component"}).
                plot(
                    ax = axes[0], kind = "bar",
                    title = "Single Component",
                    ylabel = "Explained Variance",
                    legend = False))
            
            (pca_variances_df[
                ["cum_component"]].
                rename(columns = {"cum_component": "Cumulative Component"}).
                plot(
                    ax = axes[1], kind = "bar",
                    title = "Cumulative Components",
                    ylabel = "Explained Variance",
                    legend = False))
            
            fig.suptitle("Explained Variance from PCA model")
            plt.tight_layout()
            return fig
        
        except:
            
            if self.verbose == True:
                sys.exit("[ALERT] There was a problem making explained variance ratio dataframe plot")
                
            if self.log_on == True:
                logging.error("There was a problem making explained variance ratio dataframe plot")
                sys.exit()
                
            else:
                sys.exit()
    
    def get_pca_fit_transform(self) -> pd.DataFrame:
        
        pcs = self.pca_raw_fit.transform(self.df_wider_raw_value)
        return(pd.DataFrame(
            pcs, columns = ["PC1", "PC2", "PC3"],
            index = self.df_wider_raw_value.index))
    
    def plot_pca_fit_transform(self, figsize = (20,6)) -> plt.Figure:
        
        if self.verbose == True:
            print("[INFO] Fitting to data already trained on (in-sample)")
            
        pcs = self.get_pca_fit_transform()
        
        fig, axes = plt.subplots(figsize = figsize)
        (pcs.plot(
            ax = axes, 
            title = "Historical PCs for ATM Swaptions from {} to {} (Fitting to data already trained on)".format(
                pcs.index.min().date(), pcs.index.max().date())))
        plt.tight_layout()
        return fig
    
    def get_pca_fit_transform_scale(self) -> pd.DataFrame:

        pcs = self.pca_raw_fit.transform(self.df_wider_raw_value)
        pcs_prep = (pd.DataFrame(
            pcs, columns = ["comp1", "comp2", "comp3"],
            index = self.df_wider_raw_value.index).
            reset_index().
            melt(id_vars = "date").
            rename(columns = {"variable": "comp"}))
        
        explained_variance = (self.get_pca_exp_variances()[
            ["single_component"]].
            reset_index().
            rename(columns = {"index": "comp"}))

        df_merged = (pcs_prep.merge(
            explained_variance, how = "inner", on = ["comp"]).
            assign(scaled_comp = lambda x: x.single_component * x.value)
            [["date", "comp", "scaled_comp"]].
            pivot(index = "date", columns = "comp", values = "scaled_comp").
            rename(columns = {
                "comp1": "PC1",
                "comp2": "PC2",
                "comp3": "PC3"}))

        return df_merged
    
    def get_pca_fit_transform_scale_plot(self, figsize = (20,6)) -> plt.Figure:

        pcs_scaled = self.get_pca_fit_transform_scale()
        fig, axes = plt.subplots(figsize = figsize)

        pcs_scaled.plot(
            ax = axes,
            title = "Historical PCs scaled by explained variance from {} to {}".format(
            pcs_scaled.index.min().date(), pcs_scaled.index.max().date()))
        
        return fig
    
    def get_resid(self) -> pd.DataFrame:
        
        pcs = self.get_pca_fit_transform()
        df_fitted = (pd.DataFrame(
            data = self.pca_raw.inverse_transform(pcs),
            index = self.df_wider_raw_value.index,
            columns = self.df_wider_raw_value.columns))
        
        df_merged = (self.df_wider_raw_value.reset_index().melt(
            id_vars = "date").
            rename(columns = {"value": "raw_value"}).
            merge(
                (df_fitted.reset_index().melt(
                  id_vars = "date").
                  rename(columns = {"value": "fitted_value"})),
                how = "inner",
                on = ["date", "ticker"]))
        
        residuals_df = (df_merged.assign(
            residuals = lambda x: x.raw_value - x.fitted_value)
            [["date", "ticker", "residuals"]].
            pivot(index = "date", columns = "ticker", values = "residuals"))
    
        return residuals_df
    
    def get_resid_zscore(self) -> pd.DataFrame:

        try:
            
            if self.verbose == True:
                print("[INFO] Getting PCA Z-scores values")
                
            if self.log_on == True:
                logging.info("Generating PCA Z-scores values")
        
            residuals = self.get_resid().sort_index()
            z_score = (residuals.tail(1) - residuals.tail(30).mean()) / residuals.tail(30).std()
            
            z_score_out = (z_score.reset_index().melt(
                id_vars = "date").
                merge(
                    (self.df_prep[
                        ["ticker", "tenor_year", "expiry_month"]].
                        drop_duplicates().
                        assign(ticker = lambda x: x.ticker.str.split(" ").str[0])),
                    how = "left",
                    on = ["ticker"]).
                pivot(index = "expiry_month", columns = "tenor_year", values = "value"))
            
            return z_score_out
        
        except:
            
            if self.verbose == True:
                sys.exit("[ALERT] There was a problem generating z-scores")
                
            if self.log_on == True:
                logging.error("There was a problem generating z-scores")
                sys.exit()
                
            else:
                sys.exit()

    def _get_rolling_z_score(self, df: pd.DataFrame) -> pd.DataFrame:


        return(df.assign(
            roll_mean = lambda x: x.value.rolling(window = 30).mean(),
            roll_std = lambda x: x.value.rolling(window = 30).std(),
            z_score = lambda x: (x.value - x.roll_mean) / x.roll_std))

    def get_rolling_z_score(self) -> pd.DataFrame:

        try:

            if self.verbose == True:
                print("[INFO] Getting PCA Residuals Z-scores")
            
            if self.log_on == True:
                logging.info("Getting PCA Residual Z-scores")

            residuals = (self.get_resid().sort_index().reset_index().melt(
                id_vars = "date").
                groupby("ticker").
                apply(self._get_rolling_z_score)
                [["date", "ticker", "z_score"]].
                dropna().
                pivot(index = "date", columns = "ticker", values = "z_score").
                rename(columns = self.column_renamer))
            
            return residuals

        except:

            if self.verbose == True:
                sys.exit("[ALERT] There was a problem generating z-scores")

            if self.log_on == True:
                logging.error("Therew as a problem getting z-scores")
                sys.exit()

    def plot_resid_zscore(self, figsize = (24,24), savefig = True) -> pd.DataFrame:

        try:        

            if self.verbose == True:
                print("[INFO] Generating Heatmaps")
                
            if self.log_on == True:
                logging.info("Generating Heatmaps")

            fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = figsize)
            
            max_date = self.df.date.max().date()
            recent_vols = (self.df_prep.query(
                "date == @max_date")
                [["value", "tenor_year", "expiry_month"]].
                rename(columns = {
                    "expiry_month": "Option Expiry Month",
                    "tenor_year": "Swap Rate Tenor"}).
                pivot(index = "Option Expiry Month", columns = "Swap Rate Tenor", values = "value"))

            sns.heatmap(
                data = recent_vols,
                fmt = ".3g",
                annot = True,
                cmap = "Reds",
                ax = axes[0,0])
            
            axes[0,0].set_title("ATM Swaption IV Surface at")
            
            lookback_date = self.df_prep.date.drop_duplicates().sort_values().iloc[-30]
            max_date_vols = (self.df_prep.query(
                "date == @max_date")
                [["value", "tenor_year", "expiry_month"]].
                rename(columns = {"value": "max_date"}))
            
            lookback_vols = (self.df_prep.query(
                "date == @lookback_date")
                [["value", "tenor_year", "expiry_month"]].
                rename(columns = {"value": "lookback_date"}))
            
            df_merged = (max_date_vols.merge(
                lookback_vols,
                how = "inner",
                on = ["tenor_year", "expiry_month"]).
                assign(
                    ratio = lambda x: x.max_date / x.lookback_date,
                    diff = lambda x: x.max_date - x.lookback_date))
            
            df_ratio = (df_merged[[
                "tenor_year", "expiry_month", "ratio"]].
                rename(columns = {
                    "tenor_year": "Swap Rate Tenor",
                    "expiry_month": "Option Expiry Month"}).
                pivot(index = "Option Expiry Month", columns = "Swap Rate Tenor", values = "ratio"))
            
            sns.heatmap(
                data = df_ratio,
                fmt = ".3g",
                annot = True,
                cmap = "Greens",
                ax = axes[0,1])
            
            axes[0,1].set_title("ATM Swaption IV Ratio (Prior 30D)")
            
            df_diff = (df_merged[
                ["tenor_year", "expiry_month", "diff"]].
                rename(columns = {
                    "tenor_year": "Swap Rate Tenor",
                    "expiry_month": "Option Expiry Month"}).
                pivot(index = "Option Expiry Month", columns = "Swap Rate Tenor", values = "diff"))
            
            sns.heatmap(
                data = df_diff,
                fmt = ".3g",
                annot = True,
                cmap = "Oranges",
                ax = axes[1,0])
            
            axes[1,0].set_title("ATM Swaption IV Difference (Prior 30D)")
            
            z_score = self.get_resid_zscore()
            z_score.index.name = "Option Expiry Month"
            z_score.columns.name = "Swap Tenor Year"
            
            sns.heatmap(
                data = z_score,
                fmt = ".3g",
                annot = True,
                cmap = "Blues",
                ax = axes[1,1])
            
            axes[1,1].set_title("PCA Z-Score on (Fit on Trained Data all in-sample)")
            
            fig.suptitle("As of {}".format(max_date))
            plt.tight_layout(pad = figsize[0] / 6)
            
            if savefig == True:
                
                plot_out = os.path.join(self.out_path, "out_plots")
                
                if self.verbose == True:
                    print("[INFO] Saving plot to {}".format(plot_out))
                    
                if self.log_on == True:
                    logging.info("Saving plots to {}".format(plot_out))
                    
                fig_name = os.path.join(
                    plot_out, "{}.jpeg".format(str(time.time()).replace(".","_")))
                    
                fig.savefig(fig_name)
    
            return fig
        
        except:
            
            if self.verbose == True:
                sys.exit("[ALERT] There was a problem Generating Heatmaps")
                
            if self.log_on == True:
                logging.error("There was a problem Generating Heatmaps")
                sys.exit()
                
            else:
                sys.exit()

    def make_current_surface_plotly(self):

        
        max_date = self.df_prep.date.max()

        current_grid = (self.df_prep.query(
            "date == @max_date")
            [["value", "tenor_year", "expiry_month"]].
            merge(self.tenor_join, how = "inner", on = ["tenor_year"]).
            merge(self.expiry_join, how = "inner", on = ["expiry_month"]).
            drop(columns = ["tenor_year", "expiry_month"]).
            pivot(index = "Option Expiry Month", columns = "Swap Tenor Year", values = "value")
            [["1y", "2y", "5y", "7y", "10y", "30y"]].
            T
            [["1m", "3m", "1y", "2y", "5y", "10y"]].
            T)
        
        current_grid = round(current_grid, 2)
        
        fig = px.imshow(
            current_grid,
            text_auto = True,
            aspect = "data",
            color_continuous_scale = "Greens")
        
        return fig, max_date.date()
    
    def make_current_ratio_plotly(self):

        lookback_date = self.df_prep.date.drop_duplicates().sort_values().iloc[-30]
        max_date = self.df_prep.date.max()

        max_date_vols = (self.df_prep.query(
            "date == @max_date")
            [["value", "tenor_year", "expiry_month"]].
            rename(columns = {"value": "max_date"}))
        
        lookback_vols = (self.df_prep.query(
            "date == @lookback_date")
            [["value", "tenor_year", "expiry_month"]].
            rename(columns = {"value": "lookback_date"}))
        
        df_merged = (max_date_vols.merge(
            lookback_vols,
            how = "inner",
            on = ["tenor_year", "expiry_month"]).
            assign(ratio = lambda x: x.max_date / x.lookback_date).
            merge(self.tenor_join, how = "inner", on = ["tenor_year"]).
            merge(self.expiry_join, how = "inner", on = ["expiry_month"])
            [["ratio", "Swap Tenor Year", "Option Expiry Month"]].
            pivot(index = "Option Expiry Month", columns = "Swap Tenor Year", values = "ratio")
            [["1y", "2y", "5y", "7y", "10y", "30y"]].
            T
            [["1m", "3m", "1y", "2y", "5y", "10y"]].
            T)
        
        df_merged = round(df_merged, 2)
        
        fig = px.imshow(
            df_merged,
            text_auto = True,
            aspect = "data",
            color_continuous_scale = "Blues")
        
        return fig
    
    def make_current_difference_plotly(self):

        lookback_date = self.df_prep.date.drop_duplicates().sort_values().iloc[-30]
        max_date = self.df_prep.date.max()

        max_date_vols = (self.df_prep.query(
            "date == @max_date")
            [["value", "tenor_year", "expiry_month"]].
            rename(columns = {"value": "max_date"}))
        
        lookback_vols = (self.df_prep.query(
            "date == @lookback_date")
            [["value", "tenor_year", "expiry_month"]].
            rename(columns = {"value": "lookback_date"}))
        
        df_merged = (max_date_vols.merge(
            lookback_vols,
            how = "inner",
            on = ["tenor_year", "expiry_month"]).
            assign(difference = lambda x: x.max_date - x.lookback_date).
            merge(self.tenor_join, how = "inner", on = ["tenor_year"]).
            merge(self.expiry_join, how = "inner", on = ["expiry_month"])
            [["difference", "Swap Tenor Year", "Option Expiry Month"]].
            pivot(index = "Option Expiry Month", columns = "Swap Tenor Year", values = "difference")
            [["1y", "2y", "5y", "7y", "10y", "30y"]].
            T
            [["1m", "3m", "1y", "2y", "5y", "10y"]].
            T)
        
        df_merged = round(df_merged, 2)
        
        fig = px.imshow(
            df_merged,
            text_auto = True,
            aspect = "data",
            color_continuous_scale = "Oranges")
        
        return fig
    
    def make_pca_z_score_plotly(self):

        z_score = self.get_resid_zscore()
        z_score_out = (z_score.reset_index().melt(
            id_vars = "expiry_month").
            merge(self.tenor_join, how = "inner", on = ["tenor_year"]).
            merge(self.expiry_join, how = "inner", on = ["expiry_month"])
            [["Swap Tenor Year", "Option Expiry Month", "value"]].
            pivot(index = "Option Expiry Month", columns = "Swap Tenor Year", values = "value")
            [["1y", "2y", "5y", "7y", "10y", "30y"]].
            T
            [["1m", "3m", "1y", "2y", "5y", "10y"]].
            T)
        
        z_score_out = round(z_score_out, 2)
        
        fig = px.imshow(
            z_score_out,
            text_auto = True,
            aspect = "date",
            color_continuous_scale = "Reds")

        return fig
    
    def _make_z_score_bar_plot(self) -> pd.DataFrame:

        z_score = (self.get_rolling_z_score().reset_index())
        self.last_date = z_score.date.max().date()
        
        z_score_out = (z_score.query(
            "date == date.max()").
            drop(columns = ["date"]).
            assign(col = "value").
            set_index("col").
            T.
            sort_values("value"))
        
        return z_score_out
    
    def make_z_score_bar_plot(self, figsize = (12,6)) -> plt.Figure:

        z_score = self._make_z_score_bar_plot()
        fig, axes = plt.subplots(figsize = figsize)

        colors = ["red" if i < 0 else "green" for i in z_score.value]

        axes.bar(
            x = z_score.index,
            height = z_score.value,
            color = colors)
        
        axes.set_title("Current PCA Residual Z-Score for ATM Swaption Straddles on {}".format(
            self.last_date))

        axes.set_ylabel("Z-Score")
        plt.xticks(rotation = 45)
        plt.tight_layout()

        return fig
    
    def _make_z_score_change_plot(self, period = 1) -> pd.DataFrame:

        z_score = (self.get_rolling_z_score().reset_index())
        self.last_date = z_score.date.max().date()

        first_val, second_val = len(z_score) - period - 1, len(z_score) - 1
        print(first_val, second_val)

        z_score_out = (z_score.reset_index().query(
            "index == @first_val | index == @second_val").
            sort_values("date").
            drop(columns = ["index", "date"]).
            pct_change().
            dropna().
            assign(col = "value").
            set_index("col").
            T.
            sort_values("value"))
        
        return z_score_out
    
    def make_z_score_change_plot(
            self, 
            period: int,
            color_by = "change",
            figsize = (12,6)) -> plt.Figure:

        if color_by != "z_score" and color_by != "change":
            
            print("You have to pass either z_score or change for coloring")
            return -1

        z_score = (self._make_z_score_change_plot(
            period = period))
        
        if color_by == "change":
            colors = ["red" if i < 0 else "green" for i in z_score.value]

        if color_by == "z_score":
            
            z_score_value = (self.get_rolling_z_score().reset_index().query(
                "date == date.max()").
                drop(columns = ["date"]).
                assign(z_score = "z_score").
                set_index("z_score").
                T)
            
            z_score_join = (z_score.reset_index().merge(
                z_score_value, how = "inner", on = "ticker"))
            
            colors = ["red" if i < 0 else "green" for i in z_score_join.z_score]
        
        fig, axes = plt.subplots(figsize = figsize)
        axes.bar(
            x = z_score.index,
            height = z_score.value,
            color = colors)
        
        axes.set_ylabel("% Change in Z-Score")
        axes.set_title("Change in Z-Score Residuals PCA for ATM Swaption Straddle for {}d period on {}".format(
            period,
            self.last_date))
        
        plt.xticks(rotation = 45)
        plt.tight_layout()

        return fig
    
    #def historical_pcs(self) -> pd.DataFrame:

        

'''
if __name__ == "__main__":
    
    swaption_pca = SwaptionVolPCA()
    swaption_pca.plot_resid_zscore()
'''