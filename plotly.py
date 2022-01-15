# -*- coding: utf-8 -*-
"""plotly.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tPT4a7ZAQrmdGRdA7KOhwkvV6y0SB0Kh
"""

#! pip install plotly==5.5.0
#! pip install dash

import numpy as np
import pandas as pd
from datetime import datetime
import plotly.express as px

df = pd.read_csv('news1year.csv',encoding='utf-8')

def get_daily(title):
  #df = pd.read_csv('news1year.csv',encoding='utf-8')  
  # 找出 df 中含有給定標題的那幾列的列數
  # fubon_row = df['title'].str.contains(title)
  # 取出 df 中含有給定標題的那幾列
  df_fubon = df.loc[df['title'].str.contains(title)]
  # 將含有給定標題的文章依 date 分類
  df_fubon_date = df_fubon.groupby("date")
  # 將含有給定標題的文章依 date 分類的結果取出
  fubon_article = {
      'article_n': df_fubon_date.size()
  }
  fubon_article = pd.DataFrame(fubon_article).reset_index()
  # Mr. Chateau is so handsome
  fubon_article['date'] = pd.to_datetime(fubon_article['date'], format="%m/%d").dt.date
  fubon_article['date'] = fubon_article['date'].astype('str').str.replace('1900-', '')
  # 創造一年 365 天的數列
  date0 = pd.date_range('2021-01-01', periods = 365)
  date1 = date0.strftime("%Y-%m-%d").str.replace('2021-', '')  
  date = {
      'date': date1    
  }
  date = pd.DataFrame(date)
  # # 彙整出每日含有給定標題的文章篇數
  fubon_daily = pd.merge(date, fubon_article, on = 'date', how = 'left').sort_values(by = 'date')
  fubon_daily['article_n'] = fubon_daily['article_n'].fillna(0)
  fubon_daily['date'] = pd.to_datetime(fubon_daily['date'], format="%m-%d").dt.date
  for i in list(range(0, len(fubon_daily['date']))):
    fubon_daily['date'][i] = fubon_daily['date'][i].replace(year = 2021)
  return(fubon_daily)

#test = get_daily('王柏融|大王')

#dff = test.copy()
#wang = get_daily('王柏融')
#wu = get_daily('吳念庭')
#p = pd.merge(wang, wu, on = 'date', how = 'left')

#fig = px.line(p, x="date", y="article_n_x", name='Wang')
#fig = px.line()
#fig.add_scatter(x=wang['date'], y=wang['article_n'], name='Wang')
#fig.add_scatter(x=wu['date'], y=wu['article_n'], name='Wu') 

#fig.update_layout(title='2021 PTT Baseball Articles associated to Big Wang/Wu',
                   #xaxis_title='Date',
                   #yaxis_title='Article')

#fig.show()

#fig.write_html('first_figure.html', auto_open=True)

# How to run a Dash app in Google Colab

## Requirements

### Install ngrok
#!wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
#!unzip ngrok-stable-linux-amd64.zip

### Run ngrok to tunnel Dash app port 8050 to the outside world. 
### This command runs in the background.
#get_ipython().system_raw('./ngrok http 8050 &')

### Get the public URL where you can access the Dash app. Copy this URL.
#! curl -s http://localhost:4040/api/tunnels | python3 -c \
    #"import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"

# Commented out IPython magic to ensure Python compatibility.
# ## Dash app (https://dash.plot.ly/getting-started)
# 
# ### Save file with Dash app on the Google Colab machine
# %%writefile my_app1.py
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# 
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# 
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# 
# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),
# 
#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),
# 
#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
#     )
# ])
# 
# if __name__ == '__main__':
#     app.run_server(debug=True)
# 
# ### Run Dash app
# !python my_app1.py


#! pip install jupyter-dash -q
#! pip install dash-cytoscape -q

#from jupyter_dash import JupyterDash  # pip install dash
import dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import pandas as pd  # pip install pandas
import plotly.express as px
import math
from dash import no_update


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

  html.H1(
        children='2021 PTT Baseball Article Titles Analysis',
        style={
            'textAlign': 'center'
        }
    ),

    
    dcc.Input(
            id="input_keywords", type="text", placeholder="Please enter keyword(s):"
        ),

    html.Br(),

    html.Br(),

    #dcc.Input(id='username', value='Initial Value', type='text'),
    #html.Button(id='submit-button', type='button', children='Submit'),

    html.Br(),

    html.Div(id='output_container', children=[]),

    html.Br(),

    dcc.Graph(id = 'output_daily', figure={})                     

    #dcc.Graph(figure=fig)  

])


@app.callback(
    [
      Output(component_id = 'output_container', component_property = 'children'),
      Output(component_id = 'output_daily', component_property = 'figure')
        ],
    [
     #Input(component_id = 'submit-button', component_property = 'n_clicks'),
     Input(component_id = 'input_keywords', component_property = 'value')
     ],
    #[
     #State('input_keywords', 'value')
     #]
      )

#def update_output(clicks, keywords):
def update_output(keywords):
  #if clicks is not None:
    #print(clicks, keywords)
    container = 'You entered: {}'.format(keywords)
    
    data = get_daily(keywords)
    line_chart = px.line()
    line_chart.add_scatter(x=data['date'], y=data['article_n'])

    return container, line_chart

if __name__ == '__main__':
    app.run_server(debug=True)