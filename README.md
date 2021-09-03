
 # Welcome to Rio Analytics Team 53 DS4A



<p align="center">
<img src="./Images/Rio%20Analytics-logos_black.png" width="500" height="500" class="center">
 </p>
 
 <p align="center">
Rionegro’s Town (one of Antioquia's department municipalities) recognizes and suffers from the fact  that sources of public resources are limited and the social needs tend to increase over time. Therefore, one of their aims is to predict incomes and then use this information to optimize the short and long term expenditure & investment planning and execution processes and thus solve the problem of planning and making investments without knowing what the actual income will be. An important source of this income is real estate. Project scope is limited to predict this specific income
 </p>




# 1. Exploratory Data Analisis (EDA)

<p align="center">
<img src="Images/EDA_Icon.png" class="center">
 </p><br/>


This is the link to the EDA folder in which we have all the jupyter notebooks corresponding to each EDA developed -> [EDA Folder](./EDA)

# 2. External Data

<p align="center">
<img src="Images/extrac_data.png" class="center">
 </p>


These are the links refrerring to the pages where we extract external data for building our model:
 - TRM rate -> [TRM](https://www.banrep.gov.co/es/estadisticas/trm)
 - Nominal IPVU Medellin -> [IPVU](https://www.banrep.gov.co/es/estadisticas/indice-precios-vivienda-usada-ipvu)
 - Seven Colombian metropolitan areas Occupancy rate -> [Occupancy rate](https://www.banrep.gov.co/es/estadisticas/tasas-ocupacion-y-desempleo)

# 3. How the model was built?

<p align="center">
<img src="Images/machine-learning.png" width=400 height=400 class="center">
 </p>

 Here you can find two R scripts: one R script with three time series for predicting TRM rate, nominal IPVU Medellin and seven Colombian metropolitan areas Occupancy rate and a final R script for the modeling; However we also have python files with: the model and clusterization using k-means model for a future version of the model.
  - Python model -> [Python file model](./Model/Model.py)
  - K-means model -> [Jupyter Notebook K-means](./Model/Cluster%20predial.ipynb)
  - Time Series for TRM rate, Nominal IPVU Medellin and Occupancy Rate ->  [R script Time Series](./Model/codigo%20series%20de%20tiempo.R)
  - R model -> [R file model](./Model/Código_modelamiento.R)

# 4. DataBases (CSV Files and XSLX Files)

<p align="center">
<img src="Images/databases.png" width=300 height=300 class="center">
 </p>
 
 Here you can find all the data we used to built the model.
 - Data used for building time series (each sheet is for each variable) -> [Time Series Data](./DataBases%20(CSV%20Files)/series%20pronóticos.xlsx)
 - Data about TRM Change (important variable in the model) took from Banco de la Republic page -> [TRM Change Data](./DataBases%20(CSV%20Files)/pronosticos_analisis_BR.xlsx)
 - More Data from Banco de la Republic used in the model -> [Additional Data](./DataBases%20(CSV%20Files)/Series_Variables_modelo_BR.xlsx)

# 5. Datafolio

 <p align="center">
<img src="Images/Datafolio-1.png" class="center">
 </p>



# 6. Final report

 <p align="center">
<img src="Images/report.png" width=300 height=300 class="center">
 </p>
 
 Here you can find our conclusions about the project, it is included how the model was built step by step and some other analisis about other variables -> 
 [Final Report](./FinalReport/FinalReport.pdf) 
 
 # 7. Rio Analytics members
  - Andres Caballero -> [Linkedin](https://www.linkedin.com/in/andres-caballero)
  - Sara Gonzalez 
  - Oscar Rodriguez -> [Linkedin](www.linkedin.com/in/oscar-julian-rodriguez-cardenas-5b2b721bb)
  - Mauricio Alvarado -> [Linkedin](https://www.linkedin.com/in/mauriciora/)
  - David Arbelaez -> [Linkedin](http://www.linkedin.com/in/david-arbelaez-2aab30a7)
 









