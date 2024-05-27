#IMPORT MODULES
from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ipywidgets as widgets
from dash.dependencies import Input, Output
from sklearn import datasets
import numpy as np
from pathlib import Path
import warnings

app = Dash(external_stylesheets = [dbc.themes.JOURNAL])

#DATASETS
oc = pd.read_csv(Path(__file__).parent / 'assets/outcomes.csv', low_memory = False)
oc1 = pd.read_csv(Path(__file__).parent / 'assets/outcomes1.csv', low_memory = False)
oc2 = pd.read_csv(Path(__file__).parent / 'assets/outcomes2.csv', low_memory = False)
df = pd.read_csv(Path(__file__).parent / 'assets/Displaced_People_Data.csv', low_memory = False)
dic= pd.read_csv(Path(__file__).parent / 'assets/Dictionary Table.csv', low_memory = False)


#_____PLOTLY_____

fundbar1 = go.Figure(data = [
                go.Bar(name = 'Funding Gap (USD)',
                    x = oc1['outcome area'],
                    y = oc1['gap']),
                ])
fundbar1.update_layout(
    xaxis_title='Outcome Area',
    yaxis_title='Gap (USD)',
    title='Funding Gap by Outcome Area',
    )

fundbar2 = go.Figure(data = [
                go.Bar(name = 'Funding Gap (USD)',
                    x = oc2['Region'],
                    y = oc2['gap']),
                ])
fundbar2.update_layout(
    xaxis_title='Region',
    yaxis_title='Gap (USD)',
    title='Funding Gap by Region',
    )



initial_region = oc['Region'].unique()[0]
initial_data = oc.loc[oc['Region'] == initial_region]
region_fundpie = go.Figure(data = [
    go.Pie(
        labels = oc['Region'].unique(),
        values = oc.groupby('Region')['Budget (USD)'].sum()
        )
    ])
dropdown = widgets.Dropdown(
    options = oc['Region'].unique(),
    value = oc['Region'].unique()[0],
    description = 'Region:'
)
def update_chart(change):
    region = change.new
    region_fundpie.data[0].values = [oc.groupby('Region')['Budget (USD)'].sum().loc[region]]
    region_fundpie.update_layout(
        title = region,
        legend = dict(
            font = dict(size = 8)
            ),
        )
dropdown.observe(update_chart, 'Budget (USD)')
container = widgets.VBox([dropdown])
region_fundpie.update_traces(textposition = 'inside')
region_fundpie.update_layout(
    title='Budget Breakdown by Region',
    legend = dict(
        font = dict(size = 8)
        ),
    uniformtext_minsize = 10,
    uniformtext_mode='hide'
    )

initial_country = oc['Country'].unique()[0]
initial_data = oc.loc[oc['Country'] == initial_country]
country_oepie1 = go.Figure()


# Create a pie chart for each country
for country in oc['Country'].unique():
    country_data = oc.loc[oc['Country'] == country]
    country_oepie1.add_trace(go.Pie(
        labels=country_data['outcome area'],
        values=country_data['Budget (USD)'],
        name=country
    ))
dropdown = widgets.Dropdown(
    options=oc['Country'].unique(),
    value=initial_country,
    description='Country:'
)
def update_chart(change):
    country = change.new
    country_oepie1.update_traces(visible='legendonly')
    country_oepie1.update_traces(visible=True, selector=dict(name=country))
dropdown.observe(update_chart, 'value')
container = widgets.VBox([dropdown])

country_oepie1.update_traces(textposition = 'inside')
country_oepie1.update_layout(
    title='Budget Breakdown by Outcome Area',
    legend = dict(
        font = dict(size = 8)
        ),
    updatemenus=[
        go.layout.Updatemenu(
            active=0,
            buttons=[
                dict(label='All',
                     method='update',
                     args=[{'visible': [True] * len(oc['Country'].unique())}]),
                *[
                    dict(label=country,
                         method='update',
                         args=[{'visible': [False] * i + [True] + [False] * (len(oc['Country'].unique()) - i - 1)},
                               {'title': f'{country} Budget Breakdown'}])
                    for i, country in enumerate(oc['Country'].unique())
                ]
            ]
        )
    ]
)



initial_country = oc['Country'].unique()[1]
initial_data = oc.loc[oc['Country'] == initial_country]
country_fundpie = go.Figure()
for region in oc['Region'].unique():
    region_data = oc.loc[oc['Region'] == region]
    country_fundpie.add_trace(go.Pie(
        labels=region_data['Country'],
        values=region_data['Budget (USD)'],
        name=region
    ))
dropdown = widgets.Dropdown(
    options = oc['Region'].unique(),
    value = initial_region,
    description = 'Region:'
    )
def update_chart(change):
    region = change.new
    country_fundpie.update_traces(visible='legendonly')
    country_fundpie.update_traces(visible=True, selector=dict(name=region))
dropdown.observe(update_chart, 'value')
container = widgets.VBox([dropdown])
country_fundpie.update_traces(textposition = 'inside')
country_fundpie.update_layout(
    title='UNHCR Budget Breakdown by Country',
    legend = dict(
        font = dict(size = 8)
        ),
    uniformtext_minsize = 10,
    uniformtext_mode='hide',
    updatemenus = [
        go.layout.Updatemenu(
            active=0,
            buttons=[
                dict(label='All',
                        method='update',
                        args=[{'visible': [True] * len(oc['Region'].unique())}]),
                *[
                    dict(label=region,
                            method='update',
                            args=[{'visible': [False] * i + [True] + [False] * (len(oc['Region'].unique()) - i - 1)},
                                {'title': f'{region} Budget Breakdown by Country'}])
                    for i, region in enumerate(oc['Region'].unique())
                ]])]
    )



country_oepie2 = go.Figure()

# Create a pie chart for each country
for country in oc['Country'].unique():
    country_data = oc.loc[oc['Country'] == country]
    country_oepie2.add_trace(go.Pie(
        labels=country_data['outcome area'],
        values=country_data['Expenditure (USD)'],
        name=country
    ))
# Create the dropdown widget
dropdown = widgets.Dropdown(
    options=oc['Country'].unique(),
    value=initial_country,
    description='Country:'
)
def update_chart(change):
    country = change.new
    country_oepie2.update_traces(visible='legendonly',textposition = 'inside')
    country_oepie2.update_traces(visible=True, selector=dict(name=country))

# Register the update function to the dropdown widget
dropdown.observe(update_chart, 'value')

# Create the widget container
container = widgets.VBox([dropdown])

# Set layout options
country_oepie2.update_traces(textposition = 'inside')
country_oepie2.update_layout(
    title='Expenditure Breakdown by Outcome Area',
    legend = dict(
        font = dict(size = 8)
        ),
    uniformtext_minsize = 10,
    uniformtext_mode='hide',
    updatemenus=[
        go.layout.Updatemenu(
            active=0,
            buttons=[
                dict(label='All',
                     method='update',
                     args=[{'visible': [True] * len(oc['Country'].unique())}]),
                *[
                    dict(label=country,
                         method='update',
                         args=[{'visible': [False] * i + [True] + [False] * (len(oc['Country'].unique()) - i - 1)},
                               {'title': f'{country} Expenditure Breakdown'}])
                    for i, country in enumerate(oc['Country'].unique())
                ]
            ]
        )
    ]
)



#_____PATHS_____

asylum2018 = 'assets/asylum2018.html'
asylum2019 = 'assets/asylum2019.html'
asylum2020 = 'assets/asylum2020.html'
asylum2021 = 'assets/asylum2021.html'
asylum2022 = 'assets/asylum2022.html'
origin2018 = 'assets/origin2018.html'
origin2019 = 'assets/origin2019.html'
origin2020 = 'assets/origin2020.html'
origin2021 = 'assets/origin2021.html'
origin2022 = 'assets/origin2022.html'
totalbudget = 'assets/totalbudget.html'
underfunding = 'assets/underfunding.html'
braeden_headshot = 'assets/Braeden.jpg'
jt_headshot = 'assets/JT.jpg'
puk_headshot = 'assets/Puk.jpg'
sher_headshot = 'assets/Sher.jpg'
datalab_logo = 'assets/DataLab Logo.jpg'
usaforunhcr_logo = 'assets/USA for UNHCR Logo.png'



#_____APP LAYOUT_____

app.layout = html.Div([
    dcc.Tabs([
        # CRISIS IN CONTEXT TAB
        dcc.Tab(label = 'Crisis in Context', style = {'color': '#0072BC'}, children = [
            html.Div(
                className = 'row',
                style = {
                    'padding': '30px',
                    'border': '30px #0072BC solid'
                    },
                children = [
                html.H2('Displacement Crisis Dashboard', style = {'color':'#0072BC'}),
                html.P('''In recent years, the global refugee crisis has reached a fever pitch.
                        Approximately 117,000,000 people have been forced to flee their homes due to war,
                        economic instability, the ripple effects of climate change, and similarly
                        life-changing events.'''),
                html.P('''The map below shows the total number of displaced people in the world; the darker
                        a country is, the more people are displaced there. Hover over a country to view more
                        info about its situation.'''),
                html.H4('Global Displaced Population Map:', style = {'color':'#0072BC'}),
                html.Label('Select Year:', style = {'font-weight': 'bold'}),
                dcc.Slider(
                    id = 'displacedyearcontrol',
                    min = 2018,
                    max = 2022,
                    step = 1,
                    value = 2022,
                    marks = {
                        2018: {'label':'2018'},
                        2019: {'label':'2019'},
                        2020: {'label':'2020'},
                        2021: {'label':'2021'},
                        2022: {'label':'2022'}
                        },
                    tooltip = {
                        'placement':'bottom',
                        'always_visible':False
                        },
                    updatemode = 'drag',
                    included = False
                    ),
                html.Iframe(
                    id = 'displacedmap',
                    srcDoc = open(origin2022,'r').read(),
                    style = {'height':'450px'}
                    ),
                html.Div(className = 'col-md-6', style = {'padding': '10px'}, children = [
                    html.Label('Display Refugee Origin/Asylum Location:', style = {'font-weight':'bold','padding-top':'10px'}),
                    dcc.Dropdown(
                        id = 'originasylumcontrol',
                        options = [
                            'Origin',
                            'Asylum',
                             ],
                        value = 'Origin',
                        style = {'width': '60%'}
                        )
                    ]),
                html.Div(className = 'col-md-6', style = {'padding': '10px'}, children = [
                    html.Label('Color Scale (Light to Dark):', style = {'font-weight':'bold'}),
                    html.P('0: No Data 1: 0-50,000 2: 50,000-100,000', style = {'fontSize': 10,'margin': 0}),
                    html.P('3: 100,000-250,000 4: 250,000-500,000 5: 500,000-1,000,000', style = {'fontSize': 10,'margin': 0}),
                    html.P('6: 1,000,000-2,500,000 7: 2,500,000-5,000,000 8: 5,000,000-30,000,000', style = {'fontSize': 10,'margin': 0})
                    ])
                ]),
            html.Div(
                className = 'row',
                style = {'padding': '30px',
                         'border-left': '30px #0072BC solid',
                         'border-right': '30px #0072BC solid',
                         'border-bottom': '30px #0072BC solid'
                         },
                children = [
                html.P('''To mitigate this crisis, the United Nations High Commissioner for Refugees
                        (UNHCR) allocates funds from public and private donors to distribute aid based
                        on need. As the refugee crisis has worsened in recent years, the gap between
                        UNHCR's budget and the funding that actually gets to those in need has progressively
                        widened.'''),
                html.P('''This map shows the total UNHCR needs-based budget by country. Note that budget
                        size does not correlate perfectly with the gravity of a given crisis, given that 
                        this map does not account for population size. Use the dropdown menu to toggle
                        the color display between total budget and the percent which this budget has actually
                        been funded.'''),
                html.H4('UNHCR Budget/Expenditure Map:', style = {'color': '#0072BC'}),
                html.Iframe(
                    id = 'fundingmap',
                    srcDoc = open(totalbudget,'r').read(),
                    style = {'height':'450px'}
                    ),
                html.Div(className = 'col-md-6', style = {'padding': '10px'}, children = [
                    html.Label('Color Display:', style = {'font-weight':'bold','padding-top':'10px'}),
                    dcc.Dropdown(
                        id = 'fundingmapcontrol',
                        options = [
                            'Total Budget',
                            '% Funded',
                             ],
                        value = 'Total Budget',
                        style = {'width': '60%'}
                        )
                    ]),
                html.Div(className = 'col-md-6', style = {'padding': '10px'}, children = [
                    html.Label('Color Scale (Light to Dark):', style = {'font-weight':'bold'}),
                    html.P('0: No Data 1: 0-25,000,000 2: 25,000,000-50,000,000', style = {'fontSize': 10,'margin': 0}),
                    html.P('3: 50,000,000-100,000,000 4: 100,000,000-250,000,000 5: 250,000-500,000,000', style = {'fontSize': 10,'margin': 0}),
                    html.P('6: 500,000,000-750,000,000', style = {'fontSize': 10,'margin': 0})
                    ]),
                html.P('''(NOTE: All UNHCR funding data displayed on this dashboard is from 2022.
                        Underfunding data is currently only available for a select number of countries.)''',
                       style = {'fontSize': 12,'padding':'15px'})
                ])
            ]),

        # FORCIBLY DISPLACED TAB
        dcc.Tab(label = 'Forcibly Displaced', style = {'color': '#0072BC'}, children = [
            html.Div(
                className = 'row',
                style = {'padding':'30px',
                         'border': '30px #0072BC solid'
                         },
                children = [           
                html.H2('Population/Demographics Viewer', style = {'padding': '10px', 'color':'#0072BC'}),
                html.P('''Use the below dropdown menus to toggle between paramaters of global population data.'''),
                html.Div(className='col-md-4', children=[          #Sets the position for the output on the page using col-md
                    html.Div(className='sidebar', children=[       #Sets the position of the following code as a sidebar
                        html.H4('Country of asylum:', style = {'fontSize': 10, 'color':'#0072BC'}),          #Displays a heading                        
                        dcc.Dropdown(                              #Takes input as a drop down for the country category
                            id='country',                          #Sets the id for this dropdown to be used in callback        
                            options=['Aruba', 'Afghanistan', 'Albania', 'Algeria', 'Angola', 'Egypt',           
                               'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
                               'Bahrain', 'Barbados', 'Burundi', 'Belgium', 'Benin', 'Bangladesh',
                               'Bahamas', 'Burkina Faso', 'Belarus',
                               'Bolivia (Plurinational State of)', 'Botswana', 'Brazil',
                               'Bosnia and Herzegovina', 'Bulgaria', 'Belize', 'Canada',
                               'Central African Republic', 'Cayman Islands', 'Chad', 'China',
                               'Chile', 'Cameroon', 'Congo', 'Dem. Rep. of the Congo', 'Colombia',
                               'Costa Rica', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 'Denmark',
                               'Djibouti', 'Dominican Rep.', 'Ecuador', 'Eritrea', 'Estonia',
                               'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia',
                               'United Kingdom of Great Britain and Northern Ireland', 'Georgia',
                               'Germany', 'Ghana', 'Guinea-Bissau', 'Greece', 'Guatemala',
                               'Guinea', 'Guyana', 'Haiti', 'China, Hong Kong SAR', 'Honduras',
                               'Croatia', 'Hungary', 'Iceland', 'Cote D’Ivoire', 'India',
                               'Indonesia', 'Ireland', 'Iran', 'Iraq', 'Israel', 'Italy',
                               'Jamaica', 'Jordan', 'Japan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan',
                               'Korea', 'Kuwait', 'Liberia', 'Libya', 'Lebanon', 'Lesotho',
                               'Liechtenstein', 'Sri Lanka', 'Lithuania', 'Luxembourg', 'Latvia',
                               'Madagascar', 'Mauritania', 'North Macedonia', 'Monaco', 'Moldova',
                               'Mexico', 'Mali', 'Malaysia', 'Malawi', 'Montenegro', 'Mongolia',
                               'Morocco', 'Mozambique', 'Malta', 'Mauritius', 'Myanmar',
                               'Namibia', 'Nepal', 'Netherlands (Kingdom of the)', 'Niger',
                               'Nicaragua', 'Nigeria', 'Norway', 'Nauru', 'New Zealand', 'Oman',
                               'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines',
                               'Papua New Guinea', 'Poland', 'Portugal', 'Qatar', 'Romania',
                               'South Africa', 'Russian Federation', 'Rwanda', 'El Salvador',
                               'Saudi Arabia', 'Senegal', 'Sierra Leone', 'Solomon Islands',
                               'Somalia', 'Spain', 'Serbia', 'South Sudan',
                               'Saint Kitts and Nevis', 'Sudan', 'Suriname', 'Slovakia',
                               'Slovenia', 'Eswatini', 'Sweden', 'Switzerland',
                               'Sint Maarten (Dutch part)', 'Syria', 'Tanzania',
                               'Turks and Caicos Islands', 'Thailand', 'Tajikistan',
                               'Turkmenistan', 'Togo', 'Trinidad and Tobago', 'Tunisia',
                               'Turkiye', 'United Arab Emirates', 'Uganda', 'Ukraine', 'Uruguay',
                               'United States of America', 'Uzbekistan',
                               'Venezuela (Bolivarian Republic of)', 'Samoa', 'Yemen', 'Zambia',
                               'Zimbabwe', 'Anguilla', 'Brunei Darussalam', 'Cambodia',
                               'Cabo Verde', 'Singapore', 'Viet Nam',
                               'Saint Vincent and the Grenadines', 'Grenada', 'Comoros',
                               'Vanuatu', 'Antigua and Barbuda'
                            ],
                            value='Ukraine',                          #Default value of dropdown
                            multi=False                               #Not allowing multiple values to be selected at a time
                        ),
                        html.Label('Year:', style = {'fontSize': 10, 'color':'#0072BC'}), #Displaying a name for the dropdown as a separate Text Label
                        dcc.Dropdown(                                 #Takes input as a drop down for the year category  
                            id='year2',                               #Sets the id for this dropdown to be used in callback 
                            #drop down options
                            options=[
                                {'label': '2018', 'value': '2018'},
                                {'label': '2019', 'value': '2019'},
                                {'label': '2020', 'value': '2020'},
                                {'label': '2021', 'value': '2021'},
                                {'label': '2022', 'value': '2022'}
                            ],

                            value='2021',                            #Default value of the dropdown
                            multi=False                              #Not allowing multiple values to be selected at a time
                        ),
                        html.Label('Sex:', style = {'fontSize': 10, 'color':'#0072BC'}),                         #Displaying a name for the dropdown as a separate Text Label
                        dcc.Dropdown(                                #Takes input as a drop down for the sex category
                            id='sex1',                               #Sets the id for this dropdown to be used in callback
                            #dropdown options
                            options=[
                                {'label': 'Male', 'value': 'male'},
                                {'label': 'Female', 'value': 'female'},
                                {'label': 'All', 'value': 'all'}
                            ],
                            value='all'                             #Default value of dropdown
                        ),
                        html.Label('Age:', style = {'fontSize': 10, 'color':'#0072BC'}),                        #Displaying a name for the dropdown as a separate Text Label                    
                        dcc.Dropdown(                               #Takes input as a drop down for the age category
                            id='age1',                              #Sets the id for this dropdown to be used in callback
                            #drop down options
                            options=[
                                {'label': 'All', 'value': 'age_all'},
                                {'label': '0 - 4', 'value': 'age11'},
                                {'label': '5 - 11', 'value': 'age12'},
                                {'label': '12 - 17', 'value': 'age13'},
                                {'label': '18 - 59', 'value': 'age14'},
                                {'label': '60+', 'value': 'age15'},
                                {'label': 'Unknown', 'value': 'age1_un'}
                            ],
                            value='age_all',                       #Default value of dropdown
                            multi=False                            #Not allowing multiple values to be selected at a time
                        ),
                        html.Label('Please select one to visualize:', style = {'fontSize': 10, 'color':'#0072BC'}),   #Displaying a name for the dropdown as a separate Text Label
                        dcc.Dropdown(                              #Takes input as a drop down for the age category
                            id='type_select1',                     #Sets the id for this dropdown to be used in callback
                            options=[
                                {'label': 'Population Type', 'value': 'Population Type'},
                                {'label': 'Accommodation Type', 'value': 'Accommodation type'},
                                {'label': 'Location Type', 'value': 'Location U/R/V'}
                            ],
                            value='Population Type',               #Default value of dropdown
                            multi=False                            #Not allowing multiple values to be selected at a time
                        ),
                    ]),
                ]),
                html.Div(className='col-md-8', children=[         #Sets the position for the code on the page using col-md    
                    dcc.Graph(id='test_graph'),                   #Displays the bar chart
                ]),
            ]),
            html.Div(
                className = 'row',
                style = {
                    'padding': '30px',
                    'border-left': '30px #0072BC solid',
                    'border-right': '30px #0072BC solid',
                    'border-bottom': '30px #0072BC solid'
                    },
                children = [                  #Establishes a new row on the tab
                    #Displays the code with the corresponding ids as headings in the center of the row
                    html.H4('Quick Facts:', style = {'color': '#0072BC'}),
                    html.H5(id='data_story1', style = {'textAlign': 'left'}),    
                    html.H5(id='data_story2', style = {'textAlign': 'left'}),
                    html.H5(id='data_story3', style = {'textAlign': 'left'})
            ]),
            html.Div(
                className='row',
                style = {
                    'padding': '30px',
                    'border-left': '30px #0072BC solid',
                    'border-right': '30px #0072BC solid',
                    'border-bottom': '30px #0072BC solid'
                    },
                children=[ #Establishes a new row on the tab
                html.H4('Distributions:', style = {'color': '#0072BC'}),
                html.Div(className='col-md-6', children=[         #Sets the position for the code on the page using col-md
                    dcc.Graph(id='sex_pie')                       #Displays the sex distribution pie chart
                ]),
                html.Div(className='col-md-6',children=[          #Sets the position for the code on the page using col-md
                    dcc.Graph(id='pie_displaced')                 #Displays the type distribution pie chart
                ])
            ]),
            html.Div(
                className = 'row',
                id = 'dic',
                style = {
                    'padding': '30px',
                    'textAlign':'left',
                    'border-left': '30px #0072BC solid',
                    'border-right': '30px #0072BC solid',
                    'border-bottom': '30px #0072BC solid'
                    },
                children =[
                html.H4('Key:', style = {'color': '#0072BC'}),
                    #Display the DataFrame as a DataTable
                dash_table.DataTable(
                    id = 'datatable',
                    columns = [{'name': col, 'id': col} for col in dic.columns],
                    data = dic.to_dict('records'),
                    style_table = {'overflowX': 'scroll', 'textAlign': 'center'}
                    ),
                html.P('(NOTE: All data displayed on this tab was sourced from the UNHCR Refugee Data Finder tool.)',
                      style = {
                          'fontSize': 12,
                          'padding':'15px'
                        }
                    )
                ])
        ]),

        # FUNDING TAB
        dcc.Tab(label = 'Funding', style = {'color': '#0072BC'}, children = [
            html.Div(
                className = 'row',
                style = {
                    'padding':'30px',
                    'border': '30px #0072BC solid'
                    },
                children = [
                    html.H2('UNHCR Budget Insights', style = {'color':'#0072BC'}),
                    html.P('''Use the below dropdown menus to toggle between views of UNHCR budget info. Budget refers
                            to UNHCR's financial assessment of global needs; expenditure refers to funding which has been
                            fully distributed. Charts broken down by outcome and enabling areas will display country-level
                            data only.'''),
                html.Div(className = 'col-md-3', children = [
                    html.Label('Show Budget/Expenditure:', style = {'fontSize': 12}),
                    dcc.Dropdown(
                        id = 'budexpcontrol',
                        options = [
                            'Budget',
                            'Expenditure'
                            ],
                        value = 'Budget'
                        ),
                    html.Label('Breakdown by:', style = {'fontSize':12}),
                    dcc.Dropdown(
                        id = 'breakdowncontrol',
                        options = [
                            'Region',
                            'Country',
                            'Outcome/Enabling Area'
                            ],
                        value = 'Region'
                        )
                    ]),
                html.Div(className = 'col-md-9', children = [
                    dcc.Graph(
                        id = 'budexp_fundpie',
                        figure = region_fundpie
                        )
                    ])
                ]),
            html.Div(
                className = 'row',
                style = {
                    'padding': '30px',
                    'border-left': '30px #0072BC solid',
                    'border-right': '30px #0072BC solid',
                    'border-bottom': '30px #0072BC solid'
                    },
                children = [
                html.P('''This bar chart shows the global funding gap broken down by Outcome Areas; use the zoom tool
                       to focus in on a particular region.'''),
                dcc.Dropdown(
                    id = 'fundbarcontrol',
                    options = [
                        'Region',
                        'Outcome/Enabling Area'
                        ],
                    value = 'Region'
                    ),
                dcc.Graph(
                    id = 'fundbar',
                    figure = fundbar1
                    ),
                html.P('(NOTE: All UNHCR funding data displayed on this dashboard is from 2022.)',
                       style = {'fontSize': 12,'padding':'15px'}
                       )
                ])
        ]),
        # ABOUT TAB
        dcc.Tab(label = 'About', style = {'color': '#0072BC'}, children = [
            html.Div(
                className = 'row',
                style = {
                    'padding': '30px',
                    'border': '30px #0072BC solid'
                    },
                children = [
                html.H2('Meet the Team', style = {'color':'#0072BC'}),
                html.Div(className = 'col-sm-3', style = {'padding':'10px'}, children = [
                    html.Img(src = braeden_headshot,style = {'height': '200px','width': '200px'}),
                    html.H5("Braeden Mefford C'25", style = {'color': '#0072BC'}),
                    html.P('University of the South'),
                    html.P('Majors: Math, Economics')
                    ]),
                html.Div(className = 'col-sm-3', style = {'padding':'10px'}, children = [
                    html.Img(src = jt_headshot, style = {'height': '200px','width': '200px'}),
                    html.H5("JT Jenkins C'25", style = {'color': '#0072BC'}),
                    html.P('University of the South'),
                    html.P('Major: Politics')
                    ]),
                html.Div(className = 'col-sm-3', style = {'padding':'10px'}, children = [
                    html.Img(src = puk_headshot,style = {'height': '200px','width': '200px'}),
                    html.H5("Puk Puk C'25", style = {'color': '#0072BC'}),
                    html.P('University of the South'),
                    html.P('Major: Math')
                    ]),
                html.Div(className = 'col-sm-3', style = {'padding':'10px'}, children = [
                    html.Img(src = sher_headshot, style = {'height': '200px','width': '200px'}),
                    html.H5("Sher Shah Mir C'26", style = {'color': '#0072BC'}),
                    html.P('University of the South'),
                    html.P('Major: Economics')
                    ])
                ]),
            html.Div(
                className = 'row',
                style = {
                    'padding': '30px',
                    'fontSize': 10,
                    'border-left': '30px #0072BC solid',
                    'border-right': '30px #0072BC solid',
                    'border-bottom': '30px #0072BC solid'
                    },
                children = [
                html.H3('Future Suggestions', style = {'color':'#0072BC'}),
                html.P('''The list below contains improvements we would have liked to explore and add to
                        this dashboard had we had more time. Some of these ideas could be implemented
                        within a few days; others might take weeks or months.'''),
                html.Div(className = 'col-sm-6', style = {'padding':'10px'}, children = [
                    html.H5('Short Term:', style = {'color': '#0072BC'}),
                    html.P('''- Change the color of pie charts to be fixed on a certain data type: it currently
                           represents the highest value which makes viewing trends confusing'''),
                    html.P('''- Incorporate Impact Area-level data into the Funding tab as an extra dropdown
                            option (we have collected and organized this data already)'''),
                    html.P('''- Add more years of data to the tool; population data would be much easier to
                            incorporate as the Refugee Data Finder stores data back to the 1950s when the
                            UNHCR was founded, whereas budgetary data would be more complicated since the
                            COMPASS budgeting framework has only been used for a couple years''')
                    ]),
                html.Div(className = 'col-sm-6', style = {'padding':'10px'}, children = [
                    html.H5('Long Term:', style = {'color': '#0072BC'}),
                    html.P('''- Add external data on national GDP in order to give perspective on a country's
                        resources to aid refugees without UNHCR support'''),
                    html.P('''- Add external data on climate-related disasters in order to provide insights
                        regarding what Outcome Areas will need to be prioritized in certain regions'''),
                    html.P('''- Expand on dollar-per-person insights, perhaps adding visuals on funding per
                        Impact Area/Outcome Area per person''')
                    ])
                ]),
            html.Div(
                className = 'row',
                children = [
                html.Div(
                    className = 'col-sm-6',
                    style = {
                        'padding': '30px',
                        'border-left': '30px #0072BC solid',
                        'border-right': '30px #0072BC solid',
                        'border-bottom': '30px #0072BC solid',
                        'color': '#0072BC'
                        },
                    children = [
                    html.H4('Sewanee DataLab:'),
                    html.Img(src = datalab_logo, style = {'height': '100px','width': '100px'}),
                    html.P('''The Sewanee DataLab program makes the power of data analytics accessible
                            for the greater good. We accomplish this by training and supporting a new
                            generation of data scientists who work exclusively on social impact projects.''',
                           style = {'padding-top': '5px'}
                           )
                    ]),
                html.Div(
                    className = 'col-sm-6',
                    style = {
                        'padding': '30px',
                        'border-right': '30px #0072BC solid',
                        'border-bottom': '30px #0072BC solid',
                        'color': '#0072BC'
                        },
                    children = [
                    html.H4('USA for UNHCR:'),
                    html.Img(src = usaforunhcr_logo, style = {'height': '100px','width': '100px'}),
                    html.P('''USA for UNHCR protects refugees and empowers them with hope and opportunity.
                            We are with refugees from their greatest time of need – from emergency or crisis
                            and beyond through the months and likely years that many are displaced from their
                            home countries. We give refugees the hope they deserve, restore their dignity and
                            help them rebuild their lives.''',
                           style = {'padding-top': '5px'}
                           )
                    ])
                ]),
            html.Div(
                className = 'row',
                style = {
                    'padding': '30px',
                    'border-left': '30px #0072BC solid',
                    'border-right': '30px #0072BC solid',
                    'border-bottom': '30px #0072BC solid'
                    },
                children = [
                    html.Div(className = 'col-sm-6', style = {'fontSize': 10}, children = [
                        html.H4('Resources:'),
                        html.Label('UNHCR Refugee Data Finder:'),
                        dcc.Link(href = 'https://www.unhcr.org/refugee-statistics/download/?url=2bxU2f',
                                 target = 'window'
                                 ),
                        html.Label('UNHCR Refugee Stats Methodology:'),
                        dcc.Link(href = 'https://www.unhcr.org/refugee-statistics/methodology/',
                                 target = 'window'
                                 ),
                        html.Label('UNHCR Global Appeal 2023:'),
                        dcc.Link(href = 'https://reporting.unhcr.org/globalappeal',
                                 target = 'window'
                                 )
                        ]),
                    html.Div(className = 'col-sm-6', style = {'fontSize': 10}, children = [
                        html.H4('Donate to USA for UNHCR:'),
                        dcc.Link(href = 'https://give.unrefugees.org/180117core_mainpg_p_3000/',
                                 target = 'window'
                                 )
                        ])
                ])
            ])
    ])
])

#_____CALLBACKS_____

# CRISIS IN CONTEXT CALLBACKS
@app.callback(
    Output('displacedmap','srcDoc'),
    Input('displacedyearcontrol','value'),
    Input('originasylumcontrol','value'),
    prevent_initial_call = True
    )
def displacedmap_select(displacedyearcontrol_value,originasylumcontrol_value):
        if displacedyearcontrol_value == 2018:
            if originasylumcontrol_value == 'Origin':
                filename = origin2018
            else:
                filename = asylum2018
        elif displacedyearcontrol_value == 2019:
            if originasylumcontrol_value == 'Origin':
                filename = origin2019
            else:
                filename = asylum2019
        elif displacedyearcontrol_value == 2020:
            if originasylumcontrol_value == 'Origin':
                filename = origin2020
            else:
                filename = asylum2020
        elif displacedyearcontrol_value == 2021:
            if originasylumcontrol_value == 'Origin':
                filename = origin2021
            else:
                filename = asylum2021
        else:
            if originasylumcontrol_value == 'Origin':
                filename = origin2022
            else:
                filename = asylum2022
        srcDoc = open(f'{filename}','r').read()
        return srcDoc

@app.callback(
    Output('fundingmap','srcDoc'),
    Input('fundingmapcontrol','value'),
    prevent_initial_call = True
    )
def fundingmap_select(value):
        if value == 'Total Budget':
            filename = totalbudget
        else:
            filename = underfunding
        srcDoc = open(f'{filename}','r').read()
        return srcDoc




# FORCIBLY DISPLACED TAB CALLBACKS


#Barplot(histogram) displaying the data from the dataset 'df' (data obtained from the Refugee Statistics Data Finder) based on user selections
@app.callback(
    Output('test_graph', 'figure'),    #Output id
    
    #Inputs from dropdowns
    Input('country','value'),
    Input('type_select1','value'),
    Input('sex1','value'),
    Input('age1','value'),
)
def country_barplot(country,type_select1,sex1,age1):
    
    #Conditional Statements using input from dropdowns and pointing to column names in the dataset 
    if sex1=='male' and age1=='age_all':
        y_value='Male total'
    elif sex1=='female'and age1=='age_all':
        y_value='Female total'
    elif sex1=='all' and age1=='age_all':
        y_value='Total'
    elif sex1=='male' and age1=='age11':
        y_value='Male 0 - 4'
    elif sex1=='male' and age1=='age12':
        y_value='Male 5 - 11'
    elif sex1=='male' and age1=='age13':
        y_value='Male 12 - 17'
    elif sex1=='male' and age1=='age14':
        y_value='Male 18 - 59'
    elif sex1=='male' and age1=='age15':
        y_value='Male 60'
    elif sex1=='male' and age1=='age1_un':
        y_value='Male other'
    elif sex1=='female' and age1=='age11':
        y_value='Female 0 - 4'
    elif sex1=='female' and age1=='age12':
        y_value='Female 5 - 11'
    elif sex1=='female' and age1=='age13':
        y_value='Female 12 - 17'
    elif sex1=='female' and age1=='age14':
        y_value='Female 18 - 59'
    elif sex1=='female' and age1=='age15':
        y_value='Female 60'
    elif sex1=='female' and age1=='age1_un':
        y_value='Female other'
    elif sex1=='all' and age1=='age11':
        y_value='M&F 0-4'
    elif sex1=='all' and age1=='age12':
        y_value='M&F 5-11'
    elif sex1=='all' and age1=='age13':
        y_value='M&F 12-17'
    elif sex1=='all' and age1=='age14':
        y_value='M&F 18-59'
    elif sex1=='all' and age1=='age15':
        y_value='M&F 60+'
    elif sex1=='all' and age1=='age1_un':
        y_value='M&F others'


    fig=px.histogram(
        df[df['Country of asylum']==str(country)],  #data set limited to one country as input for graph - input for country taken from dropdown
        x='Year',                                   #x yalue of graph set as a constant as the Year column from the dataset
        y=y_value,                                  #y value of graph changes depending on user selection in dropdowns
        color=type_select1,                         #changes based on user selection in dropdown
        barmode='group',
        )
    return fig




#Type Distribution piechart displaying the data from the dataset 'df' (data obtained from the Refugee Statistics Data Finder) based on user selections
@app.callback(
    Output('pie_displaced', 'figure'),   #Output id

    #Inputs from dropdowns
    Input('country','value'),
    Input('type_select1','value'),
    Input('sex1','value'),
    Input('age1','value'),
    Input('year2','value')
)
def country_pieplot(country,type_select1,sex1,age1,year2):
    pie_df1 = df[df['Country of asylum'] == str(country)]     #data set limited to one country - input taken from dropdown
    pie_df = pie_df1[pie_df1['Year'] == int(year2)]           #data set limited to one year - input taken from dropdown

    #Conditional Statements using input from dropdowns and pointing to column names in the dataset 
    if sex1=='male' and age1=='age_all':
        y_value='Male total'
    elif sex1=='female'and age1=='age_all':
        y_value='Female total'
    elif sex1=='all' and age1=='age_all':
        y_value='Total'
    elif sex1=='male' and age1=='age11':
        y_value='Male 0 - 4'
    elif sex1=='male' and age1=='age12':
        y_value='Male 5 - 11'
    elif sex1=='male' and age1=='age13':
        y_value='Male 12 - 17'
    elif sex1=='male' and age1=='age14':
        y_value='Male 18 - 59'
    elif sex1=='male' and age1=='age15':
        y_value='Male 60'
    elif sex1=='male' and age1=='age1_un':
        y_value='Male other'
    elif sex1=='female' and age1=='age11':
        y_value='Female 0 - 4'
    elif sex1=='female' and age1=='age12':
        y_value='Female 5 - 11'
    elif sex1=='female' and age1=='age13':
        y_value='Female 12 - 17'
    elif sex1=='female' and age1=='age14':
        y_value='Female 18 - 59'
    elif sex1=='female' and age1=='age15':
        y_value='Female 60'
    elif sex1=='female' and age1=='age1_un':
        y_value='Female other'
    elif sex1=='all' and age1=='age11':
        y_value='M&F 0-4'
    elif sex1=='all' and age1=='age12':
        y_value='M&F 5-11'
    elif sex1=='all' and age1=='age13':
        y_value='M&F 12-17'
    elif sex1=='all' and age1=='age14':
        y_value='M&F 18-59'
    elif sex1=='all' and age1=='age15':
        y_value='M&F 60+'
    elif sex1=='all' and age1=='age1_un':
        y_value='M&F others'


    #Type Distribution pie chart
    data = [
        go.Pie(
            labels=pie_df[type_select1],                       #label as selected drop down type categories
            values=pie_df[y_value],                            #y value of pie chart changes depending on user selection in dropdowns
            textinfo='label+percent'
        )
    ]

    layout = go.Layout(
        title=f'{type_select1} Distribution in {year2}'        #title of pie chart
    )


    fig = go.Figure(data=data, layout=layout)
    return fig



#Sex Distribution piechart displaying the data from the dataset 'df' (data obtained from the Refugee Statistics Data Finder) based on user selections
@app.callback(
    Output('sex_pie','figure'),   #Output Id

    #Inputs from dropdowns
    Input ('country','value'),   
    Input ('year2','value')
)
def sex_pie(country,year2):
    
    #Creates a new data set consisting of total number of people from each sex and a corresponding column indicating male and female, from the 'df' dataset 
    af1=df[['Country of asylum', 'Year', 'Male total']]
    af2=df[['Country of asylum', 'Year', 'Female total']]
    af1=af1.groupby(['Country of asylum', 'Year']).sum()['Male total'].reset_index(name='Total')
    af1['Sex']='Male'
    af2=af2.groupby(['Country of asylum', 'Year']).sum()['Female total'].reset_index(name='Total')
    af2['Sex']='Female'
    af3=pd.concat([af1,af2], axis=0)
    af3

    fig1 = af3[af3['Country of asylum'] == str(country)]         #data set limited to one country - input taken from dropdown
    fig2 = fig1[fig1['Year'] == int(year2)]                      #data set limited to one year - input taken from dropdown


    chart=px.pie(fig2, values='Total',names='Sex', title=f'Overall Sex Distribution in {year2}')
    return chart



#DataStory
@app.callback(
    Output('data_story1', 'children'),   #Output Id
    
    #Inputs from dropdowns needed to fetch values from columns in the dataset 'df'
    Input('country','value'),
    Input('type_select1','value'),
    Input('sex1','value'),
    Input('age1','value'),
    Input('year2','value')

)
def data_story1(country,type_select1,sex1,age1,year2):

    #Conditional statements to fetch particular columns from the dataset and change part of the final texts respectively
    if sex1=='male' and age1=='age_all':
        y_value='Male total'
        blurb='who were male'
    elif sex1=='female'and age1=='age_all':
        y_value='Female total'
        blurb='who were female'
    elif sex1=='all' and age1=='age_all':
        y_value='Total'
        blurb=' '
    elif sex1=='male' and age1=='age11':
        y_value='Male 0 - 4'
        blurb='who were male and between the ages of 0 - 4'
    elif sex1=='male' and age1=='age12':
        y_value='Male 5 - 11'
        blurb='who were male and between the ages of 5 - 11'
    elif sex1=='male' and age1=='age13':
        y_value='Male 12 - 17'
        blurb='who were male and between the ages of 12 - 17'
    elif sex1=='male' and age1=='age14':
        y_value='Male 18 - 59'
        blurb='who were male and between the ages of 18 - 59'
    elif sex1=='male' and age1=='age15':
        y_value='Male 60'
        blurb='who were male and 60+'
    elif sex1=='male' and age1=='age1_un':
        y_value='Male other'
        blurb='who were male and age unknown'
    elif sex1=='female' and age1=='age11':
        y_value='Female 0 - 4'
        blurb='who were female and between the ages of 0 - 4'
    elif sex1=='female' and age1=='age12':
        y_value='Female 5 - 11'
        blurb='who were female and between the ages of 5 - 11'
    elif sex1=='female' and age1=='age13':
        y_value='Female 12 - 17'
        blurb='who were female and between the ages of 12 - 17'
    elif sex1=='female' and age1=='age14':
        y_value='Female 18 - 59'
        blurb='who were female and between the ages of 18 - 59'
    elif sex1=='female' and age1=='age15':
        y_value='Female 60'
        blurb='who were female and 60+'
    elif sex1=='female' and age1=='age1_un':
        y_value='Female other'
        blurb='who were female and age unknown'
    elif sex1=='all' and age1=='age11':
        y_value='M&F 0-4'
        blurb='who were between the ages of 0 - 4'
    elif sex1=='all' and age1=='age12':
        y_value='M&F 5-11'
        blurb='who were between the ages of 5 - 11'
    elif sex1=='all' and age1=='age13':
        y_value='M&F 12-17'
        blurb='who were between the ages of 12 - 17'
    elif sex1=='all' and age1=='age14':
        y_value='M&F 18-59'
        blurb='who were between the ages of 18 - 59'
    elif sex1=='all' and age1=='age15':
        y_value='M&F 60+'
        blurb='who were 60+'
    elif sex1=='all' and age1=='age1_un':
        y_value='M&F others'
        blurb='whose ages were unknown'

    demo_df1 = df[df['Country of asylum'] == str(country)]     
    demo_df = demo_df1[demo_df1['Year'] == int(year2)]


    blurb_sum=demo_df[y_value].sum()


    para=f'In the year {year2}, in {country}, the total number of forcibly displaced people {blurb} were {"{:,}".format(int(blurb_sum))}.'
    return para
 


#DataStory
@app.callback(
    Output('data_story2', 'children'),  #Ouput Id
    Input('country','value'),           #Input from dropdown
)
def data_story2(country):
    
    #Calculate differences in total forcibly displaced people in 2018 vs 2022
    demo_df1 = df[df['Country of asylum'] == str(country)]
    sum1_df = demo_df1[demo_df1['Year'] == int(2018)]
    sum2_df = demo_df1[demo_df1['Year'] == int(2022)]


    sum1=sum1_df['Total'].sum()
    sum2=sum2_df['Total'].sum()

    ans1=sum2-sum1



    #Conditional statements to change parts of the text depending on difference calculated above
    if ans1>0:
        change1='increased'
        ans1=f'{"{:,}".format(ans1)}'
        
    elif ans1<0:
        change1='decreased'
        ans1=f'{("{:,}".format(abs(ans1)))}'
        
    else:
        change1='changed'
        ans1=ans1
        
    para=f"Between 2018 and 2022 the number of forcibly displaced people in {country} {change1} by {ans1}."
    return para

#DataStory
@app.callback(
    Output('data_story3', 'children'),   #Output Id
    Input('country','value'),            #Input from dropdown
)
def data_story3(country):
    
    #Calculate differences in total forcibly displaced people in 2018 vs 2022
    demo_df1 = df[df['Country of asylum'] == str(country)]
    sum1_df = demo_df1[demo_df1['Year'] == int(2018)]
    sum2_df = demo_df1[demo_df1['Year'] == int(2022)]


    sum1=sum1_df['Total'].sum()
    sum2=sum2_df['Total'].sum()

    ans1=sum2-sum1

    #Conditional statements to calculate percentage change between 2018 and 2022 forcibly displaced people, and change parts of the text depending on difference calculated above
    if ans1>0:
        change1='increased'
        change2='increase'
        if sum1>0:
            percent1=(ans1/sum1)*100
            percent1="{:0.2f}".format(percent1)
            text_part=f"This means that there was an approximate {percent1}% {change2} in the the number of forcibly displaced people in {country} during this time period."
        else:
            text_part=''
        ans1=f'{"{:,}".format(ans1)}'
        
    elif ans1<0:
        change1='decreased'
        change2='decrease'
        if sum1>0:
            percent1=(abs(ans1)/sum1)*100
            percent1="{:0.2f}".format(percent1)
            text_part=f"This means that there was an approximate {percent1}% {change2} in the number of forcibly displaced people in {country} during this time period."
        else:
            text_part=''
        ans1=f'{("{:,}".format(abs(ans1)))}'
        
    else:
        change1='changed'
        change2='change'
        if sum1>0:
            percent1=(ans1/sum1)*100
            percent1="{:0.2f}".format(percent1)
            text_part=f"This means that there was an approximate {percent1}% {change2} during this time period."
        else:
            text_part=''
        ans1=ans1
        
    
    para=f"{text_part}"
    return para



# FUNDING CALLBACKS
@app.callback(
    Output('budexp_fundpie','figure'),
    Input('budexpcontrol','value'),
    Input('breakdowncontrol','value'),
    prevent_initial_call = True
    )
def fundpie_select(budexp_value,breakdown_value):
    if budexp_value == 'Budget':
        if breakdown_value == 'Region':
            initial_region = oc['Region'].unique()[0]
            initial_data = oc.loc[oc['Region'] == initial_region]
            figure = go.Figure(data = [
                go.Pie(
                    labels = oc['Region'].unique(),
                    values = oc.groupby('Region')['Budget (USD)'].sum()
                    )
                ])
            figure.update_traces(textposition = 'inside')
            figure.update_layout(
                title = 'Budget Breakdown by Region',
                legend = dict(
                    font = dict(size = 8)
                    ),
                uniformtext_minsize = 10,
                uniformtext_mode = 'hide'
                )
        elif breakdown_value == 'Country':
            initial_region = oc['Region'].unique()[0]
            initial_data = oc.loc[oc['Region'] == initial_region]
            figure = go.Figure()
            for region in oc['Region'].unique():
                region_data = oc.loc[oc['Region'] == region]
                figure.add_trace(go.Pie(
                    labels = region_data['Country'],
                    values = region_data['Budget (USD)'],
                    name = region
                ))
            dropdown = widgets.Dropdown(
                options = oc['Region'].unique(),
                value = initial_region,
                description = 'Region:'
                )
            def update_chart(change):
                region = change.new
                figure.update_traces(visible = 'legendonly')
                figure.update_traces(visible = True, selector = dict(name=region))
            dropdown.observe(update_chart, 'value')
            container = widgets.VBox([dropdown])
            figure.update_traces(textposition = 'inside')
            figure.update_layout(
                title='Budget Breakdown by Country',
                legend = dict(
                    font = dict(size = 8)
                    ),
                uniformtext_minsize = 10,
                uniformtext_mode = 'hide',
                updatemenus = [
                    go.layout.Updatemenu(
                        active = 0,
                        buttons = [
                            dict(label = 'All',
                                 method = 'update',
                                 args = [{'visible': [True] * len(oc['Region'].unique())}]),
                            *[
                                dict(label = region,
                                     method = 'update',
                                     args = [{'visible': [False] * i + [True] + [False] * (len(oc['Region'].unique()) - i - 1)},
                                           {'title': f'{region} Budget Breakdown by Country'}])
                                for i, region in enumerate(oc['Region'].unique())
                            ]])]
                )
        else:
            figure = country_oepie1
    else:
        if breakdown_value == 'Region':
            figure = go.Figure(data = [
                go.Pie(
                    labels = oc['Region'].unique(),
                    values = oc.groupby('Region')['Expenditure (USD)'].sum()
                    )
                ])
            figure.update_traces(textposition = 'inside')
            figure.update_layout(
                title = 'Expenditure Breakdown by Region',
                legend = dict(
                    font = dict(size = 8)
                    ),
                uniformtext_minsize = 10,
                uniformtext_mode='hide'
                )
        elif breakdown_value == 'Country':
            initial_region = oc['Region'].unique()[0]
            initial_data = oc.loc[oc['Region'] == initial_region]
            figure = go.Figure()
            for region in oc['Region'].unique():
                region_data = oc.loc[oc['Region'] == region]
                figure.add_trace(go.Pie(
                    labels=region_data['Country'],
                    values=region_data['Expenditure (USD)'],
                    name=region
                ))
            dropdown = widgets.Dropdown(
                options=oc['Region'].unique(),
                value=initial_region,
                description='Region:'
                )
            def update_chart(change):
                region = change.new
                figure.update_traces(visible='legendonly')
                figure.update_traces(visible=True, selector=dict(name=region))
            dropdown.observe(update_chart, 'value')
            container = widgets.VBox([dropdown])
            figure.update_traces(textposition = 'inside')
            figure.update_layout(
                title='Expenditure Breakdown by Country',
                uniformtext_minsize = 10,
                uniformtext_mode = 'hide',
                legend = dict(
                    font = dict(size = 8)
                    ),
                updatemenus = [
                    go.layout.Updatemenu(
                        active=0,
                        buttons=[
                            dict(label='All',
                                 method='update',
                                 args=[{'visible': [True] * len(oc['Region'].unique())}]),
                            *[
                                dict(label=region,
                                     method='update',
                                     args=[{'visible': [False] * i + [True] + [False] * (len(oc['Region'].unique()) - i - 1)},
                                           {'title': f'{region} Expenditure Breakdown by Country'}])
                                for i, region in enumerate(oc['Region'].unique())
                                ]])]
                )
        else:
            figure = country_oepie2
    return figure

@app.callback(
    Output('fundbar','figure'),
    Input('fundbarcontrol','value')
    )
def fundbar_select(value):
    if value == 'Region':
        figure = fundbar2
    else:
        figure = fundbar1
    return figure

if __name__ == '__main__':
    app.run(debug = True)
