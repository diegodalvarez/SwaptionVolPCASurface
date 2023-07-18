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
This model is the streamlit version of the Swaption PCA analysis for ATM Swaptions. The streamlit functionality is for downstream deployment and to seamlessly work on top of Bloomberg Terminal. The idea behind his model is built upon measuring the rolling z-scores of ATM Swaption Implied Volatilities for richness and cheapness. 

# Building and Deploying the model

## Streamlit deployment
```sh
# Git Install
git clone https://github.com/diegodalvarez/SwaptionVolPCASurface
```

```sh
# Then to run cd into the directory and use streamlit
cd root
streamlit run streamlit_frotend.py
```

# Landing Page
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/d4a496be-2b69-45f8-af48-3327a66de468)
The landing page shows four heatmaps. 

* The upper left shows the current Swaption Surface
* The upper right shows the spread between historical Swaption implied volatilty and its current value
* The bottom left shows the ratio between historical Swaption Implied volatility and its current value
* The bottom right shows the z-scores of the residuals when fitting the surface via PCA

# Historical Volatilities
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/b2cda33c-62b0-46de-b28d-a9c3409a8871)
Using the selectbar on the left you can select historical volatilities and view any from the tenor. 

# Historical Z-Scores
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/f7ed378e-f227-4307-b549-375ff50e91b5)
Using the selectbar on the left you can select historical z-scores to see which are trading rich or cheap

# Historical PCs
Using the selectbar on the left you can select historical PCs to see how the PCs have changed over time
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/bda5bf0e-9f46-43fa-9fed-c2f7d9d229e6)

* The upper left shows the explained variance per each PC
* The upper right shows the cumulative explained variance per each PC
* The bottom left shows the historical PCs
* The bottom right shows the historical PCs scaled by their explained variance

# Barchart Richness and Cheapness
![image](https://github.com/diegodalvarez/SwaptionVolPCASurface/assets/48641554/145d281c-86e5-4f55-a9d9-82a761a8e611)
Selecting Barch Chart Richness / Cheapness shows the current z-scores from the PCA model and aligns them from cheapest to richess. 
