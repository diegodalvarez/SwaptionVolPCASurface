# Not Intended as investment advice

# Required Packages
| Name         | Pacakage                                                                                                                        | File                                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Keras        | !![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)                   | All Files|

# Swaption Volatility Surface PCA
This model looks at reducing the dimensionality of an ATM Swaption Surface IV (which will be referred as IV Surface) via PCA. The overall goal of the model is to 
1. Fit the PCA model
2. Predic the values
3. Get the Residuals of that model
4. Calculate their z-score

# Considerations
A major consideration of this model which is why it is effective is that Currency swaptions are likely to have more symmetric smiles than equity options. Another way of thinking of this is that the implied distribution of currency options can be parametrized by fewer moments. Since PCA is looking to maximize variance (2nd moment) we can ensure that the distribution is being reduced accurately when using PCA. This is not always the case in equity markets since equity options tend to trade with skew, thus requiring a dimensionality reduction model that takes into account higher moments. Another consideration is htat although there is not skew within currency options there may be higher moments such as kurtosis. 

# Getting the surface
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/be34985f-279f-4278-8b88-ef69367236a4)
# Fitting the PCA model and analyzing the results
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/9a173701-a213-47d9-a43e-6ecd3ef2935a)
# Historical PCs
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/d5f7d1b4-07e6-456a-aa5e-99b68a51de5b)
# Getting the residuals and rolling z-scores
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/91cd5f37-c482-4eeb-b21d-f3546e6a51dd)
