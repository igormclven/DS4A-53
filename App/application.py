#!/usr/bin/env python
# coding: utf-8

#Dependencias
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pickle4 as pickle
from googletrans import Translator
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc


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

app = dash.Dash(__name__)

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
    

#Frontend
app.layout = html.Div(style={'textAlign':'center'},children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls',children=[
                                           # Define the left element
                                      
                                      
                                       html.Div(html.Img(src="assets/Logo.png",width="300",height="300") ),
                                        html.P("For predictions please go to the Predictions Tab before pressing the button." ,style={'font-family':'Franklin Gothic Medium'}),
                                        html.P("Please enter the following data: ",style={'font-family':'Franklin Gothic Medium'}),
                                      
                                      html.Div(className='Inputs',
                                              children  = [
                                                   dcc.Input(
                                                id="IPVU",
                                                type="number",
                                                placeholder="Medellin's IPVU",
                                              style={'backgroundColor': 'rgb(50, 50, 50)',
                                                      'font_family':'sans-serif'},
                                                debounce = True
                                                
                                                   ),
                                            
                                                  
                                                  dcc.Input(
                                                  
                                                  id="EmploymentRate",
                                                      type="number",
                                                      placeholder = "Occupancy rate",
                                                    style={
                                                          'backgroundColor': 'rgb(50, 50, 50)',
                                                        'font_family':'sans-serif'
                                                          },                                             
                                                    debounce = True
                                                      
                                                  ),
                                                  
                                                  dcc.Input(
                                                  
                                                  id="TRMChange",
                                                      type="number",
                                                      placeholder = "TRM Change",
                                                      style={'backgroundColor': 'rgb(50, 50, 50)'},
                                                  
                                                  
                                                  )
                                                  
                                                  
                                              ]),
                                      
                                      html.Br(),
                                      html.Button('Predict', id='submit-val', style={'color':'white'},n_clicks=0),

    
                                        
                                      
                                      
                                  ]),

                                   
                                      
                                  html.Div(className='eight columns div-for-charts bg-grey',style={'overflowY': 'scroll', 'height': 650} ,children = [
                                      
                                      
                                      dcc.Tabs(id='tabs', value='tab-1', children=[
                                          
                                          #First Tab 
                                          
                                                dcc.Tab(label='What is Rio Analytics?', value='tab-1', style={'backgroundColor': 'rgb(50, 50, 50)','font-family':'Franklin Gothic Medium'},children=[
                                                    
                                                    
                                                     html.Div(style={'textAlign': 'center',
                                                                        'font-family':'Georgia'},children = [
                                                        html.H3("Rionegro's Social Class Distribution",style={'font-family':'Georgia'}),
                                                        html.Br(),
                                                       dcc.Graph(
                                                       
                                                       
                                                       figure = px.histogram(df,x=['2000','2010','2020'],
                                                                labels={'value':'Social Class','variable':'Year','estrato_2000':'2000'}).update_layout(
                                                       {'font_color':'white','plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'}
                                                       
                                                           ).add_annotation(
                                                       
                                                       text= 'Huge Concentration of people',x='0',y=20000,arrowhead=2,showarrow=True,arrowcolor='white')
                                                           
            
                                                       
                                                       ),
                                                        html.Br(),
                                                        html.P(p1,style={'font-family':'Franklin Gothic Medium'}),
                                                         
                                                        html.Img(src="assets/helping.png"),
                                                        html.Br(),
                                                        html.P(introduction,style={'font-family':'Franklin Gothic Medium'})
         
#
            
                                                        ])
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                       #End first Tab         
                                                ]),
                                                dcc.Tab(label='Important Macroeconomic Indicators', value='tab-2', style={'backgroundColor': 'rgb(50, 50, 50)','font-family':'Franklin Gothic Medium'},children=[
                                                   html.H3("How to predict Rionegro's property tax total income?",style={'font-family':'Georgia','textAlign': 'center'}),
                                                   html.Br(),
                                                   html.Img(src="assets/bman.png",height=300,width=300),
                                                   html.Br(),
                                                   html.P(p2,style={'font-family':'Franklin Gothic Medium','text-align':'center'}),
                                                   html.Br(),
                                                    html.H3("Medellin's IPVU vs Property Tax Total",style={'font-family':'Georgia','textAlign': 'center'}),
                                                   dcc.Graph(
                                                    
                                                        
                                                       figure= px.line(model_df,x='Año',y=['Property Tax Total',"Medellin's IPVU"],
              
                                                                  labels = {
                                                                               'value' : 'Normalized Data',
                                                                                'Año' : 'Year',
                                                                                'variable':"Variables"
                  
                                                                          },
        
                                                               
                                                               
                                                                       template = 'plotly_dark').update_layout(
                                                            
                                                                    {'plot_bgcolor':'rgba(0,0,0,0)',
                                                                    
                                                                        'paper_bgcolor':'rgba(0,0,0,0)'}
                                                        
                                                        
                                                        )
            
                                                    
                                                    
                                                    
                                                    ),
                                                    html.Br(),
                                                    
                                                    html.P(p3,style={'font-family':'Franklin Gothic Medium','text-align':'center'}),
                                                    
                                                    html.Br(),
                                                    
                                                    
                                                    html.H3("Occupancy rate vs Property Tax Total",style={'font-family':'Georgia','textAlign': 'center'}),
                                                    
                                                    
                                                    dcc.Graph(
                                
                                                    
                                                    
                                                figure= px.line(model_df,x='Año',y=['Property Tax Total',"Tasa Ocupacion"],
              
                                                                  labels = {
                                                                               'value' : 'Normalized Data',
                                                                                'Año' : 'Year',
                                                                                'variable':"Variables"
                  
                                                                          },
              
              

                                                               
                                                               
                                                                       template = 'plotly_dark').update_layout(
                                                            
                                                                    {'plot_bgcolor':'rgba(0,0,0,0)',
                                                                    
                                                                        'paper_bgcolor':'rgba(0,0,0,0)'}
                                                        
                                                        
                                                        )
        
                                                    
                                                    
                                                    ),
                                            html.Br(),
                                                    
                                            html.P(p4,style={'font-family':'Franklin Gothic Medium','text-align':'center'}),
                                                    
                                            html.Br(),
                                            html.H3("TRM Change vs Property Tax Total",style={'font-family':'Georgia','textAlign': 'center'}),
                                                    
                                            dcc.Graph(
                                                    
                                                    
                                                    
                                                    
                                                figure= px.line(model_df,x='Año',y=['Property Tax Total',"TRM Change"],
              
                                                                  labels = {
                                                                               'value' : 'Normalized Data',
                                                                                'Año' : 'Year',
                                                                                'variable':"Variables"
                  
                                                                          },
              
              
        
                                                               
                                                               
                                                                       template = 'plotly_dark').update_layout(
                                                            
                                                                    {'plot_bgcolor':'rgba(0,0,0,0)',
                                                                    
                                                                        'paper_bgcolor':'rgba(0,0,0,0)'}
                                                        
                                                        
                                                        )
        
                                                    
                                                    
                                                    ),
                                                    
                                                html.Br(),
                                                html.P(p5,style={'font-family':'Franklin Gothic Medium','text-align':'center'})

                                                    
                                                    
                                                    
                                                    
                                                    
                                                ]),
                                                dcc.Tab(label='Rio Analytics team', value='tab-3', style={'backgroundColor': 'rgb(50, 50, 50)','font-family':'Franklin Gothic Medium'},children=[
                                                    
                                                    
                            
                                                
                                                    
                                                html.Br(),
                                                html.H3("Andres Caballero",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.Img(src = "assets/Andres-modified.png",style={'height':300,'width':300}),
                                                html.P("Industrial Engineer",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.P("UMNG University",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.P("Data Analyst at Seguros Bolivar",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.Br(),
                                                html.Br(),
                                                    
                                                html.Br(),
                                                html.H3("Sara Gonzalez",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.Img(src = "assets/Sara.png",style={'height':300,'width':300}),
                                                html.P("Statistician",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.P("National University of Colombia",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.P("Analytics model professional at Banco Popular",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.Br(),
                                                html.Br(),
                                                    
                                                html.Br(),
                                                html.H3("David Arbelaez",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.Img(src = "assets/David-modified.png",style={'height':300,'width':300}),
                                                html.P("Adimnistrative Engineer",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.P("EIA University",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.P("Data Scientist at Rappi",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.Br(),
                                                html.Br(),
                                                    
                                                html.Br(),
                                                html.H3("Oscar Rodriguez",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.Img(src = "assets/Oscar.png",style={'height':300,'width':300}),
                                                html.P("Computer Scientist student",style={'font-family':'Georgia','textAlign': 'center'}),
                                                html.P("National University of Colombia",style={'font-family':'Georgia','textAlign': 'center'})
                                                
                                                
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                ]),
                                                dcc.Tab(id='predictionsTab',label='Predictions',value="tab-4",style={'background':'rgb(50,50,50)','font-familiy':'Franklin Gothic Medium'},
                                                        children=[
                                                    
                                            
                                        html.H4(trm_recomendation,style={'font-family':'Franklin Gothic Medium','text-align':'center'}),        
                                                        
                                        html.Div(id='predictedValue',style={'font-family':'Franklin Gothic Medium','text-align':'center'},children=[
                                            
                                        
                                            
                                            
                                            
                                        ]),          
                                             
                                           dcc.Graph(id='taxPrediction',
                                                    
                                                figure= px.line(model_df,x='Año',y='recaudo',
              
                                                                  labels = {'Año' : 'Year',
                                                                             'recaudo':'Property Tax Total' },
                                                                            

                                                               
                                                                       template = 'plotly_dark').update_layout(
                                                            
                                                                    {'plot_bgcolor':'rgba(0,0,0,0)',
                                                                    
                                                                        'paper_bgcolor':'rgba(0,0,0,0)'}
                                                        
                                                        
                                                        )
        
                                                    
                                                    
                                                    ),
                                                        
                                            html.Button("Download CSV file with predicted files",id="csv_d",style={'color':'white'}),
                                            dcc.Download(id="dccDown")
                                                    
                                                
                                                    
                                                    
                                                    
                                                    
                                                ])
                                      
                                                                                        ])
                                                
                                                 



                                ])


])


                                                          
                                                                                     
    
])


    
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
            labels ={'Año' : 'Year'},template = 'plotly_dark').update_layout(
                        {'plot_bgcolor':'rgba(0,0,0,0)',
                        'paper_bgcolor':'rgba(0,0,0,0)'}
                            ).add_annotation(text= 'Your prediction for '+str(next_year),x=next_year,y=prediction,arrowhead=3,showarrow=True,arrowcolor='white')
    
    pred = html.H4("The predicted value for "+str(next_year)+" is " + str(int(prediction//1000000000)) +"$" +" COP billions")
                             
    return figure,pred



# Ejecucion
if __name__ == '__main__':
    app.run_server()
    
#

df = pd.read_csv("CSV_Files/predictions.csv")
n = abs(21-len(df))
years_to_delete = []
for i in range(0,n):
    years_to_delete.append(20+(i+1))

df.drop(labels=years_to_delete,axis=0,inplace = True)
x = model_df.to_csv('CSV_Files/predictions.csv') 





