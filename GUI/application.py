# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24

@author: kchen
"""
#import os
import pandas as pds
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
import dash_auth
import plotly.graph_objs as go
import plotly.figure_factory as ff


VALID_USERNAME_PASSWORD_PAIRS = [
    ['ccar', 'summary']
]

app = dash.Dash(__name__,static_file='assets')

application = app.server
app.config['suppress_callback_exceptions']=True

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

filename = 'FED_Disclosure_Tables_Corp_Cards.xlsx'

def read_table ():
    table_20 = pds.read_excel(filename, sheet_name = 'Corp', encoding = 'utf-8')
    table_20_t = table_20.melt(id_vars=['Category', 'Variable'])
    table_20_t.rename(columns = {'variable': 'result_cat', 'value': 'percentage'}, inplace = True)
    
    table_26 = pds.read_excel(filename, sheet_name = 'Card',encoding = 'utf-8')
    table_26_t = table_26.melt(id_vars=['Category', 'Variable'])
    table_26_t.rename(columns = {'variable': 'result_cat', 'value': 'percentage'}, inplace = True)
    
    table_26_t['Variable'] = [str(i) for i in table_26_t['Variable'].tolist()]
    
    return table_20_t, table_26_t, table_20, table_26

corp_data_t, card_data_t, corp_data, card_data = read_table()

def corp (table_20_t, table_20,  grade, fi, sec, cat):
    if grade == 'ig':
        if fi == 'fi':
            if sec == 'sec': x = 'IG_FIN_S'
            else: x = 'IG_FIN_US'
        else:
            if sec == 'sec': x = 'IG_NFIN_S'
            else: x = 'IG_NFIN_US'
    else:
        if fi == 'fi':
            if sec == 'sec': x = 'NIG_FIN_S'
            else: x = 'NIG_FIN_US'
        else:
            if sec == 'sec': x = 'NIG_NFIN_S'
            else: x = 'NIG_NFIN_US'
    
    if cat == 'ft': y = 'Facility_type'
    elif cat == 'rate': y = 'Rating'
    elif cat == 'lien': y = 'Lien_position' 
    elif cat == 'ir': y = 'IR_variability'
    elif cat == 'ind': y = 'Industry'
    elif cat == 'guarantor': y = 'Guarantor_flag'
    elif cat == 'oth': y = 'Other'
    else: y = 'Loss_Rate'  
  
    x_ax = table_20_t[(table_20_t.result_cat == x) & (table_20_t.Category == y)].Variable
    y_ax = table_20_t[(table_20_t.result_cat == x) & (table_20_t.Category == y)].percentage
    
    fig1 = go.Figure()
    
    fig1.add_bar(x=x_ax, y=y_ax, marker = {'color': '#C4C4CD'}, name = 'Dist')
   
    fig1['layout'].update(margin={'t':0})
    fig1['layout'].update({
        'plot_bgcolor':'rgba(0,0,0,0)',
        'paper_bgcolor':'rgba(0,0,0,0)',
        'showlegend':False
        })
    fig1['layout']['yaxis1'].update(title='Pct (%)')
    fig1['layout']['xaxis1'].update(title='Risk Category')
     
    fig1.layout.template = 'plotly_dark'
    
    colorscale = [[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']]
    fig2 = ff.create_table(table_20[['Category', 'Variable', x]][table_20.Category == y],  colorscale=colorscale)
    
    return fig1, fig2



def card (table_26_t, table_26,  score, cat):
    x = score
    
    if cat == 'Credit card type': y = 'Credit card type'
    elif cat == 'Current credit limit': y = 'Current credit limit'
    elif cat == 'Days past due': y = 'Days past due' 
    elif cat == 'Product type': y = 'Product type'
    elif cat == 'Month-end account status': y = 'Month-end account status'
    elif cat == 'Account origination year': y = 'Account origination year'
    elif cat == 'Month-end close status': y = 'Month-end close status'
    elif cat == 'Cycle ending balance': y = 'Cycle ending balance'
    elif cat == 'Income at origination': y = 'Income at origination'
    elif cat == 'Original credit limit': y = 'Original credit limit'
    elif cat == 'Interest rate at cycle end': y = 'Interest rate at cycle end'
    else: y = 'Loss_Rate'
  
    x_ax = table_26_t[(table_26_t.result_cat == x) & (table_26_t.Category == y)].Variable
    y_ax = table_26_t[(table_26_t.result_cat == x) & (table_26_t.Category == y)].percentage
    
    fig1 = go.Figure()
    
    fig1.add_bar(x=x_ax, y=y_ax, marker = {'color': '#C4C4CD'}, name = 'Dist')
   
    fig1['layout'].update(margin={'t':0})
    fig1['layout'].update({
        'plot_bgcolor':'rgba(0,0,0,0)',
        'paper_bgcolor':'rgba(0,0,0,0)',
        'showlegend':False
        })
    fig1['layout']['yaxis1'].update(title='Pct (%)')
    fig1['layout']['xaxis1'].update(title='Risk Category')
     
    fig1.layout.template = 'plotly_dark'
    
    colorscale = [[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']]
    fig2 = ff.create_table(table_26[['Category', 'Variable', x]][table_26.Category == y], colorscale=colorscale)
    
    return fig1, fig2
    

"""
------------------------------------------------------------------------------------------------------------------------------------
page1 layouts
"""

page_1 = html.Div([
                   #------------------------------
                   # left panel with inputs
                   #------------------------------ 
                   html.Div(
                            className='three columns',
                            
                            children=[
                                    html.Div(children=[
                                                        html.H5('Risk Dimensions')
                                                      ],style={'border-bottom':'6px solid #FFE600', 'padding-top':20}
                                            ),
                                
                                    html.Div(children=[
                                                        html.H6('Risk Ratings:',style={'vertical-align':'top', 'padding-top':15}),
                                                        dcc.Dropdown(
                                                                    id='rating',
                                                                    options=[
                                                                            {'label':'Investment Grade', 'value':'ig'},
                                                                            {'label':'Non-investment Grade', 'value':'nig'}
                                                                            ],
                                                                    value = 'ig'
                                                                    )
                                                    ],
                                            ),
                                
                                    html.Div(children=[
                                                        html.H6('Sector:',style={'vertical-align':'top', 'padding-top':15}),
                                                        dcc.Dropdown(
                                                                    id='sector',
                                                                    options=[
                                                                            {'label':'Financial Sector', 'value':'fi'},
                                                                            {'label':'Non-financial Sector', 'value':'nfi'}
                                                                            ],
                                                                    value='fi'
                                                                    )
                                                      ]
                                            ),
                                
                                    html.Div(children=[
                                                        html.H6('Collateral:',style={'vertical-align':'top', 'padding-top':15}),
                                                        dcc.Dropdown(
                                                                    id='collateral',
                                                                    options=[
                                                                            {'label':'Secured', 'value':'sec'},
                                                                            {'label':'Unsecured', 'value':'unsec'}
                                                                            ],
                                                                    value='sec'
                                                                    )                                
                                                     ]
                                            ),
                                                        
                                    html.Div(children=[
                                                        html.H5('Risk Characteristics and Loss Rate')
                                                      ],style={'border-bottom':'6px solid #FFB46A', 'padding-top':20}
                                            ),
                                                        
                                    html.Div(children=[dcc.RadioItems(
                                                                        id = 'output1',
                                                                        options=[
                                                                                {'label': 'Facility Type', 'value': 'ft'},
                                                                                {'label': 'Rating', 'value': 'rate'},
                                                                                {'label': 'Lien Position', 'value': 'lien'},
                                                                                {'label': 'Interest Rate', 'value': 'ir'},
                                                                                {'label': 'Industry', 'value': 'ind'},
                                                                                {'label': 'Guarantor', 'value': 'guarantor'},
                                                                                {'label': 'Other', 'value': 'oth'},
                                                                                {'label': 'Loss Rate', 'value': 'lr'}
                                                                                ],
                                                                        value='ft',
                                                                        labelStyle ={'color': 'white'}
                                                                      )                                
                                                     ], style = {'padding-top': 15}
                                            )
                                    ]
                                ),
                                    
                                   
    
                    #------------------------------
                    # right panel with output
                    #------------------------------ 
                    html.Div(
                            className='eight columns',
                            children=[
                                    html.Div(children=[
                                                        html.H5('Disclosure Summary')
                                                      ], style={'padding-top':20, 'border-bottom':'6px solid #87D3F2'}
                                            ),
                                    
                                    html.Div(children=[
                                                        dcc.Graph(id='corp_graph', style = {'padding-bottom': 15}),
                                                        dcc.Graph(id='corp_table')
                                                      ], style={'padding-top':15}
                                            )
                                    ]
                            )                    
             
                ], style={'margin-left':'2%'}
                )
                
"""
------------------------------------------------------------------------------------------------------------------------------------
page2 layouts
"""
page_2 = html.Div([
                    #------------------------------
                   # left panel with inputs
                   #------------------------------ 
                   html.Div(
                            className='three columns',
                            
                            children=[
                                    html.Div(children=[
                                                        html.H5('Risk Dimensions')
                                                      ],style={'border-bottom':'6px solid #FFE600', 'padding-top':20}
                                            ),
                                
                                    html.Div(children=[
                                                        html.H6('FICO Score Range:',style={'vertical-align':'top', 'padding-top':15}),
                                                        dcc.Dropdown(
                                                                    id='fico',
                                                                    options=[
                                                                            {'label':'650 -', 'value':'Below_650'},
                                                                            {'label':'650 - 699', 'value':'650_to_699'},
                                                                            {'label':'700 - 749', 'value':'700_to_749'},
                                                                            {'label':'750 +', 'value':'Above_750'}
                                                                            ],
                                                                    value = 'Below_650'
                                                                    )
                                                    ],
                                            ),
                                
                                    html.Div(children=[
                                                        html.H5('Risk Characteristics and Loss Rate')
                                                      ],style={'border-bottom':'6px solid #FFB46A', 'padding-top':20}
                                            ),
                                                        
                                    html.Div(children=[dcc.RadioItems(
                                                                        id = 'output2',
                                                                        options=[
                                                                                {'label': 'Credit Card Type', 'value': 'Credit card type'},
                                                                                {'label': 'Current Credit Limit', 'value': 'Current credit limit'},
                                                                                {'label': 'Days Past Due', 'value': 'Days past due'},
                                                                                {'label': 'Month-end Account Status', 'value': 'Month-end account status'},
                                                                                {'label': 'Account Origination Year', 'value': 'Account origination year'},
                                                                                {'label': 'Month-end Close Status', 'value': 'Month-end close status'},
                                                                                {'label': 'Cycle Ending Balance', 'value': 'Cycle ending balance'},
                                                                                {'label': 'Income at Origination', 'value': 'Income at origination'},
                                                                                {'label': 'Original Credit Limit', 'value': 'Original credit limit'},
                                                                                {'label': 'Interest Rate at Cycle End', 'value': 'Interest rate at cycle end'},
                                                                                {'label': 'Loss Rate', 'value': 'Loss_Rate'}
                                                                                ],
                                                                        value='Credit card type',
                                                                        labelStyle ={'color': 'white'}
                                                                      )                                
                                                     ], style = {'padding-top': 15}
                                            )
                                    ]
                                ),
                                    
                                   
    
                    #------------------------------
                    # right panel with output
                    #------------------------------ 
                    html.Div(
                            className='eight columns',
                            children=[
                                    html.Div(children=[
                                                        html.H5('Disclosure Summary')
                                                      ], style={'padding-top':20, 'border-bottom':'6px solid #87D3F2'}
                                            ),
                                    
                                    html.Div(children=[
                                                        dcc.Graph(id='card_graph', style = {'padding-bottom': 15}),
                                                        dcc.Graph(id='card_table')
                                                      ], style={'padding-top':15}
                                            )
                                    ]
                            )
                 ], style={'margin-left':'2%'}
            )





"""
------------------------------------------------------------------------------------------------------------------------------------
APP layouts and callback
"""
tabs_styles = {
              'height': '44px'
              }
tab_style = {
            'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            'color': 'grey'
            }

tab_selected_style = {
                    'borderTop': '1px solid #d6d6d6',
                    'borderBottom': '1px solid #d6d6d6',
                    'backgroundColor': '#FFE600',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'padding': '6px'
                    }

app.layout = html.Div([
                        html.Div(
                                className = 'eleven columns',
                                children=[
                                        html.Div('FED CCAR Disclosure (Corporate and Credit Card Loans)',
                                                 style={'font-size':40,'color':'#FFE600','margin-left':'2%','font-weight':'bold'},
                                                 className = 'nine columns'),
                                        html.Div(html.Img(src=app.get_asset_url('EY_Logo_Beam_RGB_White_Yellow.png'),
                                                          style={'height':60}),
                                                 style={'height':70,'line-height':70,'text-align':'right'},
                                                 className = 'two columns')                                    
                                        ], style={'display':'inline-block','height':70,'line-height':70,'margin-bottom':50,'margin-top':'1%'}
                                ),
                        html.Div(
                                className = 'eleven columns',
                                children=[
                                        dcc.Tabs(id="tabs-example", children=[
                                            dcc.Tab(label='Corporate', value='tab-1-example', style=tab_style, selected_style=tab_selected_style),
                                            dcc.Tab(label='Credit Card', value='tab-2-example', style=tab_style, selected_style=tab_selected_style),
                                         ] , value='tab-1-example',)
                                        ], style={'margin-left':'2%'}
                                ),
                        html.Div(id='tabs-content-example')
   
                    ])

## call back for tabs

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return page_1
    elif tab == 'tab-2-example':
        return page_2


"""
------------------------------------------------------------------------------------------------------------------------------------
Callback for page 1
"""

@app.callback([Output('corp_graph', 'figure'), Output('corp_table', 'figure')],
              [Input('rating', 'value'), Input('sector', 'value'), Input('collateral', 'value'), Input('output1', 'value')])
def corp_calc(r, s, c, o):
    fig1, fig2 = corp(corp_data_t, corp_data, r, s, c, o)
    
    return fig1, fig2


"""
------------------------------------------------------------------------------------------------------------------------------------
Callback for page 2
"""

@app.callback([Output('card_graph', 'figure'), Output('card_table', 'figure')],
              [Input('fico', 'value'), Input('output2', 'value')])
def card_calc(f, o):
    fig1, fig2 = card(card_data_t, card_data, f, o)
    
    return fig1, fig2



if __name__ == '__main__':
    app.run_server()