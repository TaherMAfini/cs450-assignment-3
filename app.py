import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import math
tweets_df = pd.read_csv("./ProcessedTweets.csv")

app = dash.Dash(__name__)

server=app.server

month_dropdown = html.Div(id="child1_1_1", children=[html.Label("Month: ", style=dict(fontSize='1.2rem', float='left', marginRight='10px', fontWeight='bold')),dcc.Dropdown(id='month_dropdown', options=tweets_df.Month.unique(), value=tweets_df.Month.unique()[0], style=dict(display='inline-block', width='75%'))], style=dict(width='25%', margin='7px 0px 7px 0px', verticalAlign='middle'))
sent_slider = html.Div(className="child1_1_2",children=[html.Label("Sentiment Score: ", style=dict(fontSize='1.2rem', float='left', fontWeight='bold')),dcc.RangeSlider(tweets_df.Sentiment.min(),tweets_df.Sentiment.max(), id='sent_slider', value=[tweets_df.Sentiment.min(),tweets_df.Sentiment.max()], step=0.05,tooltip={"placement": "bottom", "always_visible": True}, marks=None)], style=dict(width='35%', margin='7px 0px 7px 0px'))
sub_slider = html.Div(className="child1_1_3",children=[html.Label("Subjectivity Score: ", style=dict(fontSize='1.2rem', float='left', fontWeight='bold')),dcc.RangeSlider(tweets_df.Subjectivity.min(),tweets_df.Subjectivity.max(), id='sub_slider', value=[tweets_df.Subjectivity.min(),tweets_df.Subjectivity.max()], step=0.05,tooltip={"placement": "bottom", "always_visible": True}, marks=None)], style=dict(width='35%', margin='7px 0px 7px 0px'))


app.layout =  html.Div(className='layout', children=[  
    html.Div(className="child1",children=[
        html.Div(className="child1_1", children=[month_dropdown, sent_slider, sub_slider]), html.Div(className="child1_2", children=[dcc.Graph(id='scatter_plot')])
    ]),
    html.Div(className="child2",children=[dash_table.DataTable(id='tweet_table', columns=[{"name": i, "id": i} for i in ["Raw Tweets"]], data=[], style_table={'height': '345px', 'overflowY': 'auto', 'width': '100%'}, style_cell={'textAlign': 'center', 'whiteSpace': 'normal', 'height': 'auto'}, page_action='native', page_size=8, style_header=dict(fontWeight='bold'))]),
])

@app.callback(Output('scatter_plot', 'figure'), [Input('month_dropdown', 'value'), Input('sent_slider', 'value'), Input('sub_slider', 'value')])
def update_graph(month, sent_range, sub_range):
    sent_min, sent_max = sent_range
    sub_min, sub_max = sub_range

    filtered_df = tweets_df[(tweets_df.Month == month) & (tweets_df.Sentiment >= sent_min) & (tweets_df.Sentiment <= sent_max) & (tweets_df.Subjectivity >= sub_min) & (tweets_df.Subjectivity <= sub_max)]
    figure = px.scatter(filtered_df, x='Dimension 1', y='Dimension 2', custom_data=['RawTweet'])
    figure.update_layout(xaxis_title=None, yaxis_title=None, dragmode='lasso', modebar_orientation='v', margin=dict(l=0, r=0, t=0, b=0), height=300)
    figure.update_yaxes(showticklabels=False)
    figure.update_xaxes(showticklabels=False)
    return figure

@app.callback(Output('tweet_table', 'data'), [Input('scatter_plot', 'selectedData')])
def update_table(selectedData):
    if selectedData is not None:
        selected_points = [point['pointIndex'] for point in selectedData['points']]
        selected_tweets = [point['customdata'][0] for point in selectedData['points']]
        tweets = [{"Raw Tweets": tweet} for tweet in selected_tweets]
        return tweets
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
