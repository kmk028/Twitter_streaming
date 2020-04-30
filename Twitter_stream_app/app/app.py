# import packages
import os
import re
import nltk
from collections import deque, Counter
from api import get_tweet_data

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# download nltk dependencies
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 3000)

# initialize a sentiment analyzer
sid = SentimentIntensityAnalyzer()

# X_universal is the x-axis with time stamps
X_universal = deque(maxlen=30)

# stop words for the word-counts
stops = stopwords.words('english')
stops.append('https')

# initialize the app and server
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server

# global color setting
app_color = {
    "graph_bg": "rgb(221, 236, 255)",
    "graph_line": "rgb(8, 70, 151)",
    "graph_font":"rgb(2, 29, 65)"
}

# colors for plots
chart_colors = [
    '#664DFF',
    '#893BFF',
    '#3CC5E8',
    '#2C93E8',
    '#0BEBDD',
    '#0073FF',
    '#00BDFF',
    '#A5E82C',
    '#FFBD42',
    '#FFCA30'
]

app.layout = html.Div(
    [
        # bar chart
        dcc.Interval(
                id="query_update",
                interval=int(GRAPH_INTERVAL),
                n_intervals=0,
        ),                
        html.Div(
            [
                html.H6(
                    "WORD COUNT",
                    className="graph__title",
                        )
            ]
        ),
        dcc.Graph(
            id="word_counts",
            animate=False,
            figure=go.Figure(
                layout=go.Layout(
                    plot_bgcolor=app_color["graph_bg"],
                    paper_bgcolor=app_color["graph_bg"],
                )
            ),
        ),
    ],
    className="graph__container first",
)

def bag_of_words(series):
    """
    count the words in all the tweets
    Parameters
    ----------
        seriers: pandas Series
            the text column that contains the text of the tweets
    Returns
    -------
        collections.Counter object
            a dictionary with all the tokens and their number of apperances
    """
    
    # merge the text from all the tweets into one document
    document = ' '.join([row for row in series])

    # lowercasing, tokenization, and keep only alphabetical tokens
    tokens = [word for word in word_tokenize(document.lower()) if word.isalpha()]

    # filtering out tokens that are not all alphabetical
    tokens = [word for word in re.findall(r'[A-Za-z]+', ' '.join(tokens))]

    # remove all stopwords
    no_stop = [word for word in tokens if word not in stops]

    return Counter(no_stop)

# define callback function for word-counts
@app.callback(
    Output('word_counts', 'figure'),
    [Input('query_update', 'n_intervals')])
def update_graph_bar(interval):

    # query tweets from the database
    df = get_tweet_data()
    print(df)

    # get the counter for all the tokens
    word_counter = bag_of_words(df.text)

    # get the most common n tokens
    # n is specified by the slider
    top_n = word_counter.most_common(10)[::-1]

    # get the x and y values
    X = [cnt for word, cnt in top_n]
    Y = [word for word, cnt in top_n]

    # plot the bar chart
    bar_chart = go.Bar(
        x=X, y=Y,
        name='Word Counts',
        orientation='h',
        marker=dict(color=chart_colors[::-1])
    )

    # specify the layout
    layout = go.Layout(
            xaxis={
                'type': 'log',
                'autorange': True,
                'title': 'Number of Words'
            },
            height=300,
            plot_bgcolor=app_color["graph_bg"],
            paper_bgcolor=app_color["graph_bg"],
            font={"color": app_color["graph_font"]},
            autosize=True,
            margin=go.layout.Margin(
                l=100,
                r=25,
                b=75,
                t=25,
                pad=4
            ),
        )

    return go.Figure(
        data=[bar_chart], layout=layout
    )

# run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)