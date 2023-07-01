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
Assuming that the surface trades arbitrage free and not accounting for liquidity it should be expected that the whole surface trades perfectly in-line with the curve.

## Step 2: Getting the fitted values and residuals

## Step 3: Finding the rolling z-scores

# Deploying the model

## Streamlit deployment

## Streamlit Options
