# Not Intended as investment advice

# Built with pdblp
See GitHub Repository [here](https://github.com/matthewgilbert/pdblp)

See GitHub Pages [here](https://matthewgilbert.github.io/pdblp/tutorial.html)

# Required Packages
| Name         | Pacakage                                                                                                                        | Version                                          |                           
| ------------ | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Pandas       | ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)                    | 1.3.5
| Matplotlib   | ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)        | 1.1.1
| Scikit-learn | ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) | 1.0.2
| pdblp        |                                                                                                                                 | 0.1.8
| seaborn      |                                                                                                                                 | 0.11.2
| plotly       | ![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)                    | 5.9.0
| matplotlib   | ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)        | 3.5.0

# Background
This model is going to decompose the swaption implied volatility surface. This surface differs from standard IV surfaces since it measures swaption tenor vs. option expiry. The volatility measure is used via ATM Swaption Straddles. This model is more effective than its equity counterparts because currency options exhibit more symmetric smiles than equity options. With regards to PCA another way of thinking about this is to consider that with the symmetric smile the implied distributions contain less skew. In regards to financial models ATM straddles can represent both upside and downside volatilty since there isn't a tendency for a direction. 

# Swaption Volatility Surface PCA
## Step 1: Fitting the volatility surface to PCA
The volatility surface can be reduced to 3 principal components while maintaining a reasonable amount of explained variance. This is a well-known fact within PCA and curve-based trading, and lends itseful useful since the first 3 components have economical interprations. As per the surface at hand they easily reduce reduce to three components.
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/e6639ff9-4cc8-4bda-a0e8-6ed7199be7cd)
Assuming that the surface trades arbitrage-free and not accounting for liquidity it should be expected that the whole surface trades perfectly in-line with their respective curves. With that in mind from the PCs shown below they can be inverted back to each tenor/expiry. 
![historical_pc](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/9ac9e361-8e03-4b55-ab94-03aec4db9f2e)

## Step 2: Getting the fitted values and residuals
Comparing the fitted values to the actual give the residuals. The residuals are measuring the difference between trading in-line perfectly with the curve and where the current volatility is at. Therefore using a simple rolling z-score can identify which residuals have been too cheap or too rich. See below the residuals for the 1y1y ATM Swaption.
![residual_z_score](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/f4dea0df-e6d0-4fc5-9b7f-248c9375ca82)

## Step 3: Richness and Cheapness surface and considerations
Getting the ending z-score values and then plotting them back into a surface shows which shows the heatmap below. 
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/530c322b-e361-4eea-8a05-bf5b0b21bcbd)

# Deploying the model

## Streamlit deployment

## Streamlit Options
