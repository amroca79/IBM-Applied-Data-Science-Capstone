import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


spacex_df = pd.read_csv(r'C:\Users\Deadend\DS_Projects\IBM-Applied-Data-Science-Capstone\spacex_launch_dash.csv')

success_rate = spacex_df.groupby(['Launch Site'])['class'].value_counts().reset_index(name='count')
success_rate
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

mark_values={0:'0kg',1000:'1000kg',2000:'2000kg',3000:'3000kg',4000:'4000kg',5000:'5000kg',6000:'6000kg',7000:'7000kg',8000:'8000kg',9000:'9000kg',10000:'10000kg'}

payload_rate = spacex_df[['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version Category']].sort_values(by=['Launch Site', 'Payload Mass (kg)', 'Booster Version Category'], ascending=True).reset_index(drop=True)

app = dash.Dash(__name__)


app.layout = html.Div([html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign':'center','color':'blue','font-size':40})]),
                       
                       html.Div([dcc.Dropdown(id='site_dropdown',options=[{'label':'All Sites','value':'All'},{'label':'CCAFS LC-40','value':'CCAFS LC-40'},{'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},{'label':'KSC LC-39A','value':'KSC LC-39A'},{'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}],value='All', placeholder="All" ,searchable=True)]),
                       html.Br(),
                       
                       html.Div([dcc.Graph(id='success-pie-chart', figure={})]),
                       html.Br(),
                       
                       html.P("Payload range (Kg):"),
                       html.Div([dcc.RangeSlider(id='payload_slider',min=0, max=10000, step=1000,value=[min_payload , max_payload],marks=mark_values)],style={'width':'98%','position':'relative','left':'1%'}),
                       html.Br(),
                       
                       html.Div([dcc.Graph(id='success-payload-scatter-chart',figure={})])
                       ])


@app.callback(Output(component_id='success-pie-chart',component_property='figure'),Input(component_id='site_dropdown',component_property='value'))

def get_pie_chart(site_dropdown):
    
    df_copy = success_rate
    all_sites = df_copy[df_copy['class']==1]
    launch_site = df_copy[df_copy['Launch Site']==str(site_dropdown)]
    
    if site_dropdown == 'All':
        fig = px.pie(all_sites, values='count', names='Launch Site')
        return(fig)
    else:
       fig = px.pie(launch_site, values='count', names='class')
       return(fig)
   
   

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),[Input(component_id='payload_slider',component_property='value'),Input(component_id='site_dropdown',component_property='value')])

def get_scatter(payload_slider, site_dropdown):
    
    df_copy = payload_rate
    all_sites = df_copy[df_copy['Payload Mass (kg)'].between(int(payload_slider[0]), int(payload_slider[1]))]
    launch_site = df_copy[(df_copy['Launch Site'] == str(site_dropdown)) & (df_copy['Payload Mass (kg)'].between(int(payload_slider[0]), int(payload_slider[1])))]
    
    if site_dropdown == 'All':
        fig = px.scatter(all_sites, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return(fig)
    else:
        fig = px.scatter(launch_site, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return(fig)
    

if __name__ == '__main__':
    app.run_server(port=8050, debug=True)