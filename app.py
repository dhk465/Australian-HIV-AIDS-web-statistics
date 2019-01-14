import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go

# declaring a DataFrame from csv
aasd = pd.read_csv('./Aids2.csv')
# renaming the columns
aasd.rename({'diag': 'date of diagnosis',
             'death': 'date of death',
             'T.categ': 'mode of transmission',
             'age': 'age at diagnosis'},
            axis='columns', inplace=True)
# deleting the duplicate index numbers within csv
del aasd['Unnamed: 0']
# de-abbreviate the terms e.g. "D" into "Deceased" and "hs" into "male homosexual or bisexual contact"
# aasd['state'].unique()
deabbr_state = {'NSW': 'New South Wales',
                'Other': 'Others',
                'QLD': 'Queensland',
                'VIC': 'Victoria'}
aasd['state'] = aasd['state'].map(deabbr_state)
# aasd['status'].unique()
deabbr_status = {'A': 'alive',
                 'D': 'deceased'}
aasd['status'] = aasd['status'].map(deabbr_status)
# aasd['mode of transmission'].unique()
deabbr_mode = {'hs': 'male homosexual/bisexual contact',
               'haem': 'haemophilia/coagulation disorder',
               'other': 'other/unknown',
               'hsid': 'male homosexual/bisexual intravenous drug user',
               'het': 'heterosexual contact',
               'id': 'female or heterosexual male intravenous drug user',
               'mother': 'mother with or at risk of HIV infection',
               'blood': 'receipt of blood, blood components or tissue'}
aasd['mode of transmission'] = aasd['mode of transmission'].map(deabbr_mode)
# add a new column based on the calculation date of death - date of diagnosis
aasd['days after diagnosis'] = aasd['date of death'].values - aasd['date of diagnosis'].values
# rearranging the columns
aasd = aasd[['state', 'sex', 'date of diagnosis', 'date of death', 'days after diagnosis', 'status', 'mode of transmission', 'age at diagnosis']]
# the number of the deceased during the study
aasd_alive = aasd[aasd['status'] == 'alive']
num_dec = len(aasd) - len(aasd_alive)
# the deceased participants at the end of the study are listed
# apart from these participants, the date of death value 11504 indicates the participants are alive as of the end of the study
last_day_dec = aasd[(aasd['date of death'] == 11504) & (aasd['status'] == 'deceased')]
male_stat = aasd[aasd['sex'] == 'M']
female_stat = aasd[aasd['sex'] == 'F']

# hist_age
histo01 = [go.Histogram(x=aasd['age at diagnosis'], name = 'patient count', opacity = 0.75)]
layout01 = go.Layout(
    showlegend = False,
    height = 700,
    autosize = True,
    title = 'Age Distribution',
    xaxis = {'title': 'Age at Diagnosis'},
    yaxis = {'title': 'Number of Patients'}
)
fig01 = dict(data = histo01, layout = layout01)

# pie_states
pie01 = go.Pie(
    labels = aasd['state'].unique(),
    values = aasd['state'].value_counts(),
    opacity = 0.65
)
layout02 = go.Layout(
    showlegend = True,
    height = 700,
    autosize = True,
    title = 'Number of Patients in Australian States'
)
fig02 = dict(data = [pie01], layout = layout02)

pie02 = go.Pie(
    labels = aasd['mode of transmission'].unique(),
    values = aasd['mode of transmission'].value_counts()
)
pie03 = go.Pie(
    labels = aasd[aasd['state'] == 'New South Wales']['mode of transmission'].unique(),
    values = aasd[aasd['state'] == 'New South Wales']['mode of transmission'].value_counts()
)
pie04 = go.Pie(
    labels = aasd[aasd['state'] == 'Victoria']['mode of transmission'].unique(),
    values = aasd[aasd['state'] == 'Victoria']['mode of transmission'].value_counts()
)
pie05 = go.Pie(
    labels = aasd[aasd['state'] == 'Queensland']['mode of transmission'].unique(),
    values = aasd[aasd['state'] == 'Queensland']['mode of transmission'].value_counts()
)
pie06 = go.Pie(
    labels = aasd[aasd['state'] == 'Others']['mode of transmission'].unique(),
    values = aasd[aasd['state'] == 'Others']['mode of transmission'].value_counts()
)

layout05 = go.Layout(
    showlegend = True,
    height = 700,
    autosize = True,
    title = 'Modes of Transmission in Australia'
)
layout06 = go.Layout(
    showlegend = True,
    height = 700,
    autosize = True,
    title = 'Modes of Transmission in New South Wales'
)
layout07 = go.Layout(
    showlegend = True,
    height = 700,
    autosize = True,
    title = 'Modes of Transmission Victoria'
)
layout08 = go.Layout(
    showlegend = True,
    height = 700,
    autosize = True,
    title = 'Modes of Transmission in Queensland'
)
layout09 = go.Layout(
    showlegend = True,
    height = 700,
    autosize = True,
    title = 'Modes of Transmission in other states'
)
fig05 = dict(data = [pie02], layout = layout05)
fig06 = dict(data = [pie03], layout = layout06)
fig07 = dict(data = [pie04], layout = layout07)
fig08 = dict(data = [pie05], layout = layout08)
fig09 = dict(data = [pie06], layout = layout09)

# scatter_days
scatter01 = go.Scatter(
    x = aasd.groupby('age at diagnosis', as_index=True).mean().index,
    y = aasd.groupby('age at diagnosis', as_index=True).mean()['days after diagnosis'].round(0),
    mode = 'markers'
)
layout03 = go.Layout(
    showlegend = False,
    height = 700,
    autosize = True,
    title = 'days patients lived by age group',
    xaxis = {'title': 'Age at Diagnosis'},
    yaxis = {'title': 'Days lived'}
)
fig03 = dict(data = [scatter01], layout = layout03)

# gender_histo
male_histo = go.Histogram(
    x = male_stat['age at diagnosis'],
    opacity = 0.75,
    name = 'men'
)
female_histo = go.Histogram(
    x = female_stat['age at diagnosis'],
    opacity = 0.75,
    name = 'women'
)
layout04 = go.Layout(
    barmode = 'stack',
    showlegend = True,
    height = 700,
    autosize = True,
    title = 'Age Distribution between Men and Women',
    xaxis = {'title': 'Age at Diagnosis'},
    yaxis = {'title': 'Number of Patients'}
)
fig04 = dict(data = [male_histo, female_histo], layout = layout04)

# this function will generate an html table using a dataframe
def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

################################HTML############################################
app = dash.Dash(__name__)
app.css.config.serve_locally=True

app.layout = html.Div(children=[
# https://codepen.io/chriddyp/pen/bWLwgP.css as used on https://dash.plot.ly/getting-started
    html.Link(
        href='bWLwgP.css',
        rel='stylesheet'
    ),
    html.H1(
        children='Python Semester Project'
    ),
    dcc.Markdown('''
### AIDS statistics in Australia up to 1992

The data and the graphs used in this project illustrates AIDS/HIV cases of Australia
from its rise till July 1991.

The research was carried out by *P. J. Solomon* in order to **emphasise the importance of
healthcare** and to give **an insight on the epidemic**.

For further information, it is recommended to take a look at the [report](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=8&cad=rja&uact=8&ved=2ahUKEwicwff0pujfAhVHJ1AKHbEYBJ0QFjAHegQIBxAC&url=https%3A%2F%2Fpdfs.semanticscholar.org%2F7d23%2F36da875505e66ae983a271ee6cd83ce42677.pdf&usg=AOvVaw2j7D0Cij-lVA6_Mzr8brci) on the statistics.
    '''),
    dcc.RadioItems(
    id='type',
    options=[
        {'label': 'Raw Data', 'value': 'data'},
        {'label': 'Graphs', 'value': 'graph'}
    ],
    value='data'
    ),
    html.Div(id='graph_container', children=[
        dcc.Dropdown(
            id='graph_type',
            options=[
                {'label': 'Age Distribution at diagnosis', 'value': 'age_diagnosis'},
                {'label': 'Patients by States', 'value': 'num_states'},
                {'label': 'Days lived from diagnosis', 'value': 'days_lived'}
            ],
            value='age_diagnosis'
        ),
        dcc.Checklist(id='checkbox',
            options=[{'label': 'Separate Men and Women', 'value': 'toggle_gender'}],
            values=''
        ),
        dcc.Dropdown(
            id='select_state',
            options=[
                {'label': 'Number of Patients in Australia', 'value': 'aus'},
                {'label': 'Modes of Transmission in Australia', 'value': 'mode'},
                {'label': 'Modes of Transmission in New South Wales', 'value': 'nsw'},
                {'label': 'Modes of Transmission in Victoria', 'value': 'vic'},
                {'label': 'Modes of Transmission in Queensland', 'value': 'qld'},
                {'label': 'Modes of Transmission in other states', 'value': 'other'},
            ],
            value='aus'
        ),
        dcc.Graph(id='inner_graph', style = {'height': '700'})
    ]),
    html.Div(id='raw_statistics', children=generate_table(aasd))
])

@app.callback(
    Output(component_id='graph_container', component_property='style'),
    [Input(component_id='type', component_property='value')]
)
def update_container_graph(input_value):
    if input_value == 'graph':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output(component_id='raw_statistics', component_property='style'),
    [Input(component_id='type', component_property='value')]
)
def update_container_data(input_value):
    if input_value == 'data':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output(component_id='inner_graph', component_property='figure'),
    [Input(component_id='graph_type', component_property='value'),
    Input(component_id='checkbox', component_property='values'),
    Input(component_id='select_state', component_property='value')]
)
def update_pie_chart(input_value, box_toggled, state):
    if input_value == 'age_diagnosis':
        if box_toggled == ['toggle_gender']:
            figure = fig04
        else:
            figure = fig01
    elif input_value == 'num_states':
        if state == 'mode':
            figure = fig05
        elif state == 'nsw':
            figure = fig06
        elif state == 'vic':
            figure = fig07
        elif state == 'qld':
            figure = fig08
        elif state == 'other':
            figure = fig09
        else:
            figure = fig02
    elif input_value == 'days_lived':
        figure = fig03
    return figure

@app.callback(
    Output(component_id='checkbox', component_property='style'),
    [Input(component_id='graph_type', component_property='value')]
)
def update_checkbox(input_value):
    if input_value == 'age_diagnosis':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output(component_id='select_state', component_property='style'),
    [Input(component_id='graph_type', component_property='value')]
)
def update_checkbox(input_value):
    if input_value == 'num_states':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server()
