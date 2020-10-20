# Author: Jolyn Tan
# Contributor: Samuel Lim
# A short program designed to plot data for a political compass test (http://sapplypoliticalcompass.com/).

import pandas as pd
import plotly.express as px

ECON = 'Raw_Economic'
AUTH = 'Raw_Authority'
PROG = 'Raw_Progressive'
NAME = 'Name'
ZSCR = 'Z-Score'
def label_color(row):
    if row[ECON] < 0 and row[AUTH] > 0:
        return 'red'
    if row[ECON] > 0 and row[AUTH] > 0:
        return 'blue'
    if row[ECON] < 0 and row[AUTH] < 0:
        return 'green'
    if row[ECON] > 0 and row[AUTH] < 0:
        return 'purple'
    else:
        return 'black'

political_data = pd.read_csv("political_revolution.csv")

# Note: Even though Raw_Progressive has the range [-15, 15] instead of [-10, 10], it is unnecessary to normalize it.
#       This is because Z-Scores self-normalize the data.

# Calculate Euclidean distance of Z-Scores for all values (assuming normal distribution).
# In the absence of more sophisticated statistical analysis, we bluntly assume that all values are independent.
political_data[ZSCR] = (
        ((political_data[ECON] - political_data[ECON].mean())/political_data[ECON].std()) ** 2 +
        ((political_data[AUTH] - political_data[AUTH].mean())/political_data[AUTH].std()) ** 2 +
        ((political_data[PROG] - political_data[PROG].mean())/political_data[PROG].std()) ** 2
                      ) ** 0.5
political_data = political_data.round(4)

# Print values for min and max Z-Score
print("""
Minimum RMS: 
{}

Maximum RMS: 
{}
""".format(
    political_data[political_data[ZSCR] == political_data[ZSCR].min()],
    political_data[political_data[ZSCR] == political_data[ZSCR].max()]
))

# Add average point value
political_data_averages = pd.DataFrame({
    NAME: ["AVERAGE"],
    ECON: [political_data.mean()[ECON]],
    AUTH: [political_data.mean()[AUTH]],
    PROG: [political_data.mean()[PROG]],
    ZSCR: 0  # by definition
}).round(4)
political_data = political_data.append(political_data_averages, ignore_index=True, sort=False)
print("""
Average Values:
{}
""".format(political_data_averages))

# Transform Progressive data to color
political_data['Color'] = political_data.apply(lambda row: label_color(row), axis = 1)

# Display and format plot
plotlyFig = px.scatter(political_data, x=ECON, y=AUTH, color=PROG,
                       hover_name=NAME, hover_data={"Color": False, PROG: True, ZSCR: True},
                       labels = {PROG:"Progressive"}, range_color=[-15, 15], text=NAME)
plotlyFig.update_traces(marker=dict(size=12), textposition='top center')
plotlyFig.update_xaxes(range=[-10, 10],zeroline=True, zerolinewidth=2, zerolinecolor='Black', nticks=20)
plotlyFig.update_yaxes(range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='Black', nticks=20)

plotlyFig.update_layout(
    autosize=False,
    width=1200,
    height=1200,
    xaxis_title = 'Economic', 
    yaxis_title = 'Authority',
    showlegend = False
)

plotlyFig.show()
