import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


spacex_df = pd.read_csv(r'C:\Users\Deadend\DS_Projects\IBM-Applied-Data-Science-Capstone\spacex_launch_dash.csv')

max_payload = spacex_df['PayloadMass'].max()
min_payload = spacex_df['PayloadMass'].min()

mark_values={0:'0kg',1000:'1000kg',2000:'2000kg',3000:'3000kg',4000:'4000kg',5000:'5000kg',6000:'6000kg',7000:'7000kg',8000:'8000kg',9000:'9000kg',10000:'10000kg',11000:'11000kg',12000:'12000kg',13000:'13000kg',14000:'14000kg',15000:'15000kg',16000:'16000kg'}

app = dash.Dash(__name__)


app.layout = html.Div([html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign':'center','color':'blue','font-size':40})]),
                       
                       html.Div([dcc.Dropdown(id='site_dropdown',options=[{'label':'All Sites','value':'All'},{'label':'CCSFS SLC 40', 'value':'CCSFS SLC 40'},{'label':'KSC LC 39A','value':'KSC LC 39A'},{'label':'VAFB SLC 4E','value':'VAFB SLC 4E'}],value='All', placeholder="All" ,searchable=True)]),
                       html.Br(),
                       
                       html.Div([dcc.Graph(id='success-pie-chart', figure={})]),
                       html.Br(),
                       
                       html.P("Payload range (Kg):"),
                       html.Div([dcc.RangeSlider(id='payload_slider',min=0, max=16000, step=1000,value=[min_payload , max_payload],marks=mark_values)],style={'width':'98%','position':'relative','left':'1%'}),
                       html.Br(),
                       
                       html.Div([dcc.Graph(id='success-payload-scatter-chart',figure={})])
                       ])


@app.callback(Output(component_id='success-pie-chart',component_property='figure'),Input(component_id='site_dropdown',component_property='value'))

def get_pie_chart(site_dropdown):
    
    df_copy = spacex_df
    success_rate = df_copy.groupby(['LaunchSite'])['Class'].value_counts().reset_index(name='Count')
    all_sites = success_rate[success_rate['Class']==1]
    launch_site = success_rate[success_rate['LaunchSite']==str(site_dropdown)]
    
    if site_dropdown == 'All':
        fig = px.pie(all_sites, values='Count', names='LaunchSite')
        fig.update_traces(textinfo='value')
        return(fig)
    else:
       fig1 = px.pie(launch_site, values='Count', names='Class')
       fig1.update_traces(textinfo='value')
       return(fig1)
   
   

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),[Input(component_id='payload_slider',component_property='value'),Input(component_id='site_dropdown',component_property='value')])

def get_scatter(payload_slider, site_dropdown):
    
    df_copy = spacex_df

    cluster_count = df_copy.groupby(['Block_Version','Class'])['PayloadMass'].value_counts().reset_index(name='Count')
    cluster_count2 = df_copy.groupby(['LaunchSite','Class','Block_Version'])['PayloadMass'].value_counts().reset_index(name='Count')
    
    all_sites = cluster_count[cluster_count['PayloadMass'].between(int(payload_slider[0]), int(payload_slider[1]))]
    launch_site = cluster_count2[(cluster_count2['LaunchSite'] == str(site_dropdown)) & (df_copy['PayloadMass'].between(int(payload_slider[0]), int(payload_slider[1])))]
    
    if site_dropdown == 'All':
        fig = px.scatter(all_sites, x='PayloadMass', y='Class', color='Block_Version', hover_data=['Block_Version','PayloadMass','Count'])
        return(fig)
    else:
        fig = px.scatter(launch_site, x='PayloadMass', y='Class', color='Block_Version', hover_data=['Block_Version','PayloadMass','Count'])
        return(fig)
    

if __name__ == '__main__':
    app.run_server(port=8050, debug=True)