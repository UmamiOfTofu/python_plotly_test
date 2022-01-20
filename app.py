import numpy as np
import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

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


instruction = ['請於時序圖左上角之文字格輸入欲搜尋的關鍵字', '若欲同時搜尋多個詞，請用 "|" 符號作為間隔，例如：富邦|悍將|邦邦', '若欲搜尋特定文章分類，請用 "\[" 及 "\]" 將其包住，例如：\[炸裂\]']

app.layout = html.Div([

  html.H1(
        children='2021 PTT Baseball 文章標題小分析',
        style={
            'textAlign': 'center'
        }
    ),

    
    html.Div(
        
        children=[
            html.Ul(id='list', children=[html.Li(i) for i in instruction])
        ]
    ),

    html.Hr(),

    
    dcc.Input(
            id="input_keywords", type="text", placeholder="請輸入關鍵字"
        ),

    html.Br(),

    html.Br(),

    #dcc.Input(id='username', value='Initial Value', type='text'),
    #html.Button(id='submit-button', type='button', children='Submit'),

    html.Br(),

    html.Div(id='output_container', children=[]),

    html.Br(),

    dcc.Graph(id = 'output_daily', figure={}),


    ####################################################

    html.Hr(),

    html.Br(),

    html.P('第一個關鍵字：'),
    dcc.Input(
            id="input_keywords_d_1", type="text", placeholder="請輸入關鍵字"
        ),
    
    html.Br(),
    
    html.P('第二個關鍵字：'),
    dcc.Input(
            id="input_keywords_d_2", type="text", placeholder="請輸入關鍵字"
        ),

    html.Br(),

    html.Br(),

    #dcc.Input(id='username', value='Initial Value', type='text'),
    #html.Button(id='submit-button', type='button', children='Submit'),

    #html.Br(),

    #html.Div(id='output_container_2', children=[]),

    html.Br(),

    dcc.Graph(id = 'output_daily_2', figure={})                     

      

])

"""
@app.callback(
    [
      Output(component_id = 'output_container', component_property = 'children'),
      Output(component_id = 'output_daily', component_property = 'figure')
        ],
    [
     #Input(component_id = 'submit-button', component_property = 'n_clicks'),
     Input(component_id = 'input_keywords', component_property = 'value')
     ]
      )

#def update_output(clicks, keywords):
def update_output(keywords):
  #if clicks is not None:
    #print(clicks, keywords)

    data = get_daily(keywords)
    container = '該關鍵字共有： {}'.format(data['article_n'].sum().item()) + ' 篇文章'
    
    
    line_chart = px.line()
    line_chart.add_scatter(x=data['date'], y=data['article_n'])
    line_chart.update_layout(title='2021 PTT Baseball 文章數互動時序圖',
                   xaxis_title='日期',
                   yaxis_title='文章數')
    

    return container, line_chart
"""

@app.callback(
    [  
     Output(component_id = 'output_daily_2', component_property = 'figure')
     ],
    [
     #Input(component_id = 'submit-button', component_property = 'n_clicks'),
     Input(component_id = 'input_keywords_d_1', component_property = 'value'),
     Input(component_id = 'input_keywords_d_2', component_property = 'value')
     ]
      )

#def update_output(clicks, keywords):
def update_output_2(keywords_d_1, keywords_d_2):
  #if clicks is not None:
    #print(clicks, keywords)    

    data_d_1 = get_daily(keywords_d_1)
    data_d_2 = get_daily(keywords_d_2)

    line_chart_2 = px.line()
    line_chart_2.add_scatter(x=data_d_1['date'], y=data_d_1['article_n'], name = '關鍵字1')
    line_chart_2.add_scatter(x=data_d_2['date'], y=data_d_2['article_n'], name = '關鍵字2')
    line_chart_2.update_layout(title='2021 PTT Baseball 文章數互動雙線時序圖',
                   xaxis_title='日期',
                   yaxis_title='文章數')

    return line_chart_2



if __name__ == '__main__':
    app.run_server(debug=True)