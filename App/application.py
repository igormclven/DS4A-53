#!/usr/bin/env python
# coding: utf-8

#Dependencias
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pickle
from googletrans import Translator
from dash.dependencies import Input, Output, State
import plotly.express as px


#Constantes

introduction = '''
We believe that a correct distribution of the income throughout  social investments will increase the quality live, so, how to make correct investments?, how to minimize risk in the cash flow of an investment?, how to assure that invoices will be paid?, how to plan how many projects start or how many investments we will be able to make?, how to assure the total development of a project and don’t leave projects at the middle of the timeline? and finally how to estimate the social impact based on the investments made?. All the risks that imply answering these questions can be minimized throughout accurate forecasting models.
'''

p1 ='''Rionegro’s Town recognizes and suffers from the fact  that sources of public resources are limited and the social needs tend to increase over time. Therefore, one of their aims is to predict incomes and then use this information to optimize the short and long term expenditure & investment planning and execution processes and thus solve the problem of planning and making investments without knowing what the actual income will be. An important source of this income is real estate. Project scope is limited to predict this specific income.'''

p2 = '''Our task was to built a machine learning model with the purpose of predicting Rionegro's incomes from the 
Property tax total, this is the property tax that anually levies the right of ownership or possession of a property
located in Colombia, the rate ranges between 0.3% and 3.3% over the property value, during this process of building the
model, we came up with the following three significant variables:Medellin's IPVU,occupancy rate and TRM change. '''

p3 = ''' The first relevent variable in our model was the used housing price indicator (IPVU), this macroeconomic indicator measures the quarterly and anual evolution of the prices of used housing 
, we decided to use Medellin's IPVU since Medellin is the city with most influency in Rionegro, therefore
 Medellin's IPVU is very correlated with the property tax Total as we can see in the line plot.'''

p4 = '''The second relevant variable was the employment rate in the seven Colombia's metropolitan areas at the end of
each year, this variable is the relationship between the employed population and the working-age population.
'''

p5 = ''' Our last relevant variable was TRM change, it refers to the representative exchange rate of the market at the
end of December of each year, in simpler terms it is the amount of Colombian pesos(COP) per one United States dollar(US) 

'''

#initialise the app
df = pd.read_csv("CSV_Files/2000_2020.csv")
model_df = pd.read_csv("CSV_Files/datos_modelo_front.csv")

#webScrapping
trm_change = pd.read_html('https://www.dolar-colombia.com/')[0]
us_t = trm_change.values[0,]
translator = Translator()
trans_trm = translator.translate(us_t[0])
trm_recomendation = "TRM change value for today " + str(trans_trm.text) + " is " + str(us_t[1])

#

app = dash.Dash()

#

@app.callback(
Output('dccDown','data'),
Input('csv_d','n_clicks'),
    prevent_initial_call = True
)
def down(n_clicks):
    model_df = pd.read_csv("CSV_Files/predictions.csv")
    to_download = model_df[['Año','cambio_trm','IPVU_nom_medellin','tasa_ocupacion_7a','recaudo']]
    
    return dcc.send_data_frame(to_download.to_csv, "CSV_Files/predictions.csv")
    

## Frontend ------------------------------------------------------------------------------------------

sidebar_section = html.Div([
    html.Div(children  = [
        
        html.Div(html.Img(src="assets/Logo.png",width="300",height="300"), className="text-center" ),
        html.Hr(),
        html.Div([
            html.P("For predictions please go to the Predictions Tab before pressing the button.", className="lead"),
            html.P("Please enter the following data:", className="lead"),
        ],className='p-3'),        

        html.Div(className='input-group p-3', children  = [
            dcc.Input(
                id="IPVU",
                type="number",
                placeholder="Medellin's IPVU",
                debounce = True,
                className='form-control'
            ),
        ]),
        html.Div(className='input-group px-3', children  = [
            dcc.Input(
                id="EmploymentRate",
                type="number",
                placeholder = "Occupancy rate",
                debounce = True,
                className='form-control'
            ),
        ]), 
        html.Div(className='input-group p-3', children  = [
            dcc.Input(
                id="TRMChange",
                type="number",
                placeholder = "TRM Change",
                className='form-control'    
            )
        ]),
        
        html.Div([
            html.Button('Predict', id='submit-val', className='btn btn-primary btn-lg'),
        ],className='p-3 text-center'),

    ], className="sidebar-wrapper bg-dark text-white px-3 active" ),  

], id='sidebar', className='active')

#container
container_section = html.Div(id='main', children=[
        html.Div([
            html.H3("Control Panel")
        ], className='page-heading'),
        
        html.Div(children = [
            
            dcc.Tabs(id='tabs', value='tab-1', className='py-3', children=[
                     
                # Tab1
                dcc.Tab(label='What is Rio Analytics?', value='tab-1',children=[
                    
                    html.Div(className='card',children = [
                        html.Div([
                            html.H3("Rionegro's Social Class Distribution"),
                        ], className='card-header text-center'),

                        html.Div([
                            dcc.Graph(
                                figure = px.histogram(df,x=['2000','2010','2020'],
                                labels={'value':'Social Class','variable':'Year','estrato_2000':'2000'}).add_annotation(
                                        text= 'Huge Concentration of people',x='0',y=20000,arrowhead=2,showarrow=True,arrowcolor='black')
                            ),
                            html.P(p1),
                            html.Img(src="assets/helping.png", className='mx-auto d-block p-3'),
                            html.P(introduction)
                        ], className='card-body'),
                    ])
                ]),

                #Tab 2
                dcc.Tab(label='Important Macroeconomic Indicators', value='tab-2',children=[
                    html.Div(className='card',children = [
                        html.Div([
                            html.H3("How to predict Rionegro's property tax total income?"),
                        ], className='card-header text-center'),

                        html.Div([
                            
                            html.Img(src="assets/bman.png", width='300', className='mx-auto d-block p-3'),
                            html.P(p2),
                            html.Hr(),
                            html.H3("Medellin's IPVU vs Property Tax Total",style={'textAlign': 'center'}),
                            dcc.Graph(
                                    figure= px.line(model_df,x='Año',y=['Property Tax Total',"Medellin's IPVU"],
                                    
                                    labels = {
                                            'value' : 'Normalized Data',
                                                'Año' : 'Year',
                                                'variable':"Variables"
                                },
                                template = 'plotly')
                            ),
                            html.P(p3),
                            html.Hr(),
                            html.H3("Occupancy rate vs Property Tax Total",style={'textAlign': 'center'}),
                            
                            dcc.Graph(
                                figure= px.line(model_df,x='Año',y=['Property Tax Total',"Tasa Ocupacion"],
                                labels = {
                                            'value' : 'Normalized Data',
                                                'Año' : 'Year',
                                                'variable':"Variables"

                                },
                                
                                template = 'plotly')
                            ),
                            
                            html.P(p4,style={'text-align':'center'}),
                            html.Hr(),
                            html.H3("TRM Change vs Property Tax Total",style={'textAlign': 'center'}),
                            
                            dcc.Graph(
                                
                                figure= px.line(model_df,x='Año',y=['Property Tax Total',"TRM Change"],

                                labels = {
                                            'value' : 'Normalized Data',
                                                'Año' : 'Year',
                                                'variable':"Variables"

                                },
                                
                                template = 'plotly')
                            ),
                            
                            html.P(p5,style={'text-align':'center'})

                        ], className='card-body'),


                    ]),

                ]),
                
                # Tab 3
                dcc.Tab(label='Rio Analytics team', value='tab-3',children=[

                    html.Div(className='row',children = [
                        html.Div(className='col',children = [
                            html.Div(className='card border-primary animate__animated animate__bounceIn',children = [
                                html.Img(src="assets/Andres-modified.png", className='mx-auto d-block p-3', width='300'),
                                html.Div([
                                    html.H4("Andres Caballero", className='card-title'),
                                    html.P("Industrial Engineer"),
                                    html.P("UMNG University"),
                                    html.P("Data Analyst at Seguros Bolivar"),

                                ],className='card-body text-center'),

                            ]),
                        ]),

                        html.Div(className='col',children = [
                            html.Div(className='card border-success animate__animated animate__bounceIn',children = [
                                html.Img(src="assets/Sara.png", className='mx-auto d-block p-3', width='300'),
                                html.Div([
                                    html.H4("Sara Gonzalez", className='card-title'),
                                    html.P("Statistician"),
                                    html.P("National University of Colombia"),
                                    html.P("Analytics model professional at Banco Popular"),

                                ],className='card-body text-center'),

                            ]),
                        ]),

                        html.Div(className='col',children = [
                            html.Div(className='card border-danger animate__animated animate__bounceIn',children = [

                                html.Img(src="assets/David-modified.png", className='mx-auto d-block p-3', width='300'),
                                html.Div([
                                    html.H4("David Arbelaez", className='card-title'),
                                    html.P("Adimnistrative Engineer"),
                                    html.P("EIA University"),
                                    html.P("Data Scientist at Rappi"),

                                ],className='card-body text-center'),

                            ]),
                        ]),
                    ]),

                    html.Div(className='row',children = [
                        html.Div(className='col',children = [
                            html.Div(className='card border-warning animate__animated animate__bounceIn',children = [
                                html.Img(src="assets/Oscar.png", className='mx-auto d-block p-3', width='300'),
                                html.Div([
                                    html.H4("Oscar Rodriguez", className='card-title'),
                                    html.P("Computer Scientist student"),
                                    html.P("National University of Colombia"),

                                ],className='card-body text-center')

                            ]),
                        ]),

                        html.Div(className='col',children = [
                            html.Div(className='card border-info animate__animated animate__bounceIn',children = [
                                html.Img(src="assets/Oscar.png", className='mx-auto d-block p-3', width='300'),
                                html.Div([
                                    html.H4("Mauricio Alvarado", className='card-title'),
                                    html.P("Systems Engineer"),
                                    html.P("District University"),
                                    html.P("Web Developer"),

                                ],className='card-body text-center'),

                            ]),
                        ]),

                    ]),                                
                ]),
                
                #Tab 4
                dcc.Tab(id='predictionsTab',label='Predictions',value="tab-4", children=[


                    html.Div(className='card',children = [
                        html.Div([
                            html.H4(trm_recomendation),
                            html.Div(id='predictedValue',children=[

                            ]),   
                        ], className='card-header text-center'),

                        html.Div([
                            dcc.Graph(id='taxPrediction',
                            
                            figure= px.line(model_df,x='Año',y='recaudo',
                            labels = {'Año' : 'Year',
                                    'recaudo':'Property Tax Total' },
                                    
                            template = 'plotly')
                        ),
                        html.Div([
                            html.Button("Download CSV file with predicted files",id="csv_d",className='btn btn-primary btn-lg'),
                            dcc.Download(id="dccDown")
                        ],className='p-3 text-center'),
                    
                        ], className='card-body'),
                    ])
                ])
            ])
                                                

        ], className='page-content')
    ])


## Main

app.layout = html.Div([
    sidebar_section,
    container_section,
], id='app')

# -----------------------------------------------------------------------------

    
@app.callback(
    [Output('taxPrediction','figure'),Output('predictedValue','children')],
    [Input('submit-val','n_clicks')],
    [State('IPVU','value'),State('EmploymentRate','value'),State('TRMChange','value')])
def update_children(n, ipvu, er,tc):
    
    model = pickle.load(open('finalized_model.sav', 'rb'))
      
    model_df = pd.read_csv("CSV_Files/predictions.csv")
    
    
    plot_data = model_df[['Año','cambio_trm','IPVU_nom_medellin','tasa_ocupacion_7a','recaudo']]
    next_year = (plot_data['Año'].values[-1]) + 1
    
    data = {
        'Año':[next_year],
        'cambio_trm':[float(tc)],
        'IPVU_nom_medellin':[float(ipvu)],
        'tasa_ocupacion_7a':[float(er)],
        
        
    }
    
    df = pd.DataFrame(data)
    prediction =  float(model.predict(df) *1000000000)
        
    data_aux = {
        'Año':[next_year],
        'cambio_trm':[float(tc)],
        'IPVU_nom_medellin':[float(ipvu)],
        'tasa_ocupacion_7a':[float(er)],
        'recaudo':[float(prediction)]
       
    }
    
   
    
    
   
    df_aux = pd.DataFrame(data_aux)
    
    
    
    
    predictions_df = pd.concat([plot_data,df_aux])
    model_df = pd.concat([model_df,df_aux])
    
    saving_df = model_df.to_csv('CSV_Files/predictions.csv')
    
    
    
    figure= px.line(predictions_df,x='Año',y='recaudo',
            labels ={'Año' : 'Year'},template = 'plotly').update_layout(
                        {'plot_bgcolor':'rgba(0,0,0,0)',
                        'paper_bgcolor':'rgba(0,0,0,0)'}
                            ).add_annotation(text= 'Your prediction for '+str(next_year),x=next_year,y=prediction,arrowhead=3,showarrow=True,arrowcolor='white')
    
    pred = html.H4("The predicted value for "+str(next_year)+" is " + str(int(prediction//1000000000)) +"$" +" COP billions")
                             
    return figure,pred



# Ejecucion
if __name__ == '__main__':
    app.run_server(debug=True)
    
#

df = pd.read_csv("CSV_Files/predictions.csv")
n = abs(21-len(df))
years_to_delete = []
for i in range(0,n):
    years_to_delete.append(20+(i+1))

df.drop(labels=years_to_delete,axis=0,inplace = True)
x = model_df.to_csv('CSV_Files/predictions.csv') 





